import sys

import RPi.GPIO as gpio
from mpd import MPDClient


URL = 'spotify:track:6s9iK4Hf5nLhdDMCnkDV3T'  # Gay bar url
URL = 'spotify:track:72lQhFytmSrEVWBiYUWkcR'  # ik moet zuipen

INPUT_PIN = 23


def setup_gpio():
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)
    gpio.setup(INPUT_PIN, gpio.IN, pull_up_down=gpio.PUD_UP)


def play():
    client = MPDClient()
    client.connect('localhost', 6600)

    # add gay bar song to the queue (client.addid() returns the id of the added song)
    gay_bar_id = client.addid(URL)
    status = client.status()


    try:
        current_song = int(status['song'])
    except KeyError:
        # If the queue is empty, status contains no 'song' entry.
        # Therefore, set current_song to 0, as there is no song playing
        current_song = 0

    # get current random setting
    random = int(status['random'])
    client.random(0)
    client.moveid(gay_bar_id, current_song + 1)
    client.next()

    volume = int(status['volume'])
    new_volume = min(volume + 5, 100)
    client.setvol(new_volume)

    # restore previous random setting
    client.random(random)

    # resume playing
    client.play()

    client.close()


def main():
    try:
        setup_gpio()
        print("Listening")
        while True:
            # timeout is so that when ^C is pressed, the program actually exits
            channel = gpio.wait_for_edge(INPUT_PIN, gpio.RISING, timeout=1000)
            if channel:
                print("Button press!")
                play()
    except KeyboardInterrupt:
        gpio.cleanup()
        sys.exit(1)

if __name__ == '__main__':
    # uncomment to make the button start at boot
    main()
    pass
