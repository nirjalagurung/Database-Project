document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("cpwd");

    form.addEventListener("submit", function (e) {
        // Passwords must match
        if (password.value !== confirmPassword.value) {
            e.preventDefault(); // Stop the form from submitting
            alert("Passwords do not match!");
            confirmPassword.focus();
            return;
        }

        // Password strength check
        if (password.value.length < 8) {
            e.preventDefault();
            alert("Password must be at least 8 characters long.");
            password.focus();
            return;
        }

        // Optional: Add more validations here...
    });

    // Password strength hint
    password.addEventListener("input", () => {
        if (password.value.length < 8) {
            password.style.borderColor = "crimson";
        } else {
            password.style.borderColor = "green";
        }
    });
});
document.getElementById("username").addEventListener("blur", () => {
    const username = document.getElementById("username").value;

    fetch("signup.php", {
        method: "POST",
        headers: { 
            "Content-Type": "application/json"  
        },
        body: JSON.stringify({ username })     // convert object to JSON string
    })
    .then(response => response.json())         //expect JSON back from the server
    .then(data => {
        if (data.status === "taken") {
            alert("That UserID is already taken. Please choose another.");
            document.getElementById("username").style.borderColor = "crimson";
        } else {
            document.getElementById("username").style.borderColor = "green";
        }
    })
    .catch(error => console.error("Error:", error));
});
