// Funcionalidad para la página de Cobrar Servicios

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap si existen
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Mejorar la funcionalidad de búsqueda
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        // Agregar funcionalidad de búsqueda en tiempo real (opcional)
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                // Aquí se podría agregar búsqueda AJAX si fuera necesario
                console.log('Buscando:', searchInput.value);
            }, 300);
        });
    }

    // Agregar animación suave a las filas de la tabla
    const tableRows = document.querySelectorAll('.table-servicios tbody tr');
    tableRows.forEach((row, index) => {
        row.style.opacity = '0';
        row.style.transform = 'translateY(20px)';
        setTimeout(() => {
            row.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            row.style.opacity = '1';
            row.style.transform = 'translateY(0)';
        }, index * 50);
    });

    // Mejorar la funcionalidad de los switches
    const navLinks = document.querySelectorAll('.nav-pills .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Agregar loading state
            const icon = this.querySelector('i');
            if (icon) {
                const originalClass = icon.className;
                icon.className = 'bi bi-hourglass-split';
                setTimeout(() => {
                    icon.className = originalClass;
                }, 500);
            }
        });
    });

    // Agregar funcionalidad a los botones de pagar
    const pagarButtons = document.querySelectorAll('.btn-pagar');
    pagarButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Agregar efecto visual al hacer click
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });

    // Mejorar los modales
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            // Agregar efecto de entrada suave
            const modalDialog = this.querySelector('.modal-dialog');
            modalDialog.style.transform = 'scale(0.9)';
            modalDialog.style.opacity = '0';
            setTimeout(() => {
                modalDialog.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
                modalDialog.style.transform = 'scale(1)';
                modalDialog.style.opacity = '1';
            }, 50);
        });
    });

    // Funcionalidad para copiar información al portapapeles (útil para detalles)
    const detalleItems = document.querySelectorAll('.detalle-item');
    detalleItems.forEach(item => {
        item.style.cursor = 'pointer';
        item.title = 'Click para copiar información';
        item.addEventListener('click', function() {
            const text = this.textContent;
            navigator.clipboard.writeText(text).then(function() {
                // Mostrar feedback visual
                const originalBg = item.style.backgroundColor;
                item.style.backgroundColor = '#d4edda';
                setTimeout(() => {
                    item.style.backgroundColor = originalBg;
                }, 300);
            });
        });
    });

    // Agregar funcionalidad de confirmación adicional para pagos
    const confirmarPagoButtons = document.querySelectorAll('button[type="submit"]');
    confirmarPagoButtons.forEach(button => {
        if (button.textContent.includes('Confirmar Pago')) {
            button.addEventListener('click', function(e) {
                const total = this.closest('.modal').querySelector('.total-destacado');
                if (total) {
                    const monto = total.textContent;
                    const confirmacion = confirm(`¿Está completamente seguro de procesar el pago por ${monto} en efectivo?\n\nEsta acción no se puede deshacer.`);
                    if (!confirmacion) {
                        e.preventDefault();
                        return false;
                    }
                }
            });
        }
    });

    // Funcionalidad para limpiar mensajes de alerta automáticamente
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // Cerrar automáticamente después de 5 segundos
    });

    // Agregar funcionalidad de scroll suave para los enlaces internos
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Funcionalidad para detectar cambios en el estado de la página
    window.addEventListener('beforeunload', function(e) {
        // Solo mostrar advertencia si hay formularios sin guardar
        const forms = document.querySelectorAll('form');
        let hasUnsavedChanges = false;

        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                if (input.value !== input.defaultValue) {
                    hasUnsavedChanges = true;
                }
            });
        });

        if (hasUnsavedChanges) {
            e.preventDefault();
            e.returnValue = '¿Estás seguro de salir? Los cambios no guardados se perderán.';
            return e.returnValue;
        }
    });

    console.log('✅ JavaScript de Cobrar Servicios cargado correctamente');
});