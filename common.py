import json

import requests

def client_load():
	with open('client-secret.json', 'r') as fp:
		return json.load(fp)['web']

def token_save(token):
	with open('refresh-token.txt', 'w') as fp:
		fp.write(token + '\n')

def token_load():
	with open('refresh-token.txt', 'r') as fp:
		return fp.read().strip()

def token_exchange():
	client = client_load()
	refresh_token = token_load()
	r = requests.post(client['token_uri'], data={
		'client_id': client['client_id'],
		'client_secret': client['client_secret'],
		'refresh_token': refresh_token,
		'grant_type': 'refresh_token',
	})
	r = r.json()
	assert 'error' not in r, r['error']
	return r['access_token']

def album_save(album_dict):
	with open('album-list.json', 'w', encoding='utf-8') as fp:
		json.dump(album_dict, fp, ensure_ascii=False, indent='\t')

def album_load():
	with open('album-list.json', 'r', encoding='utf-8') as fp:
		return json.load(fp)

def photo_push(photo_id, drive_id):
	with open('photo-list.csv', 'a') as fp:
		fp.write(f'{photo_id}\t{drive_id}\n')

def photo_load():
	try:
		with open('photo-list.csv', 'r') as fp:
			photo_dict = {}
			for line in fp:
				line = line.strip()
				if line == '':
					continue
				[photo_id, drive_id] = line.split('\t', 1)
				photo_dict[photo_id] = drive_id
		return photo_dict
	except FileNotFoundError:
		return {}
