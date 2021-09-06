import json
import requests as r

TOKEN = ''
USERNAME = "the-noblest"

repos = r.get(f'https://api.github.com/user/repos', auth=(USERNAME, TOKEN)).json()

with open('repos.txt', 'w') as f:
    json.dump(repos, f, indent=4, sort_keys=True)
