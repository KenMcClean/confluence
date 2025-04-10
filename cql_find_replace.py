# Use CQL to find and replace data on Confluence Cloud pages

import requests
from requests.auth import HTTPBasicAuth
import json


cloud_url = "https://<cloud url>.atlassian.net"
# Primary cloud instance URL

search_url = f"{cloud_url}/wiki/rest/api/search"
# CQL search URL

macro_name = ""

username = "<your email>"
api_token = "<your API token>"
# Credentials

auth = HTTPBasicAuth(username, api_token)
#Convert credentials to auth token

headers = {
  "Accept": "application/json"
}

query = {
  'cql': f'macro = "{macro_name}"'
}
# Declare CQL statement

response = requests.request(
   "GET",
   search_url,
   headers=headers,
   params=query,
   auth=auth
)
# Fetch the results of the CQL search

for page in json.loads(response.text)['results']:
# Iterate through the results (all of the pages that match the CQL)

    page_id = page['content']['id']
    # Declare the ID of the current page object

    page_url = f"{cloud_url}/wiki/rest/api/content/{page_id}?expand=body.storage,version"
    # Use the page ID to establish the REST API URL of the current page. Expand the body and the version.

    page_fetch = requests.request(
        "GET",
        page_url,
        headers=headers,
        auth=auth
    )
    # Fetch the current page, using the established URL

    body_json = json.loads(page_fetch.content)
    # Convert the results to JSON

    body_str = str(body_json["body"]["storage"]["value"])
    # Declare the string that represents the body of the page

    new_body = body_str.replace("rest", "vest")
    # Transform the body in some way, store it in a new variable

    new_version_num = int(body_json["version"]["number"]) + 1
    # Increase the page version by 1

    page_title = body_json["title"]
    # Establish the page title

    payload = {
        "type": "page",
        "title": page_title,
        "version": {"number": new_version_num},
        "body": {
            "storage": {
                "value": new_body,
                "representation": "storage"
            }
        }
    }
    # Establish the JSON that represents the new page

    update_page = requests.request(
        "PUT",
        cloud_url,
        headers=headers,
        auth=auth,
        json=payload

    )
    # PUT the new version of the page.  By using json= instead of data=, the conversion to JSON-type data is automatic.

    print(update_page.status_code)
    # Confirm success or failure

