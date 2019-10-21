from factionpy.logger import log
from factionpy.backend.database import DBClient
from factionpy.models.transport import Transport

db = DBClient()


def create_transport(name, transport_type, guid, api_key_id, configuration):
    log("transport.py", "Transport Type: {0}".format(transport_type), "debug")
    log("transport.py", "Guid: {0}".format(guid), "debug")
    log("transport.py", "API Key ID: {0}".format(api_key_id), "debug")
    log("transport.py", "Configuration: {0}".format(configuration), "debug")
    db.session.add(Transport(Name=name,
                             TransportType=transport_type,
                             Guid=guid,
                             ApiKeyId=api_key_id,
                             Configuration=configuration,
                             Enabled=True,
                             Visible=True))
    db.session.commit()
