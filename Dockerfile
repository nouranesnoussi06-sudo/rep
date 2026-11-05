FROM python:3.14-slim
WORKDIR /app
COPY . /app
ENV OUT_DIR=/out
CMD ["./run.sh"]
