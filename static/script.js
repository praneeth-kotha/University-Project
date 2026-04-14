// ================= CROP PREDICTION =================

function predictCrop() {

  let resultBox = document.getElementById("result");

  let data = {
    nitrogen: parseFloat(document.getElementById("nitrogen").value),
    phosphorus: parseFloat(document.getElementById("phosphorus").value),
    potassium: parseFloat(document.getElementById("potassium").value),
    temperature: parseFloat(document.getElementById("temperature").value),
    humidity: parseFloat(document.getElementById("humidity").value),
    rainfall: parseFloat(document.getElementById("rainfall").value),
    ph: parseFloat(document.getElementById("ph").value),
    carbon: parseFloat(document.getElementById("carbon").value),
    soil: document.getElementById("soil").value.trim()
  };

  for (let key in data) {
    if (key === "soil") {
      if (!data[key]) {
        resultBox.innerHTML = "⚠ Please enter soil type.";
        return;
      }
    } else {
      if (isNaN(data[key])) {
        resultBox.innerHTML = "⚠ Please fill all numeric fields.";
        return;
      }
    }
  }

  if (data.ph < 0 || data.ph > 14) {
    resultBox.innerHTML = "⚠ pH must be between 0 and 14.";
    return;
  }

  if (data.temperature < -10 || data.temperature > 60) {
    resultBox.innerHTML = "⚠ Temperature looks unrealistic.";
    return;
  }

  if (data.humidity < 0 || data.humidity > 100) {
    resultBox.innerHTML = "⚠ Humidity must be 0–100%.";
    return;
  }

  resultBox.innerHTML = "⏳ Predicting...";
  resultBox.style.color = "#333";

  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(res => {
    if (!res.ok) throw new Error("Server error");
    return res.json();
  })
  .then(result => {
    resultBox.innerHTML =
      `🌾 Recommended Crop: <span style="color:green;">${result.crop}</span>`;
  })
  .catch(err => {
    console.error(err);
    resultBox.innerHTML =
      "❌ Prediction failed. Please try again.";
  });
}


// ================= AUTO FILL =================

function autoFill() {
  document.getElementById("nitrogen").value = 80;
  document.getElementById("phosphorus").value = 70;
  document.getElementById("potassium").value = 80;
  document.getElementById("temperature").value = 25;
  document.getElementById("humidity").value = 80;
  document.getElementById("rainfall").value = 200;
  document.getElementById("ph").value = 6.5;
  document.getElementById("carbon").value = 50;
  document.getElementById("soil").value = "Loamy Soil";
}


// ================= WHATSAPP CONTACT =================

function sendWhatsApp(event) {
  event.preventDefault();

  let name = document.getElementById("name").value;
  let email = document.getElementById("email").value;
  let phone = document.getElementById("phone").value;
  let message = document.getElementById("message").value;

  let yourNumber = "916300227707"; // ✅ correct format

  let text = `Hello, I got a new message from Smart Farm AI:

Name: ${name}
Email: ${email}
Phone: ${phone}

Message:
${message}`;

  let url = `https://wa.me/${yourNumber}?text=${encodeURIComponent(text)}`;

  window.open(url, "_blank");
}