// Import the BASE_URL from the config file
import { BASE_URL } from './config.js';

function displayCSVResults(results) {
  console.log("Displaying CSV results:", results); // Log the results for debugging
    if (!Array.isArray(results)) {
        console.error("Expected results to be an array, but got:", results);
        document.getElementById("csvResult").textContent = "Error: Invalid data format.";
        return;
    }
    console.log("Results:", results); // Log the results for debugging
    const container = document.getElementById("csvResult");
    container.innerHTML = "";
  
    // إحصائيات
    let fraudCount = 0;
    let legitCount = 0;
    
    const table = document.createElement("table");
    table.className = "result-table";
    const thead = document.createElement("thead");
    thead.innerHTML = "<tr><th>#</th><th>Is Fraud?</th><th>Fraud Score</th></tr>";
    table.appendChild(thead);
    
    const tbody = document.createElement("tbody");
    
    results.forEach((item, index) => {
      const row = document.createElement("tr");

      // Check if item.Class exists, otherwise use a fallback or log an error
      const fraudClass = item.Predicted_Class !== undefined ? item.Predicted_Class : "undefined";
      const fraudScore = item.Fraud_Score !== undefined ? item.Fraud_Score : "N/A";
      const symbol = fraudClass === 0 ? "✅" : fraudClass === 1 ? "⚠️" : "❓";

      // Add the row with the appropriate symbol and fraud score
      row.innerHTML = `<td>${index + 1}</td><td>${symbol} ${fraudClass}</td><td>${fraudScore}%</td>`;
      tbody.appendChild(row);

      // Increment fraud or legit count based on the class
      if (fraudClass === 1) {
        fraudCount++;
      } else if (fraudClass === 0) {
        legitCount++;
      }
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
  
// Add console logs to debug the uploadCSV function
async function uploadCSV() {
    console.log("uploadCSV function called");
    const input = document.getElementById('csvInput');
    console.log("Input element:", input);
    const file = input.files[0];
    console.log("Selected file:", file);
    if (!file) {
      alert("Please select a CSV file.");
      console.log("No file selected");
      return;
    }
  
    const formData = new FormData();
    formData.append("file", file);
    console.log("FormData created:", formData);
  
    try {
      console.log("Sending POST request to:", `${BASE_URL}/csv`);
      const res = await fetch(`${BASE_URL}/csv`, {
        method: "POST",
        body: formData,
      });
      console.log("Response received:", res);
      const data = await res.json();
      console.log("Parsed JSON data:", data);
      displayCSVResults(data);
    } catch (error) {
      console.error("Error occurred during CSV upload:", error);
      document.getElementById("csvResult").textContent = "Error: " + error;
    }
}
  
// Add console logs to debug the sendJSON function
async function sendJSON() {
  console.log("sendJSON function called");
  const input = document.getElementById("jsonInput").value;
  console.log("Input value:", input);

  let jsonData;
  try {
    // Attempt to parse input as JSON
    jsonData = JSON.parse(input);
    console.log("Parsed input as JSON:", jsonData);
  } catch (jsonError) {
    console.log("Input is not valid JSON, attempting to parse as other formats");

    try {
      // Attempt to parse input as CSV, space-separated, or tab-separated
      const rows = input.split(/\r?\n/).filter(row => row.trim() !== "");
      
      // Automatically add headers if not present
      const headers = Array.from({ length: 28 }, (_, i) => `V${i + 1}`).concat("Amount");
      
      jsonData = rows.map(row => {
      const values = row.split(/,|\t| /).map(value => value.trim());
      if (values.length !== headers.length) {
        throw new Error("Invalid row format. Each row must have 29 values.");
      }
      return headers.reduce((obj, header, index) => {
        obj[header] = values[index];
        return obj;
      }, {});
      });
      console.log("Parsed input as tabular data:", jsonData);
    } catch (parseError) {
      console.error("Failed to parse input:", parseError);
      document.getElementById("jsonResult").textContent = "Error: Invalid input format.";
      return;
    }
  }

  try {
    console.log("Sending POST request to:", `${BASE_URL}/predict_single`);
    const res = await fetch(`${BASE_URL}/predict_single`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(jsonData),
    });
    console.log("Response received:", res);
    const data = await res.json();
    console.log("Parsed JSON response:", data);

    // Clear previous result
    const resultContainer = document.getElementById("jsonResult");
    console.log("Result container element:", resultContainer);
    resultContainer.innerHTML = "";

    // Create a styled card to display the result
    const resultCard = document.createElement("div");
    resultCard.className = "result-card";
    resultCard.innerHTML = `
      <h3>Prediction Result</h3>
      <p><strong>Fraud Class:</strong> ${data.Predicted_Class}</p>
      <p><strong>Fraud Score:</strong> ${data.Fraud_Score}%</strong></p>
    `;

    resultContainer.appendChild(resultCard);
    console.log("Result card appended to container");
  } catch (error) {
    console.error("Error occurred during JSON processing:", error);
    document.getElementById("jsonResult").textContent = "Error: " + error;
  }
}

// Attach the uploadCSV function to the global window object
window.uploadCSV = uploadCSV;

// Attach the sendJSON function to the global window object
window.sendJSON = sendJSON;
