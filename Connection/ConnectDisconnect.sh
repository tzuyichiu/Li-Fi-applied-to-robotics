#!/bin/sh

connection=$(nmcli dev show wlan0 | grep GENERAL.STATE | awk '{print $2}')

SSID=$(nmcli dev show wlan0 | grep GENERAL.CONNECTION | awk '{print $2}')

if [ "$connection" -eq 100 ] ; then
	nmcli dev disconnect wlan0
	echo "(Disconnected from $SSID)"
fi

nmcli device wifi con "$1" password "$2"
