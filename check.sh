#!/bin/bash

hass -c . --script check_config && \
    python3 -c 'import yaml,sys;yaml.safe_load(sys.stdin)' < ui-lovelace.yaml
