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
    return response.json()

# Fetch board columns
def get_board_columns(board_id):
    query = f'''
    query {{
      boards(ids: {board_id}) {{
        columns {{
          id
          title
        }}
      }}
    }}
    '''
    data = run_query(query)
    columns = data.get('data', {}).get('boards', [])[0].get('columns', [])
    return {column['title']: column['id'] for column in columns}

# Fetch board items
def get_board_items(board_id):
    query = f'''
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
    '''
    data = run_query(query)
    boards = data.get('data', {}).get('boards', [])
    if not boards:
        raise Exception(f"No boards found with ID {board_id}")
    return boards[0].get('items', [])

# Create a new label for a column
def create_label(board_id, column_id, label_name):
    query = f'''
    mutation {{
      create_label(board_id: {board_id}, column_id: "{column_id}", label: "{label_name}") {{
        id
      }}
    }}
    '''
    run_query(query)

# Update a column value for an item
def update_item_column(item_id, column_id, value):
    query = f'''
    mutation {{
      change_column_value(item_id: {item_id}, column_id: "{column_id}", value: "{value}") {{
        id
      }}
    }}
    '''
    run_query(query)

# Main logic
def main():
    # Fetch column IDs
    columns = get_board_columns(MONDAY_BOARD_ID)
    society_column_id = columns.get("Société")
    name_of_society_column_id = columns.get("Nom de la société")

    if not society_column_id or not name_of_society_column_id:
        raise Exception("Required columns 'society' or 'name_of_society' are missing.")

    # Fetch board items
    items = get_board_items(MONDAY_BOARD_ID)

    for item in items:
        society_value = next((col['text'] for col in item['column_values'] if col['id'] == society_column_id), None)
        name_of_society_value = next((col['text'] for col in item['column_values'] if col['id'] == name_of_society_column_id), None)

        if society_value == "Other" and name_of_society_value:
            # Create a new label and update the society column
            create_label(MONDAY_BOARD_ID, society_column_id, name_of_society_value)
            update_item_column(item['id'], society_column_id, name_of_society_value)
            print(f"Updated item {item['id']} with new label: {name_of_society_value}")

if __name__ == "__main__":
    main()
