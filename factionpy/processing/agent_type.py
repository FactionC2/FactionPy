from factionpy.backend.database import DBClient
from factionpy.models.agent_type import AgentType
from factionpy.models.agent_transport_type import AgentTransportType
from factionpy.models.agent_type_architecture import AgentTypeArchitecture
from factionpy.models.agent_type_configuration import AgentTypeConfiguration
from factionpy.models.agent_type_format import AgentTypeFormat
from factionpy.models.agent_type_operating_system import AgentTypeOperatingSystem
from factionpy.models.agent_type_version import AgentTypeVersion
from factionpy.models.language import Language
from factionpy.models.transport import Transport

db = DBClient()


def new_language_query(name):
    query = '''
mutation addLanguage {
  insert_languages(objects: {name: "NAME"}) {
    returning {
      id
      name
    }
  }
}
    '''
    return query.replace("NAME", name)


def new_agent_type(name, language_name):
    language = db.session.query(Language).filter_by(Name=language_name).first()

    if not language:
        language = Language()
        language.Name = language_name
        db.session.add(language)
        db.session.commit()

    transport = db.session.query(Transport).filter_by(TransportType="DIRECT").first()
    print(transport.Name)
    print(transport.Guid)

    agent_type = AgentType()
    agent_type.Name = name
    agent_type.LanguageId = language.Id
    agent_type.Development = True
    db.session.add(agent_type)
    db.session.commit()

    agent_arch = AgentTypeArchitecture()
    agent_arch.AgentTypeId = agent_type.Id
    agent_arch.Name = "Development"
    db.session.add(agent_arch)
    db.session.commit()

    agent_config = AgentTypeConfiguration()
    agent_config.AgentTypeId = agent_type.Id
    agent_config.Name = "Development"
    db.session.add(agent_config)
    db.session.commit()

    agent_format = AgentTypeFormat()
    agent_format.AgentTypeId = agent_type.Id
    agent_format.Name = "Development"
    db.session.add(agent_format)
    db.session.commit()

    agent_operation_system = AgentTypeOperatingSystem()
    agent_operation_system.AgentTypeId = agent_type.Id
    agent_operation_system.Name = "Development"
    db.session.add(agent_operation_system)
    db.session.commit()

    agent_version = AgentTypeVersion()
    agent_version.AgentTypeId = agent_type.Id
    agent_version.Name = "Development"
    db.session.add(agent_version)
    db.session.commit()

    agent_transport = AgentTransportType()
    agent_transport.Name = "Development"
    agent_transport.TransportTypeGuid = transport.Guid
    agent_transport.AgentTypeId = agent_type.Id
    db.session.add(agent_transport)
    db.session.commit()

    return agent_type
