"use strict";

var searchBox, entries, tdNotFound;

searchBox = window.document.getElementById('searchbox');
entries = window.document.getElementsByClassName('entries');
tdNotFound = window.document.getElementById('notfound');

function onType(element) {
    var input, result, found;
    input = element.value.toLowerCase();
    found = false;

    for (var i=0; i<entries.length; i++) {
        var login, userName;
        login = '@' + entries[i].getAttribute('id').toLowerCase();
        userName = entries[i].getElementsByClassName('username')[0].innerHTML.toLowerCase();
        if (login.indexOf(input) > -1 || userName.indexOf(input) > -1) {
            entries[i].style.display = 'table-row';
            found = true;
        } else {
            entries[i].style.display = 'none';
        }
    }
    if (!found) { tdNotFound.style.display = 'table-cell'; }
    else { tdNotFound.style.display = 'none'; }
}
