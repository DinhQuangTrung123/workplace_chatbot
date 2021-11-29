

function showSuccessNoti(msg) {
    toastr.success(msg)
}

function showWarningNoti(msg) {
    toastr.warning(msg)
}

function showErrorNoti(msg) {
    toastr.error(msg)
}


$(document).ajaxStart(function () {
    $.LoadingOverlay("show", {
        imageAutoResize: true,
        image: "../static/dist/img/loader/785.svg",
        imageColor: "#CF0C5A"
    });
});

$(document).ajaxStop(function () {
    $.LoadingOverlay("hide");
});

$(document).ajaxError(function (event, xhr, options, exc) {
    if (xhr.statusCode === 401 || xhr.statusCode === 403) {
        window.location = window.location.origin + '/login';
    }
});


