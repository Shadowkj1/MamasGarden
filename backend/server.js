const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

const plants = [
    { id: 1, name: "Aloe Vera", health: "Good", moistureData: [80, 60, 40, 20], recommendation: "Water once a week." },
    { id: 2, name: "Snake Plant", health: "Needs Water", moistureData: [70, 50, 30, 10], recommendation: "Water immediately!" },
];

app.get("/api/plants", (req, res) => res.json(plants));

app.get("/api/plant/:id", (req, res) => {
    let plant = plants.find(p => p.id == req.params.id);
    res.json(plant || { error: "Plant not found" });
});

app.listen(5000, () => console.log("Server running on port 5000"));
