#!/bin/bash 

action=$1

case $action in
  build)
    rm -rf dist
    python setup.py sdist
  ;;
  publish)
    twine upload dist/*
  ;;
  test_publish)
     twine upload --repository testpypi dist/*
  ;;
  *)
    echo "Usage: $0 [build|test_publish|publish]"
    exit
esac
