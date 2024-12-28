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

# Step 2: Fetch board columns
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

# Execute the function
if __name__ == "__main__":
    columns = get_board_columns(MONDAY_BOARD_ID)
    print("Column IDs:")
    for title, col_id in columns.items():
        print(f"{title}: {col_id}")
