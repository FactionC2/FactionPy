from models.agent import Agent
from logger import log


def get_agent(agent_id, include_hidden=False):
    log("get_agent", "got agent id " + str(agent_id))
    if agent_id == 'all':
        if include_hidden:
            agents = Agent.query.all()
        else:
            agents = Agent.query.filter_by(Visible=True)
        result = []
        for agent in agents:
            result.append(agent)
    else:
        agent = Agent.query.get(agent_id)
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
#     log("update_agent", "sending message: {0}".format(message))
#     rabbit_producer.send_request("UpdateAgent", message)
#     return {"Success": True, "Result": agent_json(agent)}
