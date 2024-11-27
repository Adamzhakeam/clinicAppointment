document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const phone = document.getElementById("phone").value;
    const password = document.getElementById("password").value;
  
    // Clear any previous error or success messages
    document.getElementById("errorMessage").textContent = '';
    document.getElementById("successMessage").textContent = '';
  
    // Display loading message
    const loginButton = document.getElementById("loginBtn");
    loginButton.textContent = "Logging in...";
    loginButton.disabled = true;
  
    // Create payload for API request
    const payload = {
      phone: phone,
      password: password
    };
  
    try {
      const response = await fetch('http://127.0.0.1:5000/logIn', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
  
      const data = await response.json();
  
      if (data.status) {
        // Store the token in localStorage
        localStorage.setItem('token', data.token);
  
        // Display success message
        document.getElementById("successMessage").textContent = "Login successful!";
  
        // Redirect to dashboard
        setTimeout(() => {
          window.location.href = "dashboard.html"; // Redirect to dashboard page
        }, 1000); // Optional: Add a slight delay for user experience
      } else {
        // Display error message
        document.getElementById("errorMessage").textContent = `Error: ${data.log}`;
      }
    } catch (error) {
      // Handle request error
      document.getElementById("errorMessage").textContent = "An error occurred during login. Please try again.";
    } finally {
      // Re-enable the button and reset text
      loginButton.textContent = "Login";
      loginButton.disabled = false;
    }
  });
  