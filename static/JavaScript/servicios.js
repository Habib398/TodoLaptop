const filas = document.querySelectorAll('tbody tr');
let seleccionado = null;
const btnEditar = document.getElementById('btnEditarSeleccion');
const btnEliminar = document.getElementById('btnEliminarSeleccion');
const btnCotizar = document.getElementById('btnCotizar');
const editarBody = document.getElementById('editarBody');
const formEditar = document.getElementById('formEditar');
const btnGuardarEditar = document.getElementById('btnGuardarEditar');
const eliminarBody = document.getElementById('eliminarBody');
const formEliminar = document.getElementById('formEliminar');
const btnConfirmarEliminar = document.getElementById('btnConfirmarEliminar');

filas.forEach(fila => {
    fila.addEventListener('click', () => {
        filas.forEach(f => f.classList.remove('table-primary'));
        fila.classList.add('table-primary');
        seleccionado = {
            id: fila.children[0].innerText.trim(),
            nombre: fila.children[1].innerText.trim(),
            descripcion: fila.children[2].getAttribute('data-full') || fila.children[2].innerText.trim(),
            costo_servicio: fila.children[3].innerText.replace('$','').trim()
        };
        btnEditar.disabled = false;
        btnEliminar.disabled = false;
        btnCotizar.disabled = false;
    });
});

// Al abrir modal editar
document.getElementById('modalEditar').addEventListener('show.bs.modal', () => {
    if (!seleccionado) return;
    formEditar.action = `/servicios/modificar/${seleccionado.id}/`;
    editarBody.innerHTML = `
        <div class="mb-3">
            <label class="form-label">Nombre</label>
            <input name="nombre" class="form-control" value="${seleccionado.nombre}" required />
        </div>
        <div class="mb-3">
            <label class="form-label">Descripción</label>
            <textarea name="descripcion" class="form-control">${seleccionado.descripcion || ''}</textarea>
        </div>
        <div class="mb-3">
            <label class="form-label">Precio</label>
            <input name="costo_servicio" type="number" step="0.01" class="form-control" value="${seleccionado.costo_servicio}" required />
        </div>
    `;
    btnGuardarEditar.disabled = false;
});

// Al abrir modal eliminar
document.getElementById('modalEliminar').addEventListener('show.bs.modal', () => {
    if (!seleccionado) return;
    formEliminar.action = `/servicios/eliminar/${seleccionado.id}/`;
    eliminarBody.innerHTML = `<p>¿Seguro que deseas eliminar <strong>${seleccionado.nombre}</strong>? Esta acción no se puede deshacer.</p>`;
    btnConfirmarEliminar.disabled = false;
});

// Manejar clic en botón cotizar
btnCotizar.addEventListener('click', () => {
    if (seleccionado && seleccionado.id) {
        window.location.href = `/servicios/cotizar/${seleccionado.id}/`;
    }
});