FROM python:3.12-slim

WORKDIR /goods_in_stock
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
