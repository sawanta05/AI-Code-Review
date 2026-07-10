console.log("script.js loaded");

const button = document.getElementById("reviewBtn");

button.addEventListener("click", reviewCode);

async function reviewCode() {

    console.log("Button clicked");

    const code = document.getElementById("code").value;

    console.log("Code Entered:");
    console.log(code);

    if (code.trim() === "") {
        document.getElementById("output").textContent =
            "Please enter some Python code.";
        return;
    }

    document.getElementById("output").textContent = "Reviewing code...";

    try {

        const response = await fetch("http://127.0.0.1:5000/review", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                code: code
            })

        });

        console.log("Status Code:", response.status);

        const data = await response.json();

        console.log("Response:");
        console.log(data);

        alert("Response received!");

        document.getElementById("output").textContent =
            JSON.stringify(data, null, 4);

    }

    catch (error) {

        console.error("Fetch Error:", error);

        alert("Fetch Error!");

        document.getElementById("output").textContent =
            "Error: " + error.message;

    }

}