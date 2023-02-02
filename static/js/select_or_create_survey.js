document.addEventListener("DOMContentLoaded", function() {
  const dropdownList = document.getElementById("dropdown-list");
  const createCompanyButton = document.getElementById("create-company-button");
  const createCompanyForm = document.getElementById("create-company-form");
  const surveyDropdown = document.getElementById("survey-dropdown");

  dropdownList.addEventListener("change", function() {
    // Retrieve the selected company's id
    const selectedCompanyId = dropdownList.value;
    //const selectedCompanyId = document.querySelector('dropdown-list')
    //document.querySelector('#select1')//document.querySelector('dropdown-list')
    // Fetch the active surveys for the selected company
    console.log(selectedCompanyId);
    fetch(`http://127.0.0.1:8001/api/v1/companies/${selectedCompanyId}/get_active_surveys/`, {
      headers: {
        'Authorization': 'Basic ' + btoa('user1:password')
      }
      })
      .then(response => response.json())
      .then(data => {
        // Clear the survey dropdown options
        surveyDropdown.innerHTML = "";
        // Loop through the active surveys for the selected company
        data.forEach(survey => {
          // Create a new option for each survey
          const option = document.createElement("option");
          option.value = survey.id;
          option.text = survey.title;
          // Add the option to the survey dropdown
          surveyDropdown.add(option);
        });
        // Show the survey dropdown
        surveyDropdown.style.display = "block";
      });
  });

  createCompanyButton.addEventListener("click", function() {
    createCompanyForm.style.display = "block";
    createCompanyButton.style.display = "none";
  });
});