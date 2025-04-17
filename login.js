document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent default form submission

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        fetch("login.php", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                window.location.href = "dashboard.html"; // Redirect on success
            } else {
                alert("Invalid login. Please check your UserID and password.");
            }
        })
        .catch(error => console.error("Error:", error));
    });
});