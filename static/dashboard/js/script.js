// Sidebar toggle
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('collapsed');
  document.getElementById('main-content').classList.toggle('full');
}
// Dark mode toggle
function toggleDarkMode() {
  var dark = document.body.classList.toggle('dark');
  var icon = document.getElementById('toggleIcon');

  const table = document.querySelector('table');
  if (table)
    table.classList.toggle('table-dark', dark);

  if (dark) {
    icon.classList.replace('bi-moon-fill', 'bi-sun-fill');
    localStorage.setItem('theme', 'dark');

  } else {
    icon.classList.replace('bi-sun-fill', 'bi-moon-fill');
    localStorage.setItem('theme', 'light');
  }
}
document.addEventListener('DOMContentLoaded', function () {

  const savedTheme = localStorage.getItem('theme');
  if (savedTheme == 'dark') {
    document.body.classList.add('dark');
    var icon = document.getElementById('toggleIcon');
    icon.classList.replace('bi-moon-fill', 'bi-sun-fill');
    var table = document.querySelector('table');
    if (table)
      table.classList.add('table-dark');
  }
});




// Collapse Panels
document.addEventListener('DOMContentLoaded', function () {
  var collapseButtons = document.querySelectorAll('.panel-heading');
  collapseButtons.forEach(button => {
    button.addEventListener('click', function () {
      var icon = this.querySelector('.panel-collapse-btn');
      if(icon)
      icon.classList.toggle('collapsed');
    });
  });
});


function handleResponsiveClasses() {
  var sidebar = document.getElementById('sidebar')
  var mainContent = document.getElementById('main-content')

  if (window.innerWidth < 768) {
    mainContent?.classList.add('full');
    sidebar?.classList.add('collapsed');
  } else {
    mainContent?.classList.remove('full');
    sidebar?.classList.remove('collapsed');
  }
}

// Run on page load
window.addEventListener('DOMContentLoaded', handleResponsiveClasses);

// Run on window resize
window.addEventListener('resize', handleResponsiveClasses);