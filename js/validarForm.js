document.addEventListener('DOMContentLoaded', function () {
    const formulario = document.getElementById('formulario-contacto');

    formulario.addEventListener('submit', function (event) {
        let valid = true;

        // valido campo nombre
        const nombre = document.getElementById('nombre');
        if (nombre.value.trim() === '') {
            valid = false;
            alert('Por favor, ingrese su nombre.');
        }

        // valido campo correo utilizando expresiones regulares para el arroba
        const correo = document.getElementById('correo');
        const correoPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!correoPattern.test(correo.value)) {
            valid = false;
            alert('Por favor, ingrese un correo electrónico válido.');
        }

        // valido campo temporada favorita
        const temporada = document.getElementById('temporada');
        if (temporada.value === '') {
            valid = false;
            alert('Por favor, seleccione su temporada favorita.');
        }

        // valido campo mensaje
        const mensaje = document.getElementById('mensaje');
        if (mensaje.value.trim() === '') {
            valid = false;
            alert('Por favor, ingrese un mensaje.');
        }

        // valido terminos y condiciones
        const terminos = document.getElementById('terminos');
        if (!terminos.checked) {
            valid = false;
            alert('Debe aceptar los términos y condiciones.');
        }

        // si algun campo no es valido, no se envia formulario
        if (!valid) {
            event.preventDefault();
        }
    });
});
