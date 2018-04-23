import pickle
import requests
import logging
from Controller import Lock
from Controller import NFCReader

LOCKER_ID = 1
DEBUG = False


class Locker():
    def __init__(self, locker_id=0, locked=False):
        self.locker_id = locker_id
        self.locked = locked

    def save_values(self):
        with open('locker.p', 'wb') as file:
            pickle.dump(self, file)


def main_loop():
    while True:
        reader = NFCReader()
        # Here scanner will get card's hash
        cardID = reader.read_id()

        # Backend URL to verify access request
        post_fields = {'locker_id': str(locker.locker_id),
                       'card_id': cardID}     # Set POST fields here
        r = requests.post(url=url, json=post_fields)

        # TODO: Include actual motor handling functions below
        print(r.status_code)
        if r.status_code == 200:
            logger.info("Access granted for card %s" % cardID)
            locker.locked = r.json()['status']
            servo = Lock()
            if locker.locked:
                servo.move_lock(0)
            else:
                servo.move_lock(180)
            # Beep positively and change doors position
        else:
            logger.info("Access denied for card %s" % cardID)
            # Beep for rejection

        # Fail-safe save in case system crashes
        locker.save_values()


if __name__ == "__main__":

    # Initialise logging
    logger = logging.getLogger('locker')
    hdlr = logging.FileHandler('./locker.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    locker = Locker()
    locker.locker_id = 1
    locker.save_values()
    with open('locker.p', 'rb') as file:
        locker = pickle.load(file)

    url = 'http://0.0.0.0:5000/access_locker'
    if not DEBUG:
        url = 'https://bi-pod.co.uk/api/access_locker'

    main_loop()
