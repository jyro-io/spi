import requests
from pytprint import print
from datetime import datetime
import socket
import json
import pymongo
from urllib.parse import quote_plus


class SocratesConnectError(Exception):
    pass


def log(**kwargs):
    """
    Internal, thread-safe logging function with standardized JSON formatting
    :param kwargs:
        level <int> [0:4] log message level
        log_level <int> [0:4] output threshold
        procedure <string> caller
        input <string> input to calling procedure
        message <string> message to log
    :return:
        status <bool>
    """
    if kwargs['log_level'] >= kwargs['level']:
        if kwargs['level'] == 0:
            msg_level = '[EXCEPTION]: '
        elif kwargs['level'] == 1:
            msg_level = '[INFO]: '
        elif kwargs['level'] == 2:
            msg_level = '[WARN]: '
        elif kwargs['level'] == 3:
            msg_level = '[ERROR]: '
        elif kwargs['level'] == 4:
            msg_level = '[DEBUG]: '
        else:
            msg_level = '[UNDEFINED]'
        print(json.dumps({
            "datetime": str(datetime.now()),
            "level": kwargs['level'],
            "node": socket.gethostname(),
            "input": kwargs['input'],
            "procedure": kwargs['procedure'],
            "message": msg_level + kwargs['message']
        }))
        return True
    else:
        return False


def connect_to_mongo(**kwargs):
    """
    Connect to mongo in a robust way.
    :param kwargs:
        host <string> mongo host
        username <string> mongo username
        password <string> mongo password
        j <bool> request acknowledgment that the write operation has been written to the on-disk journal
    :return:
        status <bool>
        response <string>
    """
    uri = "mongodb://%s:%s@%s" % (quote_plus(kwargs['username']), quote_plus(kwargs['password']), kwargs['host'])
    try:
        pymongo.write_concern.WriteConcern(w='majority', j=kwargs['j'])
        conn = pymongo.MongoClient(uri)
        # The ismaster command is cheap and does not require auth.
        conn.admin.command('ismaster')
        return True, conn
    except pymongo.errors.ConnectionFailure as err:
        return False, err


class Socrates:
    def __init__(self, **kwargs):
        """
        Construct a Socrates interface object
        :param kwargs:
            host <string> Socrates host
            username <string> Socrates username
            password <string> Socrates password
            verify <bool> SSL verify
        """
        self.host = kwargs['host']
        self.verify = kwargs['verify']
        r = requests.post(
            'https://'+self.host+'/auth',
            headers={"Content-Type": "application/json"},
            json={"username": kwargs['username'], "password": kwargs['password']},
            verify=kwargs['verify']
        )
        if r.status_code == 200:
            self.headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + str(r.json()['token'])}
        else:
            raise SocratesConnectError({'response': r.text})

    def get_definition_from_socrates(self, **kwargs):
        """
        Get a JSON definition record from a specified api.module endpoint
        :param kwargs:
            api <string> API to request
            module <string> module within selected api (ie endpoint)
            name <string> definition name to get
        :return:
            status <bool>
            response <string>
        """
        r = requests.post(
            'https://'+self.host+'/'+kwargs['api']+'/'+kwargs['module'],
            headers=self.headers,
            json={"operation": "get", "name": kwargs['name']},
            verify=self.verify
        )
        if r.status_code == 200:
            return True, r.json()
        else:
            return False, r.text

    def get_configuration_from_socrates(self, **kwargs):
        """
        Get a JSON configuration record from a specified api
        :param kwargs:
            api <string> API to request
            key <string> configuration key to retrieve
        :return:
            status <bool>
            response <string>
        """
        r = requests.post(
            'https://'+self.host+'/'+kwargs['api']+'/_config',
            headers=self.headers,
            json={"operation": "get", "key": kwargs['key']},
            verify=self.verify
        )
        if r.status_code == 200:
            return True, r.json()
        else:
            return False, r.text