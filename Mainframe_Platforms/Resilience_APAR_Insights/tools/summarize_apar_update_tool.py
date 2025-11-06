from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_boto3 import resource as ibm_boto3_resource
from ibm_botocore.client import Config
from ibm_watson_machine_learning.foundation_models import Model
import json
from dotenv import load_dotenv
import os

load_dotenv()

# === COS Configuration ===
COS_BUCKET_NAME = os.getenv("COS_BUCKET_NAME")
COS_API_KEY_ID = os.getenv("COS_API_KEY_ID")
COS_INSTANCE_CRN = os.getenv("COS_INSTANCE_CRN")

COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
COS_JSON_KEY = os.getenv("COS_JSON_KEY", "apar_info.json")

# === Watsonx.ai Model Configuration ===
WATSONX_URL = os.getenv("WATSONX_URL")
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

MODEL_ID = "mistralai/mistral-medium-2505"
MODEL_PARAMS = {
    "decoding_method": "greedy",
    "min_new_tokens": 1,
    "max_new_tokens": 8000
}

# Initialize COS client
cos = ibm_boto3_resource(
    "s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT,
)

# Initialize LLM model from Watsonx.ai
extractor_model = Model(
    model_id=MODEL_ID,
    credentials={"url": WATSONX_URL, "apikey": WATSONX_API_KEY},
    project_id=WATSONX_PROJECT_ID,
    params=MODEL_PARAMS
)


@tool(permission=ToolPermission.READ_ONLY)
def summarize_apar_update_tool(apar_id: str) -> str:
    """
    Summarizes the critical update, impact, and workarounds for a given APAR ID.

    Reads apar_info.json from IBM COS, retrieves the matching APAR entry,
    and uses a Watsonx LLM to generate a summary.

    Args:
        apar_id (str): The APAR ID to summarize (e.g., "AH57177").

    Returns:
        str: A concise natural-language summary for that APAR ID.
    """

    # --- Step 1: Load JSON from COS ---
    try:
        cos_object = cos.Object(COS_BUCKET_NAME, COS_JSON_KEY)
        json_bytes = cos_object.get()["Body"].read()
        apar_data = json.loads(json_bytes.decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"Error reading JSON from COS: {str(e)}")

    # --- Step 2: Find matching APAR ---
    matched_apar = None
    for apar in apar_data.get("apars", []):
        if apar.get("apar_id") == apar_id:
            matched_apar = apar
            break

    if not matched_apar:
        return f"No APAR found with ID: {apar_id}"

    # --- Step 3: Prepare summarization prompt ---
    critical_update = matched_apar.get("critical_update_description", "")
    impact_summary = matched_apar.get("impact_summary", "")
    workarounds = matched_apar.get("workarounds", [])

    workarounds_text = "\n".join(
        [f"- {w.get('description')} (Impact: {w.get('impact')})" for w in workarounds]
    )

    full_prompt = f"""
You are an expert IBM mainframe software analyst.
Summarize the following APAR ({apar_id}) in 3 concise paragraphs:

1. **Critical Update Description:** {critical_update}
2. **Impact Summary:** {impact_summary}
3. **Workarounds:** {workarounds_text}

Your summary should be written in clear, business-technical language
that can be shared in an executive risk report.
"""

    # --- Step 4: Generate summary via Watsonx.ai LLM ---
    try:
        response = extractor_model.generate(full_prompt)
        result_text = response["results"][0]["generated_text"]
    except Exception as e:
        raise RuntimeError(f"LLM generation failed: {str(e)}")

    return result_text
