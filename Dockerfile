FROM python:3.4.3
RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
WORKDIR /home/user

RUN pip install eventlet celery redis

ADD . /home/user

USER user

ENTRYPOINT ["celery", "worker",  "--loglevel=info",  "-P",  "eventlet", "-A"]
