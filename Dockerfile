FROM python:3.12

WORKDIR /makss

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]