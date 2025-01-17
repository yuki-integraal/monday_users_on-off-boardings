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

// Function to fetch all items with their "Société" label
async function getUsersInfo(boardId, firstname, lastname, email) {
    const query = `
    query {
        boards(ids: ${boardId}) {
            items_page {
                items {
                    id
                    column_values(ids: ["${firstname}", "${lastname}", "${email}"]) {
                        column {
                            id
                            title
                        }
                        id
                        text
                    }
                }
            }
        }
    }
    `;
    
    const data = await runQuery(query);

    const boards = data.data.boards || [];
    if (boards.length === 0) {
        throw new Error(`No board found with ID ${boardId}`);
    }

    const items = boards[0].items_page.items || [];
    if (items.length === 0) {
        throw new Error("No items found on the board.");
    }

    // Extract item details and "Société" labels
    const itemsWithLabels = items.map(item => {
        const firstnameLabel = item.column_values[0]?.text;
        const lastnameLabel = item.column_values[1]?.text;
        const emailLabel = item.column_values[2]?.text;

        return {
            id: item.id,
            firstname: firstnameLabel,
            lastname: lastnameLabel,
            email: emailLabel
        };
    });

    return itemsWithLabels;
}

// Modify your existing DOMContentLoaded function to use the dynamically fetched users
document.addEventListener("DOMContentLoaded", async () => {
    const dropdownContent = document.querySelector(".dropdown-content");
    const submitButton = document.getElementById("submitButton");

    try {
        // Fetch users from the Monday.com board
        const users = await getUsersInfo(MONDAY_BOARD_ID, 'pr_nom__1', 'text__1', 'email__1');

        // Populate the dropdown with checkboxes
        users.forEach(user => {
            const label = document.createElement("label");
            label.innerHTML = `
                <input type="checkbox" value="${user.id}" data-firstname="${user.firstname}" data-lastname="${user.lastname}">
                ${user.firstname} ${user.lastname}
            `;
            dropdownContent.appendChild(label);
        });

        // Add event listener to the submit button
        submitButton.addEventListener("click", () => {
            const selectedCheckboxes = Array.from(dropdownContent.querySelectorAll("input[type='checkbox']:checked"));
            
            // Collect selected user data (id, firstname, lastname)
            const selectedUsers = selectedCheckboxes.map(checkbox => {
                return {
                    id: checkbox.value,
                    firstname: checkbox.getAttribute('data-firstname'),
                    lastname: checkbox.getAttribute('data-lastname')
                };
            });
            
            // You can log selected users to see the data
            console.log(selectedUsers);

            // Prepare the query string with user data combined (id, firstname, lastname)
            const queryString = selectedUsers.map(user => {
                return `user=${encodeURIComponent(user.id)},${encodeURIComponent(user.firstname)},${encodeURIComponent(user.lastname)}`;
            }).join("&");

            // Redirect to the second page with the selected data in the query string
            location.href = `afterSubmission.html?${queryString}`;
        });

    } catch (error) {
        console.error(`Error fetching users: ${error.message}`);
    }
});