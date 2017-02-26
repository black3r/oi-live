#!/bin/bash

WORK_DIR="$(mktemp -d)"

cd "$(dirname "$0")"

BOOT_MODE=bios
SYSLINUX_MODULES="chain.c32 cmd.c32 isolinux.bin reboot.c32 vesamenu.c32 whichsys.c32 ldlinux.c32 libcom32.c32 libutil.c32 poweroff.c32"

cp -a boot "$WORK_DIR/boot"
cp -a /boot/memtest86+/memtest.bin "$WORK_DIR/boot/"
for MOD in $SYSLINUX_MODULES; do
    cp -a "/usr/lib/syslinux/$BOOT_MODE/$MOD" "$WORK_DIR/boot/syslinux/"
done
cp -a "/usr/lib/syslinux/$BOOT_MODE/pxelinux.0" "$WORK_DIR/boot/"
cp -a "/boot/vmlinuz-linux" "$WORK_DIR/boot/vmlinuz"
cp -a "/boot/oi_boot.img" "$WORK_DIR/boot/oi_boot.img"

( cd "$WORK_DIR"; tar cf oi-boot.tar boot )

cp "$WORK_DIR/oi-boot.tar" /vagrant/oi-boot.tar
echo "Boot tarball ready: $WORK_DIR/oi-boot.tar"
