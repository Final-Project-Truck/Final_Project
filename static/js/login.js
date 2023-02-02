// Function to handle the form submit
$("#login-form").submit(function(event) {
  event.preventDefault();

  // Collect the form data
  let formData = {
    "username": $("input[name='username']").val(),
    "password": $("input[name='password']").val()
  };

  // Make a POST request to the API endpoint
  $.ajax({
    type: "POST",
    url: "'api/v1/token-auth/login'",
    data: formData,
    success: function(data) {
      // Store the token in local storage
      localStorage.setItem("token", data.token);
    },
    error: function(error) {
      // Handle the error
    }
  });
});
