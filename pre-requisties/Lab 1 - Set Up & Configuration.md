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
---
##  Step 1 – IBM Enviornment Access  

### IBMid Creation Instructions

#### 1. Create IBMid
**To access an environment for the lab, please follow the instructions here as a part of the pre requisites.<br>** 
  - Start by accessing the IBMid registration page. [IBMid Creation](https://www.ibm.com/account/reg/us-en/signup?formid=urx-19776)<br>
  - Enter the required information in the fields provided, such as email address, name, company, and country.<br>
    _IMPORTANT: Your email address becomes your IBMid, which you will use to access the bootcamp environment!<br>_
  - Click the Next button. You will receive an email containing a one-time verification code.<br>
  - Go back to the registration page, enter the code that is provided in the email in the Verification Token field.<br>
  - Click Submit to create an account.<br>
  - **An email will be sent indicating that your IBMid account creation was successful and your account is now activated**.<br>
---
#### 2. Email Confirmation
**Email Aishwarya Hariharan to confirm you have registered and received the IBMid.**
---
#### 3. Join IBM Cloud Account
**Please follow the instructions here as a part of the prerequisites to ensure that you can access to watsonX orchestrate during the event.<br>**
  - Once you receive an email from IBM Cloud, start by accessing the email from no-reply@cloud.ibm.com. The subject should be "Action required: You are invited to join an account in IBM Cloud."<br>
  - Click on "Join now" in the email to join the IBMid account you have been assigned to.<br>
  - Accept the Terms and Conditions in the IBM Cloud page to finish joining the account. Click on the "Join Account" button.<br>
  - You will be routed to the Login page. Log in with your IBMid. NOTE: If you have another account on IBM cloud, you will see a popup asking if you can be switched to this account. Go ahead and click Proceed.<br>
  - Once logged in, confirm that you are in the right IBM Cloud account. This should match the account details from the IBM Cloud email.<br>
---
#### 3. Confirm watsonx Orchestrate Access
**Once you have completed these steps, verify your watsonx Orchestrate access with these steps:<br>** 
  - On the IBM Cloud landing page, click the top left navigation menu (hamburger menu) and select Resource List. Note: If you are a member of multiple IBM Cloud accounts, make sure you are working in the correct account which has the required services available.<br>
  - On the Resource List page, expand the AI / Machine Learning section, and click the watsonX Orchestrate service name.<br>
  - Click Launch watsonX Orchestrate to launch the service.<br>

---

##  Step 2 - Local Machine Setup

  - [Step 1 – Install Python 3.11+, Docker/Podman, & Github](#step-1--install-python-311-,-docker/podman-,-&-github)
  - [Step 2 – Clone the Repository](#step-2--clone-the-repository)
  - [Step 3 – Navigate into the Project Folder](#step-3--navigate-into-the-project-folder)
  - [Step 4 – Create and Activate a Virtual Environment](#step-4--create-and-activate-a-virtual-environment)
  - [Step 5 – Install and Validate ADK](#step-5--install-and-validate-adk)
  - [Step 6 – Activate Environment](#step-8--activate-environment)

---

### Step 1 – Install Python 3.11+, Docker/Podman, & Github
*We need a compatible Python version because the watsonx Orchestrate ADK relies on modern language features and libraries that are only supported in Python 3.11 or higher*.

Make sure **Python 3.11 or above** (up to 3.13) is installed. 
[Download Python](https://www.python.org/downloads/)

If you do not have it already ensure that you install either Docker or Podman.
[Download Podman](https://podman.io/)
[Download Docker](https://docs.docker.com/desktop/setup/install/mac-install/)

Finally ensure you have Github downloaded and you have an account.
[Download Github Desktop](https://desktop.github.com/download/)


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

### Step 6 – Activate Environment
Generate an API key using the instructions (upto step 8) on this page section IBM Cloud:
https://developer.watson-orchestrate.ibm.com/environment/production_import#ibm-cloud

Run the following command to activate your environment.  
```bash
orchestrate env activate <name>
```
You will be prompted to enter your WXO API key.

---

##  Step 3a – Distributed Lab Track Configuration

### RedHat / Quay.io

Create a free trial on Quay.io
[Download Quay.io](--)

---

##  Step 3b – Mainframe Lab Track Configuration

### Ansible

Make sure you have access to Ansible
[Download Ansible](--)

--- 
Congratulations! You are ready to now move into Agent Creation during the Hands-On Lab Session!
