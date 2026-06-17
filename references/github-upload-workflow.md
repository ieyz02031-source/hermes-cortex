# GitHub Upload Workflow (for Hermes Cortex)

## Problem

`git push` fails due to proxy (port 443 timeout). `mcp_github_create_or_update_file` truncates large files.

## Solution: Python + curl with GitHub PAT

```python
import yaml, json, base64, urllib.request

# Read GitHub token
config = yaml.safe_load(open("C:/Users/20716/AppData/Local/hermes/config.yaml"))
token = config["mcp_servers"]["github"]["env"]["GITHUB_PERSONAL_ACCESS_TOKEN"]

def upload_file(owner, repo, path, file_path, message, branch="main", sha=None):
    content = open(file_path, "rb").read()
    data = {"message": message, "content": base64.b64encode(content).decode(), "branch": branch}
    if sha:
        data["sha"] = sha
    
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
        data=json.dumps(data).encode(),
        method="PUT",
        headers={"Authorization": f"token {token}", "Content-Type": "application/json", "User-Agent": "hermes"}
    )
    
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    return result["content"]["size"]

def get_sha(owner, repo, path):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
        headers={"Authorization": f"token {token}", "User-Agent": "hermes"}
    )
    return json.loads(urllib.request.urlopen(req).read())["sha"]
```

## Verification

After uploading, always verify the GitHub file size matches local:
```python
req = urllib.request.Request(f"https://api.github.com/repos/{owner}/{repo}/contents/{path}")
size = json.loads(urllib.request.urlopen(req).read())["size"]
assert size == len(open(local_path, "rb").read()), f"Size mismatch: {size} vs {len(open(local_path, 'rb').read())}"
```

## Usage

```python
# Upload new file
upload_file("ieyz02031-source", "hermes-cortex", "SKILL.md", "D:/Hermes/skills/hermes-cortex/SKILL.md", "feat: add SKILL.md")

# Update existing file
sha = get_sha("ieyz02031-source", "hermes-cortex", "README.md")
upload_file("ieyz02031-source", "hermes-cortex", "README.md", "D:/Hermes/skills/hermes-cortex/README.md", "feat: update README.md", sha=sha)
```
