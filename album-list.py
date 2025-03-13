import requests

from common import *

access_token = token_exchange()

album_dict = {}

page_token = None
while True:
	r = requests.get('https://photoslibrary.googleapis.com/v1/albums', params={
		'pageSize': 50,
		'pageToken': page_token,
	}, headers={
		'Authorization': 'Bearer ' + access_token,
	})
	r = r.json()
	assert 'error' not in r, '{} - {}'.format(r['error']['code'], r['error']['message'])
	print('new albums', len(r['albums']))
	for album in r['albums']:
		album_dict[album['id']] = {
			'id': album['id'],
			'title': album['title'],
			'count': int(album['mediaItemsCount']),
			'shared': False,
			'folder': None,
			'copied': False,
		}
	if 'nextPageToken' not in r:
		break
	page_token = r['nextPageToken']

page_token = None
while True:
	r = requests.get('https://photoslibrary.googleapis.com/v1/sharedAlbums', params={
		'pageSize': 50,
		'pageToken': page_token,
	}, headers={
		'Authorization': 'Bearer ' + access_token,
	})
	r = r.json()
	assert 'error' not in r, '{} - {}'.format(r['error']['code'], r['error']['message'])
	print('new shared', len(r['sharedAlbums']))
	for album in r['sharedAlbums']:
		album_dict[album['id']] = {
			'id': album['id'],
			'title': album['title'],
			'count': int(album['mediaItemsCount']),
			'shared': True,
			'folder': None,
			'copied': False,
		}
	if 'nextPageToken' not in r:
		break
	page_token = r['nextPageToken']

album_save()
