#!/bin/bash

mv packages/_system/guest_wifi.yaml packages/_system/guest_wifi.yaml.ignore
mv packages/presence/fritz_tracker.yaml packages/presence/fritz_tracker.yaml.ignore
mv packages/devices/pumbaa.yaml packages/devices/pumbaa.yaml.ignore

docker-compose up hass
docker-compose stop hass

mv packages/_system/guest_wifi.yaml.ignore packages/_system/guest_wifi.yaml
mv packages/presence/fritz_tracker.yaml.ignore packages/presence/fritz_tracker.yaml
mv packages/devices/pumbaa.yaml.ignore packages/devices/pumbaa.yaml