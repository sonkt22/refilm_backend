FROM python

COPY . /web_review/

WORKDIR /web_review/

ENTRYPOINT ["python3", "/web_review/manage.py"]
