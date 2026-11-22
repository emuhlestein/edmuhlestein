const navbarToggle = document.querySelector('.navbar-toggle');
const navbarMenu = document.querySelector('.navbar-menu');


navbarToggle.addEventListener('click', () => {
    navbarToggle.classList.toggle('active');
    navbarMenu.classList.toggle('active');
});

// document.querySelector('.toggle-password').addEventListener('click', function () {
//   const input = document.getElementById('password');
//   const showing = input.type === 'text';

//   input.type = showing ? 'password' : 'text';
//   this.classList.toggle('showing', !showing);
//   this.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
// });

document.querySelectorAll('.toggle-password').forEach(button => {
  button.addEventListener('click', function () {
    const field = this.closest('.password-field');
    const input = field.querySelector('input');
    const showing = input.type === 'text';

    input.type = showing ? 'password' : 'text';
    this.classList.toggle('showing', !showing);
    this.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
  });
});
