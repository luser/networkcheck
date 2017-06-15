FROM tiangolo/uwsgi-nginx
RUN rm /app/main.py
RUN pip install --disable-pip-version-check web.py pysnmp
ADD static /app/static/
ADD uwsgi.ini networkcheck.py server.py signalstrength.py index.html /app/
