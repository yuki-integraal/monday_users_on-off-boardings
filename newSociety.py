import json
import requests

# Monday.com API details
MONDAY_API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQyNTM1MTE1OSwiYWFpIjoxMSwidWlkIjo2NzUwOTkwOSwiaWFkIjoiMjAyNC0xMC0xOFQxNDowNjoyOC4yMDhaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjUwNDU4MTAsInJnbiI6ImV1YzEifQ.K7dNTAl61apgnSHdAm8rYCIrzPe_Tkw1ArqeylsFu2g'
MONDAY_API_URL = "https://api.monday.com/v2"

BOARD_ID = '1727326681'  # Board ID
SOCIETE_COLUMN_ID = "soci_t___1"  # Dropdown column ID
SHORT_TEXT_COLUMN_ID = "short_text_mkkb1qte"  # Short text column ID

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

# Get all items on the board
def get_all_items(board_id):
    query = f"""
    query {{
        boards(ids: {board_id}) {{
            items {{
                id
                name
                column_values {{
                    id
                    text
                }}
            }}
        }}
    }}
    """
    data = run_query(query)
    items = data.get('data', {}).get('boards', [])[0].get('items', [])
    return items

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

# Update the dropdown column value and create the label if missing
def update_dropdown_label(board_id, item_id, column_id, label):
    mutation = f"""
    mutation {{
        change_simple_column_value(
            board_id: {board_id},
            item_id: {item_id},
            column_id: "{column_id}",
            value: "{label}",
            create_labels_if_missing: true
        ) {{
            id
        }}
    }}
    """
    response = run_query(mutation)
    return response

# Main script
def process_board_items(board_id, dropdown_column_id, short_text_column_id):
    # Step 1: Get all items on the board
    items = get_all_items(board_id)
    print(f"Found {len(items)} items on the board.")

    # Step 2: Iterate through items
    for item in items:
        item_id = item['id']
        column_values = {col['id']: col['text'] for col in item.get('column_values', [])}
        
        dropdown_value = column_values.get(dropdown_column_id)
        short_text_value = column_values.get(short_text_column_id)

        print(f"Processing Item {item_id} - Dropdown: {dropdown_value}, Short Text: {short_text_value}")
        
        # Check if dropdown value is 'Autre... / Other...'
        if dropdown_value == "Autre... / Other..." and short_text_value:
            print(f"Updating dropdown label for Item {item_id} to '{short_text_value}'...")
            try:
                # Step 3: Update dropdown column value
                response = update_dropdown_label(board_id, item_id, dropdown_column_id, short_text_value)
                print(f"Successfully updated Item {item_id}: {response}")
            except Exception as e:
                print(f"Failed to update Item {item_id}: {e}")

# Execute the script
if __name__ == "__main__":
    try:
        process_board_items(BOARD_ID, SOCIETE_COLUMN_ID, SHORT_TEXT_COLUMN_ID)
    except Exception as e:
        print(f"Error: {e}")