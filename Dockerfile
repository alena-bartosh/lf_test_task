FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY templates/ ./templates
COPY tests/ ./tests
COPY queries.tsv .

CMD ["python", "main.py"]
