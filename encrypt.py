import os
from bottle import abort

from errbot import BotPlugin, webhook
from cryptography.fernet import Fernet


class Encrypt(BotPlugin):
    """
    Encrypt
    """
    key = os.environ.get('ENCRYPTION_KEY')

    def activate(self):
        """
        Triggers on plugin activation

        """
        if not self.key:
            raise ValueError('Missing encryption key. Please set ENCRYPTION_KEY environment variable.')
        else:
            super(Encrypt, self).activate()

    @webhook('/encrypt', methods=('POST',), raw=True)
    def encrypt(self, request):
        """A webhook encrypt a string from POST body"""
        try:
            f = Fernet(self.key.encode('utf-8'))
            token = f.encrypt(request.body.read())
            self.log.info(token)
            return token
        except ValueError as e:
            self.log.exception("Encryption Key Error: " + str(e))
            abort(500, "Encryption Key Error: " + str(e))
