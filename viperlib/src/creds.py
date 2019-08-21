import logging

import keyring

from viperlib import jsondata

logger = logging.getLogger(__name__)

class creds():

    _srctype = None
    _alias = None
    _user = None
    _pwd = None
    _hnd = None

    CREDS_TYPE_PLAIN = -1000 # used for storing credentials as plain text in JSON format
    CREDS_TYPE_SECURE = -2000 # used for storing credentials securely using keyring package

    def __init__(self, type=None):
        self.type = type
        if type == None:
            self.type = self.CREDS_TYPE_SECURE
        assert self.type == self.CREDS_TYPE_PLAIN or self.type == self.CREDS_TYPE_SECURE, 'Invalid credentials type value.'
        if self.type == self.CREDS_TYPE_PLAIN:
            self._hnd = jsondata()
            self._hnd.filename = 'credentials'

    @property
    def type(self):
        return self._srctype

    @type.setter
    def type(self, val):
        self._srctype = val

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, val):
        self._alias = val

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, val):
        self._user = val

    @property
    def password(self):
        return self._pwd

    @password.setter
    def password(self, val):
        self._pwd = val

    @property
    def location(self):
        return self._hnd.location

    @location.setter
    def location(self, val):
        self._hnd.location = val

    def get(self):
        if self.type == self.CREDS_TYPE_SECURE:
            self.user = keyring.get_password(self.alias, 'uid')
            self.password = keyring.get_password(self.user, 'pwd')
        elif self.type == self.CREDS_TYPE_PLAIN:
            self._hnd.get_from_file()
            t = self._hnd.contents[self.alias]
            self.user = t['uid']
            self.password = t['pwd']
        else:
            raise ValueError('Could not detemine credentials type.')
