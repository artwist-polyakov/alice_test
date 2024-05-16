export function reloadNginx(r) {
    r.return(200, "Reloading Nginx...");

    // Используем exec для выполнения команды перезагрузки
    r.variables.exec("/usr/sbin/nginx -s reload");
}
