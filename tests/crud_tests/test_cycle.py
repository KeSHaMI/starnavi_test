from config import domain
import requests



user = None

post = None

like = None

token = None

def test_create_user():
	global user
	URL = f'{domain}/api/create/user/'

	client = requests.session()

	client.get(URL)  # sets cookie
	if 'csrftoken' in client.cookies:
	   
	    csrftoken = client.cookies.get('csrftoken')
	else:
	    # older versions
	    csrftoken = client.cookies.get('csrf')

	data = {'username': 'Test1', 'password': '12345678Bla', 'email': 'test@gmail.com', 'csrfmiddlewaretoken':csrftoken}

	r = client.post(URL, data=data)

	user = r.json()
	print(r.json())

	assert r.json()['username'] == 'Test1'


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

	with open('token.txt', 'wb') as f:
		f.write(bytes(token, 'utf-8'))

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

	data = {'title': 'TestPost1', 'body': 'Lorem ipsum..', 'user':user['id'], 'csrfmiddlewaretoken':csrftoken}
	r = client.post(URL, data=data, headers={'Authorization':'Bearer {}'.format(token)})

	post = r.json()
	print(r.json())

	assert r.json()['title'] == 'TestPost1'

def test_add_like():
	global like
	URL = f'{domain}/api/create/like/'

	client = requests.session()

	client.get(URL)  # sets cookie
	if 'csrftoken' in client.cookies:
	   
	    csrftoken = client.cookies.get('csrftoken')
	else:
	    # older versions
	    csrftoken = client.cookies.get('csrf')

	data = {'post': post['id'], 'user':user['id'], 'csrfmiddlewaretoken':csrftoken}


	r = client.post(URL, data=data, headers={'Authorization':'Bearer {}'.format(token)})
	like = r.json()

	assert r.status_code == 200

def test_minus_like():
	like_id = like['id']

	URL = f'{domain}/api/delete/like/{like_id}/'

	client = requests.session()

	client.get(URL)  # sets cookie
	if 'csrftoken' in client.cookies:
	   
	    csrftoken = client.cookies.get('csrftoken')
	else:
	    # older versions
	    csrftoken = client.cookies.get('csrf')

	r = client.delete(URL, headers={'Authorization':'Bearer {}'.format(token)})

	assert r.status_code == 200

def test_analytics():
	URL = f'{domain}/api/analytic/'

	r = requests.get(URL, params={'date_from':'2020-07-20', 'date_to':'2020-07-20'}, headers={'Authorization':'Bearer {}'.format(token)})

	assert r.status_code == 200