#!/bin/sh

DHCP='siaddr 10.0.0.1
boot_file pxelinux.0'
CONFIG='/var/udhcpd.conf'
killall -q -9 udhcpd
if [ -z "$(grep boot_file $CONFIG)" ]; then
    echo -e "$DHCP" >> ${CONFIG}
fi
udhcpd -S ${CONFIG}
