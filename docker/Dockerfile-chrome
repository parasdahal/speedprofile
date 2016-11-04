FROM ubuntu:trusty
MAINTAINER Chris Carpita <ccarpita@gmail.com>

# Install Chrome debian sources
RUN apt-get update \
    && apt-get install -y wget \
    && apt-get clean \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Install pptitude and python dependencies
RUN apt-get update \
    && apt-get install -y xvfb python-pip unzip openjdk-7-jre google-chrome-stable \
    && apt-get clean \
    && pip install selenium browsermob-proxy xvfbwrapper --upgrade

# Install direct binary dependencies
RUN wget https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.2/browsermob-proxy-2.1.2-bin.zip \
    && unzip browsermob-proxy-2.1.2-bin.zip \
    && wget http://selenium-release.storage.googleapis.com/2.41/selenium-server-standalone-2.41.0.jar \
    && wget https://chromedriver.storage.googleapis.com/2.25/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && chmod +x chromedriver

# Add the entrypoint script to the container
COPY speedprofile.py /speedprofile.py
COPY docker/entrypoint.sh /entrypoint.sh

# Start selenium server
RUN mkdir -p /log \
    && /usr/bin/java -jar selenium-server-standalone-2.41.0.jar >> /log/selenium.$(date +"%Y%d%m").log 2>&1&

# Specify entrypoint and default command
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
CMD ["http://www.google.com"]
