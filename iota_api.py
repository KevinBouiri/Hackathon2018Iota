from iota import Iota, ProposedTransaction, Address, Tag, TryteString
from time import sleep
import configparser


class Car:
    def __init__(self, seed):
        self.api = Iota('https://iotanode.us:443', seed)

    def getAddress(self, count=1):
        new_address = self.api.get_new_addresses(count=count)
        print(new_address)
        return new_address

    def sendiota(self, address, amount):
        self.api.send_transfer(
            depth=100,

            # One or more :py:class:`ProposedTransaction` objects to add to the
            # bundle.
            transfers=[
                ProposedTransaction(
                    # Recipient of the transfer.
                    address=Address(
                        address,
                    ),
                    # Amount of IOTA to transfer.
                    # This value may be zero.
                    value=amount,
                    # Optional tag to attach to the transfer.
                    tag=Tag(b'EXAMPLEK'),
                    # Optional message to include with the transfer.
                    message=TryteString.from_string('Hello!'),
                ),
            ],
        )

    def __getAPI(self):
        return self.api


def test():
    print("Test Start")
    config = configparser.ConfigParser()
    config.read('config.cfg')
    seed = config['IOTA']['seed']

    mycar = Car(seed)
    address = mycar.getAddress(2)
    print('Neue Adresse: ' + str(address['addresses'][0]))

    bundles_count_pre = mycar.__getAPI().get_transfers()['bundles']

    print("Sende 0 IOTA an die neue Addresse")
    mycar.sendiota(address['addresses'][1], 0)
    print('Senden gestartet. Es wird auf die bestätigung der Tranbsaktion gewartet.')

    while bundles_count_pre == mycar.__getAPI().get_transfers()['bundles']:
        print('.', end='', flush=True)

    print("IOTA sind angekommen.")

    print('Neuer IOTA Kontostand: ' + str(mycar.__getAPI().get_inputs()['totalBalance']))


def test2():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    seed = config['IOTA']['seed']

    api = Iota('https://iotanode.us:443', seed)
    original = now = len(api.get_transfers()['bundles'])
    while original == now:
        try:
            now = len(api.get_transfers()['bundles'])
        except Exception as e:
            print('Fehler: ', e)
        sleep(0.5)
    print('Transaktion empfangen.')


if __name__ == '__main__':
    test()
