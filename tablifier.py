import json
import pandas


def tablify_identity_criteria(json_file_location: str, table_location):
    ic_json_file = open(json_file_location)
    types_and_identity_criteria_for_types = json.loads(ic_json_file.read())
    short_identity_criteria = list()
    types = set()
    relations = set()
    for type, identity_criteria in types_and_identity_criteria_for_types.items():
        if not type == 'metadata':
            types.add(type)
            for identity_criterion in identity_criteria:
                shortened_identity_criterion = identity_criterion['relation']+'@'+str(identity_criterion['identity_position'])
                relations.add(shortened_identity_criterion)
                short_identity_criteria.append([type, shortened_identity_criterion])
    types = list(types)
    types.sort()
    relations = list(relations)
    relations.sort()
    identity_criteria_table = pandas.DataFrame(index=types,columns=relations)
    for type in types:
        for relation in relations:
            if [type, relation] in short_identity_criteria:
                identity_criteria_table.loc[type,relation] = '+'
    identity_criteria_table.to_excel(table_location)