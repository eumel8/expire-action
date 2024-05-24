# expire-action

Expire (delete) tags from container registry ghcr.io on a specific timeset (30 days)

hint: requires a Personal access token with scope: delete:packages, repo, write:packages

## Usage

### For user:

```yaml
on:
  schedule:
    - cron: "10 6 * * *"

name: Expire container tags

jobs:
  expire-tags:
    runs-on: ubuntu-latest
    name: "expire-tags"
    steps:
      - uses: eumel8/expire-action@1.0.0
        with:
          token: ${{secrets.token}}
          repo_type: user
          image_name: myimage
          days_treshold: 100
          protected_tags_regex: "^dev$\\|^latest$\\|^2.0.0$" # protect dev, latest, 2.0.0
```

### For org:

```yaml
on:
  schedule:
    - cron: "10 6 * * *"

name: Expire container tags

jobs:
  expire-tags:
    runs-on: ubuntu-latest
    name: "expire-tags"
    steps:
      - uses: eumel8/expire-action@1.0.0
        with:
          token: ${{secrets.token}}
          repo_type: org
          orgname: my-org
          image_name: myapp%2Fmyimage
          days_treshold: 100
          protected_tags_regex: "[23].*" # protect 2.0.0, 3.0.0
```

## Inputs

| Parameter             | Description                                             |
|-----------------------|---------------------------------------------------------|
| `token`               | The Personal Access Token with the required scopes.     |
| `repo_type`           | The type of repository (`user` or `org`).               |
| `orgname`             | The name of the organization (only for `org` repo_type).|
| `image_name`          | The name of the container image.                        |
| `days_treshold`       | The number of days after which tags will be expired.    |
| `protected_tags_regex`| Regex pattern for tags that should not be deleted.      |
