from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watson_machine_learning.foundation_models import Model
import requests
from dotenv import load_dotenv
import os

load_dotenv()
import json

# === Watsonx.ai Configuration ===
WATSONX_URL = os.getenv("WATSONX_URL")
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
MODEL_ID = os.getenv("WATSONX_MODEL_ID", "mistralai/mistral-medium-2505")
MODEL_PARAMS = {
    "decoding_method": "greedy",
    "min_new_tokens": 1,
    "max_new_tokens": 8000
}

# === FastAPI Fix Service Endpoint ===
FIX_API_BASE_URL = os.getenv(
    "FIX_API_BASE_URL",
    "https://itops.21rj19x2zzm7.us-south.codeengine.appdomain.cloud/fix"
)

# === Initialize Watsonx Model ===
llm_model = Model(
    model_id=MODEL_ID,
    credentials={"url": WATSONX_URL, "apikey": WATSONX_API_KEY},
    project_id=WATSONX_PROJECT_ID,
    params=MODEL_PARAMS
)


@tool(permission=ToolPermission.READ_ONLY)
def ansible_fix_tool(apar_id: str) -> dict:
    """
    Fetches fix result JSON from the FastAPI endpoint for a given APAR ID,
    and uses a Watsonx.ai LLM to create a detailed narrative summary
    describing the actions performed, verification, and next steps.

    Args:
        apar_id (str): APAR identifier (e.g., "AH57177")

    Returns:
        dict: {
            "apar_id": str,
            "summary_text": str,
            "raw_fix_json": {...}
        }
    """
    # --- Step 1: Fetch JSON from the FastAPI Fix Service ---
    try:
        api_url = f"{FIX_API_BASE_URL}/{apar_id}"
        response = requests.get(api_url, timeout=20)
        response.raise_for_status()
        fix_data = response.json()
    except Exception as e:
        return {
            "apar_id": apar_id,
            "error": f"Failed to fetch fix data from {api_url}: {str(e)}"
        }

    # --- Step 2: Prepare data for summarization prompt ---
    steps_text = "\n".join([
        f"{i+1}. {step['step']} — {step['details']}"
        for i, step in enumerate(fix_data.get("fix_steps", []))
    ])
    next_actions_text = "\n".join(fix_data.get("next_actions", []))
    verification_status = fix_data.get("verification_status", "unknown")

    full_prompt = f"""
You are an IBM z/OS system reliability analyst.

Summarize the fix workflow for APAR {apar_id} in a clear, detailed, and business-technical format.
The fix service returned the following JSON data:

System: {fix_data.get('system')}
Subsystem: {fix_data.get('subsystem')}
Maintenance Window: {fix_data.get('maint_window')}
Fix Status: {fix_data.get('status')}
Verification Status: {verification_status}

Summary: {fix_data.get('summary')}
Fix Steps:
{steps_text}

Next Actions:
{next_actions_text}

Write a well-structured summary including:
1. Overview of what the fix did.
2. The critical steps executed during the fix.
3. Verification results and system health.
4. Recommended next actions or monitoring tasks.

Your response should be 2–3 paragraphs long, concise yet technically rich.
"""

    # --- Step 3: Generate summary using Watsonx LLM ---
    try:
        llm_response = llm_model.generate(full_prompt)
        summary_text = llm_response["results"][0]["generated_text"].strip()
    except Exception as e:
        return {
            "apar_id": apar_id,
            "error": f"LLM generation failed: {str(e)}",
            "raw_fix_json": fix_data
        }

    # --- Step 4: Return formatted result ---
    return {
        "apar_id": apar_id,
        "summary_text": summary_text,
        "raw_fix_json": fix_data
    }
