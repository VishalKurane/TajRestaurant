document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("reservationForm");

    form.addEventListener("submit", function (event) {
        // Let the form submit first
        setTimeout(() => {
            // Clear the form fields after submission
            form.reset();
        }, 0);
    });
});
