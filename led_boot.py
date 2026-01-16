import time
import evdev
from rpi_ws281x import *

# --- LED CONFIGURATION ---
LED_COUNT      = 2
LED_PIN        = 18
LED_FREQ_HZ    = 800000
LED_DMA        = 10
LED_BRIGHTNESS = 80
LED_INVERT     = False
LED_CHANNEL    = 0

# Xbox Green (Bright Neon Green)
COLOR_XBOX = Color(0, 255, 0)
# PlayStation Blue (Deep Blue)
COLOR_PS   = Color(0, 0, 255)
# Purple (Blue + Red)
COLOR_BOTH = Color(0, 255, 255)
# White (All on - Dimmed slightly to prevent overheating)
COLOR_NONE = Color(100, 100, 100)

def detect_controllers():
    """
    Scans connected input devices for keywords.
    Returns: (is_xbox_present, is_ps_present)
    """
    xbox_found = False
    ps_found = False
    try:
        # List all input devices
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            name = device.name.lower()
            if "xbox" in name or "microsoft" in name or "x-box" in name:
                xbox_found = True
            if "sony" in name or "playstation" in name or "dualshock" in name:
                ps_found = True
    except Exception as e:
        # If a device disconnects mid-scan, just ignore for this loop
        pass
    return xbox_found, ps_found

# --- MAIN LOGIC ---
if __name__ == '__main__':
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    print("LED Service Started...")

    try:
        while True:
            # 1. Check who is plugged in
            has_xbox, has_ps = detect_controllers()
            # 2. Decide Color
            if has_xbox and has_ps:
                current_color = COLOR_BOTH  # Purple
            elif has_ps:
                current_color = COLOR_PS    # Blue
            elif has_xbox:
                current_color = COLOR_XBOX  # Green
            else:
                current_color = COLOR_NONE  # White
            # 3. Update LEDs
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, current_color)
            strip.show()
            # 4. Wait before checking again (2 seconds is responsive enough)
            time.sleep(2)

    except KeyboardInterrupt:
        # Turn off on exit
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0,0,0))
        strip.show()
