document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('temporada-form');
    const temporadaIdInput = document.getElementById('temporada-id');
    const numeroInput = document.getElementById('numero');
    const tituloInput = document.getElementById('titulo');
    const descripcionInput = document.getElementById('descripcion');
    const imagenInput = document.getElementById('imagen');
    const submitButton = document.getElementById('submit-button');
    const listaTemporadas = document.getElementById('lista-temporadas');

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
        const id = temporadaIdInput.value;
        const numero = numeroInput.value;
        const titulo = tituloInput.value;
        const descripcion = descripcionInput.value;
        const imagen = imagenInput.files[0];

        const formData = new FormData();
        formData.append('numero', numero);
        formData.append('titulo', titulo);
        formData.append('descripcion', descripcion);
        if (imagen) {
            formData.append('imagen', imagen);
        }

        if (id) {
            // actualizar temporada
            fetch(`/temporadas/${id}`, {
                method: 'PUT',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.mensaje === "Temporada modificada") {
                    alert('Temporada actualizada exitosamente');
                    cargarTemporadas();
                    form.reset();
                    temporadaIdInput.value = '';
                    submitButton.textContent = 'Agregar';
                    modal.style.display = "none";
                } else {
                    alert('Error al actualizar la temporada');
                }
            });
        } else {
            // agregar nueva temporada
            fetch('/temporadas', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.mensaje === "Temporada agregada correctamente.") {
                    alert('Temporada agregada exitosamente');
                    cargarTemporadas();
                    form.reset();
                    modal.style.display = "none";
                } else {
                    alert('Error al agregar la temporada');
                }
            });
        }
    });

    function cargarTemporadas() {
        fetch('/temporadas')
        .then(response => response.json())
        .then(data => {
            listaTemporadas.innerHTML = '';
            data.forEach(temporada => {
                const article = document.createElement('article');
                article.classList.add('temporada');
                article.innerHTML = `
                    <div class="card-container--value">
                        <h3>Temporada ${temporada.numero}</h3>
                        <div class="card-container--de">
                            <button id="btn-editar" onclick="editarTemporada(${temporada.id})">
                                <img src="../static/img/lapiz-copia.png" alt="Editar" />
                            </button>
                            <button id="btn-eliminar" onclick="eliminarTemporada(${temporada.id})">
                                <img src="../static/img/icon_trash.png" alt="Eliminar" />
                            </button>
                        </div>
                    </div>    
                    <img src="/static/img/${temporada.imagen_url}" alt="">
                    <p>${temporada.titulo}</p>
                    <p>${temporada.descripcion}</p>                   
                `;
                listaTemporadas.appendChild(article);
            });
        });
    }
    

    window.editarTemporada = function(id) {
        fetch(`/temporadas/${id}`)
        .then(response => response.json())
        .then(data => {
            temporadaIdInput.value = data.id;
            numeroInput.value = data.numero;
            tituloInput.value = data.titulo;
            descripcionInput.value = data.descripcion;
            submitButton.textContent = 'Actualizar';
            modal.style.display = "block";
        });
    };

    window.eliminarTemporada = function(id) {
        if (confirm('¿Estás seguro de que deseas eliminar esta temporada?')) {
            fetch(`/temporadas/${id}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.mensaje === "Temporada eliminada") {
                    alert('Temporada eliminada exitosamente');
                    cargarTemporadas();
                } else {
                    alert('Error al eliminar la temporada');
                }
            });
        }
    };

    cargarTemporadas();
});
