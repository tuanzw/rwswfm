$("#modal").on("shown.bs.modal", function (e) {
    console.log(e)
    $(this).find("select").each(function () {
        const $p = $(this).parent();
        $(this).select2({
            dropdownParent: $p
        });
    });
});