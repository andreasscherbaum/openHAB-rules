# Tankerkoenig

This ruleset works with the [Tankerkoenig Binding](https://www.openhab.org/addons/bindings/tankerkoenig/). You also need an API key.

More blog posts here:

* [Version 1](https://andreas.scherbaum.la/blog/archives/1039-openHAB-and-Tankerkoenig-gas-prices-+-Telegram-integration.html)
* [Version 2](https://andreas.scherbaum.la/blog/archives/1051-openHAB-and-Tankerkoenig-gas-prices-+-Telegram-integration-Second-iteration.html)

## Ansible

This is rolled out on openHAB using Ansible. Therefore the files in this directory are a meta configuration, and during deployment certain values will be replaced in the templates.

Here are the relevant parts of the Playbook for deployment:
```
- name: Copy Things files
  template:
    src: "{{ playbook_dir }}/openhab/{{ item }}"
    dest: "/etc/openhab2/things/{{ item }}"
    owner: openhab
    group: openhabian
    mode: 0640
  with_items:
    - tankerkoenig.things
  register: things_files

- name: Copy Items files
  template:
    src: "{{ playbook_dir }}/openhab/{{ item }}"
    dest: "/etc/openhab2/items/{{ item }}"
    owner: openhab
    group: openhabian
    mode: 0640
  with_items:
    - tankerkoenig.items
  register: items_files

- name: Copy Rules files
  template:
    src: "{{ playbook_dir }}/openhab/{{ item }}"
    dest: "/etc/openhab2/rules/{{ item }}"
    owner: openhab
    group: openhabian
    mode: 0640
  with_items:
    - tankerkoenig.rules
  register: rules_files
```


## API Key

The API Key lives in a text file in _credentials/tankerkoenig.txt_ in the Playbook directory. Change the path if necessary.


## Telegram Group

My installation communicates with a Telegram group. The [group id](https://andreas.scherbaum.la/blog/archives/1031-Find-Telegram-Group-ID.html) is stored in _credentials/telegram-channel.txt_.

The [Telegram Bot](https://andreas.scherbaum.la/blog/archives/1040-openHAB-and-Telegram-Bot.html) needs to be setup and ready to receive messages.
