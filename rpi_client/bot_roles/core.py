from utils import get_mac_address, shutdown, restart

class Core(object):
    """
    Commands must take the kwargs argument
    """
    def __init__(self, socket):
        self.socket = socket
        self.commands = ['shutdown', 'restart']


    def shutdown(self, kwargs):
        shutdown()

    def restart(self, kwargs):
        restart()

    def get_mac_address(self):
        return get_mac_address() 
