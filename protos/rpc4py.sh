#! /usr/bin/env bash


python3 -m grpc_tools.protoc -I. --python_out=../www/src/ --grpc_python_out=../www/src/ spider.proto
python3 -m grpc_tools.protoc -I. --python_out=../spider/src/ --grpc_python_out=../spider/src/ spider.proto
