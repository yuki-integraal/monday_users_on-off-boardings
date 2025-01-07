const users = [
    { id: 1, firstname: "John", lastname: "Doe" },
    { id: 2, firstname: "Jane", lastname: "Smith" },
    { id: 3, firstname: "Alice", lastname: "Johnson" },
    { id: 4, firstname: "Bob", lastname: "Brown" }
];

document.addEventListener("DOMContentLoaded", () => {
    const deletedNamesDiv = document.getElementById("deletedNames");

    // Extract query string parameters
    const params = new URLSearchParams(window.location.search);
    const deletedIds = params.get("deletedIds")?.split(",") || [];

    // Filter users based on the deleted IDs
    const deletedUsers = users.filter(user => deletedIds.includes(user.id.toString()));

    // Display deleted user names
    if (deletedUsers.length > 0) {
        deletedUsers.forEach(user => {
            const userDiv = document.createElement("div");
            userDiv.textContent = `${user.firstname} ${user.lastname}`;
            deletedNamesDiv.appendChild(userDiv);
        });
    } else {
        deletedNamesDiv.textContent = "No users selected.";
    }
});
