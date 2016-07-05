#!/bin/sh
set -e

virtualenv ./virtualenv
./virtualenv/bin/pip install uwsgi web.py

cat > networkcheck.conf <<EOF
description "uWSGI instance to serve networkcheck"

start on runlevel [2345]
stop on runlevel [!2345]

setuid www-data
setgid www-data

script
    cd $(pwd)
    . virtualenv/bin/activate
    uwsgi --ini networkcheck.ini --check-static ./static
end script
EOF

sudo cp networkcheck.conf /etc/init/

cat > networkcheck <<EOF
server {
    listen 10000;
    server_name 192.168.1.10;

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:$(pwd)/networkcheck.sock;
    }
}
EOF

sudo cp networkcheck /etc/nginx/sites-available/
test -L /etc/nginx/sites-enabled/networkcheck || sudo ln -s /etc/nginx/sites-available/networkcheck /etc/nginx/sites-enabled

echo "Run 'sudo start networkcheck' to start the service."
echo "Run 'sudo service nginx restart' to restart nginx."
