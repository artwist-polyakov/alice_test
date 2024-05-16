function reloadNginx(r) {
    var sys = require('sys');
    sys.exec('/usr/sbin/nginx -s reload', function(stdout, stderr) {
        r.return(200, "Nginx reloaded successfully");
    });
}

export default {reloadNginx};