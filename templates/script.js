document.addEventListener("DOMContentLoaded", () => {
    const plantScroll = document.getElementById("plantScroll");

    // 🏗️ Duplicate plant cards to ensure a seamless loop
    function duplicateCards() {
        const clone = plantScroll.cloneNode(true);
        clone.setAttribute("aria-hidden", "true");
        plantScroll.parentElement.appendChild(clone);
    }

    duplicateCards();

    // 🌿 Adjust scrolling animation speed dynamically
    function adjustAnimationSpeed() {
        const totalWidth = plantScroll.scrollWidth / 2;
        const speed = totalWidth / 100; // Adjust speed based on content width
        plantScroll.style.animationDuration = `${speed}s`;
    }

    adjustAnimationSpeed();

    // 🛑 Pause scrolling when hovered
    plantScroll.addEventListener("mouseenter", () => {
        plantScroll.style.animationPlayState = "paused";
    });

    // ▶ Resume scrolling when mouse leaves
    plantScroll.addEventListener("mouseleave", () => {
        plantScroll.style.animationPlayState = "running";
    });

    // 🌱 Smooth Expansion on Hover
    const cards = document.querySelectorAll(".plant-card");

    cards.forEach(card => {
        card.addEventListener("mouseenter", () => {
            card.classList.add("expanded");
        });

        card.addEventListener("mouseleave", () => {
            card.classList.remove("expanded");
        });
    });
});
