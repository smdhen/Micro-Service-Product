FROM python:3-alpine3.10
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirement.txt
CMD python ./Product.py
