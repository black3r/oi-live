OI-Live build toolkit
=====================

This is a set of scripts utilizing Vagrant, VirtualBox and Ansible, to
build a bootable live GNU/Linux-based environment, suitable for
usage as a programming competition environment.

## Requirements

- POSIX compatible environment compatible with Vagrant
- Vagrant
- VirtualBox (other provisioners not supported yet)
- Ansible
- ~40GB free HDD space on your VirtualBox drive during build process
- ~2GB free HDD space on the drive containing this folder (the build process will output bootable iso to `./output/`)

## How to use

### First build

We use a 2-phase build, first we prepare the virtual machine, that will serve
as a base for our live environment in the default vagrant box called oilive.
We create an initrd image inside this environment and then we shut down the
oilive virtual machine, to "freeze" the filesystem, mount the virtual disk
from the oilive machine to a second machine called builder read-only, and
create disk image of the environment we will use.

The command sequence to perform this first build would be:

- `vagrant up`
- `vagrant halt`
- `vagrant up builder`
- `vagrant halt builder`

### Second build

If you want to perform a second full build from the same machine, you should
delete the built files (`/data/oi-live.tar` and `/output/oi-live.iso`) and
launch the machines with `--provision` flag to run the build scripts again.

### Making an overlay image

When we just want to flip a few configuration options, there is no need to
perform a full build procedure again. We should just be able to change these
in a live-booted built environment, and create an overlay with these changes.

TODO

## How to maintain

At least every year, we need to ship a new version. This usually consists
of a few bugfixing/testing steps and a few customization steps. Example
release workflow:

- Bugfixing / testing
  - Try if the last build still works
    - It mostly doesn't, so some fixes are usually required to make the build
    working.
  - Check if all the security features in contest mode still work:
    - IPv6 should not be accessible at all
    - You should only be able to access the tester url with IPv4
    - User can't mount external USB or CD
    - User can't change network properties (disconnect from network or
    connect to another network if Wi-Fi accessible)
    - User is automatically logged in
  - Install any additionally needed software (consult with competition
  organizers and rules to support all necessary programming languages)
  - Check if all icons on desktop can be launched.
  - Check if firefox and chromium icons launch with the tester opened
  - Try to run & build a hello world application in every language
  - Try to run the ISO on some real hardware
- Customizing for the event.
  - Modify build configuration in /group_vars/all/ with correct year
  and contest URL & IP
  - Create new wallpapers and put them in /oilive/files/theme/
  - Set a new root password in /oilive/tasks/oilive-users.yml
  - Customize icons on desktop in 
  /oilive/files/home/.config/plasma-org.kde.plasma.desktop-appletsrc

When you're finished and have got some spare time, you can always look at some
of the issues on the tracker to make the OI-Live experience even better for 
both users and deployers :)
