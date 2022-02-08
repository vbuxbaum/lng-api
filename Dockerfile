FROM python:3.9

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./ ./

ENTRYPOINT ["gunicorn","--chdir","/app","app:app","-w 1","--threads","1","-b","0.0.0.0:8000"]
