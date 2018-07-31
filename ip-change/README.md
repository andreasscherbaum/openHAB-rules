# ip-change

Notify about IP-address changes of the home internet router.


## Description

I'm using a [FRITZ!Box](https://en.avm.de/products/fritzbox/) at home, and the [openHAB](https://www.openhab.org/) setup is documented [here](https://andreas.scherbaum.la/blog/archives/957-Add-a-FRITZ!Box-to-openHAB,-using-Ansible.html).

As part of the setup I notify myself when the WAN IP-address of the router changes, although only day over. This usually is a sign for some trouble, either at home, or with the ISP. And this will break all open connections, like phone calls, video conferences, downloads or uploads.

I don't really care for IP-address changes at night, and the router will hangup and reconnect in the morning anyway.
