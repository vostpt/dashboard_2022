FROM python:latest
RUN apt update
RUN apt install -y libgdal-dev 
COPY . /opt/app
WORKDIR /opt/app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8082
CMD ["python3", "app.py"]
