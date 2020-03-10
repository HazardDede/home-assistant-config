#!/bin/bash

mv packages/_system/guest_wifi.yaml packages/_system/guest_wifi.yaml.ignore
mv packages/devices/pumbaa.yaml packages/devices/pumbaa.yaml.ignore

docker-compose -f ./.dev/docker-compose.yaml up hass $@
docker-compose -f ./.dev/docker-compose.yaml stop hass $@
docker-compose -f ./.dev/docker-compose.yaml down

mv packages/_system/guest_wifi.yaml.ignore packages/_system/guest_wifi.yaml
mv packages/devices/pumbaa.yaml.ignore packages/devices/pumbaa.yaml