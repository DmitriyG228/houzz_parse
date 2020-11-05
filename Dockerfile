FROM mongo:latest


RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 python3-pip \
	cron \
	curl wget \
	supervisor \
	vim \
	mc
RUN pip3 install \
        requests \
        pymongo \
        scrapy \
        wheel \
        scrapy-rotating-proxies \
        scrapy-useragents \
        httplib2 \
        itemloaders \
        pathlib

CMD [ "useradd --create-home houzz_parse" ]

COPY project/cron/scrapper_cron /etc/cron.d/scrapper_cron
CMD [ "chmod ugo+x /etc/cron.d/" ]

COPY ./project/conf/mongod.conf /etc/

#COPY ./project/cron/scrapper_cron /var/spool/cron/crontabs/root
COPY ./main.py /home/houzz_parse/
COPY ./project /home/houzz_parse/
COPY ./project/conf/supervisor.conf /etc/supervisor/conf.d/supervisor.conf


#CMD service rsyslog start && service cron start && tail -f /var/log/syslog
CMD /usr/bin/supervisord