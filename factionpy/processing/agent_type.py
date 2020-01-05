from factionpy.backend.database import DBClient
from factionpy.models.agent_type import AgentType
from factionpy.models.language import Language
from factionpy.models.transport import Transport

db = DBClient()


def new_agent_type(name, language_name):
    language = db.session.query(Language).filter_by(Name=language_name).first()

    if not language:
        language = Language()
        language.Name = language_name
        db.session.add(language)
        db.session.commit()

    agent_type = AgentType()
    agent_type.Name = name
    agent_type.LanguageId = language.Id
    agent_type.Development = True
    db.session.add(agent_type)
    db.session.commit()
    return agent_type
