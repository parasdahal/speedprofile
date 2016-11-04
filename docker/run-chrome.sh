#!/bin/bash
docker run -v $(pwd)/output:/output ccarpita/speedprofile-chrome "$@"
