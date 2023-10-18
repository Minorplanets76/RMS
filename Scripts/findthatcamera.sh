#!/bin/bash
# Chris Chad Oct 2023
# Script to detect if camera available and if not search for it on
# home network and then reset it to desire IP.
# For use with RMS
echo "Where's that heckin' camera?"
camIP=$(sudo nmap -sn 192.168.42.10 | grep -B 2 "00:12:15:C6:A1:19" | head -n 1 | cut -d " " -f 5)
# echo $camIP

# sudo nmap -sn 192.168.42.0-20
echo $camIP
if [ $camIP = "192.168.42.10" ] ; then
	echo "Well it appears to have the correct address"
	echo "Maybe a camera fault?"
	sudo nmap 192.168.42.10 -p 554 | head -n 3 | tail -n 1
	sudo nmap 192.168.42.10 -p 554 | head -n 6 | tail -n 1
	# reboot camera

else
	echo "Not where it should be"
	echo "Let's see if it defected back to the home networkk again"
	camIP=$(sudo nmap -sn 192.168.1.1/24 | grep -B 2 "00:12:15:C6:A1:19" | head -n 1 | cut -d " " -f 5)
	echo $camIP
	echo -en "\e[38;5;9mBeating camera into submission"
	source ~/vRMS/bin/activate
	cd ~/source/RMS
	python -m Utils.SetCameraAddress $camIP 192.168.42.10
fi
