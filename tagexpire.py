import requests
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
    response = requests.get(f'https://api.github.com/user/packages/container/'+image_name+'/versions', auth=auth)
    response.raise_for_status()  # Raise an exception if the request failed

    tags = response.json()
    for tag in tags:
        # Parse the created_at date
        created_at = datetime.strptime(tag['created_at'], '%Y-%m-%dT%H:%M:%SZ')

        # If the tag is older than the threshold, delete it
        if created_at < threshold_date:
            print(f'Deleted tag {tag["id"]}')
            response = requests.delete(f'https://api.github.com/user/packages/container/'+image_name+'/versions/'+{tag["id"]}+', auth=auth)
            response.raise_for_status()  # Raise an exception if the request failed
            print(f'Deleted tag {tag["name"]}')

elif repo_type == 'org':
    response = requests.get(f'https://api.github.com/orgs/'+orgname+'/packages/container/'+image_name+'/versions', auth=auth)
    response.raise_for_status()  # Raise an exception if the request failed

    tags = response.json()
    for tag in tags:
        # Parse the created_at date
        created_at = datetime.strptime(tag['created_at'], '%Y-%m-%dT%H:%M:%SZ')

        # If the tag is older than the threshold, delete it
        if created_at < threshold_date:
            response = requests.delete(f'https://api.github.com/orgs/'+orgname+'/packages/container/{image_name}/versions/'+{tag["id"]}+', auth=auth)
            response.raise_for_status()  # Raise an exception if the request failed
            print(f'Deleted tag {tag["name"]}')
