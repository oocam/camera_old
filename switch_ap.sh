#!/bin/bash 

#reverting dhcpcd.conf 
sudo mv /etc/dhcpcd.conf /etc/dhcpcd.conf.tmp 
sudo mv /etc/dhcpcd.conf.backup /etc/dhcpcd.conf
sudo mv /etc/dhcpcd.conf.tmp /etc/dhcpcd.conf.backup

#reverting dnsmasq.conf
sudo mv /etc/dnsmasq.conf.orig /etc/dnsmasq.conf.tmp 
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo mv /etc/dnsmasq.conf.tmp /etc/dnsmasq.conf

reboot
