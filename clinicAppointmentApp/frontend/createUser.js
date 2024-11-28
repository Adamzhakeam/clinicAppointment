document.getElementById("createUserForm").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const firstName = document.getElementById("firstName").value;
    const lastName = document.getElementById("lastName").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const password = document.getElementById("password").value;
    const roleId = document.getElementById("roleId").value;
  
    const messageBox = document.getElementById("messageBox");
    messageBox.textContent = '';
    messageBox.className = '';
  
    const payload = {
      firstName: firstName,
      lastName: lastName,
      email: email,
      phone: phone,
      password: password,
      roleId: roleId
    };
  
    const token = localStorage.getItem("token");
  
    if (!token) {
      messageBox.textContent = "Unauthorized! Please log in.";
      messageBox.className = "error";
      return;
    }
  
    try {
      const response = await fetch('http://127.0.0.1:5000/createUser', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload),
      });
  
      const data = await response.json();
  
      if (data.status) {
        messageBox.textContent = data.log;
        messageBox.className = "success";
        document.getElementById("createUserForm").reset();
      } else {
        messageBox.textContent = `Error: ${data.log}`;
        messageBox.className = "error";
      }
    } catch (error) {
      messageBox.textContent = "An error occurred. Please try again.";
      messageBox.className = "error";
    }
  });
  