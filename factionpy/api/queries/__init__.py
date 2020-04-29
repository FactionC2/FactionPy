from gql import gql


def get_type_fields(client, type_name):
    query = '''
query MyQuery {
    __type(name: "agents") {
        name
        fields {
            name
        }
    }
}'''.replace("TYPENAME", type_name)
    result = client.execute(gql(query))
    results = []
    for item in result["__type"]["fields"]:
        results.append(item['name'])
    return results
