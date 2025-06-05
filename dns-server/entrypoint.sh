#!/bin/sh
echo "Starting dnsmasq for broscamp.photo..."
exec dnsmasq -k -C /etc/dnsmasq.conf
