// Keep global reference to Chart instance so we can destroy it
let portfolioChartInstance = null;

// Async function to call backend
async function submitAdvisor(answers) {
  try {
    const res = await fetch("http://localhost:8000/advisor", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers })
    });

    if (!res.ok) {
      console.error("Fetch error:", res.status, res.statusText);
      return;
    }

    const data = await res.json();
    console.log("Advisor response:", data);

    if (data.portfolio) {
      renderPortfolioChart(data.portfolio);
    } else {
      console.error("No portfolio received:", data);
    }
  } catch (err) {
    console.error("Error calling backend:", err);
  }
}

// Hook submit button
document.getElementById("submit-btn").addEventListener("click", () => {
  const answers = getAnswersFromForm(); // read inputs
  submitAdvisor(answers);
});

// Function to get user answers
function getAnswersFromForm() {
  const answers = [];
  document.querySelectorAll(".question").forEach((q) => {
    answers.push(q.value); // adjust depending on input type
  });
  return answers;
}

// Function to render portfolio chart
function renderPortfolioChart(portfolio) {
  const ctx = document.getElementById("portfolioChart").getContext("2d");

  // Destroy old chart if it exists
  if (portfolioChartInstance) {
    portfolioChartInstance.destroy();
  }

  portfolioChartInstance = new Chart(ctx, {
    type: "pie",
    data: {
      labels: Object.keys(portfolio),
      datasets: [{
        data: Object.values(portfolio),
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        title: { display: true, text: "Portfolio Distribution" }
      }
    }
  });
}
