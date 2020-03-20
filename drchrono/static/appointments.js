document.addEventListener("DOMContentLoaded", documentReady);

let app = {};

function documentReady() {
    $('#cancel-button').on('click', warnCancel)
}

function warnCancel(e) {
    if (!confirm("Are you sure you want to cancel this appointment?")) {
        e.preventDefault()
    }
}