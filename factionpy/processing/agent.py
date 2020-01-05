from factionpy.backend.database import DBClient
from factionpy.models.agent import Agent
from factionpy.logger import log

db = DBClient()


def get_agent(agent_id, include_hidden=False):
    log("get_agent", "got agent id " + str(agent_id), "debug")
    if agent_id == 'all':
        if include_hidden:
            agents = db.session.query(Agent).all()
        else:
            agents = db.session.query(Agent).filter_by(Visible=True)
        result = []
        for agent in agents:
            result.append(agent)
    else:
        agent = db.session.query(Agent).get(agent_id)
        result = agent
    return result

# def update_agent(agent_id, agent_name=None, visible=None):
#     agent = Agent.query.get(agent_id)
#     if agent_name:
#         agent.Name = agent_name
#
#     if visible is not None:
#         agent.Visible = visible
#
#     message = dict({
#         "Id": agent_id,
#         "Name": agent.Name,
#         "Visible": agent.Visible
#     })
#     log("update_agent", "sending message: {0}".format(message), "debug")
#     rabbit_producer.send_request("UpdateAgent", message)
#     return {"Success": True, "Result": agent_json(agent)}
