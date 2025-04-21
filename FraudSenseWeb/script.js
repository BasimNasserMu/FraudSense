// Import the BASE_URL from the config file
import { BASE_URL } from './config.js';

function displayCSVResults(results) {
    const container = document.getElementById("csvResult");
    container.innerHTML = "";
  
    // إحصائيات
    let fraudCount = 0;
    let legitCount = 0;
  
    const table = document.createElement("table");
    table.className = "result-table";
    const thead = document.createElement("thead");
    thead.innerHTML = "<tr><th>#</th><th>Prediction</th></tr>";
    table.appendChild(thead);
  
    const tbody = document.createElement("tbody");
  
    results.forEach((item, index) => {
      const row = document.createElement("tr");
      row.innerHTML = `<td>${index + 1}</td><td>${item.Predicted_Class}</td>`;
      tbody.appendChild(row);
  
      if (item.Predicted_Class === "Fraud") fraudCount++;
      else legitCount++;
    });
  
    table.appendChild(tbody);
  
    // الإحصائيات
    const stats = document.createElement("div");
    stats.className = "stats";
    stats.innerHTML = `
      <p>🔍 Total Predictions: ${results.length}</p>
      <p>⚠️ Fraud: ${fraudCount}</p>
      <p>✅ Not Fraud: ${legitCount}</p>
    `;
  
    container.appendChild(stats);
    container.appendChild(table);
  }
  
  async function uploadCSV() {
    const input = document.getElementById('csvInput');
    const file = input.files[0];
    if (!file) {
      alert("Please select a CSV file.");
      return;
    }
  
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const res = await fetch(`${BASE_URL}/csv`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      displayCSVResults(data);
    } catch (error) {
      document.getElementById("csvResult").textContent = "Error: " + error;
    }
  }
  

async function sendJSON() {
  const input = document.getElementById("jsonInput").value;
  try {
    const jsonData = JSON.parse(input);
    const res = await fetch(`${BASE_URL}/predict_single`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(jsonData),
    });
    const data = await res.json();

    // Clear previous result
    const resultContainer = document.getElementById("jsonResult");
    resultContainer.innerHTML = "";

    // Create a styled card to display the result
    const resultCard = document.createElement("div");
    resultCard.className = "result-card";
    resultCard.innerHTML = `
      <h3>Prediction Result</h3>
      <p><strong>Fraud Score:</strong> ${data.Fraud_Score}</p>
    `;

    resultContainer.appendChild(resultCard);
  } catch (error) {
    document.getElementById("jsonResult").textContent = "Error: " + error;
  }
}

// Attach the uploadCSV function to the global window object
window.uploadCSV = uploadCSV;

// Attach the sendJSON function to the global window object
window.sendJSON = sendJSON;
