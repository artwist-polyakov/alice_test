function reloadNginx(r) {
    r.subrequest('/internal/reload', {}, function(reply) {
        r.return(reply.status, reply.responseBody);
    });
}
