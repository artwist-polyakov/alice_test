FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5555

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5555"]