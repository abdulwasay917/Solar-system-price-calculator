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

    // Hybrid Logic (Using capacity-hidden class for perfect height matching)
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
        calculate();
    }

    companySelect.addEventListener("change", handleCompanyChange);
    handleCompanyChange();

    // Default Frames = Panels
    document.getElementById("panel_quantity").addEventListener("input", function(){
        // Agar input khali ho jaye to text box me automatic 0 show ho sake
        if (this.value === "") {
            document.getElementById("frame_quantity").value = 0;
        } else {
            document.getElementById("frame_quantity").value = this.value;
        }
        calculate();
    });

    // Safe Empty/Backspace Check for inputs
    // Isse jab bhi backspace se text delete hoga, error nahi aayega aur values properly update hongi
    ['panel_quantity', 'frame_quantity'].forEach(id => {
        let element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', function() {
                if (this.value === '') {
                    this.value = 0;
                    calculate();
                }
            });
        }
    });

    // Live Calculation Listeners
    inputs.forEach(function(id){
        let element = document.getElementById(id);
        element.addEventListener("change", calculate);
        element.addEventListener("input", calculate);
    });

    function calculate(){
        // Agar value khali ("") ho to "0" pass karein taake undefined error na aaye
        let pQty = document.getElementById("panel_quantity").value;
        let fQty = document.getElementById("frame_quantity").value;

        let data = {
            panel_quantity: pQty === "" ? "0" : pQty,
            panel_watt: document.getElementById("panel_watt").value,
            frame_quantity: fQty === "" ? "0" : fQty,
            inverter_company: companySelect.value,
            inverter_capacity: companySelect.value === "None" ? null : capacitySelect.value
        };

        // Purana return statement hata diya taake zero value par bhi API hit ho sake
        // aur calculation reset ho kar Rs. 0 dikhaye.

        fetch("/api/calculate/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            updateResult(result);
        })
        .catch(error => {
            console.log(error);
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
        document.querySelectorAll("input").forEach(input => input.value = "0"); // Reset values to 0 instead of empty string

        document.getElementById("panel_watt").value = "585";
        companySelect.value = "Desi";

        // Reset capacity options
        capacitySelect.innerHTML = `
            <option value="8">8 kW</option>
            <option value="10">10 kW</option>
        `;
        capacitySelect.value = "8";
        capacitySelect.disabled = false;
        capacityDiv.classList.remove("capacity-hidden"); // Space handling fix

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
});