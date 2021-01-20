FROM debian:buster

LABEL maintainer="informatique@agepoly.ch"
LABEL description="L'intranet de l'AGEPoly. See line for configuration."
LABEL version="2.3.1"

RUN echo "locales locales/locales_to_be_generated multiselect en_US.UTF-8 UTF-8" | debconf-set-selections

RUN apt-get update
RUN apt-get install -y locales
RUN locale-gen en_US.UTF-8

ENV DEBIAN_FRONTEND noninteractive
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US
ENV LC_ALL en_US.UTF-8

ENV RABBITMQ_NODENAME rabbit@localhost

# install debian packets
RUN apt-get update
RUN apt-get install -y \
    apache2 \
    git \
    libapache2-mod-wsgi-py3 \
    libapache2-mod-xsendfile \
    libffi-dev \
    libjpeg-dev \
    librsvg2-2 \
    libxml2-dev \
    libldap2-dev \ 
    libsasl2-dev \
    libxslt1-dev \
    libz-dev \
    memcached \
    python3 \
    python3-crypto \
    python3-dev \
    python3-pip \
    supervisor \
    default-mysql-client \
    rabbitmq-server \
    sqlite3 \
    default-libmysqlclient-dev \
    erlang \
    libmagickwand-dev \
    librsvg2-bin \
    s6

# setup apache
RUN a2dissite 000-default
COPY ./DockerDeployment/truffe2.apache /etc/apache2/sites-available/truffe2.conf
RUN a2ensite truffe2

# setup cron
COPY ./DockerDeployment/truffe2.crontab /etc/cron.d/truffe2
RUN chmod 0600 /etc/cron.d/truffe2

# install s6 (process manager)
COPY ./DockerDeployment/s6 /lib/s6

# install app dependency
COPY ./truffe2/data/pip-reqs.txt  /var/www/truffe2/data/pip-reqs.txt 
RUN pip3 install -r /var/www/truffe2/data/pip-reqs.txt && pip3 install mysqlclient && pip3 install pyyaml

# Non local clone
# ARG truffe_branch=agep/prod
# RUN git clone --single-branch  --branch $truffe_branch https://deploy+truffe2+gitlab-image:y33PxTX64NYCsmS3fw6t@gitlab.com/agepoly/it/dev/truffe2.git /tmp/truffe2-git 
RUN apt-get purge -y git
RUN apt-get clean

# Local copy/clone
COPY ./truffe2 /tmp/truffe2-git/truffe2

WORKDIR /tmp/truffe2-git

RUN cp -r /tmp/truffe2-git/truffe2 -t /var/www/

WORKDIR /var/www/truffe2
RUN rm -fr /tmp/truffe2-git

# add docker suited settings
COPY ./DockerDeployment/settingsLocal.py /var/www/truffe2/app/settingsLocal.py

# test settings (mount a config file and override the env var in production)
COPY ./DockerDeployment/config.example /var/www/truffe2/app/config-test.yaml
ENV APP_CONFIG=/var/www/truffe2/app/config-test.yaml

# log file / dir creation
RUN    mkdir -p /var/log/truffe2 && touch /var/log/truffe2/django.log 2 && touch /var/log/truffe2/cron.log && chown -R www-data:www-data /var/log/truffe2 \
    && mkdir -p /var/log/celery && touch /var/log/celery/celery.log && chown -R www-data:www-data /var/log/celery

# static assets
RUN python3 /var/www/truffe2/manage.py collectstatic --noinput


# Setup demo (overidded at startup if connfig file change)
RUN chown -R www-data:www-data /var/www/
RUN python3 /var/www/truffe2/manage.py migrate --noinput
RUN mkdir -p /var/www/truffe2/media/uploads/_generic/{Logo,Subvention,Withdrawal,ExpenseClaim,CashBook,Invoice,ProviderInvoice}
RUN python3 /var/www/truffe2/manage.py update_index
RUN echo 'from main.test_data import setup_testing_all_data; setup_testing_all_data()' | DISABLE_HAYSTACK=True python3 manage.py shell

# make sure www-data own the app file
RUN chown -R www-data:www-data /var/www/

VOLUME /var/www/truffe2/media/
EXPOSE 80

CMD "/lib/s6/init"

