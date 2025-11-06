from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from datetime import datetime
import requests, os
from dotenv import load_dotenv
load_dotenv()


SNOW_INSTANCE = os.getenv("SNOW_INSTANCE")
SNOW_USER = os.getenv("SNOW_USER")
SNOW_PASSWORD = os.getenv("SNOW_PASSWORD")
SNOW_TABLE = "incident"

SNOW_CATEGORY =  "IT Operations"
SNOW_SUBCATEGORY = "SNOW_SUBCATEGORY", "Mainframe"
SNOW_URGENCY = "SNOW_URGENCY", "3"
SNOW_IMPACT = "SNOW_IMPACT", "2"
SNOW_CALLER_ID = "SNOW_CALLER_ID"
SNOW_ASSIGNMENT_GROUP = "SNOW_ASSIGNMENT_GROUP"


@tool(permission=ToolPermission.READ_WRITE)
def create_snow_incident_tool(short_description: str, incident_details: str = "") -> dict:
    """
    Creates a ServiceNow incident with the given short_description and optional detailed context.
    """
    if not SNOW_INSTANCE or not SNOW_USER or not SNOW_PASSWORD:
        return {"status": "error", "message": "ServiceNow credentials or instance URL not configured."}

    snow_url = f"{SNOW_INSTANCE.rstrip('/')}/api/now/table/{SNOW_TABLE}"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    auth = (SNOW_USER, SNOW_PASSWORD)

    description = (
        f"{incident_details}\n\n---\n"
        f"Ticket created automatically by watsonx Orchestrate Agent\n"
        f"Timestamp: {datetime.utcnow().isoformat()}Z"
    )

    payload = {
        "short_description": short_description,
        "description": description,
        "category": SNOW_CATEGORY,
        "subcategory": SNOW_SUBCATEGORY,
        "urgency": SNOW_URGENCY,
        "impact": SNOW_IMPACT
    }

    if SNOW_CALLER_ID:
        payload["caller_id"] = SNOW_CALLER_ID
    if SNOW_ASSIGNMENT_GROUP:
        payload["assignment_group"] = SNOW_ASSIGNMENT_GROUP

    try:
        resp = requests.post(snow_url, auth=auth, headers=headers, json=payload, timeout=50)
        resp.raise_for_status()

        result = resp.json().get("result", {})
        sys_id = result.get("sys_id")
        number = result.get("number")
        link = f"{SNOW_INSTANCE.rstrip('/')}/nav_to.do?uri={SNOW_TABLE}.do?sys_id={sys_id}" if sys_id else None

        return {
            "status": "success",
            "short_description": short_description,
            "snow_incident": {"number": number, "url": link, "sys_id": sys_id}
        }

    except Exception as e:
        err_text = None
        try:
            err_text = resp.text  # type: ignore
        except:
            pass
        return {"status": "error", "error": str(e), "snow_response": err_text}
