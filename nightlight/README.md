# Night Light or Day Light

In the living room is a power socket which turns off over night, in order not to blend people in the dark. Connected to the socket is a photo screen which rotates through a number of pictures, naturally that is quite bright. openHAB turns off the power socket at night, and turns it on again in the morning.

Reversing the actions (on -> off, and off -> on) makes a day light.

## Implementation

This has three rules:
* one timer rule to turn the light on in the morning
* one timer rule to turn the light off in the evening
* one system start rule to set the correct state when openHAB starts
