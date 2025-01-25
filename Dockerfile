FROM --platform=linux/amd64 python:3.11.5-slim

ADD . /opt/app/pereprava_bot/

WORKDIR /opt/app/pereprava_bot/

# Install python modules
RUN pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["bash", "/opt/app/pereprava_bot/scripts/entrypoint.sh"]