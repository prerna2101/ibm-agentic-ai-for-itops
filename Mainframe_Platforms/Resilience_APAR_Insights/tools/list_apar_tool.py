from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_boto3 import resource as ibm_boto3_resource
from ibm_botocore.client import Config
import json
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

# === COS Configuration (read from environment or set directly) ===

COS_BUCKET_NAME = os.getenv("COS_BUCKET_NAME")
COS_API_KEY_ID = os.getenv("COS_API_KEY_ID")
COS_INSTANCE_CRN = os.getenv("COS_INSTANCE_CRN")
COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
COS_JSON_KEY = os.getenv("COS_JSON_KEY", "products_db2_12.json")

# Initialize COS resource
cos = ibm_boto3_resource(
    "s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT,
)

@tool(permission=ToolPermission.READ_ONLY)
def list_apar_tool() -> list:
    """
    Reads the DB2 z/OS product JSON file from an IBM COS bucket
    and returns a tabular APAR summary.

    The JSON file is expected to have a structure similar to:
    products_db2_12.json (with 'products_data' → 'features' → 'apars').

    Environment Variables Required:
        COS_BUCKET_NAME, COS_API_KEY_ID, COS_INSTANCE_CRN, COS_ENDPOINT
        (Optionally COS_JSON_KEY to specify the JSON object key)

    Returns:
        list: List of dicts representing the APAR summary table.
    """

    # --- Fetch JSON from COS ---
    try:
        cos_object = cos.Object(COS_BUCKET_NAME, COS_JSON_KEY)
        json_bytes = cos_object.get()["Body"].read()
        json_data = json.loads(json_bytes.decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"Error reading JSON from COS: {str(e)}")

    # --- Extract APAR details ---
    apar_entries = []
    seen = set()

    for product in json_data.get("products_data", []):
        for feature in product.get("features", []):
            for apar in feature.get("apars", []):
                apar_id = apar.get("apar_id")
                if apar_id not in seen:
                    seen.add(apar_id)
                    apar_entries.append({
                        "APAR ID": apar.get("apar_id"),
                        "Type": apar.get("apar_type"),
                        "Risk Score": apar.get("risk_assessment_score"),
                        "Risk Level": apar.get("risk_assessment"),
                        "Hold Symptom": apar.get("hold_symptom"),
                        "Held Sysmod": apar.get("held_sysmod"),
                    })

    # Convert to DataFrame for structure (optional)
    df = pd.DataFrame(apar_entries)

    # --- Return formatted output for Orchestrate ---
    return df.to_dict(orient="records")
