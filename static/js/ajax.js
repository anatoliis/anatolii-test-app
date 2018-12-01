var AJAX = function() {
    this.XMLHttpFactories = [
        function () {return new XMLHttpRequest()},
        function () {return new ActiveXObject("Msxml2.XMLHTTP")},
        function () {return new ActiveXObject("Msxml3.XMLHTTP")},
        function () {return new ActiveXObject("Microsoft.XMLHTTP")}
    ];
    this.createXMLHTTPObject = function() {
        var xmlhttp = false;
        for (var i=0; i < this.XMLHttpFactories.length; i++) {
            try {
                xmlhttp = this.XMLHttpFactories[i]();
            }
            catch (e) {
                continue;
            }
            break;
        }
        return xmlhttp;
    };
    this.sendXHR = function(url, method, data, uploadProgress, callback, is_file) {
        var req = this.createXMLHTTPObject();
        if (!req) {return;}
        req.open(method, url, true);

        if (data === null || data === undefined) {data = {};}

        req.onreadystatechange = function() {
            if (req.readyState != 4) return;
            if (req.status != 200 && req.status != 304) {return;}
            if (callback) {
                if (req.response) {
                    var json = JSON.parse(req.response);
                    callback(json);
                } else {
                    callback(null);
                }
            }
        };
        if (req.readyState == 4){return;}
        req.send(data);
    };
};
AJAX.prototype.get = function(url, data, callback) {
    this.sendXHR(url, "GET", data, null, callback, false);
};
AJAX.prototype.post = function(url, data, callback) {
    this.sendXHR(url, "POST", data, null, callback, false);
};
AJAX.prototype.put = function(url, data, callback) {
    this.sendXHR(url, "PUT", data, null, callback, false);
};
AJAX.prototype.delete = function(url, data, callback) {
    this.sendXHR(url, "DELETE", data, null, callback, false);
};

