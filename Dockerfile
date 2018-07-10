FROM python:3.7-alpine
COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt
RUN rm -rf /tmp

COPY ./YSA /app
WORKDIR /app

EXPOSE 5000
CMD ["python", "api.py"]
