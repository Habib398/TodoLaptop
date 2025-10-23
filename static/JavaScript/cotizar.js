// Variables globales
let productosAgregados = [];
const precioServicio = parseFloat("{{ servicio.costo|floatformat:2 }}");

// Referencias a elementos DOM
const selectProducto = document.getElementById('select_producto');
const cantidadProducto = document.getElementById('cantidad_producto');
const btnAgregarProducto = document.getElementById('btn_agregar_producto');
const productosAgregadosDiv = document.getElementById('productos_agregados');
const precioProductosSpan = document.getElementById('precio_productos');
const precioTotalSpan = document.getElementById('precio_total');
const productosJsonInput = document.getElementById('productos_json');
const formCotizar = document.getElementById('formCotizar');

// Función para actualizar el display de productos
function actualizarProductosDisplay() {
    if (productosAgregados.length === 0) {
        productosAgregadosDiv.innerHTML = '<p class="text-muted text-center">No hay productos agregados</p>';
    } else {
        let html = '';
        productosAgregados.forEach((item, index) => {
            const subtotal = item.precio * item.cantidad;
            html += `
                <div class="producto-item" data-index="${index}">
                    <div>
                        <strong>${item.nombre}</strong><br>
                        <small class="text-muted">$${item.precio.toFixed(2)} x ${item.cantidad} unidades</small>
                    </div>
                    <div class="d-flex align-items-center">
                        <span class="precio-display me-3">$${subtotal.toFixed(2)}</span>
                        <button type="button" class="btn btn-sm btn-outline-danger" onclick="eliminarProducto(${index})">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
            `;
        });
        productosAgregadosDiv.innerHTML = html;
    }
}

// Función para calcular totales
function calcularTotales() {
    const totalProductos = productosAgregados.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    const totalGeneral = precioServicio + totalProductos;

    precioProductosSpan.textContent = `$${totalProductos.toFixed(2)}`;
    precioTotalSpan.textContent = `$${totalGeneral.toFixed(2)}`;

    // Actualizar el campo hidden con los productos en JSON
    productosJsonInput.value = JSON.stringify(productosAgregados.map(item => ({
        producto_id: item.id,
        cantidad: item.cantidad
    })));
}

// Función para agregar producto
function agregarProducto() {
    const selectOption = selectProducto.selectedOptions[0];
    if (!selectOption || !selectOption.value) {
        alert('Por favor selecciona un producto');
        return;
    }

    const cantidad = parseInt(cantidadProducto.value);
    const stock = parseInt(selectOption.dataset.stock);

    if (cantidad <= 0) {
        alert('La cantidad debe ser mayor a 0');
        return;
    }

    if (cantidad > stock) {
        alert(`No hay suficiente stock. Disponible: ${stock}`);
        return;
    }

    const productoId = selectOption.value;
    const existingIndex = productosAgregados.findIndex(item => item.id === productoId);

    if (existingIndex >= 0) {
        // Actualizar cantidad si ya existe
        const nuevaCantidad = productosAgregados[existingIndex].cantidad + cantidad;
        if (nuevaCantidad > stock) {
            alert(`No hay suficiente stock. Disponible: ${stock}, ya tienes: ${productosAgregados[existingIndex].cantidad}`);
            return;
        }
        productosAgregados[existingIndex].cantidad = nuevaCantidad;
    } else {
        // Agregar nuevo producto
        productosAgregados.push({
            id: productoId,
            nombre: selectOption.dataset.nombre,
            precio: parseFloat(selectOption.dataset.precio),
            cantidad: cantidad
        });
    }

    // Limpiar form
    selectProducto.value = '';
    cantidadProducto.value = '1';

    // Actualizar displays
    actualizarProductosDisplay();
    calcularTotales();
}

// Función para eliminar producto
function eliminarProducto(index) {
    productosAgregados.splice(index, 1);
    actualizarProductosDisplay();
    calcularTotales();
}

// Event listeners
btnAgregarProducto.addEventListener('click', agregarProducto);

// Permitir agregar con Enter en el campo cantidad
cantidadProducto.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        agregarProducto();
    }
});

// Validación del formulario
formCotizar.addEventListener('submit', function(e) {
    const nombreCliente = document.getElementById('nombre_cliente').value.trim();
    if (!nombreCliente) {
        e.preventDefault();
        alert('Por favor ingresa el nombre del cliente');
        document.getElementById('nombre_cliente').focus();
        return;
    }
});

// Inicializar display
actualizarProductosDisplay();
calcularTotales();