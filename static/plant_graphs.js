let chartInstance;  // Store the chart instance globally

fetch("/api/plant-logs")  // Now fetching from MongoDB
    .then(response => response.json())
    .then(data => {
        console.log("✅ Fetched Plant Logs from MongoDB:", data);

        if (!Array.isArray(data) || data.length === 0) {
            console.error("❌ No valid data received from MongoDB");
            document.getElementById("chartTitle").innerText = "No Data Available";
            return;
        }

        // Extract timestamps and convert "2025/02/08 - 23:12:50" → "23:12"
        const timestamps = data.map(entry => {
            try {
                if (!entry.timestamp || !entry.timestamp.includes(" - ")) {
                    console.warn("⚠️ Invalid timestamp format:", entry.timestamp);
                    return "N/A";
                }
                let time = entry.timestamp.split(" - ")[1]; // Extract "23:12:50"
                return time ? time.substring(0, 5) : "N/A"; // Keep only "HH:MM"
            } catch (error) {
                console.warn("⚠️ Error parsing timestamp:", entry.timestamp);
                return "N/A";
            }
        });

        // Define datasets with labels and colors
        const datasetMap = {
            "temperatureF": { label: "Temperature (°F)", data: [], color: "#FF5733" },
            "humidity": { label: "Humidity (%)", data: [], color: "#3498DB" },
            "light": { label: "Light Level (Lux)", data: [], color: "#F1C40F" },
            "moisture": { label: "Moisture Level (%)", data: [], color: "#27AE60" },
            "waterLevel": { label: "Water Level (cm)", data: [], color: "#1ABC9C" }
        };

        // Fill datasets dynamically, ensuring valid numeric values
        Object.keys(datasetMap).forEach(metric => {
            datasetMap[metric].data = data.map(entry => {
                const value = parseFloat(entry[metric]);
                return isNaN(value) ? null : value; // Ensure valid numeric data
            });
        });

        // Initialize first chart (Temperature by default)
        updateChart("temperatureF");

        // Listen for dropdown change
        document.getElementById("graphType").addEventListener("change", function () {
            updateChart(this.value);
        });

        function updateChart(metric) {
            const ctx = document.getElementById("dataChart").getContext("2d");
            const selectedDataset = datasetMap[metric];

            // Update chart title
            document.getElementById("chartTitle").innerText = selectedDataset.label;

            // Destroy existing chart if it exists
            if (chartInstance) {
                chartInstance.destroy();
            }

            // Create a new chart
            chartInstance = new Chart(ctx, {
                type: "line",
                data: {
                    labels: timestamps,
                    datasets: [{
                        label: selectedDataset.label,
                        data: selectedDataset.data,
                        borderColor: selectedDataset.color,
                        borderWidth: 3,
                        fill: false,
                        pointBackgroundColor: selectedDataset.color,
                        pointBorderColor: selectedDataset.color,
                        pointRadius: 4,
                        pointHoverRadius: 6,
                        tension: 0.4 // Smooth curve effect
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: {
                        duration: 1000, // Smooth animation
                        easing: "easeOutQuad"
                    },
                    layout: {
                        padding: {
                            left: 10, right: 10, top: 5, bottom: 0
                        }
                    },
                    plugins: {
                        legend: {
                            display: false,
                            labels: {
                                color: "black",
                                font: { size: 14 }
                            }
                        },
                        tooltip: {
                            backgroundColor: "rgba(0,0,0,0.8)",
                            titleColor: "#fff",
                            bodyColor: "#fff"
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: "Timestamp",
                                color: "black",
                                font: { size: 14, weight: "bold" }
                            },
                            ticks: {
                                color: "black",
                                maxRotation: 0,
                                autoSkip: true,
                                maxTicksLimit: 12
                            },
                            grid: { color: "rgba(0,0,0,0.1)" }
                        },
                        y: {
                            title: {
                                display: true,
                                text: selectedDataset.label,
                                color: "black",
                                font: { size: 14, weight: "bold" }
                            },
                            ticks: {
                                color: "black"
                            },
                            grid: { color: "rgba(0,0,0,0.1)" }
                        }
                    }
                }
            });
        }
    })
    .catch(error => console.error("❌ Error fetching plant logs from MongoDB:", error));

    document.addEventListener("DOMContentLoaded", function () {
        fetchRecommendation();
    
        function fetchRecommendation() {
            fetch('/get_recommendation')
                .then(response => response.json())
                .then(data => {
                    console.log("🌱 AI Recommendation:", data);
                    document.getElementById("ai-recommendation").innerHTML = 
                        `<strong>AI Suggestion:</strong> ${data.recommendation}`;
                })
                .catch(error => console.error("❌ Error fetching recommendation:", error));
        }
    });
    