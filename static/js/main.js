function toggleMenu() {
  var sidebar = document.querySelector('.sidebar')

  sidebar.classList.toggle('shown')
}

var menuButton = document.querySelector('.menu-button')
  menuButton.addEventListener('click', toggleMenu)
