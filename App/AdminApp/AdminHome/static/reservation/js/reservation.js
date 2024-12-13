document.addEventListener('DOMContentLoaded', function () {
    let AZ_FUNCTION_GET_BOOKING;
    let AZ_FUNCTION_DELETE_RESERVATION;

    // Fetch the configuration dynamically
    async function fetchConfig() {
        try {
            const response = await fetch("/config");
            if (!response.ok) {
                throw new Error(`Failed to fetch config: ${response.status}`);
            }
            const config = await response.json();

            AZ_FUNCTION_GET_BOOKING = config.AZ_FUNCTION_GET_BOOKING;
            AZ_FUNCTION_DELETE_RESERVATION = config.AZ_FUNCTION_DELETE_RESERVATION;

            if (!AZ_FUNCTION_GET_BOOKING || !AZ_FUNCTION_DELETE_RESERVATION) {
                throw new Error("Required environment variables are missing in the config response.");
            }

            // console.log("Config Loaded:", { AZ_FUNCTION_GET_BOOKING, AZ_FUNCTION_DELETE_RESERVATION });
        } catch (error) {
            console.error("Error fetching config:", error);
            throw error; // Prevent further execution
        }
    }

    // Fetch data from API and populate the table
    async function fetchAndPopulateTable() {
        try {
            const response = await fetch(AZ_FUNCTION_GET_BOOKING);
            if (!response.ok) {
                throw new Error(`Error fetching booking data: ${response.status}`);
            }
            const data = await response.json();
            populateTable(data);
        } catch (error) {
            console.error("Error fetching booking data:", error);
        }
    }

    // Function to populate table rows
    function populateTable(data) {
        const tableBody = document.querySelector("#reservationTable tbody");
        tableBody.innerHTML = ""; // Clear existing rows
        data.forEach(row => {
            const tableRow = document.createElement("tr");
            tableRow.innerHTML = `
                <td>${row.reservation_id}</td>
                <td>${row.user_email}</td>
                <td>${row.guest_name}</td>
                <td>${row.guest_email}</td>
                <td>${row.guest_phone}</td>
                <td>${row.checkin_date}</td>
                <td>${row.checkin_time}</td>
                <td>${row.no_of_guest}</td>
                <td>
                    <button class="delete-btn" data-id="${row.reservation_id}">
                        🗑️
                    </button>
                </td>
            `;
            tableBody.appendChild(tableRow);
        });

        // Attach delete functionality to delete buttons
        attachDeleteHandlers();
    }

    // Attach event listeners to all delete buttons
    function attachDeleteHandlers() {
        const deleteButtons = document.querySelectorAll(".delete-btn");
        deleteButtons.forEach(button => {
            button.addEventListener("click", function () {
                const reservationId = this.getAttribute("data-id");
                if (confirm(`Are you sure you want to delete reservation ID ${reservationId}?`)) {
                    deleteReservation(reservationId);
                }
            });
        });
    }

    // Function to delete a reservation
    async function deleteReservation(reservationId) {
        try {
            // Replace the placeholder {reservation_id} with the actual reservationId
            const deleteUrl = AZ_FUNCTION_DELETE_RESERVATION.replace("{reservation_id}", reservationId);

            const response = await fetch(deleteUrl, {
                method: "DELETE",
            });

            if (response.ok) {
                alert(`Reservation ID ${reservationId} deleted successfully!`);
                // Refresh the table
                await fetchAndPopulateTable();
            } else {
                const errorText = await response.text();
                throw new Error(`Failed to delete reservation: ${errorText}`);
            }
        } catch (error) {
            console.error("Error deleting reservation:", error);
            alert(`Error deleting reservation: ${error.message}`);
        }
    }

    // Initialize the app
    async function initializeApp() {
        try {
            await fetchConfig(); // Load config
            await fetchAndPopulateTable(); // Populate table after config is loaded
        } catch (error) {
            console.error("Initialization failed:", error);
        }
    }

    initializeApp(); // Start the app
});
