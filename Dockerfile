FROM python:3.10
RUN pip install --upgrade pip
RUN mkdir /app

COPY ./requirements.txt /app

COPY ./CodeChallangeProject /app
WORKDIR /app/
RUN git clone https://github.com/vishnubob/wait-for-it.git

RUN pip install -r requirements.txt
