document.addEventListener("DOMContentLoaded", documentReady);

let app = {};

function documentReady() {
    $('#cancel-button').on('click', warnCancel)
    $('#complete-button').on('click', completeApp)

    $('.app-card').on('click',(function(e) {
        e.preventDefault();
        selectApp(e);
    }));

    $('#show-breaks').on('click', showBreaks)
}

function warnCancel(e) {
    if (!confirm("Are you sure you want to cancel this appointment?")) {
        e.preventDefault()
    }
}

function completeApp(e) {
    e.preventDefault()
    var appID = e.currentTarget.id
    $(`#{appID}.status p`).text().replaceWith('Complete')
}

function selectApp(e) {
    var appID = e.currentTarget.id
    var currentAppID = app.currentID
    app.currentID = appID

    for (let card of $('.app-card')) {
        $("#" + card.id).removeClass("selected")
        $("#" + card.id).addClass("unselected")
    }

    $("#" + appID).removeClass("unselected")
    $("#" + appID).addClass("selected")

    // refresh if a new app is selected
    if (appID != currentAppID) {
        // FIXME: de-hardcode base url
        window.location.href = `http://localhost:8000/appointment/${appID}`;
    }

}

function showBreaks(e) {
    // TODO: update button text [show, hide]
    // implement show/hide breaks (scheduled, unscheduled)
}