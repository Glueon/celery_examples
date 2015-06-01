FROM python:3.4.3
RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
WORKDIR /home/user

RUN pip install eventlet celery redis

ADD . /home/user

RUN echo "#!/bin/bash\ncelery worker  --loglevel=info  -P eventlet -A $1" > /init.sh && chmod +x /init.sh
USER user

ENTRYPOINT ["celery", "worker",  "--loglevel=info",  "-P",  "eventlet", "-A"]
