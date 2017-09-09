#!/bin/bash

path="/var/log/scripts/"
find $path -name "*.log" -exec rm {} \;

