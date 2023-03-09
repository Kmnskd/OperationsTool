FROM python:3.8.10

COPY src /usr/local/ios_testflight_upload/src

WORKDIR /usr/local/ios_testflight_upload/src

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]