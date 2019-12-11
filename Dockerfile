FROM python:3.8-slim

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

RUN useradd  -d /app leanda && \
    chmod +x leanda.py && \
    mkdir -p leanda-sync && \ 
    chown leanda -R /app

# RUN useradd  -d /home/leanda leanda && \
#     mkdir -p /home/leanda/.leanda && \
#     chmod +x leanda.py && \
#     mkdir /sandbox && \ 
#     chown leanda /sandbox && \ 
#     chown leanda -R /home/leanda
USER leanda

