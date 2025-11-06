from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_boto3 import resource as ibm_boto3_resource
from ibm_botocore.client import Config
from ibm_watson_machine_learning.foundation_models import Model
from dotenv import load_dotenv
import os

load_dotenv()
import json
import requests
from datetime import datetime


# =========================
# IBM COS CONFIG (env vars)
# =========================
COS_BUCKET_NAME = os.getenv("COS_BUCKET_NAME")
COS_API_KEY_ID = os.getenv("COS_API_KEY_ID")
COS_INSTANCE_CRN = os.getenv("COS_INSTANCE_CRN")
COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
COS_JSON_KEY = os.getenv("COS_JSON_KEY", "apar_info.json")

# =========================
# Watsonx.ai LLM CONFIG
# =========================
WATSONX_URL = os.getenv("WATSONX_URL")
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
MODEL_ID = os.getenv("WATSONX_MODEL_ID", "mistralai/mistral-medium-2505")
MODEL_PARAMS = {
    "decoding_method": "greedy",
    "min_new_tokens": 1,
    "max_new_tokens": 8000
}

# =========================
# ServiceNow CONFIG
# =========================
SNOW_INSTANCE = os.getenv("SNOW_INSTANCE")
SNOW_USER = os.getenv("SNOW_USER")
SNOW_PASSWORD = os.getenv("SNOW_PASSWORD")
SNOW_TABLE = os.getenv("SNOW_TABLE")
SNOW_CALLER_ID = os.getenv("SNOW_CALLER_ID", "ibm_z_team")      # optional default caller_id
SNOW_CATEGORY = os.getenv("SNOW_CATEGORY", "Inquiry / Help")
SNOW_SUBCATEGORY = os.getenv("SNOW_SUBCATEGORY", "Software")
SNOW_ASSIGNMENT_GROUP = os.getenv("SNOW_ASSIGNMENT_GROUP", "")  # optional
SNOW_URGENCY = os.getenv("SNOW_URGENCY", "2")         # 1=High, 2=Medium, 3=Low (SNOW default scale)
SNOW_IMPACT = os.getenv("SNOW_IMPACT", "2")           # 1=High, 2=Medium, 3=Low

# ===============
# COS client init
# ===============
cos = ibm_boto3_resource(
    "s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT,
)

# ====================
# LLM model init (Wx)
# ====================
extractor_model = Model(
    model_id=MODEL_ID,
    credentials={"url": WATSONX_URL, "apikey": WATSONX_API_KEY},
    project_id=WATSONX_PROJECT_ID,
    params=MODEL_PARAMS
)


@tool(permission=ToolPermission.READ_WRITE)
def summarize_apar_and_create_snow_incident_tool(apar_id: str) -> dict:
    """
    Given an APAR ID, read apar_info.json from IBM COS, summarize the
    critical update, impact, and workarounds using a Watsonx.ai LLM,
    and create a ServiceNow incident for the APAR.

    Args:
        apar_id (str): e.g., "AH57177"

    Returns:
        dict: {
          "status": "success" | "not_found" | "error",
          "apar_id": str,
          "snow_incident": {
             "sys_id": str,
             "number": str,
             "url": str
          },
          "summary": str,   # LLM-generated summary text
          "context": {...}  # key APAR fields included in the incident
        }
    """
    # -------- Load APAR JSON from COS --------
    try:
        cos_object = cos.Object(COS_BUCKET_NAME, COS_JSON_KEY)
        json_bytes = cos_object.get()["Body"].read()
        apar_data = json.loads(json_bytes.decode("utf-8"))
    except Exception as e:
        return {
            "status": "error",
            "apar_id": apar_id,
            "error": f"Failed to read JSON from COS: {str(e)}"
        }

    # -------- Find APAR entry --------
    matched_apar = None
    for apar in apar_data.get("apars", []):
        if apar.get("apar_id") == apar_id:
            matched_apar = apar
            break

    if not matched_apar:
        return {
            "status": "not_found",
            "apar_id": apar_id,
            "message": f"No APAR found with ID: {apar_id}"
        }

    # -------- Build prompt for LLM summarization --------
    critical_update = matched_apar.get("critical_update_description", "")
    impact_summary = matched_apar.get("impact_summary", "")
    workarounds = matched_apar.get("workarounds", [])
    workarounds_text = "\n".join(
        [f"- {w.get('description')} (Impact: {w.get('impact')})" for w in workarounds]
    ) or "- None documented."

    product = apar_data.get("product", {})
    product_name = product.get("product_name", "Unknown Product")
    risk_level = matched_apar.get("risk_assessment", "unknown")
    risk_score = matched_apar.get("risk_assessment_score", "N/A")
    hold_symptom = matched_apar.get("hold_symptom", "")
    held_sysmod = matched_apar.get("held_sysmod", "")
    status = matched_apar.get("status", "")
    ptf_available = matched_apar.get("ptf_available", None)
    ptf_id = matched_apar.get("ptf_id", None)

    full_prompt = f"""
You are an expert IBM mainframe software analyst.
Create a concise ServiceNow-ready incident summary for the APAR below.

APAR ID: {apar_id}
Product: {product_name}
Risk Level: {risk_level} (score {risk_score})
Status: {status}
PTF Available: {ptf_available}
PTF ID: {ptf_id}
Hold Symptom: {hold_symptom}
Held Sysmod: {held_sysmod}

Critical Update Description:
{critical_update}

Impact Summary:
{impact_summary}

Workarounds:
{workarounds_text}

Write a crisp 4–6 sentence summary suitable for an incident description.
Avoid marketing language; be precise and action-oriented.
If IPL or downtime is implied, state it explicitly.
"""

    # -------- Call Watsonx.ai LLM --------
    try:
        llm_response = extractor_model.generate(full_prompt)
        llm_text = llm_response["results"][0]["generated_text"].strip()
    except Exception as e:
        return {
            "status": "error",
            "apar_id": apar_id,
            "error": f"LLM generation failed: {str(e)}"
        }

    # -------- Create ServiceNow Incident --------
    if not SNOW_INSTANCE or not SNOW_USER or not SNOW_PASSWORD:
        return {
            "status": "error",
            "apar_id": apar_id,
            "summary": llm_text,
            "error": "ServiceNow credentials or instance URL not configured."
        }

    snow_url = f"{SNOW_INSTANCE.rstrip('/')}/api/now/table/{SNOW_TABLE}"
    snow_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    snow_auth = (SNOW_USER, SNOW_PASSWORD)

    short_desc = f"[DB2 APAR {apar_id}] {product_name} — {risk_level.title()} risk (score {risk_score})"
    # Combine structured fields to aid triage
    structured_context = {
        "apar_id": apar_id,
        "product": product_name,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "status": status,
        "ptf_available": ptf_available,
        "ptf_id": ptf_id,
        "hold_symptom": hold_symptom,
        "held_sysmod": held_sysmod,
        "timestamp_utc": datetime.utcnow().isoformat() + "Z"
    }

    description = (
        f"{llm_text}\n\n"
        f"--- Context ---\n"
        f"{json.dumps(structured_context, indent=2)}\n"
        f"--- Workarounds ---\n"
        f"{workarounds_text}"
    )

    snow_payload = {
        "short_description": short_desc,
        "description": description,
        "category": SNOW_CATEGORY,
        "subcategory": SNOW_SUBCATEGORY,
        "urgency": SNOW_URGENCY,
        "impact": SNOW_IMPACT
    }
    if SNOW_CALLER_ID:
        snow_payload["caller_id"] = SNOW_CALLER_ID
    if SNOW_ASSIGNMENT_GROUP:
        snow_payload["assignment_group"] = SNOW_ASSIGNMENT_GROUP

    try:
        resp = requests.post(
            snow_url,
            auth=snow_auth,
            headers=snow_headers,
            json=snow_payload,
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json().get("result", {})
        sys_id = data.get("sys_id")
        number = data.get("number")
        link = f"{SNOW_INSTANCE.rstrip('/')}/nav_to.do?uri={SNOW_TABLE}.do?sys_id={sys_id}" if sys_id else None

        return {
            "status": "success",
            "apar_id": apar_id,
            "summary": llm_text,
            "snow_incident": {
                "sys_id": sys_id,
                "number": number,
                "url": link
            },
            "context": structured_context
        }
    except Exception as e:
        # Include SNOW response content if available for debugging
        err_text = None
        try:
            err_text = resp.text  # type: ignore
        except:
            pass
        return {
            "status": "error",
            "apar_id": apar_id,
            "summary": llm_text,
            "error": f"ServiceNow incident creation failed: {str(e)}",
            "snow_response": err_text
        }
