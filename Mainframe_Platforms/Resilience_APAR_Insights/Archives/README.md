# 🧠 ITOPs Agents for Mainframe Platforms using IBM Watsonx Orchestrate ADK

This project demonstrates how to build an AI-powered **IT Operations (ITOPs) Assistant Agent** for Mainframe Operations using the **IBM Watsonx Orchestrate Agent Development Kit (ADK)**.  
The assistant helps IT teams automate operational insights and diagnostics with natural language commands.


---

## ⚙️ Create Agent using Orchestrate ADK

### 1. Install Python 3.11+
Make sure **Python 3.11** or above (up to **3.13**) is installed.


### 2. Clone the Repository
Open VS Code Terminal and Run below commands.  
```bash
git clone https://github.ibm.com/ibm-us-fsm-ce/AgenticAIforITOps.git
````


### 3. Navigate into the Project Folder

```bash
cd AgenticAIforITOps/Resilience APAR Insights/
```


### 4. Create a Virtual Environment

```bash
python -m venv envadk
or
python3 -m venv envadk

source envadk/bin/activate
```


### 5. Install ADK and Validate

```bash
pip install ibm-watsonx-orchestrate
# If you get errors, update ADK
pip install --upgrade ibm-watsonx-orchestrate

# Validate installation
orchestrate --version
orchestrate --help
```
### 6. Reserve Watsonx Orchestrate

1. Open https://techzone.ibm.com/my/reservations in your browser.  
2. In the search bar, type “watsonx Orchestrate Trial/Standard plan” and select the corresponding environment.
    

![orchestrate_env_name](images/orchestrate_env_name.png)


3. Click Request an environment.   
4. Fill out the form with the required details and submit.  

![reserving](images/reserving.png)

5. After successful reservation, you’ll receive an email invitation to join the environment. Click the link in the email to join.  

Similarly, reserve the “watsonx Discovery with Assistant, AI, and Speech” environment.


### 7. Add Watsonx Environment

1. Go to https://techzone.ibm.com/my/reservations  
2. Under watsonx Orchestrate Trial/Standard plan, click Open this environment.  

 ![my_reservations](images/my_reservations.png)
  
3. Check your Cloud Account Number and click on Cloud Resources.
 ![env_details](images/environment_details.png)

4. Ensure you are in same IBM cloud account as in techzone reservation.    
In the Resource List, expand AI / Machine Learning and click on the Watson Orchestrate-itz resource.  
  ![env_details](images/resources.png)

5. Run the following command to add your environment.
Replace `<service-instance-url>` with your Watsonx Orchestrate URL and `<name>` with any name (e.g., Itops):
```bash
orchestrate env add -n <name> -u <service-instance-url>
```
  ![env_details](images/orchestrate_launch_page.png)

### 8. Activate Environment
Generate an API key using the instructions (upto step 8) on this page section IBM Cloud:
https://developer.watson-orchestrate.ibm.com/environment/production_import#ibm-cloud

Run the following command to activate your environment.  
```bash
orchestrate env activate <name>
```
You will be prompted to enter your WXO API key.

### 9. Create `.env` File
1. Go to https://techzone.ibm.com/my/reservations  
2. Under Watsonx Discovery with Assistant, AI, and Speech, click Open this environment. 

 ![my_reservations](images/my_reservations.png)
  
3. Check your Cloud Account Number and click Cloud Resources or Go to https://cloud.ibm.com/resources.  
 ![env_details](images/environment_details.png)

4. Ensure you are in same IBM cloud account as in techzone reservation.   
