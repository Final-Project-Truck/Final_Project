document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("review-company-button").addEventListener("click", function() {
    document.getElementById("review-company-form").style.display = "block";
  });

  // Get the input element for the search bar
  const searchInput = document.getElementById("search-input");

  // Get the dropdown list element
  const dropdownList = document.getElementById("dropdown-list");
  // Keep track of whether a "Create Company" button was added
  let createButtonAdded = false;
  // Listen for changes in the search bar
  searchInput.addEventListener("input", function() {
    // Get the value of the search input
    const searchValue = this.value;

    // Make a GET request to the API to search for companies
    fetch(`http://127.0.0.1:8001/api/v1/companies/?search=${searchValue}`, {
      headers: {
        'Authorization': 'Basic ' + btoa('user1:password')
      }
    })
    .then(response => response.json())

    .then(data => {
      // Clear the dropdown list
      dropdownList.innerHTML = "";
      // Remove any existing "Create Company" buttons
      const createButton = document.getElementById("create-company-button");
      if (createButton) {
        createButton.remove();
        createButtonAdded = false;
      }

      // Loop through the results and add each company as an option in the dropdown list
      data.forEach(company => {
        const option = document.createElement("option");
        option.value = company.id;
        option.innerText = company.name;
        dropdownList.appendChild(option);
      });
      // If there are no matches, add a "Create Company" button
      if (!dropdownList.options.length && !createButtonAdded) {
        const createButton = document.createElement("button");
        createButton.id = "create-company-button";
        createButton.innerText = "Create Company";
        dropdownList.parentNode.insertBefore(createButton, dropdownList.nextSibling);
        createButtonAdded = true;
      }
    });
  });

  // Listen for click events on the "Create Company" button
  document.addEventListener("click", function(event) {
    if (event.target.id === "create-company-button") {
      console.log("Create Company button clicked");
      document.getElementById("create-company-form").style.display = "block";
    }
  });
});
