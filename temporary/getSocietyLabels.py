import json
import requests

# Monday.com API details
MONDAY_API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQyNTM1MTE1OSwiYWFpIjoxMSwidWlkIjo2NzUwOTkwOSwiaWFkIjoiMjAyNC0xMC0xOFQxNDowNjoyOC4yMDhaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjUwNDU4MTAsInJnbiI6ImV1YzEifQ.K7dNTAl61apgnSHdAm8rYCIrzPe_Tkw1ArqeylsFu2g'
MONDAY_BOARD_ID = '1727326681'

# Monday.com API endpoint
MONDAY_API_URL = "https://api.monday.com/v2"

# Helper function to run GraphQL queries
def run_query(query):
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(MONDAY_API_URL, json={'query': query}, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")
    
    response_data = response.json()
    if "errors" in response_data:
        raise Exception(f"GraphQL error: {response_data['errors']}")
    
    return response_data

# Function to fetch dropdown menu entries
def get_dropdown_options(board_id, column_id):
    query = f"""
    query {{
        boards(ids: {board_id}) {{
            columns(ids: "{column_id}") {{
                settings_str
            }}
        }}
    }}
    """
    data = run_query(query)
    
    # Parse the settings_str to get dropdown options
    boards = data.get('data', {}).get('boards', [])
    if not boards:
        raise Exception(f"No board found with ID {board_id}")
        
    columns = boards[0].get('columns', [])
    if not columns:
        raise Exception(f"No column found with ID {column_id}")
        
    settings_str = columns[0].get('settings_str', '{}')
    settings = json.loads(settings_str)
    
    # Extract labels from dropdown options
    label_names = [label['name'] for label in settings.get('labels', [])]

    return label_names

# Main execution
if __name__ == "__main__":
    SOCIETE_COLUMN_ID = "soci_t___1"  # Column ID for Société
    
    try:
        dropdown_options = get_dropdown_options(MONDAY_BOARD_ID, SOCIETE_COLUMN_ID)
        print("Dropdown Options for 'Société':")
        for option in dropdown_options:
            print(option)
    except Exception as e:
        print(f"Error: {e}")