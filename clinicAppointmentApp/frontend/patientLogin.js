document.getElementById("patientLoginForm").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const phone = document.getElementById("phone").value;
    const password = document.getElementById("password").value;
  
    const messageBox = document.getElementById("messageBox");
    messageBox.textContent = '';
    messageBox.className = '';
  
    const payload = { phone, password };
  
    try {
      const response = await fetch('http://127.0.0.1:5000/patientLogin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
  
      const data = await response.json();
  
      if (data.status) {
        // Save the token in localStorage and redirect to patient dashboard
        localStorage.setItem('token', data.token);
        window.location.href = 'patientDashboard.html';
      } else {
        // Display error message
        messageBox.textContent = data.log;
        messageBox.className = 'error';
      }
    } catch (error) {
      messageBox.textContent = 'An error occurred. Please try again later.';
      messageBox.className = 'error';
    }
  });
  