# pistation
Scripts on the pistation

# led_boot.py
Internal LED colors for front grill, changes colours based on the USB controllers plugged in. Showing white for none, green for an xbox controller, blue for a playstation controller and purple for both.

## Pip
`python3 -m venv led-env`

`source led-env/bin/activate`

`pip3 install rpi_ws281x adafruit-circuitpython-neopixel evdev`

## Cron
`@reboot /home/pi/led-env/bin/python3 /home/pi/led_boot.py &`
