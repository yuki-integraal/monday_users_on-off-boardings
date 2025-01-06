const users = [
    { id: 1, firstname: "John", lastname: "Doe" },
    { id: 2, firstname: "Jane", lastname: "Smith" },
    { id: 3, firstname: "Alice", lastname: "Johnson" },
    { id: 4, firstname: "Bob", lastname: "Brown" }
];

document.addEventListener("DOMContentLoaded", () => {
    const dropdownContent = document.querySelector(".dropdown-content");
    const submitButton = document.getElementById("submitButton");

    // Populate the dropdown with checkboxes
    users.forEach(user => {
        const label = document.createElement("label");
        label.innerHTML = `
            <input type="checkbox" value="${user.id}">
            ${user.firstname} ${user.lastname}
        `;
        dropdownContent.appendChild(label);
    });

    // Add event listener to the submit button
    submitButton.addEventListener("click", () => {
        const selectedCheckboxes = Array.from(dropdownContent.querySelectorAll("input[type='checkbox']:checked"));
        const selectedIds = selectedCheckboxes.map(checkbox => checkbox.value);
        alert(`Selected User IDs: ${selectedIds.join(", ")}`);
    });
});