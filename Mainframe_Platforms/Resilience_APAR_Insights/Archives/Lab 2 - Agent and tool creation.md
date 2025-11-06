# Lab 2 - Agent and tool Creation

## Resilience Apar Insights Agents using IBM watsonx Orchestrate ADK

Learn how to define and configure agents using provided YAML, Python files and adding tools from MCP servers. This step sets the foundation for building intelligent, task-specific agents that power your automation flow.

More details on Resilience APAR insight — [View the file](./Resilience_APAR_Insights_guide.md)

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
![wxo_homepage](images/agent-hs.png)

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
















