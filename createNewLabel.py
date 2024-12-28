import json
import requests

# Monday.com API details
MONDAY_API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQyNTM1MTE1OSwiYWFpIjoxMSwidWlkIjo2NzUwOTkwOSwiaWFkIjoiMjAyNC0xMC0xOFQxNDowNjoyOC4yMDhaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjUwNDU4MTAsInJnbiI6ImV1YzEifQ.K7dNTAl61apgnSHdAm8rYCIrzPe_Tkw1ArqeylsFu2g'
MONDAY_API_URL = "https://api.monday.com/v2"

BOARD_ID = '1727326681'  # Board ID
SOCIETE_COLUMN_ID = "soci_t___1"  # Dropdown column ID
ITEM_ID = 1750434075  # Item ID from the board

# Helper function to run GraphQL queries
def run_query(query):
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(MONDAY_API_URL, json={'query': query}, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")
    return response.json()

# Get current dropdown options for a column
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
    settings_str = data.get('data', {}).get('boards', [])[0].get('columns', [])[0].get('settings_str', '{}')
    settings = json.loads(settings_str)
    return [label['name'] for label in settings.get('labels', [])]

# Function to add 'tomate' to the dropdown column if it doesn't already exist
def ensure_dropdown_label_exists(board_id, column_id, item_id, label):
    # Step 1: Get existing dropdown labels
    dropdown_options = get_dropdown_options(board_id, column_id)
    print("Existing Dropdown Options:", dropdown_options)
    
    # Step 2: Check if 'tomate' exists
    if label in dropdown_options:
        print(f"'{label}' already exists in the dropdown options.")
        return

    # Step 3: Add 'tomate' using change_simple_column_value
    print(f"'{label}' not found in the dropdown options. Adding it dynamically...")
    mutation = f"""
    mutation {{
        change_simple_column_value(
            item_id: {item_id}, 
            board_id: {board_id}, 
            column_id: "{column_id}", 
            value: "{label}", 
            create_labels_if_missing: true
        ) {{
            id
        }}
    }}
    """
    response = run_query(mutation)
    print(f"Response: {response}")

# Main execution
if __name__ == "__main__":
    try:
        ensure_dropdown_label_exists(BOARD_ID, SOCIETE_COLUMN_ID, ITEM_ID, "tomate")
    except Exception as e:
        print(f"Error: {e}")
