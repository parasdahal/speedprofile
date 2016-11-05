# Speedprofile
Create HAR and performance data headlessly with Chrome and Firefox using Browsermob-Proxy

This tool helps you to capture HTTP Archive (HAR) and additional performance data using Navigation Timing API from either Chrome or Firefox headlessly.

### Setup (Manual)

1. Install xvfb

   sudo apt-get install -y xvfb
   
2. Download Browsermob-proxy

   wget https://github.com/downloads/lightbody/browsermob-proxy/browsermob-proxy-2.0-beta-6-bin.zip  
   unzip browsermob-proxy-2.0-beta-6-bin.zip

3. Download selenium-server

   wget http://selenium-release.storage.googleapis.com/2.41/selenium-server-standalone-2.41.0.jar
 
4. Start selenium-server

   java /usr/bin/java -jar selenium-server.jar >> ./log/selenium.$(date +"%Y%d%m").log 2>&1&
 
5. Download chrome driver
   
   wget -N http://chromedriver.storage.googleapis.com/2.10/chromedriver_linux64.zip  
   unzip chromedriver_linux64.zip  
   chmod +x chromedriver

6. Install Python Dependencies for browsermob-proxy, selenium and xvfb

   sudo apt-get install python-pip  
   sudo pip install selenium browsermob-proxy xvfbwrapper --upgrade  

###Usage

python speedprofile.py --url [url to test] --browser [chrome/fireox] --path [path to save output files]


### Dockerized Setup and Usage (Chrome Only)

1. Install Docker -- https://www.docker.com/

2. Run the build-chrome script to create a docker image tagged `speedprofile-chrome`

```sh
./docker/build-chrome.sh

# To test your local image, run:
docker run -v $(pwd)/output:/output speedprofile-chrome <url>

# Performance/HAR files will be generated in the local "output" folder.
```

3. Quickstart: If you want to skip the build (2), you can simply run the public docker image with the included wrapper script:

```
./docker/run-chrome.sh <url>
```
