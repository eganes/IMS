function login() {
    // Add login functionality
    console.log('Login clicked');

    event.preventDefault();

    setTimeout(function () {
        // Redirect to the dashboard page
        window.location.href = 'pages/dashboard.html';
    }, 1000);
}

function signup() {
    // Add signup functionality
    console.log('Signup clicked');

    event.preventDefault();

    setTimeout(function () {
        // Redirect to the dashboard page
        window.location.href = 'pages/signup.html';
    }, 1000);
}
