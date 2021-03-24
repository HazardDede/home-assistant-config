#!/bin/bash

mv packages/logic/vacuum_pumbaa.yaml packages/logic/vacuum_pumbaa.ignore

docker-compose -f ./.dev/docker-compose.yaml up hass $@
docker-compose -f ./.dev/docker-compose.yaml stop hass $@
docker-compose -f ./.dev/docker-compose.yaml down

mv packages/logic/vacuum_pumbaa.ignore packages/logic/vacuum_pumbaa.yaml
