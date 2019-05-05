# URL Notifications

Send any kind of URL notifications


## Problem description

[openHAB](https://www.openhab.org/) has the HTTP binding, which can be used to send notifications to services "on the Internet", using _sendHttpGetRequest()_. However this is not a reliable way, if the notification request can't be delivered, there is no queueing in place to send out the notifications at a later time, or just repeat it.


## Content

* deliver-http-notifications.py: script which queues and sends notifications
* notifications.rules: examples


## Installation

Place _deliver-http-notifications.py_ somewhere in your openHAB installation, I'm using:

```
- name: Copy Notification script
  copy:
    src: "{{ playbook_dir }}/openhab/deliver-http-notifications.py"
    dest: "/var/lib/openhab2/deliver-http-notifications.py"
    owner: openhab
    group: openhabian
    mode: 0750
```

Install the "_Send spool_" rule from _notifications.rules_: this rule will try to send all entries from spool every minute.


## Usage:

In your rule, send/spool a notification like this:

```
executeCommandLine('/var/lib/openhab2/deliver-http-notifications.py@@/var/lib/openhab2/cache/http-notifications@@https://trigger.url/path?param=test')
```

_/var/lib/openhab2/cache/http-notifications_ is the spool directory where each message request is spooled if it can't be send immediately. Make sure you replace spaces with '@@', this is an openHAB limitation.
