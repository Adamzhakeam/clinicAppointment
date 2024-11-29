document.addEventListener("DOMContentLoaded", () => {
    const doctorForm = document.getElementById("doctorForm");
    const messageDiv = document.getElementById("message");
    // const departmentSelect = document.getElementById("department");
  
    // // Function to fetch departments (replace with your API endpoint)
    // async function fetchDepartments() {
    //   try {
    //     const response = await fetch("http://127.0.0.1:5000/departments");
    //     const data = await response.json();
  
    //     if (data.status) {
    //       data.departments.forEach((department) => {
    //         const option = document.createElement("option");
    //         option.value = department.id;
    //         option.textContent = department.name;
    //         departmentSelect.appendChild(option);
    //       });
    //     } else {
    //       console.error("Error fetching departments:", data.log);
    //     }
    //   } catch (error) {
    //     console.error("Error:", error);
    //   }
    // }
  
    // // Load departments on page load
    // fetchDepartments();
  
    // Handle form submission
    doctorForm.addEventListener("submit", async (event) => {
      event.preventDefault();
  
      // Collect form data
      const formData = new FormData(doctorForm);
      const doctorDetails = Object.fromEntries(formData.entries());
  
      // API call to register doctor
      try {
        const response = await fetch("http://127.0.0.1:5000/createDoctor", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`, // Ensure admin token is available
          },
          body: JSON.stringify(doctorDetails),
        });
  
        const data = await response.json();
        console.log('>>>>>>>>>>',data);
        if (data.status) {
          messageDiv.textContent = `${doctorDetails.firstName} has been successfully registered!`;
          messageDiv.className = "text-success";
          doctorForm.reset();
        } else {
          messageDiv.textContent = `Error: ${data.log}`;
          messageDiv.className = "text-danger";
        }
      } catch (error) {
        console.error("Error:", error);
        messageDiv.textContent = "An error occurred while registering the doctor.";
        messageDiv.className = "text-danger";
      }
    });
  });
  