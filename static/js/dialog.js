; (function () {
    const modalEl = document.getElementById("modal");
    if (!modalEl) return;

    const modal = new bootstrap.Modal(modalEl);

    // ==================== Select2 Functions ====================
    const initSelect2 = () => {
        const selects = modalEl.querySelectorAll("select:not(.select2-hidden-accessible)");

        selects.forEach(select => {
            $(select).select2({
                dropdownParent: $(modalEl),
                theme: "classic",
                width: "100%"
            });
        });
    };

    const cleanupSelect2 = () => {
        const activeSelects = modalEl.querySelectorAll("select.select2-hidden-accessible");

        activeSelects.forEach(select => {
            const $select = $(select);
            if ($select.data('select2')) {
                $select.select2('destroy');
            }

            // Let vanilla JS handle attribute and data cleanup cleanly
            select.classList.remove("select2-hidden-accessible");
            select.removeAttribute("data-select2-id");
            delete select.dataset.select2Id;
        });

        // Scoped DOM cleanup
        modalEl.querySelectorAll(".select2-container").forEach(el => el.remove());
        document.querySelectorAll("[data-select2-id]").forEach(el => el.removeAttribute("data-select2-id"));
    };

    // ==================== HTMX & Bootstrap Events ====================

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
            // Initialize Select2 after content is swapped
            initSelect2();
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
            cleanupSelect2();
            const dialog = document.getElementById("dialog");
            if (dialog) {
                dialog.innerHTML = "";
            }
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