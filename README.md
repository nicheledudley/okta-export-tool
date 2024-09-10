# Okta Export Tool


This Python tool exports data from your Okta environment into a CSV format for access reviews. It retrieves information about Okta applications, groups, and users, including detailed user attributes like title, department, manager, and more.

Much of the functionality is built using the [Okta API](https://developer.okta.com/docs/api/) documentation.

## Features

- Export Okta applications, groups, and users.
- Includes detailed user information, such as:
  - Full Name
  - Title
  - Division
  - Department
  - Manager
  - Team
- Supports pagination to handle large datasets.
- Progress indicators to visualize the export process.

## Prerequisites

To use this tool, you will need the following:

- Python 3.x installed on your system.
- An Okta API token with read permissions for users, groups, and applications.
- Access to your Okta organization's base URL.

## Installation

### Step 1: Clone the repository

Clone this repository to your local machine:

```bash
git clone https://github.com/nicheledudley/okta-export-tool 
cd okta-export-tool
```

### Step 2: Set up a virtual environment
Create and activate a Python virtual environment to isolate dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install the required dependencies
After activating the virtual environment, install the dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 4: Set up the `.env` file
In the root directory of the project, create a `.env` file. to store your Okta API token and your Okta organization's base URL.

Add the following lines to the `.env` file:

```
OKTA_API_TOKEN=your_okta_api_token_here
OKTA_BASE_URL=https://your_okta_domain.okta.com
```
Make sure to replace `your_okta_api_token_here` with your actual Okta API token and `your_okta_domain.okta.com` with your organization's base URL.

## Usage

### Step 1: Run the script
Run the script to fetch data from Okta and generate a CSV file. This will collect all applications, groups, and users, and output detailed information about each user.

```bash
python3 okta_access_review.py
```

### Step 2: View the output
The tool will create a file called `okta_access_review.csv` in the project directory. This CSV file will include columns such as:

> **Note:** Some of these will be specific to your Okta setup and attributes and might need to be adjusted if you do not have all of these fields mapped

- **Application:** The name of the Okta application.
- **Application ID:** The unique ID of the application.
- **Group**: The name of the group associated with the application.
- **Group ID:** The unique ID of the group.
- **User Full Name:** The full name of the user.
- **User Login:** The user’s login email.
- **Title:** The user's job title.
- **Division:** The division the user belongs to.
- **Department:** The department the user belongs to.
- **Manager:** The user’s manager.
- **Team:** The team to which the user belongs.

## Contributing
If you want to contribute to this project, follow these steps:

 1. Fork the repository.
 2. Create a new branch for your feature or bug fix:
```bash
git checkout -b feature-or-bugfix-branch-name
```
 3. Make your changes and commit them:
```bash
git add .
git commit -m "Description of changes"
```
 4. Push to your forked repository:
```bash
git push origin feature-or-bugfix-branch-name
```
 5. Open a pull request on the original repository.
