FROM python:3.10
LABEL maintainer="Aswin Kumar, aswin2kumarforme@gmail.com   "
WORKDIR /app
ADD . /app
COPY Requirements.txt /app
RUN python3 -m pip install -r Requirements.txt
ENV FLASK_APP=app.py
EXPOSE 5000
CMD flask run --host 0.0.0.0 --port 5000