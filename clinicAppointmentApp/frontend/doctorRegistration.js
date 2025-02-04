document.addEventListener("DOMContentLoaded", () => {
  const doctorForm = document.getElementById("doctorForm");
  const messageDiv = document.getElementById("message");
  const specializationSelect = document.getElementById("specialization");

  // Function to fetch specializations
  async function fetchSpecializations() {
      try {
          const response = await fetch("http://127.0.0.1:5000/fetchAllSpecialisations", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              }
          });
          const data = await response.json();

          if (data.status) {
              data.data.forEach((specialization) => {
                  const option = document.createElement("option");
                  option.value = specialization.specializationId;
                  option.textContent = specialization.specializationName;
                  specializationSelect.appendChild(option);
              });
          } else {
              console.error("Error fetching specializations:", data.log);
          }
      } catch (error) {
          console.error("Error:", error);
      }
  }

  // Load specializations on page load
  fetchSpecializations();

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
                  Authorization: `Bearer ${localStorage.getItem("token")}`
              },
              body: JSON.stringify(doctorDetails),
          });

          const data = await response.json();
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
