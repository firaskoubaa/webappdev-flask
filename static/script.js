const current_location=location.href;

/////Making the selected navbar item bolder
//Getting my current locaton URL
const menu_item=document.querySelectorAll('.navigationbar_1item a');
const menu_length= menu_item.length;
const e=0;
for (let i=0; i<menu_length;i++){
  if (menu_item[i].href === current_location){
    menu_item[i].className="active";
    e=1;
  }
}
if (e == 0){
  menu_item[0].className="active";
}

/////Display the search table once the search button is clicked
// var pos = current_location.indexOf("?searched_keywords=");
// if (pos === 22){
//   var x = document.getElementById("book_search_table");
//   x.style.display = "block";
//   x.style.border = "none";
// }
var serstat=document.getElementById("search_status").textContent;
// alert(serstat)
if (serstat == "not found") {
  var disp_mess_err = document.getElementById("no_book_found");
  disp_mess_err.style.display = "block";
  document.getElementById("empty_bs_table").style.display="none";
}
else if (serstat == "found"){
  document.getElementById("book_search_table").style.display="block";
  document.getElementById("empty_bs_table").style.display="none";
  // disp_res_tab.style.border = "none";
}

///// Alert message whene the user tries to insert a new book in a full database (10 books)
// alert(document.getElementById("biggest_sb_id10").textContent);
// alert(document.getElementsByClassName("add_button ").onclick)
// var addforcl = document.getElementsByClassName("add_form");
// alert("hello")
// addforcl.onsubmit = function() {alert('Hello!')};
// cont cop = document.getElementById("biggest_sb_id10").textContent; 
// if (document.getElementById("biggest_sb_id10").textContent == 10) {alert("hello")};

/////Creating a button that takes the user  to the top of the page 
//Select the button
mybutton = document.getElementById("top_page");
// When the user scrolls down 500px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};
function scrollFunction() {
  if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
// When the user clicks on the button, scroll to the top of the document
function movetotop_Function() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
} 





// Adding data row to the bookshel database &&& deleating data from the bbokshelf
// function do_ajax(p) {
//   var req = new XMLHttpRequest();
//   var button_id = p;
//   req.open('POST', '/ajax_reader', true);
//   req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
//   req.send("button_id=" + button_id);  
// }