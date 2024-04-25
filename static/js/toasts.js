;(function() {
    const toastEl = document.getElementById("toast")    
    const toastBody = document.getElementById("toast-body")    
    const toast = new bootstrap.Toast(toastEl)

    htmx.on("showMessage", (e) => {
        toastBody.innerText = e.detail.value
        toast.show()
    })
})()