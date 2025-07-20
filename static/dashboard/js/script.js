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
    if(table)
        table.classList.toggle('table-dark', dark);

    if (dark) {
        icon.classList.replace('bi-moon-fill', 'bi-sun-fill');

    } else {
        icon.classList.replace('bi-sun-fill', 'bi-moon-fill');
    }
}
// Collapse Panels
  document.addEventListener('DOMContentLoaded', function () {
    const collapseButtons = document.querySelectorAll('.panel-heading');
    collapseButtons.forEach(button => {
      button.addEventListener('click', function () {
        const icon = this.querySelector('.panel-collapse-btn');
        icon.classList.toggle('collapsed');
      });
    });
  });