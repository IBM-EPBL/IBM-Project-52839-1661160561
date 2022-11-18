FROM python:3.10
LABEL maintainer="Aswin Kumar, aswin2kumarforme@gmail.com   "
WORKDIR /app
ADD . /app
COPY requirements.txt /app
RUN python3 -m pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]