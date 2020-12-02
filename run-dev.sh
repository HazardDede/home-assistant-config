#!/bin/bash

mv packages/hubs/roomba.yaml packages/hubs/roomba.yaml.ignore
mv packages/logic/vacuum_pumbaa.yaml packages/logic/vacuum_pumbaa.ignore
# mv packages/hubs/homeconnect.yaml packages/hubs/homeconnect.yaml.ignore

docker-compose -f ./.dev/docker-compose.yaml up hass $@
docker-compose -f ./.dev/docker-compose.yaml stop hass $@
docker-compose -f ./.dev/docker-compose.yaml down

mv packages/logic/vacuum_pumbaa.ignore packages/logic/vacuum_pumbaa.yaml
mv packages/hubs/roomba.yaml.ignore packages/hubs/roomba.yaml
# mv packages/hubs/homeconnect.yaml.ignore packages/hubs/homeconnect.yaml