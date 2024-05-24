import requests
from requests.exceptions import HTTPError
from datetime import datetime, timedelta
import json
import math
import sys

# define command line arguments username, token, image_name, days_threshold, orgname
token = sys.argv[1]
repo_type = sys.argv[2]
image_name = sys.argv[3]
days_threshold = int(sys.argv[4])
orgname = sys.argv[5] if len(sys.argv) > 5 else None

# Token for authentication
authheader = {'Authorization': 'Bearer ' + token}

# Calculate the date threshold
threshold_date = datetime.now() - timedelta(days=days_threshold)

# Get all tags based on repo_type and operate deletion
if repo_type == 'user':
    try:
        response = requests.get(f'https://api.github.com/user/packages/container/{image_name}', headers=authheader)
        response.raise_for_status()
        versions = response.json()
        version_count = math.ceil(int(versions['version_count'])//100 + 1)
        print("version count ", version_count)
        # loop through the versions and check if the created_at is older than the threshold
        for i in range(1, version_count + 1):
            response = requests.get(f'https://api.github.com/user/packages/container/{image_name}/versions?per_page=100&page={i}', headers=authheader)
            tags = response.json()
            for tag in tags:
                created_at = datetime.strptime(tag['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                if created_at < threshold_date:
                    print(f'Delete tag {tag["id"]} - {tag["name"]}')
                    try:
                        response = requests.delete(f'https://api.github.com/user/packages/container/{image_name}/versions/{tag["id"]}', headers=authheader)
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
        response = requests.get(f'https://api.github.com/orgs/{orgname}/packages/container/{image_name}', headers=authheader)
        response.raise_for_status()
        versions = response.json()
        version_count = math.ceil(int(versions['version_count'])//100 + 1)
        print("version count ",version_count)
        # loop through the versions and check if the created_at is older than the threshold
        for i in range(1, version_count + 1):
            response = requests.get(f'https://api.github.com/orgs/{orgname}/packages/container/{image_name}/versions?per_page=100&page={i}', headers=authheader)
            tags = response.json()
            for tag in tags:
                created_at = datetime.strptime(tag['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                if created_at < threshold_date:
                    print(f'Delete tag {tag["id"]} - {tag["name"]}')
                    try:
                        response = requests.delete(f'https://api.github.com/orgs/{orgname}/packages/container/{image_name}/versions/{tag["id"]}', headers=authheader)
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
