FROM python:3.9

WORKDIR /app
ARG TARGET_BRANCH
ENV DEPLOYMENT=local

RUN apt-get update \
&& apt-get -y install git \
&& git clone https://github.com/toposoid/data-accessor-vald-web.git \
&& cd data-accessor-vald-web \
&& git fetch origin ${TARGET_BRANCH} \
&& git checkout ${TARGET_BRANCH} \
&& pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt \


COPY ./docker-entrypoint.sh /app/
ENTRYPOINT ["/app/docker-entrypoint.sh"]
