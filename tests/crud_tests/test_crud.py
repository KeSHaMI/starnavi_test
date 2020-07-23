import requests
from config import domain

token = None
post = None

def test_create_user_token():
	global token
	URL = f'{domain}/api/token/'

	client = requests.session()

	client.get(URL)  # sets cookie
	if 'csrftoken' in client.cookies:
	   
	    csrftoken = client.cookies.get('csrftoken')
	else:
	    # older versions
	    csrftoken = client.cookies.get('csrf')

	data = {'password': '12345678Bla', 'email': 'test@gmail.com', 'csrfmiddlewaretoken':csrftoken}

	r = client.post(URL, data=data)

	token = r.json()['access']

	assert r.status_code == 200


def test_create_post():

	global post
	URL = f'{domain}/api/create/post/'

	client = requests.session()

	client.get(URL)  # sets cookie
	if 'csrftoken' in client.cookies:
	   
	    csrftoken = client.cookies.get('csrftoken')
	else:
	    # older versions
	    csrftoken = client.cookies.get('csrf')

	data = {'title': 'TestPost1', 'body': 'Lorem ipsum..', 'user':'11', 'csrfmiddlewaretoken':csrftoken}

	r = client.post(URL, data=data, headers={'Authorization':'Bearer {}'.format(token)})

	post = r.json()

	assert r.json()['title'] == 'TestPost1'


def test_get_post():
	URL = '{}/api/get/post/{}'.format(domain, post['id'])

	r = requests.get(URL, headers={'Authorization':'Bearer {}'.format(token)})

	assert r.json()['title'] == 'TestPost1'

def test_get_all_post():
	URL = f'{domain}/api/get_all/post/'

	r = requests.get(URL, headers={'Authorization':'Bearer {}'.format(token)})

	assert r.json()[0]['title'] == 'TestPost1'

def test_update_post():
	URL = '{}/api/update/post/{}/'.format(domain, post['id'])

	client = requests.session()

	client.get(URL)  # sets cookie
	if 'csrftoken' in client.cookies:
	   
	    csrftoken = client.cookies.get('csrftoken')
	else:
	    # older versions
	    csrftoken = client.cookies.get('csrf')

	data = {'body': 'Updated!', 'csrfmiddlewaretoken':csrftoken}


	r = client.post(URL, data=data, headers={'Authorization':'Bearer {}'.format(token)})
	

	assert r.json()['body'] == 'Updated!'




like = None


def test_create_like():

	global like
	URL = f'{domain}/api/create/like/'

	client = requests.session()

	client.get(URL)  # sets cookie
	if 'csrftoken' in client.cookies:
	   
	    csrftoken = client.cookies.get('csrftoken')
	else:
	    # older versions
	    csrftoken = client.cookies.get('csrf')

	data = {'post':post['id'], 'user':'11', 'csrfmiddlewaretoken':csrftoken}

	r = client.post(URL, data=data, headers={'Authorization':'Bearer {}'.format(token)})

	like = r.json()

	assert r.status_code == 200


def test_get_like():
	assert 'id' in like
	URL = '{}/api/get/like/{}'.format(domain, like['id'])

	r = requests.get(URL, headers={'Authorization':'Bearer {}'.format(token)})

	assert r.status_code == 200

def test_get_all_like():
	URL = f'{domain}/api/get_all/like/'

	r = requests.get(URL, headers={'Authorization':'Bearer {}'.format(token)})

	assert r.status_code == 200

def test_delete_like():
	URL = '{}/api/delete/like/{}'.format(domain, like['id'])

	r = requests.delete(URL, headers={'Authorization':'Bearer {}'.format(token)})

	assert r.status_code == 200

def test_delete_post():
	URL = '{}/api/delete/post/{}'.format(domain, post['id'])

	r = requests.delete(URL, headers={'Authorization':'Bearer {}'.format(token)})

	assert r.status_code == 200