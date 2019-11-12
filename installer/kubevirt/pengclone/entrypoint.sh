#!/bin/sh

URL=$1

[ -z $URL ] && echo "Abort! No URL is specified." && exit 1

qemu-img convert -p -O raw \
	"json:{'file.driver': 'http', 'file.url': '$URL', 'file.timeout': 3600}" \
	/mnt/disk.img
