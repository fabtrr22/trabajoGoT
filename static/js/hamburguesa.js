document.addEventListener("DOMContentLoaded", function() {
    const menuHamburguesa = document.getElementById("menu-hamburguesa");
    const navLinks = document.getElementById("nav-links");

    menuHamburguesa.addEventListener("click", function() {
        navLinks.classList.toggle("mostrar");
    });
});