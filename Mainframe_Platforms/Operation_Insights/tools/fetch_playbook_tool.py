import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(
    description=("Fetches the Ansible playbook YAML content from the hosted zConcert API."),
)
def fetch_playbook_tool(playbook_name: str) -> str:
    """
    Fetches the specified playbook YAML content from the zConcert API endpoint.
    Returns a properly formatted Markdown string for clean rendering.
    """
    base_url = "https://z-concert-api.22bx791aigbq.us-south.codeengine.appdomain.cloud"
    url = f"{base_url.rstrip('/')}/{playbook_name}"

    try:
        resp = requests.get(url, timeout=50)
        resp.raise_for_status()

        return (
            f"Here is the playbook **{playbook_name}** content:\n\n"
            f"```yaml\n{resp.text.strip()}\n```\n\n"
            "Please review the playbook content. Are you ready to apply it?"
        )

    except Exception as e:
        return f"Error fetching playbook `{playbook_name}`:\n```\n{str(e)}\n```"
