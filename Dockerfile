FROM python:3.9
ARG REQUIREMENTS_FILE

WORKDIR /app

COPY ./ ./
ENV VIRTUAL_ENV=/opt/venv

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m pip install --upgrade pip \
    && pip3 install -r ${REQUIREMENTS_FILE:-requirements.txt} 


ENTRYPOINT ["gunicorn","--chdir","/app","app:app","-w 1","--threads","1","-b","0.0.0.0:8000"]
