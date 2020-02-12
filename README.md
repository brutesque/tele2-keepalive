# Tele2 KeepAlive

Tele2 NL has a subscription that allows for unlimited data. Unfortunately they give you a GB budget which they need you to 
refill manually. This script will send a SMS with a request to refill the data budget on a time interval.

Tested with Huawei E3372 LTE USB stick. This script is meant to work together with [rpi-router](https://github.com/brutesque/rpi-router)

#### Installation instructions
Enter the following command to install the script:
```bash
$ bash -c "$(curl -fsSL raw.githubusercontent.com/brutesque/tele2-keepalive/master/install.sh)"
```

If everything went well, the raspberry pi will reboot and SMS messages will appear in the outbox.

#### Resources
- https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/
