FROM python:3.10.6


WORKDIR /home/dem/solution/Documents/docker
# RUN mkdir app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /home/dem/solution/Documents/docker/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /home/dem/solution/Documents/docker/requirements.txt

COPY . /home/dem/solution/Documents/docker

CMD ["uvicorn", "app.main:app", "--host", "127.0.0.0", "--port", "8000"]