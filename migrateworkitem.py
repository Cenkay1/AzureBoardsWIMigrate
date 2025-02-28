import requests
import json
from requests.auth import HTTPBasicAuth

# 🔹 TFS and Azure DevOps details
TFS_URL = ""  # Base URL for TFS server
AZURE_DEVOPS_URL = ""  # Base URL for Azure DevOps organization
TFS_PROJECT = ""  # Name of the TFS project
AZURE_PROJECT = ""  # Name of the Azure DevOps project
TFS_PAT = ""  # Personal Access Token for TFS authentication
AZURE_PAT = ""  # Personal Access Token for Azure DevOps authentication

# 🔹 API versions for TFS and Azure DevOps
TFS_API_VERSION = "5.0"
AZURE_API_VERSION = "6.0"

def get_tfs_work_items():
    """Fetches all Work Items from the specified TFS project."""
    url = f"{TFS_URL}/{TFS_PROJECT}/_apis/wit/wiql?api-version={TFS_API_VERSION}"
    
    headers = {"Content-Type": "application/json"}
    
    # WIQL query to fetch all Work Item IDs in the given project
    query = {
        "query": """
        SELECT [System.Id] 
        FROM WorkItems 
        WHERE [System.TeamProject] = @project
        """
    }
    
    response = requests.post(url, json=query, headers=headers, auth=HTTPBasicAuth('', TFS_PAT))
    
    if response.status_code != 200:
        print("❌ Error while fetching Work Items from TFS:", response.text)
        return []
    
    work_items = response.json().get("workItems", [])
    return [item["id"] for item in work_items]  # Return a list of Work Item IDs

def get_tfs_work_item_details(work_item_id):
    """Retrieves details of a specific Work Item from TFS."""
    url = f"{TFS_URL}/_apis/wit/workitems/{work_item_id}?api-version={TFS_API_VERSION}"
    
    response = requests.get(url, auth=HTTPBasicAuth('', TFS_PAT))
    
    if response.status_code != 200:
        print(f"❌ Error while fetching details for Work Item {work_item_id}:", response.text)
        return None
    
    return response.json()  # Return the Work Item details as JSON

def create_azure_devops_work_item(work_item):
    """Creates a new Work Item in Azure DevOps based on TFS data."""
    url = f"{AZURE_DEVOPS_URL}/{AZURE_PROJECT}/_apis/wit/workitems/$task?api-version={AZURE_API_VERSION}"
    
    fields = work_item.get("fields", {})
    
    # Construct the payload for the new Work Item
    payload = [
        {"op": "add", "path": "/fields/System.Title", "value": fields.get("System.Title", "Migrated from TFS.")},
        {"op": "add", "path": "/fields/System.Description", "value": fields.get("System.Description", "No description available.")},
        {"op": "add", "path": "/fields/System.WorkItemType", "value": fields.get("System.WorkItemType", "Task")}
    ]
    
    headers = {
        "Content-Type": "application/json-patch+json"
    }
    
    response = requests.post(url, auth=HTTPBasicAuth('', AZURE_PAT), headers=headers, data=json.dumps(payload))
    
    if response.status_code in [200, 201]:
        print(f"✅ Work Item {work_item['id']} successfully migrated: {response.json().get('url')}")
    else:
        print(f"❌ Error while migrating Work Item {work_item['id']}:", response.text)

def migrate_work_items():
    """Migrates all Work Items from TFS to Azure DevOps."""
    work_item_ids = get_tfs_work_items()
    
    if not work_item_ids:
        print("⚠️ No Work Items found to migrate.")
        return
    
    print(f"🔄 {len(work_item_ids)} Work Items found, starting migration...")

    for work_item_id in work_item_ids:
        work_item = get_tfs_work_item_details(work_item_id)
        if work_item:
            create_azure_devops_work_item(work_item)

if __name__ == "__main__":
    migrate_work_items()  # Start the migration process
