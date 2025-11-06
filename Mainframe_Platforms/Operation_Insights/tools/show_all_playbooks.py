import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool(
    description=("Shows all available playbooks from the zConcert API."),
)
def show_all_playbooks() -> dict:
    return f"There are 4 playbooks available: `invalidTCP`, `prepPLT2`, `solvePLT2`, `validTCP`."
