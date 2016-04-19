#!/bin/sh

dir=$(dirname $0)
nohup python ${dir}/server.py > ${dir}/server.log 2>&1 &
