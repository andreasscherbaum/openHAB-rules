# Lights with Motion Sensor and delayed off

The example rules show how to turn on and delayed turn off lights based on motion sensors.


## Setup

Imagine stairs, a small floor, and a hobby area. One motion sensor near the stairs, one in the floor, one inside the door in the hobby area. All three sensors can turn on the lights. When the last sensor goes off, a delayed off routine is triggered, which slowly dims the light, and then finally turns it off. This gives everyone enough time to exit the area.


## Devices

2 different types of motion sensors:

* Xiaomi Mi Motion Smart Sensor (Zigbee)
* Philips Hue Motion sensor (Zigbee)

1 type of light:

* IKEA TRADFRI bulb E27 WS opal 1000lm

All devices connected to a [RaspBee II](https://phoscon.de/en/raspbee2), running on a separate Raspberry Pi.

The light is a "colortemperaturelight", which allows controlling the brightness and color temperature.


## Workflow

* Any motion sensor changing to "ON" triggers "Motion Sensors Floor Upstairs present on", which in turn sets the _Upper_Floor_Presence_ virtual switch.
* Any motion sensor updated triggers "Motion Sensors Floor Upstairs update", which cancels any in-progress "off" timer (if there is one running already).
* Any motion sensor changing to "OFF" triggers "Motion Sensors Floor Upstairs present off", which in turn starts a timer for $LightsOnSeconds seconds, and afer the timer expires changes _Upper_Floor_Presence_ to OFF.
* _Upper_Floor_Presence_ changing to "ON" triggers "Floor Upstairs Light on", which kills all "off" timers, then turns the light on with very low brightness, and starts more timers to turn up the brightness in the following seconds
* _Upper_Floor_Presence_ changing to "OFF" triggers "Floor Upstairs Light off", which slowly dims the ligt, until it is turned off after a couple seconds.
* On system (openHAB) start, the light is turned off by "Init Floor Upstairs Light"
* If someone accidentally turns off the power to the light, "light-floor-upstairs goes Offline - audio notification" sends an audio notification


## Deployment

This is rolled out using Ansible, which replaces a couple variables, and details like the _.things_ and _.items_ files are all auto-generated. Only have to change the template, and upon deployment all Items and Things are updated. Saves a lot of Copy&Paste.


## Notification

There is code in the rules to send notifications to Telegram channels. Configure a [Telegram bot](https://andreas.scherbaum.la/blog/archives/1040-openHAB-and-Telegram-Bot.html), create one or two groups, and set the [group ids](https://andreas.scherbaum.la/blog/archives/1031-Find-Telegram-Group-ID.html) near the top of the file. In my case I'm using _TELEGRAM_CHANNEL_HA_ for general notifications, and _TELEGRAM_CHANNEL_HA_DETAILS_ receives more details.
