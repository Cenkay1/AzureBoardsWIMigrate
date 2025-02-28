# TFS to Azure DevOps Work Item Migration

This script migrates Work Items from a TFS (Team Foundation Server) project to an Azure DevOps project using REST APIs.

## Prerequisites

- **Python 3.x** installed on your machine.
- Required Python packages:
  ```sh
  pip install requests
  ```
- A **Personal Access Token (PAT)** for both TFS and Azure DevOps with necessary permissions.

## Configuration

Before running the script, update the following variables in the script:

```python
TFS_URL = ""  # Base URL of your TFS server
AZURE_DEVOPS_URL = ""  # Base URL of your Azure DevOps organization
TFS_PROJECT = ""  # TFS project name
AZURE_PROJECT = ""  # Azure DevOps project name
TFS_PAT = ""  # Personal Access Token for TFS
AZURE_PAT = ""  # Personal Access Token for Azure DevOps
```

## API Versions

- **TFS API Version:** `5.0`
- **Azure DevOps API Version:** `6.0`

## How It Works

1. **Fetch Work Items from TFS**  
   - The script queries all Work Items in the specified TFS project.
2. **Retrieve Details for Each Work Item**  
   - It fetches detailed information for each Work Item.
3. **Create Work Items in Azure DevOps**  
   - The script replicates Work Items in Azure DevOps while preserving key details.

## Usage

Run the script using the following command:

```sh
python migrate_tfs_to_azure.py
```

## Error Handling

- If there are errors retrieving Work Items from TFS, they will be displayed in the console.
- If an error occurs while creating a Work Item in Azure DevOps, the response details will be printed.

## Notes

- The script currently migrates only basic fields (`Title`, `Description`, `WorkItemType`).
- Additional field mappings may be required for more complex migrations.
- Ensure that the necessary permissions are granted for both TFS and Azure DevOps PATs.

## License

This project is licensed under the MIT License.

