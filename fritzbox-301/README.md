# FRITZ!DECT 301 battery alarm

Notify about battery running low in a FRITZ!DECT 301


## Description

I'm using a [FRITZ!DECT 301](https://en.avm.de/products/fritzdect/fritzdect-301/) at home, to control the room temperature.

This rule sends a daily reminder as long as the battery in the device is low.

I opted for a regular reminder, and not just an alarm when the status changed: it's too easy to forget or ignore the one-time alarm generated by the channel change.

Notification should be expanded, like send an email or push a notification to a mobile phone.


## Switch definition

The channel is defined as follow:

```
Switch Battery_Alarm  "Battery Alarm"  {channel="avmfritz:FRITZ_DECT_301:********:********:battery_low"}
```