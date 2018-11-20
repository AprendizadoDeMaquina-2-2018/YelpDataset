FROM python:3.5.6-slim-stretch

ENV JUPYTER_ENABLE_LAB=yes

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

ENTRYPOINT jupyter notebook --ip 0.0.0.0 --no-browser --allow-root --NotebookApp.token=''