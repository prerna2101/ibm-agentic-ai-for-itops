import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from ibm_watsonx_orchestrate.run import connections
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
from typing import Optional


@tool(
    name="concertzEvents",
    description=("Supported ops: cicsplex, allRegions, regionsByPlex, regionDetails, and recheckRegion."),
    permission=ToolPermission.READ_ONLY,
)

def getConcertZEvents(op: str, details: str = "") -> dict:
    base = "https://z-concert-api.22bx791aigbq.us-south.codeengine.appdomain.cloud/"
    
    try:
        if op == "cicsplex":
            url = f"{base}/operation/cicsplex"
            r = requests.get(url, verify=False, timeout=50)
            r.raise_for_status(); 
            return r.json()

        if op == "allRegions":
            url = f"{base}/operation/cics/regions"
            r = requests.get(url, verify=False, timeout=50)
            r.raise_for_status(); 
            return r.json()

        if op == "regionsByPlex":
            detail = details.lower()
            url = f"{base}/operation/cicsplex/region/{detail}"
            r = requests.get(url, verify=False, timeout=50)
            r.raise_for_status(); 
            return r.json()
        
        if op == "regionDetails":
            url = f"{base}/operation/cics/region/{details}"
            r = requests.get(url, verify=False, timeout=50)
            r.raise_for_status()
            return r.json()
        if op == "recheckRegion":
            url = f"{base}/operation/cics/region/recheck/{details}"
            r = requests.get(url, verify=False, timeout=50)
            r.raise_for_status()
            return r.json()

        return {"error": f"Unsupported op '{op}'"}
    except requests.RequestException as e:
        return {"error": str(e)}
