document.addEventListener("DOMContentLoaded", () => {
  const displayToday = document.querySelector(".display-today");
  const displayWeek = document.querySelector(".display-week");
  const displayMonth = document.querySelector(".display-month");
  const radioButtons = document.querySelectorAll('input[name="btnradio"]');

  function updateDisplay() {
    displayToday.classList.add("display-none");
    displayWeek.classList.add("display-none");
    displayMonth.classList.add("display-none");

    if (document.getElementById("btnradio1").checked) {
      displayToday.classList.remove("display-none");
    } else if (document.getElementById("btnradio2").checked) {
      displayWeek.classList.remove("display-none");
    } else if (document.getElementById("btnradio3").checked) {
      displayMonth.classList.remove("display-none");
    }
  }

  // Attach event listeners to all radio buttons
  radioButtons.forEach((radio) => {
    radio.addEventListener("change", updateDisplay);
  });

  // Initial check to display the correct content based on the checked radio button
  updateDisplay();
});

// Move completeTodo function outside the DOMContentLoaded block
function completeTodo(todoId) {
  fetch(`/complete_todo/${todoId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (response.ok) {
        window.location.reload(); // Reload the page to update the todo list
      } else {
        console.error("Failed to complete todo");
      }
    })
    .catch((error) => console.error("Error:", error));
}
