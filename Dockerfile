FROM tiangolo/uwsgi-nginx:python3.11
RUN apt-get update && apt-get install -y iputils-ping
RUN rm /app/main.py
RUN pip install --disable-pip-version-check web.py pysnmp
ADD static /app/static/
ADD uwsgi.ini networkcheck.py server.py signalstrength.py index.html /app/
ADD config.py /app/
