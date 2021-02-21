# MSX Software

This playbook install MSX software:

+ Tested on Fedora 33

## Software installed

+ [OpenMSX](https://openmsx.org/) emulator.
+ [Catapult GUI](https://github.com/openMSX/catapult).
+ [BIOS ROMS](http://msx2.org/Funet%20(2006-05-28)/emulator/openMSX/System%20Roms/), these ROMs will be installed in the **user** home directory.

## Configuration

Modify:

+ **user** in [group_vars/msx.yaml](group_vars/msx.yaml) to configure the user where you want to configure MSX stuff.
+ Create a public/private key for **user** and copy it to the **~/.ssh/authorized_keys** file for **user** to allow the user to perform passwordless ssh to himself or configure a remote user for passwordless ssh to **user** if you run the playbook from a different computer.