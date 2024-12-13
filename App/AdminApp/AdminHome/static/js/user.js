// API endpoint URL (Replace with your actual URL)
const apiUrl = 'https://fa-usermgmt-apis-01.azurewebsites.net/api/GetUser?code=Kvr-arDx9GvFn7X0QSwjlT26Ughotfaf1HCjC3LP6nDvAzFuFWVVIQ%3D%3D';


// Function to fetch users and populate the table
function fetchUsers() {
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#userTable tbody');
            tableBody.innerHTML = ''; // Clear existing table rows

            data.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.userid}</td>
                    <td>${user.full_name}</td>
                    <td>${user.email}</td>
                    <td>${user.phone}</td>
                    <td>${user.created_at}</td>`;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching users:', error);
        });
}


// Function to filter the table based on search inputs
function filterTable() {
    const userIdSearch = document.getElementById('search-userid').value.toLowerCase();
    const fullNameSearch = document.getElementById('search-fullname').value.toLowerCase();
    const emailSearch = document.getElementById('search-email').value.toLowerCase();
    const phoneSearch = document.getElementById('search-phone').value.toLowerCase();

    const rows = document.querySelectorAll('#userTable tbody tr');

    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        const userId = cells[0].textContent.toLowerCase();
        const fullName = cells[1].textContent.toLowerCase();
        const email = cells[2].textContent.toLowerCase();
        const phone = cells[3].textContent.toLowerCase();

        if (
            userId.includes(userIdSearch) &&
            fullName.includes(fullNameSearch) &&
            email.includes(emailSearch) &&
            phone.includes(phoneSearch)
        ) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Call the fetchUsers function when the page loads
window.onload = fetchUsers;
