#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
docker build "$DIR/../" -f "$DIR/Dockerfile-chrome" -t speedprofile-chrome
