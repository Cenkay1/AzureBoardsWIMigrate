import requests
import json
from requests.auth import HTTPBasicAuth

# 🔹 TFS ve Azure DevOps bilgileri
TFS_URL = ""
AZURE_DEVOPS_URL = ""
TFS_PROJECT = ""
AZURE_PROJECT = ""
TFS_PAT = ""
AZURE_PAT = ""

# 🔹 API versiyonları
TFS_API_VERSION = "5.0"
AZURE_API_VERSION = "6.0"

def get_tfs_work_items():
    """Belirtilen proje içindeki Work Item'ları çeker."""
    url = f"{TFS_URL}/{TFS_PROJECT}/_apis/wit/wiql?api-version={TFS_API_VERSION}"
    
    headers = {"Content-Type": "application/json"}
    
    query = {
        "query": """
        SELECT [System.Id] 
        FROM WorkItems 
        WHERE [System.TeamProject] = @project
        """
    }
    
    response = requests.post(url, json=query, headers=headers, auth=HTTPBasicAuth('', TFS_PAT))
    
    if response.status_code != 200:
        print("❌ TFS Work Item'ları çekerken hata oluştu:", response.text)
        return []
    
    work_items = response.json().get("workItems", [])
    return [item["id"] for item in work_items]

def get_tfs_work_item_details(work_item_id):
    """TFS'den belirli bir Work Item'ın detaylarını çeker."""
    url = f"{TFS_URL}/_apis/wit/workitems/{work_item_id}?api-version={TFS_API_VERSION}"
    
    response = requests.get(url, auth=HTTPBasicAuth('', TFS_PAT))
    
    if response.status_code != 200:
        print(f"❌ Work Item {work_item_id} detaylarını çekerken hata oluştu:", response.text)
        return None
    
    return response.json()

def create_azure_devops_work_item(work_item):
    """Azure DevOps'a yeni Work Item oluşturur."""
    url = f"{AZURE_DEVOPS_URL}/{AZURE_PROJECT}/_apis/wit/workitems/$task?api-version={AZURE_API_VERSION}"
    
    fields = work_item.get("fields", {})
    
    payload = [
        {"op": "add", "path": "/fields/System.Title", "value": fields.get("System.Title", "TFS'den taşındı.")},
        {"op": "add", "path": "/fields/System.Description", "value": fields.get("System.Description", "Açıklama yok.")},
        {"op": "add", "path": "/fields/System.WorkItemType", "value": fields.get("System.WorkItemType", "Task")}
    ]
    
    headers = {
        "Content-Type": "application/json-patch+json"
    }
    
    response = requests.post(url, auth=HTTPBasicAuth('', AZURE_PAT), headers=headers, data=json.dumps(payload))
    
    if response.status_code in [200, 201]:
        print(f"✅ Work Item {work_item['id']} başarıyla taşındı: {response.json().get('url')}")
    else:
        print(f"❌ Work Item {work_item['id']} taşınırken hata oluştu:", response.text)

def migrate_work_items():
    """Belirli proje için tüm Work Item'ları taşır."""
    work_item_ids = get_tfs_work_items()
    
    if not work_item_ids:
        print("⚠️ Taşınacak Work Item bulunamadı.")
        return
    
    print(f"🔄 {len(work_item_ids)} Work Item bulundu, taşınıyor...")

    for work_item_id in work_item_ids:
        work_item = get_tfs_work_item_details(work_item_id)
        if work_item:
            create_azure_devops_work_item(work_item)

if __name__ == "__main__":
    migrate_work_items()
