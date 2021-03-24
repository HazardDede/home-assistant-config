# Smart Home Roadmap & Ideas

## Call Monitor

Send Notifications when somebody is calling (done)
Bug: Phonebook is not working (even with fritzconnection directly)
Automatically lower volume of media player (done)

Pause media player on a phone call (done)
https://community.home-assistant.io/t/pause-media-player-on-a-calll/263024
https://community.home-assistant.io/t/mute-media-player-when-on-phone-only-when-home/255221

## Climate monitor

Each room: setpoint, actual temperature, difference
Humidity alerts; requires more H&T sensors

## Evaluate new thermostats

Tado, Fritz!Thermostat?

## Overhaul of camera

* Reinstall raspbian and configure motioneye
* Better integration into home assistant

Send camera snapshot when motion is detected:
https://community.home-assistant.io/t/send-camera-snapshot-notification-on-motion/254565
 
MQTT Integration for on/off (done)
https://community.home-assistant.io/t/motioneye-home-assistant-camera-motion-automation/41712/34
 
Howto enable motioneye webcontrol (dones)
https://community.home-assistant.io/t/motioneye-integration/194350
 
HASS Integration for showing latetst motion (done)
https://www.home-assistant.io/integrations/push/
 
Realtime Camera (done)
https://www.floriangaechter.com/blog/motioneye-in-home-assistant/

## Summary of energy costs

Summary of daily, monthly, yearly energy consumption and costs

## Running costs

Evaluate / Implement a solution to track whether a appliance is running right now (based on power drain)
Make a sensor to figure out the costs of the last run

## Overhaul of housekeeping jobs

Find a better way to track housekeeping job schedules

## Stall sensor

Implement sensor to figure out if a device is stall

## Fix appdaemon when home assistant restarts

Unfortunately the window sensor is None / unavailable when home assistant starts and this fails
in appdaemon (done)

## Convert the appdaemon stuff to a real home assistant plugin

I want to deprecate home assistant. The only thing that is still running and adds benefit is the climate controller.

# Find a nice way to control our regular lights

Find out how to use flush-mounting switches to preserve our Busch&Jaeger design

## More Sensors

HT: Bath Ground, Bedroom
Window: Gallery, Nursery

## Local Dyson

Use a local dyson via mqtt which does not need to login to your dyson account:

https://github.com/shenxn/ha-dyson/

## Shelly Firmware

Get an update when a new shelly firmware is available! Make it an alert so it will get pesky!

## Docker image update

Find a way to retrieve the current image tag of the deployed docker images and retrieve the latest and greatest image tag from the web!

## Appendix

Disable automations when not home
https://community.home-assistant.io/t/automation-state-based-on-presence/264157

Using shortcuts to contact home assistant
https://companion.home-assistant.io/docs/integrations/siri-shortcuts/