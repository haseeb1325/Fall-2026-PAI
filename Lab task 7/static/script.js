document.getElementById("btn-get").addEventListener("click", getWeather);

async function getWeather() {
    const city = document.getElementById("city").value.trim();

    if (!city) {
        alert("Please enter a city name!");
        return;
    }

    try {
        const response = await fetch("/get_weather", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ city })
        });

        const data = await response.json();

        if (response.ok && data.cod === 200) {
            document.getElementById("city-name").textContent = data.name;
            document.getElementById("temp").textContent = `🌡 Temperature: ${data.main.temp} °C`;
            document.getElementById("desc").textContent = `☁ Condition: ${data.weather[0].description}`;
        } else {
            const msg = data.message || "City not found!";
            document.getElementById("city-name").textContent = msg;
            document.getElementById("temp").textContent = "";
            document.getElementById("desc").textContent = "";
        }
    } catch (err) {
        console.error(err);
        alert("An error occurred. Check console for details.");
    }
}
