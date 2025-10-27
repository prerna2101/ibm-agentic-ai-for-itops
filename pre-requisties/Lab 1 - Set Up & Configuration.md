# Lab 1 - Set Up & Configuration
## ITOPs Agents using IBM watsonx Orchestrate ADK

To ensure a smooth and productive experience during the IBM TechXchange Workshop: Agentic AI for ITOps, all participants must complete the following setup steps prior to the event on November 6.

We’ve organized the prerequisites into three buckets:

## 1. IBM Environment Access
Set up your IBM credentials and platform access to participate in the hands-on labs.
- Create or verify your IBMid
- Ensure access to the watsonx Orchestrate environment
- Complete any onboarding steps required for environment assignment

## 2. Local Machine Setup
Prepare your personal device with the necessary tools and packages.
- Install Python (recommended version will be specified)
- Set up the Agent Development Kit (ADK)
- Verify that your system meets the minimum requirements

## 3. Lab Track Configuration
Customize your setup based on your selected lab track.
- Follow the track-specific pre-requisites for additional setup steps.
---

## Table of Contents
### Set Up & Configuration Step-by-Step Guide

- [Step 1 – IBM Enviornment Access](#step-1--IBM-Enviornment-access)
- [Step 2 – Local Machine Setup](#step-2--local-machine-setup)
- [Step 3a – Distributed Lab Track Configuration](#step-3a--distributed-lab-track-configuration)
- [Step 3b – Mainframe Lab Track Configuration](#step-3b--mainframe-lab-track-configuration)


  - [Step 1 – Install Python 3.11+](#step-1--install-python-311)
  - [Step 2 – Clone the Repository](#step-2--clone-the-repository)
  - [Step 3 – Navigate into the Project Folder](#step-3--navigate-into-the-project-folder)
  - [Step 4 – Create and Activate a Virtual Environment](#step-4--create-and-activate-a-virtual-environment)
  - [Step 5 – Install and Validate ADK](#step-5--install-and-validate-adk)
  - [Step 6 – Add Your Environment](#step-7--add-your-environment)
  - [Step 7 – Activate Environment](#step-8--activate-environment)


# Set Up & Configuration Step-by-Step Guide

### Step 1 – Install Python 3.11+
*We need a compatible Python version because the watsonx Orchestrate ADK relies on modern language features and libraries that are only supported in Python 3.11 or higher*.

Make sure **Python 3.11 or above** (up to 3.13) is installed. 
[Download Python](https://www.python.org/downloads/)

---

### Step 2 – Clone the Repository

In your terminal enter the following:

```bash
git clone https://github.ibm.com/ibm-us-fsm-ce/AgenticAIforITOps.git
```

*Cloning the repo gives you access to all the pre-built scripts, YAML files, and configurations required for agent creation and orchestration.*

---

### Step 3 – Navigate into the Project Folder

To ensure you are in the correct place, in your terminal enter the following:

```bash
cd AgenticAIforITOps/Distributed\ Platforms/
```
---

### Step 4 – Create and Activate a Virtual Environment

In your terminal now enter: 

```bash
python -m venv envadk
source envadk/bin/activate
```
*A virtual environment isolates dependencies, preventing conflicts with other Python projects and ensuring a clean setup for the ADK.*

---

### Step 5 – Install and Validate ADK

Enter the following commands into your terminal:

```bash
pip install ibm-watsonx-orchestrate
pip install --upgrade ibm-watsonx-orchestrate

orchestrate --version
```
*Installing the watsonx Orchestrate ADK provides the core tools for building and managing agents.* 

---

### Step 6 – Add Your Environment

1. Go to https://techzone.ibm.com/my/reservations  
2. Under watsonx Orchestrate Trial/Standard plan, click Open this environment.  

 <p align="center">
  <img src="images/my_res.png" width=800px/>
</p>
  
3. Check your Cloud Account Number and click on IBM Cloud Login to sign in with your IBMiD for access to watsonx Orchestrate.

 ![env_details](images/environment_details.png)

4. Ensure you are in same IBM Cloud Account as indicated in the Techzone reservation.    
In the hamburger menu in the top left click to open the Resource List, expand AI / Machine Learning, and click on the Watson Orchestrate-itz resource.  
  ![env_details](images/resources.png)

5. Run the following command in your terminal with the information on the Orchestrate landing page to add your environment.
Replace `<service-instance-url>` with your Watsonx Orchestrate URL and `<name>` with any name (e.g., Itops):
```bash
orchestrate env add -n <name> -u <service-instance-url>
```
  ![env_details](images/orchestrate_launch_page.png)

---

### Step 8 – Activate Environment
Generate an API key using the instructions (upto step 8) on this page section IBM Cloud:
https://developer.watson-orchestrate.ibm.com/environment/production_import#ibm-cloud

Run the following command to activate your environment.  
```bash
orchestrate env activate <name>
```
You will be prompted to enter your WXO API key.

---

Congratulations! You are ready to now move into Agent Creation!
 [Find the lab here](https://github.ibm.com/ibm-us-fsm-ce/agentic-ai-for-itops/blob/main/Distributed%20Platforms/Lab%203%20-%20Deploy%20%26%20Test.md)
