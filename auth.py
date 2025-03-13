# run on windows powershell terminal to allow activation of venv
# Set-ExecutionPolicy Unrestricted -Scope Process

# requirements: requests

import http.server

from common import *
from server import Server

client = client_load()

print('=== client id ===')
print(client['client_id'])
print()

print('=== client secret ===')
print(client['client_secret'])
print()

address = ('localhost', 46775)
print('=== server url ===')
print('http://{:s}:{:d}/init'.format(*address))
print()

print('Navigate to the page above and follow the instructions.')
print('To kill the server press Ctrl+C on this window.')
print()

server = http.server.HTTPServer(address, Server)
server.title = 'Copy Photos to Drive'
server.client = client
server.scope = ' '.join([
	'https://www.googleapis.com/auth/drive',
	'https://www.googleapis.com/auth/photoslibrary.readonly',
])
server.access_type = 'offline'
server.callback = token_save
try:
	server.serve_forever()
except KeyboardInterrupt:
	print()
	server.server_close()
