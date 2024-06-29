document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('personaje-form');
    const personajeIdInput = document.getElementById('personaje-id');
    const nombreInput = document.getElementById('nombre');
    const descripcionInput = document.getElementById('descripcion');
    const imagenInput = document.getElementById('imagen');
    const submitButton = document.getElementById('submit-button');
    const listaPersonajes = document.getElementById('lista-personajes');

    const modal = document.getElementById("modal");
    const openModalButton = document.getElementById("openModal");
    const closeModalButton = document.getElementsByClassName("close")[0];

    openModalButton.onclick = function() {
        modal.style.display = "block";
    }

    closeModalButton.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const id = personajeIdInput.value;
        const nombre = nombreInput.value;
        const descripcion = descripcionInput.value;
        const imagen = imagenInput.files[0];

        const formData = new FormData();
        formData.append('nombre', nombre);
        formData.append('descripcion', descripcion);
        if (imagen) {
            formData.append('imagen', imagen);
        }

        if (id) {
            // actualizar personaje
            fetch(`/personajes/${id}`, {
                method: 'PUT',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.mensaje === "Personaje modificado") {
                    alert('Personaje actualizado exitosamente');
                    cargarPersonajes();
                    form.reset();
                    personajeIdInput.value = '';
                    submitButton.textContent = 'Agregar';
                    modal.style.display = "none";
                } else {
                    alert('Error al actualizar el personaje');
                }
            });
        } else {
            // agregar nuevo personaje
            fetch('/personajes', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.mensaje === "Personaje agregado correctamente.") {
                    alert('Personaje agregado exitosamente');
                    cargarPersonajes();
                    form.reset();
                    modal.style.display = "none";
                } else {
                    alert('Error al agregar el personaje');
                }
            });
        }
    });

    function cargarPersonajes() {
        fetch('/personajes')
        .then(response => response.json())
        .then(data => {
            listaPersonajes.innerHTML = '';
            data.forEach(personaje => {
                const article = document.createElement('article');
                article.classList.add('personaje');
                article.innerHTML = `
                    <div class="card-container--value">
                        <h3>${personaje.nombre}</h3>
                        <div class="card-container--de">
                            <button id="btn-editar" onclick="editarPersonaje(${personaje.id})">
                                <img src="../static/img/lapiz-copia.png" alt="Editar" />
                            </button>
                            <button id="btn-eliminar" onclick="eliminarPersonaje(${personaje.id})">
                                <img src="../static/img/icon_trash.png" alt="Eliminar" />
                            </button>
                        </div>
                    </div>    
                    <img src="/static/img/${personaje.imagen_url}" alt="">
                    <p>${personaje.descripcion}</p>                   
                `;
                listaPersonajes.appendChild(article);
            });
        });
    }
    

    window.editarPersonaje = function(id) {
        fetch(`/personajes/${id}`)
        .then(response => response.json())
        .then(data => {
            personajeIdInput.value = data.id;
            nombreInput.value = data.nombre;
            descripcionInput.value = data.descripcion;
            submitButton.textContent = 'Actualizar';
            modal.style.display = "block";
        });
    };

    window.eliminarPersonaje = function(id) {
        if (confirm('¿Estás seguro de que deseas eliminar este personaje?')) {
            fetch(`/personajes/${id}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.mensaje === "Personaje eliminado") {
                    alert('Personaje eliminado exitosamente');
                    cargarPersonajes();
                } else {
                    alert('Error al eliminar el personaje');
                }
            });
        }
    };

    cargarPersonajes();
});
