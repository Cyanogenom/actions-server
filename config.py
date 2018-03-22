from re import compile
LISTEN_IP = '127.0.0.1'
LISTEN_PORT = 8080

send_data_url = compile(r'^/?send-data/?$')
_get_data_url = compile(r'^/?get-data/?.*$')
_health_check_url = compile(r'^/?healthcheck/?$')
get_max_values = compile(r'max=(\d+.?\d+)')
get_min_values = compile(r'min=(\d+.?\d+)')
project_id = 'ennergiia-research'