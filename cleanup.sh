#!/bin/sh
ps aux | grep python | grep pibot | awk '{print $2}' | xargs sudo kill -9
