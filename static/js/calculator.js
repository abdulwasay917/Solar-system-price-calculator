document.addEventListener("DOMContentLoaded", function(){

    const inputs = [
        "panel_quantity",
        "panel_watt",
        "frame_quantity",
        "company",
        "capacity"
    ];

    const companySelect = document.getElementById("company");
    const capacityDiv = document.getElementById("capacityDiv");
    const capacitySelect = document.getElementById("capacity");

    // Race condition handle karne ke liye global variable
    let currentAbortController = null;

    // 1. Debounce Utility Function (350ms Delay)
    function debounce(func, delay = 350) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => {
                func.apply(this, args);
            }, delay);
        };
    }

    // 2. Debounced Wrapper (Pehle define karein taake Initialization Error na aaye)
    const debouncedCalculate = debounce(calculate, 350);

    // 3. Hybrid Logic
    function handleCompanyChange(){
        if(companySelect.value === "Hybrid"){
            capacityDiv.classList.remove("capacity-hidden");
            capacitySelect.innerHTML = `<option value="6">6 kW</option>`;
            capacitySelect.disabled = true;
        }
        else if(companySelect.value === "None"){
            capacityDiv.classList.add("capacity-hidden");
            capacitySelect.disabled = false;
        }
        else{
            capacityDiv.classList.remove("capacity-hidden");
            capacitySelect.innerHTML = `
                <option value="8">8 kW</option>
                <option value="10">10 kW</option>
            `;
            capacitySelect.disabled = false;
        }
        debouncedCalculate();
    }

    companySelect.addEventListener("change", handleCompanyChange);
    handleCompanyChange();

    // Default Frames = Panels
    document.getElementById("panel_quantity").addEventListener("input", function(){
        if (this.value === "") {
            document.getElementById("frame_quantity").value = 0;
        } else {
            document.getElementById("frame_quantity").value = this.value;
        }
    });

    // Safe Empty/Backspace Check for inputs
    ['panel_quantity', 'frame_quantity'].forEach(id => {
        let element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', function() {
                if (this.value === '') {
                    this.value = 0;
                }
            });
        }
    });

    // Live Calculation Listeners using Debounce
    inputs.forEach(function(id){
        let element = document.getElementById(id);
        if (element) {
            element.addEventListener("change", debouncedCalculate);
            element.addEventListener("input", debouncedCalculate);
        }
    });

    function calculate(){
        let pQty = document.getElementById("panel_quantity").value;
        let fQty = document.getElementById("frame_quantity").value;

        let selectedCapacity = null;
        if (companySelect.value !== "None") {
            selectedCapacity = capacitySelect.value ? parseInt(capacitySelect.value, 10) : null;
        }

        let data = {
            panel_quantity: pQty === "" ? 0 : parseInt(pQty, 10),
            panel_watt: parseInt(document.getElementById("panel_watt").value, 10),
            frame_quantity: fQty === "" ? 0 : parseInt(fQty, 10),
            inverter_company: companySelect.value,
            inverter_capacity: selectedCapacity
        };

        if (currentAbortController) {
            currentAbortController.abort();
        }
        currentAbortController = new AbortController();

        fetch("/api/calculate/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken") || getCsrfFromInput(),
                "ngrok-skip-browser-warning": "true"
            },
            body: JSON.stringify(data),
            signal: currentAbortController.signal
        })
        .then(response => {
            if (!response.ok) throw new Error("Calculation failed with status: " + response.status);
            return response.json();
        })
        .then(result => {
            console.log("Calculation Result:", result);
            updateResult(result);
        })
        .catch(error => {
            if (error.name === 'AbortError') {
                return;
            }
            console.error("API Error:", error);
        });
    }

    function updateResult(data){
        document.getElementById("panel_price").innerHTML = "Rs. " + (data.panel_price ?? 0);
        document.getElementById("frame_price").innerHTML = "Rs. " + (data.frame_price ?? 0);
        document.getElementById("equipment_price").innerHTML = "Rs. " + (data.equipment_price ?? 0);
        document.getElementById("inverter_price").innerHTML = "Rs. " + (data.inverter_price ?? 0);
        document.getElementById("labour_price").innerHTML = "Rs. " + (data.labour_price ?? 0);
        document.getElementById("grand_total").innerHTML = "Rs. " + (data.grand_total ?? 0);
        document.getElementById("installment_total").innerHTML = "Rs. " + (data.installment_total ?? 0);
        document.getElementById("first_month_payment").innerHTML = "Rs. " + (data.first_month_payment ?? 0);
        document.getElementById("monthly_payment").innerHTML = "Rs. " + (data.monthly_payment ?? 0);
    }

    // Reset Button Functionality
    document.getElementById("reset").addEventListener("click", function(){
        if (currentAbortController) {
            currentAbortController.abort();
        }

        document.querySelectorAll("input").forEach(input => input.value = "0");

        document.getElementById("panel_watt").value = "585";
        companySelect.value = "Desi";

        capacitySelect.innerHTML = `
            <option value="8">8 kW</option>
            <option value="10">10 kW</option>
        `;
        capacitySelect.value = "8";
        capacitySelect.disabled = false;
        capacityDiv.classList.remove("capacity-hidden");

        document.querySelectorAll(
            "#panel_price,#frame_price,#equipment_price,#inverter_price,#labour_price,#grand_total,#installment_total,#first_month_payment,#monthly_payment"
        )
        .forEach(item => item.innerHTML = "Rs. 0");
    });

    function getCookie(name){
        let cookieValue = null;
        if(document.cookie && document.cookie !== ''){
            let cookies = document.cookie.split(';');
            for(let i = 0; i < cookies.length; i++){
                let cookie = cookies[i].trim();
                if(cookie.substring(0, name.length + 1) === (name + "=")){
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function getCsrfFromInput() {
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfInput ? csrfInput.value : '';
    }
});