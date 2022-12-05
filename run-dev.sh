#!/bin/bash

docker-compose -f ./.dev/docker-compose.yaml up hass $@
docker-compose -f ./.dev/docker-compose.yaml stop hass $@
docker-compose -f ./.dev/docker-compose.yaml down
