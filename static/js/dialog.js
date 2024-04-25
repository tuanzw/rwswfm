; (function () {
    const modal = new bootstrap.Modal(document.getElementById("modal"))
    const modal_id_array = ["table_id_carrier", "table_id_user"]

    htmx.on("htmx:load", (e) => {
        console.log("load", e)
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
    })

    htmx.on("htmx:afterSwap", (e) => {
        console.log(e.detail.target.id)
        if (e.detail.target.id == "dialog") {
            modal.show()
        }
    })
    htmx.on("htmx:beforeSwap", (e) => {
        console.log(e)
        // if (modal_id_array.includes(e.detail.target.id)) {
        //     modal.hide()
        // }
    })
    htmx.on("hidden.bs.modal", () => {
        document.getElementById("dialog").innerHTML = ""
    })
    htmx.on("on-success", () => {
        console.log("on-success")
        modal.hide()
    })
    htmx.on("frm-has-errors", () => {
        console.log("frm-has-errors")
        document.getElementById("btn-id-save").disabled = true
    })
    htmx.on("frm-no-errors", () => {
        console.log("frm-no-errors")
        document.getElementById("btn-id-save").disabled = false
    })
})()