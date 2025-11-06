# Lab 2 - Agent and Tool Creation

## Resilience APAR Insights Agents using IBM watsonx Orchestrate ADK

Learn how to define and configure agents using provided YAML, Python files, and tools from MCP servers.  
This lab sets the foundation for building intelligent, task-specific agents that power automation flows within IBM Watsonx Orchestrate.

---

##  Use Case Overview

In large enterprise IT systems, software and hardware issues are tracked as **APARs (Authorized Program Analysis Reports)**.  
This lab demonstrates how to build a **Resilience APAR Insights Agent** that can:

1. Retrieve APAR-level defect details from IBM Z OS systems.  
2. Summarize critical updates and their impact using **Watsonx.ai**.  
3. Automatically create incidents in **ServiceNow**.  
4. Trigger **Ansible playbooks** to remediate issues automatically.

This shows how Watsonx Orchestrate can serve as an intelligent automation layer for IT Operations — powered by AI and connected tools.

---

##  Understanding the `itops_agent.yaml` File

The YAML file defines the **configuration blueprint** for your Watsonx Orchestrate agent.

###  Key Sections Explained

| Section | Purpose | Example |
|----------|----------|----------|
| `name` | Identifies the agent inside Watsonx Orchestrate. | `itops_agent_bootcamp` |
| `llm` | Specifies the model used for reasoning. | `watsonx/meta-llama/llama-3-405b-instruct` |
| `description` | Explains what the agent does. | “Retrieves and summarizes IBM Z OS APAR information.” |
| `instructions` | Defines rules for how the agent should behave. | Maps queries to tool calls (e.g. “list APAR defects”). |
| `tools` | Lists MCP tools available to the agent. | `list_apar_tool`, `summarize_apar_update_tool`, etc. |
| `chat_with_docs` | Optional document retrieval toggle. | `enabled: false` |

###  How It Works

When you import this YAML:
1. Watsonx Orchestrate registers the agent.  
2. The YAML maps user queries to specific MCP tools.  
3. The LLM processes natural-language input and calls tools automatically.  
4. Each MCP tool returns structured data or triggers an action.  

Together, these definitions make your agent both **intelligent** and **actionable**.

---

##  What Is an MCP Server?

An **MCP (Model Context Protocol) Server** hosts small, purpose-built “tools” that your agent can use.  
Each tool handles a specific backend function — such as fetching APAR data, summarizing text, or running an automation job.

Adding an MCP server is like giving your agent new abilities — no coding required.

| MCP Tool | Description | What Happens When You Call It |
|-----------|--------------|-------------------------------|
| `list_apar_tool` | Lists APAR defects. | Queries backend data to fetch APAR IDs, Type, Risk Level, and Hold Symptom. |
| `summarize_apar_update_tool` | Summarizes APAR updates. | Uses Watsonx.ai to convert technical updates into readable summaries. |
| `summarize_apar_and_create_snow_incident_tool` | Creates ServiceNow incidents. | Opens an incident in ServiceNow and returns its link. |
| `ansible_fix_tool` | Executes Ansible automation. | Runs an Ansible playbook to apply the fix automatically. |

>  *Think of each MCP tool as a mini-app that the agent can use to perform real-world IT operations tasks.*

---

##  Getting Started (Beginner Setup)

### Step 1 – Access IBM Cloud
- Go to [https://cloud.ibm.com](https://cloud.ibm.com)  
- Launch **Watsonx Orchestrate** from your IBM Cloud Dashboard.

### Step 2 – Install UVX
`uvx` (Universal Virtual Executor) connects MCP tools to Watsonx Orchestrate.

```bash
uvx --version        # Verify installation
pip install uvx      # Install if missing
### Step 3 – Workflow Summary

Before diving into the detailed steps, let’s quickly understand the overall workflow that you’ll follow in this lab.

1. **Import the YAML Agent (`itops_agent.yaml`)**  
   The YAML file defines your agent’s structure — including its name, description, LLM configuration, and tool mappings.  
   When imported into Watsonx Orchestrate, it registers the agent and prepares it for interaction.

2. **Add MCP Tools to the Agent**  
   You’ll connect multiple MCP tools (hosted on IBM Code Engine) to your agent.  
   Each tool gives your agent a new ability — for example, fetching APAR data, summarizing updates, or creating ServiceNow incidents.

3. **Test the Agent via Chat Commands**  
   Once setup is complete, you’ll use the Watsonx Orchestrate chat interface to interact with your agent using natural language.  
   The agent will interpret your commands, invoke the correct MCP tools, and return responses in real time.

>  **Tip:** Think of this workflow as “teaching” your agent how to understand questions, call the right backend tools, and deliver intelligent answers — all without writing code.

# Agent Creation Step-by-Step Guide
---

## Step 1 – Import Tools & Agents

*This step registers some of our pre-built agents into your Watsonx Orchestrate environment.*

In your terminal use the import script:
```bash
./import-all.sh
```

Click on Launch Watsonx Orchestrate from IBM cloud.
![env_details](images/orchestrate_launch_page.png)

After that you will land on the WxO homepage
![wxo_homepage](images/wxo-homepage.png)

Click on the manage agents tab from the bottom right corner
![wxo_homepage](images/wxo-manage-agents.png)

Select your agent 'itops_agent_bootcamp' from the list
![wxo_homepage](images/agents-tools-hs.png)

After that you will land on the homepage of your agent where you can modify your agent and add extra details
![wxo_homepage](images/agents-hs.png)

Now we will add some tools from our MCP servers.
Scroll down to reach the tools section and select Add tool
![wxo_homepage](images/select-tools.png)

Then select 'add from file or mcp server'
![wxo_homepage](images/select-mcp-tool.png)

After proceeding forward in the next section add the server name as - 'list_apar_tool' and in the install command enter the following-
```bash
uvx mcp-proxy https://itops-mcp-tool-1.21rj19x2zzm7.us-south.codeengine.appdomain.cloud/sse
```
![wxo_homepage](images/mcp-tool1.png)

Once you get the success message, in the next page, switch the activation toggle for the tool to 'on' position
![wxo_homepage](images/mcp-tool1-toggle.png)
Then again click add MCP server from the top and add the next tool

Give the name as 'summarize_apar_update_tool'and in the install command enter the following-
```bash
uvx mcp-proxy https://itops-mcp-tool-2.21rj19x2zzm7.us-south.codeengine.appdomain.cloud/sse
```

![wxo_homepage](images/mcp-tool2.png)

Once you get the success message, in the next page, switch the activation toggle for the tool to 'on' position
![wxo_homepage](images/mcp-tool2-toggle.png)


Once everything is done, move to the homepage of your agent and you can start asking questions

Ask the first question as
```bash
List the APAR level defect information
```
![wxo_homepage](images/tool1-output.png)

Then ask the second question for getting the summary of the defect from watsonx ai-
```bash
summarize the critical updates & their impact for APAR ID- AH49479

```

![wxo_homepage](images/tool2-output.png)
![wxo_homepage](images/tool2-output2.png)


Then ask the third question for getting the summary of the defect from watsonx ai-
```bash
Create a Service Now incident for APAR ID - AH49479

```

![wxo_homepage](images/tool3-output.png)

This will create a Service Now incident for you and give you a url in the response that will take you to the service now website for more details

![wxo_homepage](images/service-now.png)

Then ask the third question for getting the summary of the defect from watsonx ai-
```bash
Run the ansible playbook to fix the defect for APAR ID - AH49479

```

![wxo_homepage](images/tool4-output.png)
![wxo_homepage](images/tool4-output2.png)


## 🧭 Architecture Overview

The architecture below shows how the **Watsonx Orchestrate agent**, the **MCP servers**, and the **external systems** interact to automate IT operations.

---

###  1. Watsonx Orchestrate Layer

This is the core automation platform where your agent lives and operates.

- **Agent Runtime** – Handles user interactions through natural language.
- **LLM Reasoning** – Uses large language models (like Llama 3) to interpret intent.
- **Agent Configuration (YAML)** – Defines how the agent maps user queries to specific MCP tools.

When a user asks a question, Watsonx Orchestrate reads the YAML definition, identifies which tool to call, and executes it.

---

###  2. Agent Definition (`itops_agent.yaml`)

This YAML file acts as the **blueprint** for your agent.  
It contains:

- The **agent’s name**, **description**, and **model** configuration.
- A list of **tools** the agent can call (retrieved from MCP servers).
- Instruction logic that helps the agent decide when and how to use each tool.

Example responsibilities defined in YAML:
- When a user asks for “APAR defect details” → call `list_apar_tool`.  
- When a user asks for a “summary of updates” → call `summarize_apar_update_tool`.

---

###  3. MCP Servers (Model Context Protocol)

MCP servers are like **skill libraries** for your agent.  
Each MCP server hosts one or more **tools** that handle a specific backend task.

Your agent connects to these servers using the `uvx mcp-proxy` command.

| MCP Server | Tool Name | Purpose |
|-------------|------------|----------|
| `https://itops-mcp-tool-1...` | `list_apar_tool` | Fetches APAR defect information from backend data sources. |
| `https://itops-mcp-tool-2...` | `summarize_apar_update_tool` | Uses Watsonx.ai to generate summaries for APAR updates. |
| (Optional) | `summarize_apar_and_create_snow_incident_tool` | Creates ServiceNow incident records automatically. |
| (Optional) | `ansible_fix_tool` | Executes Ansible playbooks for automated fixes. |

> 💡 Each MCP server expands your agent’s “skillset” without modifying its code.

---

###  4. External Systems

The MCP tools interact with different backend systems and APIs to complete their tasks.

| System | Role | Example Output |
|---------|------|----------------|
| **IBM Z OS APAR Database** | Stores APAR-level defect and patch information. | Returns JSON data about APAR IDs, severity, and fix status. |
| **Watsonx.ai Endpoint** | Provides natural-language processing and summarization. | Returns human-readable summaries of technical updates. |
| **ServiceNow** | Handles IT incident creation and tracking. | Returns a link to the created ServiceNow incident. |
| **Ansible Automation Platform** | Executes pre-defined playbooks for system remediation. | Returns logs or success confirmation from the automation job. |

---

###  5. End-to-End Workflow

Here’s the overall interaction flow:

1.  **User** sends a natural-language query to the Watsonx Orchestrate chat interface.  
2.  **Watsonx Orchestrate Agent** interprets the request using the `itops_agent.yaml` file.  
3.  The agent calls the relevant **MCP tool** hosted on IBM Code Engine.  
4.  The MCP tool performs the backend operation (fetch, summarize, create ticket, or execute playbook).  
5.  The response is returned to Watsonx Orchestrate and displayed back to the user.

---

###  Summary Diagram (Text Representation)


┌────────────────────────────────────────────┐
│ Watsonx Orchestrate Agent │
│ (User Interaction + LLM Reasoning Layer) │
└────────────────────────────────────────────┘
│
│ Reads config
▼
┌────────────────────────────────────────────┐
│ itops_agent.yaml │
│ (Defines tools, logic, and model) │
└────────────────────────────────────────────┘
│
│ Invokes tools via UVX
▼
┌────────────────────────────────────────────┐
│ MCP Servers │
│--------------------------------------------│
│ list_apar_tool │
│ summarize_apar_update_tool │
│ summarize_apar_and_create_snow_incident_tool │
│ ansible_fix_tool │
└────────────────────────────────────────────┘
│
│ Connects to external systems
▼
┌────────────────────────────────────────────┐
│ External Systems & Platforms │
│--------------------------------------------│
│ IBM Z OS APAR DB | Watsonx.ai Model │
│ ServiceNow | Ansible Automation │
└────────────────────────────────────────────┘
![Architecture Diagram](images/A_flowchart_diagram_in_the_image_illustrates_the_a.png)

















