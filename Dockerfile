FROM docker.m.daocloud.io/library/python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
