FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
