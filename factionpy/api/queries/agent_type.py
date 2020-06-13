import re
import json
from gql import gql


def list_to_graphql_dict(value):
    response = list()
    for item in value:
        response.append(dict({
            "name": item
        }))
    return response


def process_commands(commands_dict_orig):
    commands_dict = commands_dict_orig
    result = list()
    for command in commands_dict:
        parameter_list = dict({"data": []})
        for parameter in command["command_parameters"]:
            parameter_list["data"].append(parameter)
        command["command_parameters"] = parameter_list
        result.append(command)
    return result


def process_authors(authors_list):
    return "{" + ','.join(authors_list) + "}"


def unquote_keys(agent_type_value):
    return re.sub(r'(?<!: )"(\S*?)"', '\\1', json.dumps(agent_type_value))


def create_agent_type(agent_type):
    name = agent_type["name"]
    language = agent_type["language"]
    authors = process_authors(agent_type["authors"])
    guid = agent_type["guid"]
    operating_systems = list_to_graphql_dict(agent_type["operating_systems"])
    architectures = list_to_graphql_dict(agent_type["architectures"])
    versions = list_to_graphql_dict(agent_type["versions"])
    formats = list_to_graphql_dict(agent_type["formats"])
    configurations = list_to_graphql_dict(agent_type["configurations"])
    build_command = agent_type["build_command"]
    build_location = agent_type["build_location"]
    agent_transport_types = agent_type["agent_transport_types"]
    commands = process_commands(agent_type.get("commands"))
    query = (
        'mutation create_agent_type {'
        '  insert_agent_types(objects: {'
        f'    name: "{name}",'
        '    language: {'
        '      data: {'
        f'        name: "{language}" '
        '      }'
        '    },'
        f'    guid: "{guid}",'
        f'    development: false,'
        f'    build_location: "{build_location}",'
        f'    build_command: "{build_command}",'
        f'    authors: "{authors}",'
        '    agent_transport_types: {'
        f"      data: {unquote_keys(agent_transport_types)}"
        '    },'
        '    agent_type_architectures: {'
        f"      data: {unquote_keys(architectures)}"
        '    },'
        '    agent_type_configurations: {'
        f"      data: {unquote_keys(configurations)}"
        '    },'
        '    agent_type_formats: {'
        f"      data: {unquote_keys(formats)}"
        '    },'
        '    agent_type_operating_systems: {'
        f"      data: {unquote_keys(operating_systems)}"
        '    },'
        '   agent_type_versions: {'
        f"      data: {unquote_keys(versions)}"
        '    }'

        '    commands: {'
        f"      data: {unquote_keys(commands)}"
        '  }}    '
        'on_conflict: {'
        '   constraint: guid'
        '   update_columns: ['
        '       name, '
        '       build_location, '
        '       build_command, '
        '       agent_transport_types, '
        '       agent_type_architectures, '
        '       agent_type_configurations,'
        '       agent_type_formats,'
        '       agent_type_operating_systems,'
        '       agent_type_versions,'
        '       commands'
        '   ]'
        '}) {'
        '    returning {'
        '      id'
        '      guid'
        '      development'
        '      name'
        '      language {'
        '        id'
        '        name'
        '      }'
        '      agent_transport_types {'
        '        build_command'
        '        build_location'
        '        id'
        '        name'
        '        transport_type_guid'
        '      }'
        '      agent_type_architectures {'
        '        id'
        '        name'
        '      }'
        '      agent_type_configurations {'
        '        id'
        '        name'
        '      }'
        '      agent_type_formats {'
        '        id'
        '        name'
        '      }'
        '      agent_type_operating_systems {'
        '        id'
        '        name'
        '      }'
        '      authors'
        '      build_command'
        '      build_location'
        '    }'
        '  }'
        '}'
    )
    query = query.replace('"True"', 'true')
    query = query.replace('"False"', 'false')
    return gql(query)


