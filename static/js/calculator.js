document.addEventListener(
"DOMContentLoaded",
function(){


const inputs = [

    "panel_quantity",
    "panel_watt",
    "frame_quantity",
    "company",
    "capacity"

];


// default frames = panels

document
.getElementById("panel_quantity")
.addEventListener(
"input",
function(){

    document.getElementById("frame_quantity").value = this.value;

    calculate();

});



// live calculation

inputs.forEach(
function(id){

    document
    .getElementById(id)
    .addEventListener(
    "change",
    calculate
    );


    document
    .getElementById(id)
    .addEventListener(
    "input",
    calculate
    );

});




// API Call

function calculate(){


let data = {


    panel_quantity:
    document.getElementById("panel_quantity").value,


    panel_watt:
    document.getElementById("panel_watt").value,


    frame_quantity:
    document.getElementById("frame_quantity").value,


    inverter_company:
    document.getElementById("company").value,


    inverter_capacity:
    document.getElementById("capacity").value


};



if(!data.panel_quantity){

    return;

}



fetch(
"/api/calculate/",
{

method:"POST",

headers:{

"Content-Type":"application/json",

"X-CSRFToken":getCookie("csrftoken")

},


body:JSON.stringify(data)


}

)

.then(response=>response.json())

.then(result=>{


updateResult(
result
);


})

.catch(error=>{

console.log(error);

});


}




// Update UI

function updateResult(data){


document
.getElementById("panel_price")
.innerHTML =
"Rs. "+data.panel_price;



document
.getElementById("frame_price")
.innerHTML =
"Rs. "+data.frame_price;



document
.getElementById("equipment_price")
.innerHTML =
"Rs. "+data.equipment_price;



document
.getElementById("inverter_price")
.innerHTML =
"Rs. "+data.inverter_price;



document
.getElementById("labour_price")
.innerHTML =
"Rs. "+data.labour_price;



document
.getElementById("grand_total")
.innerHTML =
"Rs. "+data.grand_total;



document
.getElementById("installment_total")
.innerHTML =
"Rs. "+data.installment_total;



document
.getElementById("first_month_payment")
.innerHTML =
"Rs. "+data.first_month_payment;



document
.getElementById("monthly_payment")
.innerHTML =
"Rs. "+data.monthly_payment;



}




// Reset Button


document
.getElementById("reset")
.addEventListener(
"click",
function(){


document
.querySelectorAll("input")
.forEach(
input=>input.value=""
);



document
.getElementById("panel_watt")
.value="550";


document
.getElementById("company")
.value="Desi";


document
.getElementById("capacity")
.value="8";



document
.querySelectorAll(
"#panel_price,#frame_price,#equipment_price,#inverter_price,#labour_price,#grand_total,#installment_total,#first_month_payment,#monthly_payment"
)
.forEach(
item=>item.innerHTML="Rs. 0"
);



});





// CSRF Cookie

function getCookie(name) {

let cookieValue = null;


if(document.cookie && document.cookie !== ''){


let cookies = document.cookie.split(';');


for(let i=0;i<cookies.length;i++){


let cookie = cookies[i].trim();


if(cookie.substring(0,name.length+1)
===
(name+'=')){


cookieValue =
decodeURIComponent(
cookie.substring(name.length+1)
);


break;

}


}

}


return cookieValue;

}



});