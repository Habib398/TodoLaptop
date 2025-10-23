let carrito = [];

function agregarAlCarrito(id, nombre, precio, stockDisponible) {
    const itemExistente = carrito.find(item => item.producto_id === id);

    if (itemExistente) {
        if (itemExistente.cantidad < stockDisponible) {
            itemExistente.cantidad++;
        } else {
            alert('No hay más stock disponible de este producto');
            return;
        }
    } else {
        carrito.push({
            producto_id: id,
            nombre: nombre,
            precio: parseFloat(precio),
            cantidad: 1,
            stock_disponible: stockDisponible
        });
    }

    actualizarCarrito();
}

function actualizarCantidad(id, nuevaCantidad) {
    const item = carrito.find(item => item.producto_id === id);
    if (item) {
        if (nuevaCantidad > 0 && nuevaCantidad <= item.stock_disponible) {
            item.cantidad = nuevaCantidad;
            actualizarCarrito();
        } else if (nuevaCantidad > item.stock_disponible) {
            alert('No hay suficiente stock disponible');
        }
    }
}

function eliminarDelCarrito(id) {
    carrito = carrito.filter(item => item.producto_id !== id);
    actualizarCarrito();
}

function actualizarCarrito() {
    const carritoItems = document.getElementById('carritoItems');
    const btnCobrar = document.getElementById('btnCobrar');

    if (carrito.length === 0) {
        carritoItems.innerHTML = `
            <div class="carrito-vacio">
                <i class="bi bi-cart-x"></i>
                <p>El carrito está vacío<br>Selecciona productos para comenzar</p>
            </div>
        `;
        btnCobrar.disabled = true;
    } else {
        carritoItems.innerHTML = carrito.map(item => {
            const subtotal = item.precio * item.cantidad;
            return `
                <div class="carrito-item">
                    <div class="carrito-item-header">
                        <div style="flex: 1;">
                            <h6>${item.nombre}</h6>
                            <small class="text-muted">$${item.precio.toFixed(2)} c/u</small>
                        </div>
                        <i class="bi bi-trash btn-eliminar" onclick="eliminarDelCarrito(${item.producto_id})"></i>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="cantidad-controls">
                            <button type="button" onclick="actualizarCantidad(${item.producto_id}, ${item.cantidad - 1})">-</button>
                            <input type="number" value="${item.cantidad}" min="1" max="${item.stock_disponible}"
                                   onchange="actualizarCantidad(${item.producto_id}, parseInt(this.value))">
                            <button type="button" onclick="actualizarCantidad(${item.producto_id}, ${item.cantidad + 1})">+</button>
                        </div>
                        <strong style="color: #00B4FF;">$${subtotal.toFixed(2)}</strong>
                    </div>
                </div>
            `;
        }).join('');
        btnCobrar.disabled = false;
    }

    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    document.getElementById('subtotalDisplay').textContent = `$${total.toFixed(2)}`;
    document.getElementById('totalDisplay').textContent = `$${total.toFixed(2)}`;

    document.getElementById('carritoData').value = JSON.stringify(carrito);
}

function confirmarVenta() {
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    if (confirm(`¿Confirmar venta por $${total.toFixed(2)} en efectivo?`)) {
        document.getElementById('formVenta').submit();
    }
}

function limpiarCarrito() {
    if (carrito.length > 0 && confirm('¿Estás seguro de limpiar el carrito?')) {
        carrito = [];
        actualizarCarrito();
    }
}

// Event delegation para agregar productos al carrito
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn-agregar-producto') || e.target.closest('.btn-agregar-producto')) {
        const button = e.target.classList.contains('btn-agregar-producto') ? e.target : e.target.closest('.btn-agregar-producto');
        const productoCard = button.closest('.producto-card');
        
        const id = parseInt(productoCard.dataset.id);
        const nombre = productoCard.dataset.nombre;
        const precio = productoCard.dataset.precio;
        const stockDisponible = parseInt(productoCard.dataset.stock);
        
        agregarAlCarrito(id, nombre, precio, stockDisponible);
    }
});

// Búsqueda de productos
document.getElementById('searchInput').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const productos = document.querySelectorAll('.producto-card');

    productos.forEach(producto => {
        const nombre = producto.querySelector('h5').textContent.toLowerCase();
        if (nombre.includes(searchTerm)) {
            producto.style.display = 'block';
        } else {
            producto.style.display = 'none';
        }
    });
});