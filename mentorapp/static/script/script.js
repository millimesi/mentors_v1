document.addEventListener('DOMContentLoaded', function() {
   let buttons = document.querySelectorAll('.see-more-btn');
   buttons.forEach(button => {
       button.addEventListener('click', function() {
        let isAuthenticated = this.getAttribute('data-auth') === 'True';
        if (isAuthenticated) {
            let index = this.getAttribute('data-index');
            seeMore(index);
        } else {
            alert('You need to login first!')
            window.location.href = '/login';
       }});
   });
});
function seeMore(index){
   let moreText = document.getElementById("more_" + index);
   let button = document.getElementById("more_btn_" + index);
   if (moreText.style.display === 'none'){
    moreText.style.display = 'inline';
    button.innerHTML = "See less";
   } else {
    moreText.style.display = 'none';
    button.innerHTML = "See more";
   }
}