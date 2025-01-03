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

# Function to fetch all items with their "Société" label
def get_items_with_societe_label(board_id, column_id, new_column_id):
    query = f"""
    query {{
        boards(ids: {board_id}) {{
            items_page {{
                items {{
                    id
                    column_values (ids: ["{column_id}", "{new_column_id}"]) {{
                        column {{
                            id
                            title
                        }}
                        id
                        text
                    }}
                }}
            }}
        }}
    }}
    """
    data = run_query(query)

    # Parse the items and their "Société" labels
    boards = data.get('data', {}).get('boards', [])
    if not boards:
        raise Exception(f"No board found with ID {board_id}")
        
    items = boards[0]['items_page'].get('items', [])

    if not items:
        raise Exception("No items found on the board.")

    # Extract item details and "Société" labels
    items_with_labels = []
    for item in items:
        item_id = item.get('id')
        societe_label = item.get('column_values', [{}])[0].get('text', None)
        new_societe_label = item.get('column_values', [{}])[1].get('text', None)
        items_with_labels.append({
            "id": item_id,
            "societe": societe_label,
            "new_societe": new_societe_label
        })

    return items_with_labels

# Main execution
if __name__ == "__main__":
    SOCIETE_COLUMN_ID = "soci_t___1"  # Column ID for Société
    NEW_SOCIETE_COLUMN_ID = "short_text_mkkb1qte"  # Column ID for new Société
    
    try:
        items = get_items_with_societe_label(MONDAY_BOARD_ID, SOCIETE_COLUMN_ID, NEW_SOCIETE_COLUMN_ID)
        print("Items with their 'Société' label:")
        for item in items:
            print(f"ID: {item['id']}, Société: {item['societe']}, New Société: {item['new_societe']}")
    except Exception as e:
        print(f"Error: {e}")