#!/bin/bash
while true; do
  ab -n 10000 -c 100 http://192.168.49.2:31522/docs
done
