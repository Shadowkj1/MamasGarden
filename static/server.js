document.addEventListener("DOMContentLoaded", function () {
    // 🎯 Sample Plant Data for Chart
    let plantData = {
        labels: ["12 AM", "6 AM", "12 PM", "6 PM"],
        datasets: [
            {
                label: "Moisture Level (%)",
                data: [80, 60, 40, 20],
                borderColor: "blue",
                borderWidth: 2
            },
            {
                label: "Sunlight (hrs)",
                data: [0, 2, 5, 3],
                borderColor: "yellow",
                borderWidth: 2
            },
            {
                label: "Water Level (%)",
                data: [100, 80, 60, 30],
                borderColor: "green",
                borderWidth: 2
            }
        ]
    };

    // 📈 Create Chart
    let ctx = document.getElementById("plantChart").getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: plantData
    });

    // 🤖 AI Recommendations
    let aiAdvice = "Water your Snake Plant today to keep it hydrated!";
    document.getElementById("aiAdvice").textContent = aiAdvice;
});
