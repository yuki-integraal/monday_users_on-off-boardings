document.addEventListener("DOMContentLoaded", () => {
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
        const userDiv = document.createElement("div");
        userDiv.textContent = `${user.firstname} ${user.lastname}`;
        deletedNamesDiv.appendChild(userDiv);
    }
});
