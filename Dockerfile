from ubuntu:16.04
MAINTAINER rabbit
RUN apt-get update
RUN apt-get install -y build-essential unzip wget libssl-dev libffi-dev curl
RUN apt-get install -y python python-dev libpq-dev
RUN apt-get install -y postgresql postgresql-contrib
RUN apt-get install -y postgresql-server-dev-all
RUN apt-get install -y libjpeg-dev
RUN apt-get install -y libtiff5-dev
RUN apt-get install -y libjpeg8-dev
RUN apt-get install -y zlib1g-dev
RUN apt-get install -y libfreetype6-dev
RUN apt-get update
RUN apt-get install -y liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install --upgrade pip
RUN apt-get install -y vim
RUN apt-get install -y git
RUN apt-get install -y nginx
RUN pip install uwsgi

ADD /adminPanel /adminPanel/
RUN pip install --upgrade  -r /adminPanel/requirements.txt
EXPOSE 8001


# Setting the permissions to the files
RUN chmod 750 /adminPanel/clearLogs.sh

# Settings for Crontab
RUN mkdir /var/log/scripts/
RUN chmod 777 /var/log/scripts/

CMD env > /root/env.txt
ADD /adminPanel/crontab /etc/cron.d/cron
RUN chmod 0644 /etc/cron.d/cron
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log


