FROM python:3.5-slim
MAINTAINER wikitolearn sysadmin@wikitolearn.org

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

WORKDIR /latex2svg

RUN apt-get update && apt-get upgrade

RUN apt-get install -y texlive-base
#pdflatex
RUN apt-get install -y texlive-latex-base
#pdfcrop
RUN apt-get install -y texlive-extra-utils
RUN apt-get install -y pdf2svg

ADD requirements.txt . 
RUN pip install -r requirements.txt

ADD . .

ENTRYPOINT ["python"]
CMD ["app.py"]