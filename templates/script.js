// Fetch plants and display them in the dashboard
async function loadPlants() {
    let response = await fetch("http://localhost:5000/api/plants");
    let plants = await response.json();

    let container = document.getElementById("plantList");
    container.innerHTML = "";

    plants.forEach(plant => {
        let div = document.createElement("div");
        div.className = "plant-card";
        div.innerHTML = `<h3>${plant.name}</h3><p>Health: ${plant.health}</p>`;
        div.onclick = () => window.location.href = `profile.html?id=${plant.id}`;
        container.appendChild(div);
    });
}

// Load plant data for profile
async function loadPlantProfile() {
    let params = new URLSearchParams(window.location.search);
    let plantId = params.get("id");

    let response = await fetch(`http://localhost:5000/api/plant/${plantId}`);
    let plant = await response.json();

    document.getElementById("plantName").textContent = plant.name;
    document.getElementById("aiAdvice").textContent = `AI Recommendations: ${plant.recommendation}`;

    // Chart.js - Create a line chart
    let ctx = document.getElementById("plantChart").getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: ["12 AM", "6 AM", "12 PM", "6 PM"],
            datasets: [{
                label: "Moisture Level (%)",
                data: plant.moistureData,
                borderColor: "blue",
                borderWidth: 2
            }]
        }
    });
}

if (window.location.pathname.includes("profile.html")) {
    loadPlantProfile();
} else {
    loadPlants();
}
