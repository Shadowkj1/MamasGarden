let chartInstance;  // Store the chart instance globally

fetch("/api/plant-logs")
    .then(response => response.json())
    .then(data => {
        console.log("Fetched JSON Data:", data);

        if (!Array.isArray(data) || data.length === 0) {
            console.error("Invalid or empty JSON format");
            return;
        }

        // Extract timestamps and convert "2025/02/08 - 23:12:50" → "23:12"
        const timestamps = data.map(entry => {
            let time = entry.timestamp.split(" - ")[1]; // Extract time part "23:12:50"
            return time.substring(0, 5); // Keep only "HH:MM"
        });

        // Define datasets with labels and colors
        const datasetMap = {
            "temperatureF": { label: "Temperature (°F)", data: data.map(entry => parseFloat(entry.temperatureF)), color: "red" },
            "humidity": { label: "Humidity (%)", data: data.map(entry => parseFloat(entry.humidity)), color: "blue" },
            "light": { label: "Light Level", data: data.map(entry => parseFloat(entry.light)), color: "yellow" },
            "moisture": { label: "Moisture Level", data: data.map(entry => parseFloat(entry.moisture)), color: "green" },
            "waterLevel": { label: "Water Level", data: data.map(entry => parseFloat(entry.waterLevel)), color: "cyan" }
        };

        // Initialize first chart (Temperature by default)
        updateChart("temperatureF");

        // Listen for dropdown change
        document.getElementById("graphType").addEventListener("change", function() {
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
                        borderWidth: 2,
                        fill: false,
                        pointBackgroundColor: selectedDataset.color,
                        pointBorderColor: selectedDataset.color,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    layout: {
                        padding: {
                            left: 10, right: 10, top: 5, bottom: 0 // Reduce top padding
                        }
                    },
                    plugins: {
                        legend: {
                            display: false,
                            position: "top", // Moves legend to the top
                            align: "end", // Moves legend to the top-right corner
                            labels: {
                                color: "black", // Makes legend text black
                                font: {
                                    size: 14
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: "Timestamp",
                                color: "black"
                            },
                            ticks: {
                                color: "black",
                                maxRotation: 0, // Prevents excessive tilting
                                autoSkip: true, // Prevents overcrowding
                                maxTicksLimit: 12 // Controls number of x-axis labels shown
                            },
                            grid: { color: "rgba(0,0,0,0.2)" }
                        },
                        y: {
                            title: {
                                display: true,
                                text: selectedDataset.label,
                                color: "black"
                            },
                            ticks: {
                                color: "black"
                            },
                            grid: { color: "rgba(0,0,0,0.2)" }
                        }
                    }
                }
            });
        }
    })
    .catch(error => console.error("Error fetching plant logs:", error));
