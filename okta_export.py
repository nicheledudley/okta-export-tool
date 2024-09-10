from dotenv import load_dotenv
import os
import requests
import pandas as pd
from tqdm import tqdm  # Progress bar

# Load environment variables from the .env file
load_dotenv()

# Retrieve sensitive info from environment variables
api_token = os.getenv("OKTA_API_TOKEN")
base_url = os.getenv("OKTA_BASE_URL")

if not api_token or not base_url:
    raise ValueError("API token or Base URL not set in environment variables")

headers = {
    'Authorization': f'SSWS {api_token}',
    'Accept': 'application/json'
}

# Function to handle pagination for API calls
def get_paginated_data(url):
    data = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data.extend(response.json())
        url = response.links.get('next', {}).get('url')
    return data

# Function to get all applications (with pagination)
def get_applications():
    url = f"{base_url}/api/v1/apps"
    return get_paginated_data(url)

# Function to get all groups for a given application (with pagination)
def get_groups_for_application(app_id):
    url = f"{base_url}/api/v1/apps/{app_id}/groups"
    return get_paginated_data(url)

# Function to get details for a specific group
def get_group_details(group_id):
    url = f"{base_url}/api/v1/groups/{group_id}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to get all users for a given group (with pagination)
def get_users_for_group(group_id):
    url = f"{base_url}/api/v1/groups/{group_id}/users"
    return get_paginated_data(url)

# Fetch and map all data
def collect_okta_data():
    data = []
    apps = get_applications()

    # Add progress bar for the number of applications
    for app in tqdm(apps, desc="Processing Applications"):
        app_name = app.get('label', 'Unknown App')  # Fallback to 'Unknown App' if not found
        app_id = app.get('id')

        groups = get_groups_for_application(app_id)

        # Add progress bar for the groups within each application
        for group in tqdm(groups, desc=f"Processing Groups for {app_name}", leave=False):
            group_id = group.get('id')

            # Get group details to find the group name
            group_details = get_group_details(group_id)
            group_name = group_details.get('profile', {}).get('name', 'Unknown Group Name')  # Fallback to 'Unknown Group Name'

            users = get_users_for_group(group_id)

            # Add progress bar for users within each group
            for user in tqdm(users, desc=f"Processing Users in {group_name}", leave=False):
                user_profile = user.get('profile', {})
                user_name = user_profile.get('login', 'Unknown User')  # Fallback to 'Unknown User'
                first_name = user_profile.get('firstName', 'Unknown First Name')  # Fallback to 'Unknown First Name'
                last_name = user_profile.get('lastName', 'Unknown Last Name')  # Fallback to 'Unknown Last Name'
                full_name = f"{first_name} {last_name}"

                # Additional fields requested
                title = user_profile.get('title', 'Unknown Title')
                division = user_profile.get('division', 'Unknown Division')
                department = user_profile.get('department', 'Unknown Department')
                manager = user_profile.get('manager', 'Unknown Manager')
                team = user_profile.get('team', 'Unknown Team')

                # Append the collected data, including additional fields
                data.append({
                    "Application": app_name,
                    "Application ID": app_id,
                    "Group": group_name,
                    "Group ID": group_id,
                    "User Login": user_name,
                    "User Full Name": full_name,
                    "Title": title,
                    "Division": division,
                    "Department": department,
                    "Manager": manager,
                    "Team": team
                })

    return pd.DataFrame(data)

# Save to CSV
df = collect_okta_data()
df.to_csv("okta_access_review.csv", index=False)
print("Data exported to okta_access_review.csv")
