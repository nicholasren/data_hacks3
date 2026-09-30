#!/bin/bash 

action=$1

case $action in
  build)
    rm -rf dist
    uv build
  ;;
  publish)
    uvx twine upload dist/*
  ;;
  test_publish)
     uvx twine upload --repository testpypi dist/*
  ;;
  *)
    echo "Usage: $0 [build|test_publish|publish]"
    exit
esac
