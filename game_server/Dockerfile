FROM python:3.11
WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install jq sysstat
RUN apt-get update
RUN apt-get install -y p7zip atop
COPY . .

