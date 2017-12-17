#!/bin/bash
raspivid -w 640 -h 480 -fps 15 -o - -t 0 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8090}' :demux=h264
