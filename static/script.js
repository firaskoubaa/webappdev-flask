/////Making the selected navbar item bolder
//Getting my current locaton URL
const current_location=location.href;
const menu_item=document.querySelectorAll('.navigationbar_1item a');
const menu_length= menu_item.length;
for (let i=0; i<menu_length;i++){
  if (menu_item[i].href=== current_location){
    menu_item[i].className="active";
  }
}

/////Show the book search table
// function show_book_search_table() {
//   var x = document.getElementById("book_search_table");
//   if (x.style.display === "none") {
//     x.style.display = "block";
//   } else {
//     x.style.display = "none";
//   }
// } 

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



/////testing: submitting form without refreching the page 

$("#search_submit_button").click(function(){ 
    $( "#book_search_table" ).load(" #book_search_table" );
});