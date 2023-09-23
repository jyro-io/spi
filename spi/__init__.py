import requests
import pymongo
from urllib.parse import quote_plus
import datetime


# Connect to Mongo in a robust manner
def connect_to_mongo(**kwargs):
  """
  Connect to mongo in a robust way.
  :param kwargs:
      host <string> mongo host
      username <string> mongo username
      password <string> mongo password
      j <bool> request acknowledgment that the write operation has been written to the on-disk journal
      options <string> uri options
  :return:
      status <bool>
      response <string>
  """
  if 'options' in kwargs:
    uri = "mongodb://%s:%s@%s/%s" % \
          (quote_plus(kwargs['username']), quote_plus(kwargs['password']), kwargs['host'], kwargs['options'])
  else:
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
      raise SocratesConnectError

  def get_predictive_model(self, **kwargs):
    """
    Get a trained predictive model from Archimedes
    :param kwargs:
        datasource <string> datasource name
        definition <string> scraper definition name
    :return:
        status <bool>
        response <string>
    """
    try:
      if 'datasource' in kwargs and 'definition' in kwargs:
        r = requests.post(
          self.protocol+'://'+self.host+'/archimedes/model',
          headers=self.headers,
          json={"operation": "get", "datasource": kwargs['datasource'], "definition": kwargs['definition']},
          verify=self.verify
        )
      else:
        return False, {"error": "expecting datasource and definition keys in kwargs"}
      if r.status_code == 200:
        return True, r.json()
      else:
        return False, {"error": str(r.content)}
    except requests.exceptions.ConnectionError:
      return False, {"error": "connection error"}

  def get_definition(self, **kwargs):
    """
    Get a JSON definition record from a specified api.module endpoint
    :param kwargs:
        api <string> API to request
        module <string> module within selected api (ie endpoint)
        name <string> definition name, if not given then return all datasources
    :return:
        status <bool>
        response <string>
    """
    try:
      if 'name' in kwargs:
        r = requests.post(
          self.protocol+'://'+self.host+'/'+kwargs['api']+'/'+kwargs['module'],
          headers=self.headers,
          json={"operation": "get", "name": kwargs['name']},
          verify=self.verify
        )
      else:
        r = requests.post(
          self.protocol+'://'+self.host+'/'+kwargs['api']+'/'+kwargs['module'],
          headers=self.headers,
          json={"operation": "get"},
          verify=self.verify
        )
      if r.status_code == 200:
        return True, r.json()
      else:
        return False, {"error": str(r.content)}
    except requests.exceptions.ConnectionError:
      return False, {"error": "connection error"}

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
    try:
      r = requests.post(
        self.protocol+'://'+self.host+'/'+kwargs['api']+'/'+kwargs['module'],
        headers=self.headers,
        json={"operation": "add", "name": kwargs['name'], "definition": kwargs['definition']},
        verify=self.verify
      )
      if r.status_code == 200:
        return True, r.json()
      else:
        return False, {"error": str(r.content)}
    except requests.exceptions.ConnectionError:
      return False, {"error": "connection error"}

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
    try:
      r = requests.post(
        self.protocol+'://'+self.host+'/'+kwargs['api']+'/'+kwargs['module'],
        headers=self.headers,
        json={"operation": "update", "name": kwargs['name'], "definition": kwargs['definition']},
        verify=self.verify
      )
      if r.status_code == 200:
        return True, r.json()
      else:
        return False, {"error": str(r.content)}
    except requests.exceptions.ConnectionError:
      return False, {"error": "connection error"}

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
    try:
      r = requests.post(
        self.protocol+'://'+self.host+'/'+kwargs['api']+'/'+kwargs['module'],
        headers=self.headers,
        json={"operation": "delete", "name": kwargs['name']},
        verify=self.verify
      )
      if r.status_code == 200:
        return True, r.json()
      else:
        return False, {"error": str(r.content)}
    except requests.exceptions.ConnectionError:
      return False, {"error": "connection error"}

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
    jsonBody = {
      'operation': 'get_raw_data',
      'name': kwargs['name'],
      'start': kwargs['start'],
      'end': kwargs['end']
    }
    if 'key' in kwargs:
      jsonBody['key'] = kwargs['key']
    elif 'topic' in kwargs:
      jsonBody['key'] = kwargs['topic']
    else:
      return False, {"error": "expecting 'key' or 'topic' in kwargs"}
    try:
      r = requests.post(
        self.protocol+'://'+self.host+'/archimedes/datasource',
        headers=self.headers,
        json=jsonBody,
        verify=self.verify
      )
      if r.status_code == 200:
        return True, r.json()
      else:
        return False, {"error": str(r.content)}
    except requests.exceptions.ConnectionError:
      return False, {"error": "connection error"}

  def get_iteration_set(self, **kwargs):
    """
    Get defined set of keys from configured datasource to parallelize processing
    :param kwargs:
        name <string> definition name to get
    :return:
        status <bool>
        response <string>
    """
    try:
      r = requests.post(
        self.protocol+'://'+self.host+'/archimedes/datasource',
        headers=self.headers,
        json={"operation": "get_iteration_set", "name": kwargs['name']},
        verify=self.verify
      )
      if r.status_code == 200:
        return True, r.json()
      else:
        return False, {"error": str(r.content)}
    except requests.exceptions.ConnectionError:
      return False, {"error": "connection error"}

  def get_unreviewed_index_records(self, **kwargs):
    """
    Get unreviewed index records from given module
    :param kwargs:
        name <string> definition name to get
    :return:
        status <bool>
        response <string>
    """
    try:
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
        return False, {"error": str(r.content)}
    except requests.exceptions.ConnectionError:
      return False, {"error": "connection error"}

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
    if kwargs['api'] is None:
      kwargs['api'] = 'archimedes'
    try:
      r = requests.post(
        self.protocol+'://'+self.host+'/'+kwargs['api']+'/_config',
        headers=self.headers,
        json={"operation": "get", "key": kwargs['key']},
        verify=self.verify
      )
      if r.status_code == 200:
        return True, r.json()
      else:
        return False, {"error": str(r.content)}
    except requests.exceptions.ConnectionError:
      return False, {"error": "connection error"}

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
    try:
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
        return False, {"error": str(r.content)}
    except requests.exceptions.ConnectionError:
      return False, {"error": "connection error"}

  def get_cluster_nodes(self):
    """
    Get list of nodes in the Socrates cluster
    :return:
        status <bool>
        response <JSON>
    """
    try:
      r = requests.post(
        self.protocol+'://'+self.host+'/socrates/_cluster',
        headers=self.headers,
        json={"operation": "get_nodes"},
        verify=self.verify
      )
      if r.status_code == 200:
        return True, r.json()
      else:
        return False, {"error": str(r.content)}
    except requests.exceptions.ConnectionError:
      return False, {"error": "connection error"}

  def get_cluster_services(self):
    """
    Get list of services in the Socrates cluster
    :return:
        status <bool>
        response <JSON>
    """
    try:
      r = requests.post(
        self.protocol+'://'+self.host+'/socrates/_cluster',
        headers=self.headers,
        json={"operation": "get_services"},
        verify=self.verify
      )
      if r.status_code == 200:
        return True, r.json()
      else:
        return False, {"error": str(r.content)}
    except requests.exceptions.ConnectionError:
      return False, {"error": "connection error"}

  def get_ohlc_interval(self, interval, unit):
    if "m" == unit:
      interval = datetime.timedelta(minutes=interval)
    elif "h" == unit:
      interval = datetime.timedelta(hours=interval)
    elif "d" == unit:
      interval = datetime.timedelta(days=interval)
    else:
      return False, {"error": f"invalid unit, expecting [m,h,d]"}
    return interval

  def get_longest_metric_period(self, datasource):
    metric_list = ['sma']
    longest = 0
    for op in datasource['metadata']['etl']:
      if 'metric' == op['operation']:
        if op['name'] in metric_list:
          for period in op['parameters']['periods']:
            if longest < period:
              longest = period
    return longest
