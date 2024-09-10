FROM python:3.9.19

COPY . /oneforall
WORKDIR /oneforall
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "subdomain_worker.py", "|| exit 1"]