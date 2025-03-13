import requests

from common import *

access_token = token_exchange()

album_dict = album_load()
photo_dict = photo_load()

for album_id, album in album_dict.items():
	if album['copied']:
		continue
	print(album)
	if album['folder'] is None:
		r = requests.post('https://www.googleapis.com/upload/drive/v3/files', params={
			'supportsAllDrives': True,
			'uploadType': 'multipart',
		}, files={
			'metadata': (
				None,
				json.dumps({
					'mimeType': 'application/vnd.google-apps.folder',
					'parents': ['16eezjFeGdXpBwy-I42vG5dTObfhLkwXo'],
					'name': album['title'],
				}),
				'application/json; charset=UTF-8',
			),
		}, headers={
			'Authorization': 'Bearer ' + access_token,
		})
		r = r.json()
		assert 'error' not in r, '{} - {}'.format(r['error']['code'], r['error']['message'])
		album['folder'] = r['id']
		album_save(album_dict)
	photo_list = []
	page_token = None
	while True:
		r = requests.post('https://photoslibrary.googleapis.com/v1/mediaItems:search', data={
			'albumId': album_id,
			'pageSize': 100,
			'pageToken': page_token,
		}, headers={
			'Authorization': 'Bearer ' + access_token,
		})
		r = r.json()
		assert 'error' not in r, '{} - {}'.format(r['error']['code'], r['error']['message'])
		print('new items', len(r['mediaItems']))
		photo_list.extend(r['mediaItems'])
		if 'nextPageToken' not in r:
			break
		page_token = r['nextPageToken']
	for i, photo in enumerate(photo_list):
		photo_id = album_id + '/' + photo['id']
		if photo_id in photo_dict:
			continue
		print(photo)
		r = requests.get(photo['baseUrl'] + '=d')
		assert r.ok
		content = r.content
		r = requests.post('https://www.googleapis.com/upload/drive/v3/files', params={
			'supportsAllDrives': True,
			'uploadType': 'multipart',
		}, files={
			'metadata': (
				None,
				json.dumps({
					'mimeType': photo['mimeType'],
					'parents': [album['folder']],
					'name': '{:03d}-{:s}'.format(i, photo['filename']),
					'description': photo['description'] if 'description' in photo else None,
					'createdTime': photo['mediaMetadata']['creationTime'],
					'originalFilename': photo['filename'],
				}),
				'application/json; charset=UTF-8',
			),
			'file': content,
		}, headers={
			'Authorization': 'Bearer ' + access_token,
		})
		r = r.json()
		assert 'error' not in r, '{} - {}'.format(r['error']['code'], r['error']['message'])
		photo_dict[photo_id] = r['id']
		photo_push(photo_id, photo_dict[photo_id])
	album['copied'] = True
	album_save(album_dict)
