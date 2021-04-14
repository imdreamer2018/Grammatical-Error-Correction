FROM rappdw/docker-java-python:openjdk1.8.0_171-python3.6.6

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 --no-cache-dir install torch==1.3.0 -i https://mirrors.aliyun.com/pypi/simple/
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
COPY . .
CMD [ "python3", "app.py"]