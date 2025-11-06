from ibm_watsonx_orchestrate.agent_builder.tools import tool
import requests
import json

def _pretty_yaml_or_json(text: str) -> str:
    """
    Try JSON -> YAML style, then YAML -> YAML. Fall back to original text.
    Keeps keys order; no extra quoting. Avoids adding non-stdlib deps.
    """
    try:
        # 1) If API returns JSON, pretty print it
        obj = json.loads(text)
        return json.dumps(obj, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        pass

    # 2) Try PyYAML if available
    try:
        import yaml  # PyYAML may be present in your env
        obj = yaml.safe_load(text)
        # Dump as YAML with nice indentation, no key sorting
        return yaml.safe_dump(obj, sort_keys=False, default_flow_style=False)
    except Exception:
        # 3) Give up—return original
        return text

@tool(description="Fetches the Ansible playbook YAML content from the zConcert API.")
def fetch_playbook_tool(playbook_name: str) -> str:
    base_url = "https://z-concert-api.22bx791aigbq.us-south.codeengine.appdomain.cloud"
    url = f"{base_url.rstrip('/')}/{playbook_name}"
    try:
        resp = requests.get(url, timeout=50)
        resp.raise_for_status()
        pretty = _pretty_yaml_or_json(resp.text).strip()
        # Return **plain Markdown** so Orchestrate renders a code block
        return (
            f"Here is the playbook **{playbook_name}** content:\n\n"
            f"```yaml\n{pretty}\n```\n\n"
        )
    except Exception as e:
        return f"Error fetching playbook `{playbook_name}`:\n```\n{e}\n```"

@tool(description="Retrieves the most recent Ansible playbook execution results from the zConcert API.")
def get_playbook_result_tool() -> dict:
    base_url = "https://z-concert-api.22bx791aigbq.us-south.codeengine.appdomain.cloud/response"
    try:
        resp = requests.get(base_url, timeout=50)
        resp.raise_for_status()
        pretty = _pretty_yaml_or_json(resp.text).strip()
        # Include BOTH: a nice chat rendering AND raw fields for chaining
        markdown = (
            "**Latest playbook execution result**\n\n"
            f"```yaml\n{pretty}\n```"
        )
        return {
            "status": "success",
            "execution_content": resp.text,   # raw (for programmatic use)
            "pretty": pretty,                 # pretty text if a caller wants it
            "markdown": markdown              # UI-friendly rendering
        }
    except Exception as e:
        err_md = f"Error getting playbook result:\n```\n{e}\n```"
        return {"status": "error", "error": str(e), "markdown": err_md}
