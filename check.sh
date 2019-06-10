#!/bin/bash

sed -i.org "s/url: '.*'/url: 'http:\/\/dummy\.de'/" ./packages/outdoor/waste_bin.yaml

hass -c . --script check_config && \
    python3 -c 'import yaml,sys;yaml.safe_load(sys.stdin)' < ui-lovelace.yaml

rm packages/outdoor/waste_bin.yaml && \
    mv packages/outdoor/waste_bin.yaml.org packages/outdoor/waste_bin.yaml