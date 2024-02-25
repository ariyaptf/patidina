/**
 * This file contains JavaScript code for handling form interactions on the website.
 * It defines public variables and functions for manipulating form fields and displaying data.
 * The initial display of fields is set up, and there are functions for handling changes in book selection,
 * amount contributed, distribution preference, target groups, requested books, and phone number.
 * The form_submittable function is called when the form is ready for submission.
 */
// public variables
var selectedBook = 0; // หนังสือที่เลือก
var price = 0; // ราคาของหนังสือ
var stock = 0; // จำนวนหนังสือที่มีอยู่
var contribute = 0; // จำนวนเงินที่ร่วมปันธรรม
var quantity = 0; // จำนวนหนังสือที่ร่วมปันธรรม
var request_book = 0; // จำนวนหนังสือที่ขอรับ
var phone_number = ''; // เบอร์โทรศัพท์มือถือ
var otp = '' // รหัส OTP

var div_id_book = document.getElementById('div_id_book');

var div_id_name = document.getElementById('div_id_name');

var div_id_amount_contributed = document.getElementById('div_id_amount_contributed');

var div_id_quantity = document.getElementById('div_id_quantity');

var id_quantity = document.getElementById('id_quantity');

var div_id_requested_books = document.getElementById('div_id_requested_books');
var id_requested_books = document.getElementById('id_requested_books');

var div_id_distribution_preference = document.getElementById('div_id_distribution_preference');

var div_id_phone_number = document.getElementById('div_id_phone_number');

var div_id_shipping_address = document.getElementById('div_id_shipping_address');

var div_id_for_PanDham = document.getElementById('div_id_for_PanDham');
var id_for_PanDham = document.getElementById('id_for_PanDham');

var div_id_target_groups = document.getElementById('div_id_target_groups');

var div_id_target_address = document.getElementById('div_id_target_address');

var div_id_note = document.getElementById('div_id_note');

var form_submit = document.getElementById('form_submit');

// initial display of fields
function initial_display() {
    div_id_amount_contributed.style.display = 'none';

    div_id_quantity.style.display = 'none';
    id_quantity.disabled = true;

    div_id_distribution_preference.style.display = 'none';

    div_id_requested_books.style.display = 'none';

    div_id_shipping_address.style.display = 'none';

    div_id_for_PanDham.style.display = 'none';
    id_for_PanDham.disabled = true;

    div_id_target_groups.style.display = 'none';

    div_id_target_address.style.display = 'none';

    form_submit.disabled = true;

    form_submittable();
}

// ฟังก์ชันที่ใช้ในการแสดงค่าที่ถูกเลือกจากฟิลด์ book เพื่อดูราคาของหนังสือ
function book_change() {
    // อ่านค่าที่ถูกเลือกจากฟิลด์ book
    var selectedValue = document.querySelector('select[name=book]').value;

    if (selectedValue) {
        // อ่านข้อมูลทั้งหมดของหนังสือจาก storeData
        selectedBook = storeData.find(function(book) {
            return book.pk === Number(selectedValue);
        });
        // อ่านราคาของหนังสือและจำนวนหนังสือที่มีอยู่
        price = selectedBook && selectedBook.fields && selectedBook.fields.price;
        stock = selectedBook && selectedBook.fields && selectedBook.fields.stock;
        // แสดงฟิลด์ amount_contributed
        div_id_amount_contributed.value = price;
        div_id_amount_contributed.style.display = 'block';
        div_id_quantity.style.display = 'block';
        div_id_distribution_preference.style.display = 'block';
        div_id_target_groups.style.display = 'block';

        // ปรับปรุงฟอร์ม
        var amountContributedRange = document.getElementById("amount_contributed_range");
        if (amountContributedRange) {
            amountContributedRange.min = 0;
            amountContributedRange.max = price * stock;
            amountContributedRange.step = price;
            showRangeValue(price)
        }
        // ตรวจสอบว่าฟอร์มพร้อมสำหรับการส่งหรือไม่
        form_submittable();
    } else {
        initial_display()
    }
}

// ฟังก์ชันที่ใช้ในการแสดงค่าที่ถูกเลือกจากฟิลด์ amount_contributed เพื่อดูจำนวนหนังสือที่สามารถร่วมปันธรรมได้
function showRangeValue(value) {
    contribute = Number(value)
    quantity = Math.floor(contribute/price)

    var helptext = document.getElementById("amount_contributed_range_helptext")
    helptext.innerHTML = "ร่วมปันธรรม " + contribute.toLocaleString() +" บาท จำนวน "+ quantity.toLocaleString() + " เล่ม"

    id_quantity.value = quantity
    request_book = document.getElementById('id_requested_books').value;
    id_requested_books.max = quantity
    id_for_PanDham.value = quantity - request_book
}


// ฟังก์ชันที่ใช้ในการแสดงหรือซ่อนฟิลด์ requested_books ขึ้นอยู่กับค่าที่ถูกเลือกจากฟิลด์ distribution_preference
function distributionPreference_change() {
    // อ่านค่าที่ถูกเลือกจากฟิลด์ distribution_preference
    var selectedValue = document.querySelector('select[name=distribution_preference]').value;

    // ถ้าค่าที่ถูกเลือกคือ 'request_book', แสดงฟิลด์ requested_books
    if (selectedValue === 'request_book') {
        div_id_requested_books.style.display = 'block';
        div_id_shipping_address.style.display = 'block';

        div_id_for_PanDham.style.display = 'block';

        request_book = 1
        id_requested_books.value = request_book
        id_for_PanDham.value = quantity - request_book

        div_id_target_groups.style.display = 'block';
    }
    // ถ้าค่าที่ถูกเลือกไม่ใช่ 'requested_books', ซ่อนฟิลด์ requested_books
    else {
        div_id_requested_books.style.display = 'none';

        div_id_shipping_address.style.display = 'none';

        div_id_for_PanDham.style.display = 'block';
        id_for_PanDham.value = quantity

        div_id_target_groups.style.display = 'block';
    }
}

function target_groups_change(event, value) {
    var checkboxes = document.querySelectorAll('input[name="target_groups"]:checked');
    var selectedValues = Array.from(checkboxes).map(function(checkbox) {
        return checkbox.value;
    });

    if (selectedValues.includes('8')) {
        div_id_target_address.style.display = 'block';
    } else {
        div_id_target_address.style.display = 'none';
    }
}

function requested_books_change(event, value) {
    request_book = Number(value)
    // ตรวจสอบว่าจำนวนหนังสือที่ขอรับมากกว่าจำนวนหนังสือที่ร่วมปันธรรมได้หรือไม่
    if (request_book > quantity) {
        alert('จำนวนหนังสือที่ขอรับมากกว่าจำนวนหนังสือที่ร่วมปันธรรมได้')
        id_requested_books.value = quantity
        request_book = quantity
    }
    // คำนวณจำนวนหนังสือที่สามารถส่งให้กับ PanDham
    id_for_PanDham.value = quantity - request_book
    // ตรวจสอบว่าฟอร์มพร้อมสำหรับการส่งหรือไม่
    form_submittable();
}

function form_submittable() {
    console.log(selectedBook, quantity, request_book, phone_number);
    if (selectedBook && quantity && phone_number) {
        form_submit.disabled = false;
    } else {
        form_submit.disabled = true;
    }
}

function phone_number_change(event, value) {
    console.log(value)
    var phoneno = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    if(value.match(phoneno)) {
        phone_number = value;
        // ตรวจสอบว่าฟอร์มพร้อมสำหรับการส่งหรือไม่
        form_submittable();
    }
    else {
        alert("เบอร์โทรศัพท์มือถือไม่ถูกต้อง");
        return false;
    }

}


initial_display();


