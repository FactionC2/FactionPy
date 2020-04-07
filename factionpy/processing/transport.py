from gql import gql
from factionpy.api import client


def new_create_transport_query(name, transport_type, guid, configuration):
    query = '''
mutation {
  insert_transports(objects: {
    name: "NAME", 
    transport_type: "TRANSPORT_TYPE", 
    guid: "GUID", 
    configuration: "CONFIGURATION"
  }) 
  {
    returning {
      id
      name
      guid
      transport_type
      configuration
      created
      last_checkin
      enabled
      visible
    }
  }
}
    '''
    populated_query = query.replace("NAME", name)\
        .replace("TRANSPORT_TYPE", transport_type)\
        .replace("GUID", guid)\
        .replace("CONFIGURATION", configuration)

    return gql(populated_query)


def create_transport(name, transport_type, guid, configuration):
    query = new_create_transport_query(name, transport_type, guid, configuration)
    client.execute(query)
