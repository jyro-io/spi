import requests
from pytprint import print
from datetime import datetime
import simdjson
import pymongo
from urllib.parse import quote_plus


# Connect to Mongo in a robust manner
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
        pymongo.read_preferences.ReadPreference()
        conn = pymongo.MongoClient(uri)
        # The ismaster command is cheap and does not require auth.
        conn.admin.command('ismaster')
        return True, conn
    except pymongo.errors.ConnectionFailure as err:
        return False, err


class SocratesConnectError(Exception):
    pass


class Socrates:
    def __init__(self, **kwargs):
        """
        Construct an authenticated Socrates client object
        :param kwargs:
            protocol <string> HTTP/S
            host <string> Socrates host
            username <string> Socrates username
            password <string> Socrates password
            verify <bool> SSL verify
        """
        self.host = kwargs['host']
        self.verify = kwargs['verify']
        self.protocol = kwargs['protocol']
        r = requests.post(
            self.protocol+'://'+self.host+'/auth',
            headers={"Content-Type": "application/json"},
            json={"username": kwargs['username'], "password": kwargs['password']},
            verify=kwargs['verify']
        )
        if r.status_code == 200:
            self.headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + str(r.json()['token'])}
        else:
            self.log(
                level='ERROR',
                procedure='self.__init__',
                message='failed to authenticate',
                detail=str(r.content)
            )

    def log(self, **kwargs):
        print(simdjson.dumps({
            "datetime": str(datetime.now()),
            "jyro": {
                "level": kwargs['level'],
                "app": "spi",
                "procedure": kwargs['procedure'],
                "message": kwargs['message'],
                "detail": simdjson.dumps(kwargs['detail'])
            }
        }))

    def get_definition(self, **kwargs):
        """
        Get a JSON definition record from a specified api.module endpoint
        :param kwargs:
            api <string> API to request
            module <string> module within selected api (ie endpoint)
            name <string> definition name
        :return:
            status <bool>
            response <string>
        """
        r = requests.post(
            self.protocol+'://'+self.host+'/'+kwargs['api']+'/'+kwargs['module'],
            headers=self.headers,
            json={"operation": "get", "name": kwargs['name']},
            verify=self.verify
        )
        if r.status_code == 200:
            return True, r.json()
        else:
            self.log(
                level='ERROR',
                procedure='self.get_definition',
                message='failed to get definition',
                detail=str(r)
            )
            return False, None

    def add_definition(self, **kwargs):
        """
        Create various definition types in Socrates
        :param kwargs:
            api <string> API to request
            module <string> module within selected api (ie endpoint)
            name <string> definition name
            definition <string> definition JSON body
        :return:
            status <bool>
            response <string>
        """
        r = requests.post(
            self.protocol+'://'+self.host+'/'+kwargs['api']+'/'+kwargs['module'],
            headers=self.headers,
            json={"operation": "add", "name": kwargs['name'], "definition": kwargs['definition']},
            verify=self.verify
        )
        if r.status_code == 200:
            return True, r.json()
        else:
            self.log(
                level='ERROR',
                procedure='self.add_definition',
                message='failed to add definition',
                detail=str(r.content)
            )
            return False, None

    def update_definition(self, **kwargs):
        """
        Update various definition types in Socrates
        :param kwargs:
            api <string> API to request
            module <string> module within selected api (ie endpoint)
            name <string> definition name
            definition <string> definition JSON body
        :return:
            status <bool>
            response <string>
        """
        r = requests.post(
            self.protocol+'://'+self.host+'/'+kwargs['api']+'/'+kwargs['module'],
            headers=self.headers,
            json={"operation": "update", "name": kwargs['name'], "definition": kwargs['definition']},
            verify=self.verify
        )
        if r.status_code == 200:
            return True, r.json()
        else:
            self.log(
                level='ERROR',
                procedure='self.update_definition',
                message='failed to update definition',
                detail=str(r.content)
            )
            return False, None

    def delete_definition(self, **kwargs):
        """
        Delete various definition types in Socrates
        :param kwargs:
            api <string> API to request
            module <string> module within selected api (ie endpoint)
            name <string> definition name
        :return:
            status <bool>
            response <string>
        """
        r = requests.post(
            self.protocol+'://'+self.host+'/'+kwargs['api']+'/'+kwargs['module'],
            headers=self.headers,
            json={"operation": "delete", "name": kwargs['name']},
            verify=self.verify
        )
        if r.status_code == 200:
            return True, r.json()
        else:
            self.log(
                level='ERROR',
                procedure='self.delete_definition',
                message='failed to delete definition',
                detail=str(r.content)
            )
            return False, None

    def get_raw_data(self, **kwargs):
        """
        Get raw time-series data from given datasource parameters
        :param kwargs:
            name <string> definition name to get
            key <string> key for iteration_field
            start <string> %Y-%m-%dT%H:%M:%S
            end <string> %Y-%m-%dT%H:%M:%S
        :return:
            status <bool>
            response <string>
        """
        r = requests.post(
            self.protocol+'://'+self.host+'/archimedes/datasource',
            headers=self.headers,
            json={
                'operation': 'get_raw_data',
                'name': kwargs['name'],
                'key': kwargs['key'],
                'start': kwargs['start'],
                'end': kwargs['end']
            },
            verify=self.verify
        )
        if r.status_code == 200:
            return True, r.json()
        else:
            self.log(
                level='ERROR',
                procedure='self.get_raw_data',
                message='failed to get raw data',
                detail=str(r.content)
            )
            return False, None

    def get_iteration_set(self, **kwargs):
        """
        Get defined set of keys from configured datasource to parallelize processing
        :param kwargs:
            name <string> definition name to get
        :return:
            status <bool>
            response <string>
        """
        r = requests.post(
            self.protocol+'://'+self.host+'/archimedes/datasource',
            headers=self.headers,
            json={"operation": "get_iteration_set", "name": kwargs['name']},
            verify=self.verify
        )
        if r.status_code == 200:
            return True, r.json()
        else:
            self.log(
                level='ERROR',
                procedure='self.get_iteration_set',
                message='failed to get iteration set',
                detail=str(r.content)
            )
            return False, None

    def get_unreviewed_index_records(self, **kwargs):
        """
        Get unreviewed index records from given module
        :param kwargs:
            name <string> definition name to get
        :return:
            status <bool>
            response <string>
        """
        r = requests.post(
            self.protocol+'://'+self.host+'/archimedes/scraper',
            headers=self.headers,
            json={
                "operation": "get_unreviewed_index_records",
                "name": kwargs['name'],
                "datasource": kwargs['datasource']
            },
            verify=self.verify
        )
        if r.status_code == 200:
            return True, r.json()
        else:
            self.log(
                level='ERROR',
                procedure='self.get_unreviewed_index_records',
                message='failed to get unreviewed index records',
                detail=str(r.content)
            )
            return False, None

    def get_config(self, **kwargs):
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
            self.protocol+'://'+self.host+'/'+kwargs['api']+'/_config',
            headers=self.headers,
            json={"operation": "get", "key": kwargs['key']},
            verify=self.verify
        )
        if r.status_code == 200:
            return True, r.json()
        else:
            self.log(
                level='ERROR',
                procedure='self.get_config',
                message='failed to get config',
                detail=str(r.content)
            )
            return False, None

    def push_raw_data(self, **kwargs):
        """
        Push raw time-series data to Archimedes datasource
        :param kwargs:
            name <string> definition name to get
            key <string> key for iter_field
            records <list> [{},...]
        :return:
            status <bool>
            response <string>
        """
        r = requests.post(
            self.protocol+'://'+self.host+'/archimedes/datasource',
            headers=self.headers,
            json={
                'operation': 'push_raw_data',
                'name': kwargs['name'],
                'records': kwargs['records']
            },
            verify=self.verify
        )
        if r.status_code == 200:
            return True, r.json()
        else:
            self.log(
                level='ERROR',
                procedure='self.push_raw_data',
                message='failed to push raw data',
                detail=str(r.content)
            )
            return False, None

    def get_cluster_nodes(self):
        """
        Get list of nodes in the Socrates cluster
        :return:
            status <bool>
            response <JSON>
        """
        r = requests.post(
            self.protocol+'://'+self.host+'/socrates/_cluster',
            headers=self.headers,
            json={"operation": "get_nodes"},
            verify=self.verify
        )
        if r.status_code == 200:
            return True, r.json()
        else:
            self.log(
                level='ERROR',
                procedure='self.get_cluster_nodes',
                message='failed to get cluster nodes',
                detail=str(r.content)
            )
            return False, None

    def get_cluster_services(self):
        """
        Get list of services in the Socrates cluster
        :return:
            status <bool>
            response <JSON>
        """
        r = requests.post(
            self.protocol+'://'+self.host+'/socrates/_cluster',
            headers=self.headers,
            json={"operation": "get_services"},
            verify=self.verify
        )
        if r.status_code == 200:
            return True, r.json()
        else:
            self.log(
                level='ERROR',
                procedure='self.get_cluster_services',
                message='failed to get cluster services',
                detail=str(r.content)
            )
            return False, None
