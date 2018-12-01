"use_strict";

var ajax, buttons;

ajax = new AJAX();

buttons = window.document.getElementsByTagName('button');
for (var i=0; i<buttons.length; i++) {
    buttons[i].setAttribute('onclick', 'buttonClick(this);');
}

function createElement(name, className, attributes, content) {
    var newElement;
    newElement = window.document.createElement(name);
    newElement.className = className || '';
    if (attributes) {
        for (var key in attributes) {
            newElement.setAttribute(key, attributes[key]);
        }
    }
    if (content) {
        newElement.appendChild(window.document.createTextNode(content));
    }
    return newElement;
}

function destroyChilds(parent) {
    var childs;
    childs = parent.childNodes;
    while (childs.length > 0) {
        destroyChilds(childs[0]);
        parent.removeChild(childs[0]);
    }
}

function fadeOut(element, remove, hide){
    element.style.opacity = 1;

    (function fade() {
        if ((element.style.opacity -= .1) < 0) {
            if (remove) { element.parentElement.removeChild(element); }
            if (hide) { element.style.display = "none"; }
        } else {
            requestAnimationFrame(fade);
        }
    })();
}

function fadeIn(element, display){
    if (parseFloat(element.style.opacity) !== 0) {
        element.style.opacity = 1;
        return;
    }
    element.style.opacity = 0;
    element.style.display = display || "block";

    (function fade() {
        var val = parseFloat(element.style.opacity);
        if (val < 1) {
            element.style.opacity = val + .1;
            requestAnimationFrame(fade);
        }
    })();
}

function rowClick(target) {
    var targetUser;
    targetUser = target.parentElement.getAttribute('id');
    window.location = "/profile/" + targetUser;
}

function buttonClick(button) {
    var parent, container, action, rowButton, targetUser, data;

    rowButton = button.className.indexOf('btn-row') > -1;
    parent = button.parentElement;
    container = parent.parentElement;
    targetUser = rowButton?container.getAttribute('id'):pageOwner;
    action = button.innerHTML.toLowerCase();

    if (action === 'revoke') { action = 'remove'; }

    switch (action) {
        case 'remove':
            data = {'action': 'conn_remove', 'target': targetUser};
            ajax.put('/ajax?data_type=json', JSON.stringify(data), function (response) {
                response = JSON.parse(response['body']);
                if (response.status !== 'ok') { console.log(response.status); return; }
                if (currentPage === 'search') {
                    button.className = button.className.replace(/(btn-danger|btn-warning)/, 'btn-success');
                    button.innerHTML = 'Send';
                    var statusTd = container.getElementsByClassName('col-status')[0];
                    destroyChilds(statusTd);
                    statusTd.appendChild(createElement('span', 'label label-info', null, 'None'));
                }
                else if (rowButton) {
                    if (container.getAttribute('type') === 'accepted') {
                        var connectionsSpan = window.document.getElementById('connections');
                        connectionsSpan.innerHTML = parseInt(connectionsSpan.innerHTML) - 1;
                    }
                    fadeOut(container, true);
                    checkTable();
                } else if (currentPage === 'profile') {
                    fadeOut(parent, false);
                    setTimeout(function() {
                        destroyChilds(parent);
                        parent.innerHTML = 'You can send invitation to this user. ';
                        parent.className = parent.className.replace(/alert-(info|success)/, 'alert-warning');
                        var newButton = createElement(
                            'button',
                            'btn btn-xs btn-success',
                            {'type':'button', 'onclick': 'buttonClick(this);'},
                            'Send');
                        parent.appendChild(newButton);
                        fadeIn(parent, 'block')
                    }, 200);
                    checkTable();
                }
            });
            break;

        case 'accept':
            data = {'action': 'conn_create', 'target': targetUser};
            ajax.put('/ajax?data_type=json', JSON.stringify(data), function (response) {
                response = JSON.parse(response['body']);
                if (response.status !== 'ok') { console.log(response.status); return; }
                if (currentPage === 'search') {
                    parent.removeChild(button);
                    parent.appendChild(createElement('span', 'label label-success', null, 'Accepted'));
                }
                else if (rowButton) {
                    parent.removeChild(button);
                    parent.appendChild(createElement('span', 'label label-success', null, 'Accepted'));
                    var connectionsSpan = window.document.getElementById('connections');
                    connectionsSpan.innerHTML = parseInt(connectionsSpan.innerHTML) + 1;
                } else {
                    fadeOut(parent, false);
                    setTimeout(function() {
                        destroyChilds(parent);
                        parent.innerHTML = 'You are connected to this user. ';
                        parent.className = parent.className.replace('alert-info', 'alert-success');
                        var newButton = createElement(
                            'button',
                            'btn btn-xs btn-danger',
                            {'type':'button', 'onclick': 'buttonClick(this);'},
                            'Remove');
                        parent.appendChild(newButton);
                        fadeIn(parent, 'block')
                    }, 200);
                }
            });
            break;

        case 'send':
            data = {'action': 'conn_create', 'target': targetUser};
            ajax.put('/ajax?data_type=json', JSON.stringify(data), function (response) {
                response = JSON.parse(response.body);
                if (response.status !== 'ok') { console.log(response.status); return; }
                if (currentPage === 'profile') {
                    fadeOut(parent, false);
                    setTimeout(function () {
                        destroyChilds(parent);
                        parent.innerHTML = 'You\'ve sent an invitation to this user. ';
                        parent.className = parent.className.replace('alert-info', 'alert-warning');
                        var newButton = createElement(
                            'button',
                            'btn btn-xs btn-danger',
                            {'type': 'button', 'onclick': 'buttonClick(this);'},
                            'Revoke');
                        parent.appendChild(newButton);
                        fadeIn(parent, 'block')
                    }, 200);
                } else {
                    button.className = button.className.replace('btn-success', 'btn-warning');
                    button.innerHTML = 'Revoke';
                    var statusTd = container.getElementsByClassName('col-status')[0];
                    destroyChilds(statusTd);
                    statusTd.appendChild(createElement('span', 'label label-default', null, 'Sent'));
                }
            });
            break;

        case 'remove user':
            data = {'action': 'user_remove', 'target': targetUser};
            ajax.put('/ajax?data_type=json', JSON.stringify(data), function (response) {
                response = JSON.parse(response['body']);
                if (response.status !== 'ok') { console.log(response.status); return; }
                var quantitySpan = window.document.getElementById('quantity');
                quantitySpan.innerHTML = parseInt(quantitySpan.innerHTML) - 1;
                fadeOut(container, true);
            });
            break;

        case 'view':
            window.location = "/profile/" + targetUser;
    }
}
