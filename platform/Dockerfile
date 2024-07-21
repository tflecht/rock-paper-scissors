FROM python:3.10
WORKDIR /src
COPY web_server .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install jq sysstat
WORKDIR /src
EXPOSE 8000

