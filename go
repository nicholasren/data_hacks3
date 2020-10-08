#!/bin/bash 

action=$1

if [[ "$action" = "" ]];then
  echo "Usage: $0 [build|publish]"
fi

if [[ "$action" = "build" ]];then
  rm -rf dist
  python setup.py sdist
fi

if [[ "$action" = "publish" ]];then
   twine upload dist/*
fi
