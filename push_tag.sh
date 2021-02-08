#!/usr/bin/env bash

# semantic versioning
version=$(cat VERSION)

git tag ${version} && \
git push --tags