; (function () {
    const modalEl = document.getElementById("modal");
    if (!modalEl) return;

    const modal = new bootstrap.Modal(modalEl);

    // Tooltip initialization after HTMX loads content
    htmx.on("htmx:load", () => {
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));
    });

    // Show modal if the #dialog container gets new content
    htmx.on("htmx:afterSwap", (e) => {
        if (e.detail.target.id === "dialog") {
            console.log("HTMX:afterSwap → showing modal");
            modal.show();
        }
    });

    // Blur focused element before modal is hidden (cancel or ESC) to prevent aria-hidden warning
    modalEl.addEventListener("hide.bs.modal", () => {
        const activeEl = document.activeElement;
        if (modalEl.contains(activeEl)) {
            activeEl.blur();
        }
    });

    // Hide modal on custom 'on-success' trigger from server
    htmx.on("on-success", () => {
        console.log("HTMX:on-success → hiding modal");
        const activeEl = document.activeElement;
        if (modalEl.contains(activeEl)) {
            activeEl.blur();
        }
        modal.hide();
    });

    // Cleanup modal content once it's hidden
    htmx.on("hidden.bs.modal", (e) => {
        if (e.target.id === "modal") {
            document.getElementById("dialog").innerHTML = "";
        }
    });

    // Disable submit button if form has errors
    htmx.on("frm-has-errors", () => {
        console.log("HTMX:form has errors → disable submit");
        const btn = document.getElementById("btn-id-save");
        if (btn) btn.disabled = true;
    });

    // Enable submit button if form is valid
    htmx.on("frm-no-errors", () => {
        console.log("HTMX:form has no errors → enable submit");
        const btn = document.getElementById("btn-id-save");
        if (btn) btn.disabled = false;
    });
})();