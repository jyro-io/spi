#!/usr/bin/env bash

# semantic versioning
version=$(cat VERSION)

git tag ${version} --force && \
git push --tags --force