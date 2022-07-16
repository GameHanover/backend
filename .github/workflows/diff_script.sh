#!/bin/bash

DIFF=$(git diff HEAD^ HEAD ${GITHUB_WORKSPACE}/VERSION)
if [[ -z "$DIFF" ]]; then
  IFS='.'; read -r -a array <<< "$(cat ${GITHUB_WORKSPACE}/VERSION)"
  CNT="${array[1]}"
  ((CNT++))
  echo "${array[0]}.${CNT}.0" >${GITHUB_WORKSPACE}/VERSION
  echo 1
else
  echo 0
fi
