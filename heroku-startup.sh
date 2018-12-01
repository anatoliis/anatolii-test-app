#!/usr/bin/env bash
set -ex
heroku container:login
heroku container:push web
heroku container:release web
heroku logs --tail
