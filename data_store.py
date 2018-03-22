from google.cloud import datastore
from time import time


def create_client(project_id):
    return datastore.Client(project_id)


def set_data(client, json_data):
    key = client.key('Data')

    data = datastore.Entity(key, exclude_from_indexes=tuple(['json_data']))

    data.update({
        'created': time(),
        'json_data': json_data,
    })

    client.put(data)

    return data.key


def get_data(client, min, max):
    query = client.query(kind='Data')
    query.add_filter('created', '>=', min)
    query.add_filter('created', '<=', max)

    return list(query.fetch())
