"use strict";

function checkTable() {
    var table = window.document.getElementsByClassName('nodes')[0];
    if (!table) return;
    if (table.getElementsByTagName('tr').length <= 1) {
        table = table.parentElement;
        var container = table.parentElement;
        fadeOut(table, false, true);
        setTimeout(function() {
            container.appendChild(
                createElement('div',
                    'alert alert-warning',
                    {'role': 'alert'},
                    'This user doesn\'t have any connections yet.'))
        }, 250);
    }
}

function sendAction(data) {

    return response.status === 'ok';
}

function buttonAction(targetUser, action, button, row) {
    return;
    switch (action) {
        case 'remove':

            break;
        case 'accept':
            var data = {'action': 'conn_accept', 'target': targetUser};
            ajax.put('/ajax?data_type=json', JSON.stringify(data), function (response) {
                response = JSON.parse(response['body']);
                console.log(response);
                var parent = button.parentElement;
                parent.removeChild(button);
                parent.appendChild(createElement('span', 'label label-success', null, 'Accepted'));
                var connectionsSpan = window.document.getElementById('connections');
                var connectionsCount = parseInt(connectionsSpan.innerHTML);
                connectionsSpan.innerHTML = connectionsCount + 1;
            });
            break;
        case 'view':
            window.location = "/profile/" + targetUser;
    }
}
