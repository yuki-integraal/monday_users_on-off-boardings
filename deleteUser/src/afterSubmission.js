const MONDAY_API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQyNTM1MTE1OSwiYWFpIjoxMSwidWlkIjo2NzUwOTkwOSwiaWFkIjoiMjAyNC0xMC0xOFQxNDowNjoyOC4yMDhaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjUwNDU4MTAsInJnbiI6ImV1YzEifQ.K7dNTAl61apgnSHdAm8rYCIrzPe_Tkw1ArqeylsFu2g'; 
const MONDAY_BOARD_ID = '1727326681';
const MONDAY_API_URL = 'https://api.monday.com/v2';

// Helper function to run GraphQL queries
async function runQuery(query) {
    const headers = {
        'Authorization': MONDAY_API_KEY,
        'Content-Type': 'application/json'
    };

    const response = await fetch(MONDAY_API_URL, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ query })
    });

    if (!response.ok) {
        throw new Error(`Query failed with status code ${response.status}: ${response.statusText}`);
    }

    const responseData = await response.json();
    if (responseData.errors) {
        throw new Error(`GraphQL error: ${JSON.stringify(responseData.errors)}`);
    }

    return responseData;
}

// Function to delete an item by ID (with board ID included)
async function deleteItem(itemId) {
    const mutation = `
    mutation {
        change_simple_column_value (
            board_id: ${MONDAY_BOARD_ID}, 
            item_id: ${itemId}, 
            column_id: "status", 
            value: "2"
        ) {
            id
        }
    }
    `;
    return runQuery(mutation);
}

document.addEventListener("DOMContentLoaded", async () => {
    const deletedNamesDiv = document.getElementById("deletedNames");

    const params = new URLSearchParams(window.location.search);

    // Get all 'user' parameters
    const users = params.getAll('user');

    // Split each 'user' string by commas to get id, firstname, and lastname
    const userData = users.map(user => {
        const [id, firstname, lastname] = user.split(',');
        return { id, firstname, lastname };
    });

    for (const user of userData) {
        try {
            // Attempt to delete the item on Monday.com
            await deleteItem(user.id); // REMOVE TO ACTIVATE USER DELETION

            // Show the name of the successfully deleted user
            const userDiv = document.createElement("div");
            userDiv.textContent = `Deleted: ${user.firstname} ${user.lastname}`;
            deletedNamesDiv.appendChild(userDiv);

        } catch (error) {
            alert(error.message);
            console.error(`Failed to delete user ${user.firstname} ${user.lastname}: ${error.message}`);
            const errorDiv = document.createElement("div");
            errorDiv.textContent = `Failed to delete: ${user.firstname} ${user.lastname}, please contact support.`;
            errorDiv.style.color = 'red';
            deletedNamesDiv.appendChild(errorDiv);
        }
    }
});