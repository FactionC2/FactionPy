import re
import json
from gql import gql


def __list_to_graphql_dict(value: list) -> list:
    response = list()
    for item in value:
        response.append(dict({
            "name": item
        }))
    return response


def __process_commands(commands_dict_orig: dict) -> list:
    commands_dict = commands_dict_orig
    result = list()
    for command in commands_dict:
        parameter_list = dict({"data": []})
        for parameter in command["command_parameters"]:
            parameter_list["data"].append(parameter)
        command["command_parameters"] = parameter_list
        result.append(command)
    return result


def __process_authors(authors_list: list) -> str:
    return "{" + ','.join(authors_list) + "}"


def __unquote_keys(agent_type_value):
    return re.sub(r'(?<!: )"(\S*?)"', '\\1', json.dumps(agent_type_value))


def create_agent_type(agent_type: dict):
    name = agent_type["name"]
    language = agent_type["language"]
    authors = __process_authors(agent_type["authors"])
    guid = agent_type["guid"]
    operating_systems = __list_to_graphql_dict(agent_type["operating_systems"])
    architectures = __list_to_graphql_dict(agent_type["architectures"])
    versions = __list_to_graphql_dict(agent_type["versions"])
    formats = __list_to_graphql_dict(agent_type["formats"])
    configurations = __list_to_graphql_dict(agent_type["configurations"])
    build_command = agent_type["build_command"]
    build_location = agent_type["build_location"]
    agent_transport_types = agent_type["agent_transport_types"]
    commands = __process_commands(agent_type.get("commands"))
    query = (
        'mutation create_agent_type {\n'
        '  insert_agent_types(objects: {\n'
        f'    name: "{name}",\n'
        '    language: {\n'
        '      data: {\n'
        f'        name: "{language}" \n'
        '      }\n'
        '    },\n'
        f'    guid: "{guid}",\n'
        f'    development: false,\n'
        f'    build_location: "{build_location}",\n'
        f'    build_command: "{build_command}",\n'
        f'    authors: "{authors}",\n'
        '    agent_transport_types: {\n'
        f"      data: {__unquote_keys(agent_transport_types)}\n"
        '    },\n'
        '    agent_type_architectures: {\n'
        f"      data: {__unquote_keys(architectures)}\n"
        '    },\n'
        '    agent_type_configurations: {\n'
        f"      data: {__unquote_keys(configurations)}\n"
        '    },\n'
        '    agent_type_formats: {\n'
        f"      data: {__unquote_keys(formats)}\n"
        '    },\n'
        '    agent_type_operating_systems: {\n'
        f"      data: {__unquote_keys(operating_systems)}\n"
        '    },\n'
        '   agent_type_versions: {\n'
        f"      data: {__unquote_keys(versions)}\n"
        '    }\n'
        '    commands: {\n'
        f"      data: {__unquote_keys(commands)}\n"
        '  }}    \n'
        ') {\n'
        '    returning {\n'
        '      id\n'
        '      guid\n'
        '      development\n'
        '      name\n'
        '      language {\n'
        '        id\n'
        '        name\n'
        '      }\n'
        '      agent_transport_types {\n'
        '        build_command\n'
        '        build_location\n'
        '        id\n'
        '        name\n'
        '        transport_type_guid\n'
        '      }\n'
        '      agent_type_architectures {\n'
        '        id\n'
        '        name\n'
        '      }\n'
        '      agent_type_configurations {\n'
        '        id\n'
        '        name\n'
        '      }\n'
        '      agent_type_formats {\n'
        '        id\n'
        '        name\n'
        '      }\n'
        '      agent_type_operating_systems {\n'
        '        id\n'
        '        name\n'
        '      }\n'
        '      authors\n'
        '      build_command\n'
        '      build_location\n'
        '    }\n'
        '  }\n'
        '}'
    )
    query = query.replace('"True"', 'true')
    query = query.replace('"False"', 'false')
    print(query)
    return gql(query)


