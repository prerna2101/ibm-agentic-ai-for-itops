# IBM Agentic AI Lab Setup (Windows)

This guide covers initial local machine setup using **PowerShell** on **Windows**.

## 1. Python Installation (via Microsoft Store)

The easiest way to get Python running reliably on Windows is via the Microsoft Store:

1. **Open the Microsoft Store** (search for it in the Windows Start Menu).
2. **Search for "Python 3.13"** (or the latest stable version).
3. Ensure the app is published by the **Python Software Foundation (PSF)**.
4. Click "**Get**" or "**Install**" and wait for the download to complete.
5. After installation, open PowerShell and verify the install by running:

   ```
   python --version
   ```
   or
   ```
   python3.13 --version
   ```
   This should show your installed version number.

## 2. Create the Virtual Environment

In your PowerShell terminal, run:

```
python3.13 -m venv envadk
```
This creates the `envadk` folder containing the virtual environment.

## 3. Activate the Environment (Key Difference)

This step differs from Mac/Linux. Instead of using `source envadk/bin/activate`, on Windows **run the PowerShell-specific script**:

```
.\envadk\Scripts\Activate.ps1
```
Your prompt should now start with `(envadk)`.

## 4. Install the Core Library

If your environment is activated, install the IBM Agentic AI SDK:

```
pip install ibm-watsonx-orchestrate
```

---
