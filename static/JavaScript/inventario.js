const filas = document.querySelectorAll('tbody tr');
let seleccionado = null;
const btnEditar = document.getElementById('btnEditarSeleccion');
const btnEliminar = document.getElementById('btnEliminarSeleccion');
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
            precio: fila.children[3].innerText.replace('$','').trim(),
            cantidad: fila.children[4].innerText.trim()
        };
        btnEditar.disabled = false;
        btnEliminar.disabled = false;
    });
});

// Al abrir modal editar
document.getElementById('modalEditar').addEventListener('show.bs.modal', () => {
    if (!seleccionado) return;
    formEditar.action = `/inventario/modificar/${seleccionado.id}/`;
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
            <input name="precio" type="number" step="0.01" class="form-control" value="${seleccionado.precio}" required />
        </div>
        <div class="mb-3">
            <label class="form-label">Cantidad en stock</label>
            <input name="cantidad_stock" type="number" min="0" class="form-control" value="${seleccionado.cantidad}" required />
        </div>
    `;
    btnGuardarEditar.disabled = false;
});

// Al abrir modal eliminar
document.getElementById('modalEliminar').addEventListener('show.bs.modal', () => {
    if (!seleccionado) return;
    formEliminar.action = `/inventario/eliminar/${seleccionado.id}/`;
    eliminarBody.innerHTML = `<p>¿Seguro que deseas eliminar <strong>${seleccionado.nombre}</strong>? Esta acción no se puede deshacer.</p>`;
    btnConfirmarEliminar.disabled = false;
});