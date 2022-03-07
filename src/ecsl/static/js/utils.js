function handleResponseErrors(status_code, success_message) {
    // Get the first digit from the status code response
    const codeFirstDigit = String(status_code)[0];
    // Initializes the toast config obj
    const toast = Swal.mixin({
        toast: true,
        position: 'top',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    });
    // Assign the icon & title for the toast obj depending on the status code
    if (codeFirstDigit == 1) {
        toast.fire({
            icon: 'info',
            title: '¡Esperando respuesta del servidor!'
        });
    } else if (codeFirstDigit == 2) {
        toast.fire({
            icon: 'success',
            title: success_message
        });
    } else if (codeFirstDigit == 3) {
        toast.fire({
            icon: 'warning',
            title: '¡El servidor ha solicitado redirigirse a otra dirección URL!'
        });
    } else if (codeFirstDigit == 4) {
        toast.fire({
            icon: 'error',
            title: '¡El servidor no pudo procesar su solicitud. Por favor, inténtelo de nuevo!'
        });
    } else if (codeFirstDigit == 5) {
        toast.fire({
            icon: 'error',
            title: '¡Error al conectar al servidor. Por favor, inténtelo mas tarde!'
        });
    }
}