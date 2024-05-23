import requests
from requests.exceptions import HTTPError
from datetime import datetime, timedelta
import json
import sys

# define command line arguments username, token, image_name, days_threshold, orgname
username = sys.argv[1]
token = sys.argv[2]
repo_type = sys.argv[3]
image_name = sys.argv[4]
days_threshold = int(sys.argv[5])
orgname = sys.argv[6] if len(sys.argv) > 6 else None

# Basic auth using your username and PAT
auth = (username, token)

# Calculate the date threshold
threshold_date = datetime.now() - timedelta(days=days_threshold)

# Get all tags based on repo_type and operate deletion
if repo_type == 'user':
    try:
        response = requests.get(f'https://api.github.com/user/packages/container/{image_name}', auth=auth)
        response.raise_for_status()
        versions = response.json()
        version_count = int(versions['version_count'])
        print("version count ", version_count)
        # loop through the versions and check if the created_at is older than the threshold
        for i in range(1, version_count + 1):
            response = requests.get(f'https://api.github.com/user/packages/container/{image_name}/versions?per_page=1&page={i}', auth=auth)
            tags = response.json()
            tag = tags[0]
            created_at = datetime.strptime(tag['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            if created_at < threshold_date:
                print(f'Delete tag {tag["id"]} - {tag["name"]}')
                try:
                    response = requests.delete(f'https://api.github.com/user/packages/container/{image_name}/versions/{tag["id"]}', auth=auth)
                    response.raise_for_status()
                except HTTPError as e:
                    if response.status_code == 404:
                        print("The requested resource was not found.")
                    elif response.status_code == 500:
                        print("The server encountered an internal error.")
                    else:
                        print(f"HTTP error occurred: {e}")
                        print(f"Response message: {response.text}")
    except HTTPError as e:
        if response.status_code == 404:
            print("The requested resource was not found.")
        elif response.status_code == 500:
            print("The server encountered an internal error.")
        else:
            print(f"HTTP error occurred: {e}")
            print(f"Response message: {response.text}")  

elif repo_type == 'org':
    try:
        response = requests.get(f'https://api.github.com/orgs/{orgname}/packages/container/{image_name}', auth=auth)
        response.raise_for_status()
        versions = response.json()
        version_count = int(versions['version_count'])
        print("version count ",version_count)
        # loop through the versions and check if the created_at is older than the threshold
        for i in range(1, version_count + 1):
            response = requests.get(f'https://api.github.com/orgs/{orgname}/packages/container/{image_name}/versions?per_page=1&page={i}', auth=auth)
            tags = response.json()
            for tag in tags:
                created_at = datetime.strptime(tag['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                if created_at < threshold_date:
                    print(f'Delete tag {tag["id"]} - {tag["name"]}')
                    try:
                        response = requests.delete(f'https://api.github.com/orgs/{orgname}/packages/container/{image_name}/versions/{tag["id"]}', auth=auth)
                        response.raise_for_status()
                    except HTTPError as e:
                        if response.status_code == 404:
                            print("The requested resource was not found.")
                        elif response.status_code == 500:
                            print("The server encountered an internal error.")
                        else:
                            print(f"HTTP error occurred: {e}")
                            print(f"Response message: {response.text}")

    except HTTPError as e:
        if response.status_code == 404:
            print("The requested resource was not found.")
        elif response.status_code == 500:
            print("The server encountered an internal error.")
        else:
            print(f"HTTP error occurred: {e}")
            print(f"Response message: {response.text}")  
