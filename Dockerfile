FROM python:slim-bullseye
LABEL authors="williamdavidsuarezarevalo"
WORKDIR /usr/src/app
RUN apt-get update --yes
RIN apt-get install build-essential --yes
TUN apt-get install cmake --yes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY .env .
CMD ["streamlit","run","app.py"]
