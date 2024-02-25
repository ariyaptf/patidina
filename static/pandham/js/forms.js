var id_quantity = document.getElementById('id_1-quantity');
var amount_contributed_range = document.getElementById('amount_contributed_range');
var helptext = '';

function showRangeValue(value, price) {
    contribute = Number(value)
    quantity = Math.floor(contribute/price)

    var helptext = document.getElementById("amount_contributed_range_helptext")
    helptext.innerHTML = "ร่วมปันธรรม " + contribute.toLocaleString() +" บาท จำนวน "+ quantity.toLocaleString() + " เล่ม"

    localStorage.setItem('helptext', helptext.innerHTML);
    id_quantity.value = quantity
}


function target_groups_change(event, value) {
    const checkboxes = document.querySelectorAll('input[name="2-target_groups"]:checked');
    const selectedValues = Array.from(checkboxes).map(checkbox => checkbox.value);

    var target_address = document.getElementById('div_id_2-target_address');
    if (target_address) {
        if (selectedValues.includes('8')) {
            target_address.style.display = 'block';
        } else {
            target_address.style.display = 'none';
        }
    }
}


function requested_books_change(event) {
    requested_books = event.target.value;
    var PanDham = document.getElementById('id_2-for_PanDham');
    console.log(PanDham.value);
    PanDham.value = parseInt(PanDham.value) - parseInt(requested_books);
}


document.addEventListener("DOMContentLoaded", function() {
    var save_helptext = localStorage.getItem('helptext');
    var helptext = document.getElementById('amount_contributed_range_helptext');
    if (helptext) {
        helptext.innerHTML = save_helptext;
    }

    var target_address = document.getElementById('div_id_2-target_address');
    if (target_address) {
        target_address.style.display = 'none';
    }
});
