import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import yaml
from datetime import date, timedelta

CREDS_FILE = "/data/workspace/agents/site-updater/skills/google-ads/google-ads.yaml"
if not os.path.exists(CREDS_FILE):
    print("No creds", file=sys.stderr)
    sys.exit(1)

with open(CREDS_FILE) as f:
    config = yaml.safe_load(f)

creds = Credentials(
    None,
    refresh_token=config["refresh_token"],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=config["client_id"],
    client_secret=config["client_secret"]
)
sc = build("searchconsole", "v1", credentials=creds)

end_date = date.today() - timedelta(days=3)
start_date = end_date - timedelta(days=13)

req = {
    "startDate": start_date.isoformat(),
    "endDate": end_date.isoformat(),
    "dimensions": ["query", "page"],
    "rowLimit": 100
}

res = sc.searchanalytics().query(siteUrl="sc-domain:aiverktygsladan.se", body=req).execute()

rows = res.get("rows", [])
for r in rows:
    print(f"{r['keys'][0]} | {r['keys'][1]} | imp:{r['impressions']} | clk:{r['clicks']} | pos:{r['position']:.1f}")
