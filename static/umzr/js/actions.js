document.getElementById("comments-tab").addEventListener("click", function() {
  document.getElementById("tasks-content").style.display = "none";
  document.getElementById("comments-content").style.display = "block";
});

document.getElementById("tasks-tab").addEventListener("click", function() {
  document.getElementById("comments-content").style.display = "none";
  document.getElementById("tasks-content").style.display = "block";
});

var nav = document.querySelectorAll('.panels');
for (var i = 0; i < nav.length; i++) {
    nav[i].onclick = function() {
    var active = document.querySelector('.active');
    if (active) 
        {
        active.classList.remove('active');
        active.classList.remove('text-black');
        active.classList.toggle('text-white');
        };

    this.classList.toggle('active');
    this.classList.remove('text-white');
    this.classList.toggle('text-black');
  }
}