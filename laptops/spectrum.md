# Spectrum Software

This playbook install spectrum software:

+ Tested on Debian Bullseye

## Software installed

+ [ZesarUX](https://github.com/chernandezba/zesarux/). Tested with 9.1 release.

## Configuration

Modify:

+ **zesarux_src** in [group_vars/spectrum.yaml](group_vars/spectrum.yaml) to point the ZesarUX you want to install.
+ **zesarux_tgz** and **zesarux_dirname** should be changed according to **zesarux_src**.
