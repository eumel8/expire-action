# expire-action

Expire (delete) tags from container registry ghcr.io on a specific timeset (30 days)

hint: requires a github username and a Personal access token with skope: delete:packages, repo, write:packages

usage:

for user:

```
on:
  schedule:
    - cron: "10 6 * * *"  

name: Expire container tags

jobs:
  expire-tags:
    runs-on: ubuntu-latest
    name: "expire-tags"
    steps:
      - uses: eumel8/expire-action@dev
        with:
          username: ${{secrets.username}}
          token: ${{secrets.token}}
          repo_type: user
          image_name: myimage
          days_treshold: 100
```

for org:

```
on:
  schedule:
    - cron: "10 6 * * *"  

name: Expire container tags

jobs:
  expire-tags:
    runs-on: ubuntu-latest
    name: "expire-tags"
    steps:
      - uses: eumel8/expire-action@dev
        with:
          username: ${{secrets.username}}
          token: ${{secrets.token}}
          repo_type: org
          orgname: my-org
          image_name: myapp%2Fmyimage
          days_treshold: 100
```


