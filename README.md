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
- ~25GB free HDD space on your VirtualBox drive during build process
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
