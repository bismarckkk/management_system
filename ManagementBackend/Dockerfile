FROM python:3.6-alpine
MAINTAINER bismarckkk zuoqingyu@nuaa.edu.cn
WORKDIR /code
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
RUN apk update
RUN apk add --no-cache gcc musl-dev linux-headers g++ jpeg-dev zlib-dev libxslt-dev
COPY requirements.txt requirements.txt
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
COPY . .
CMD ["python3", "/code/app.py", "-s", "/code/config/settings.json"]
