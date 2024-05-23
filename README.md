# expire-action

Expire (delete) tags from container registry ghcr.io on a specific timeset (30 days)

usage:

```
on: [push]

jobs:
  pylint:
    runs-on: ubuntu-latest
    name: "expire-tags"
    steps:
      - uses: eumel8/expire-action@dev
        with:
          python_version: "3.9"
          username: ${{secrets.username}}
          token: ${{secrets.token}}
          repo_type: user
          image_name: myimage
          days_treshold: 100
          orgname:
```


