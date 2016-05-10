#!/usr/bin/env bash

docker run -it -p 8080:9080 -v ~/PycharmProjects/time_tracker/chat:/data golang /data/server