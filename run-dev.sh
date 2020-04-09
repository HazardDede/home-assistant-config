#!/bin/bash

mv packages/_system/guest_wifi.yaml packages/_system/guest_wifi.yaml.ignore
mv packages/vacuum/pumbaa.yaml packages/vacuum/pumbaa.yaml.ignore

docker-compose -f ./.dev/docker-compose.yaml up hass $@
docker-compose -f ./.dev/docker-compose.yaml stop hass $@
docker-compose -f ./.dev/docker-compose.yaml down

mv packages/_system/guest_wifi.yaml.ignore packages/_system/guest_wifi.yaml
mv packages/vacuum/pumbaa.yaml.ignore packages/vacuum/pumbaa.yaml