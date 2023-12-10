FROM python:slim-bullseye
LABEL authors="williamdavidsuarezarevalo"
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY .env .
CMD ["streamlit","run","app.py"]
