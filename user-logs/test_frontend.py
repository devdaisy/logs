import requests
import pandas as pd
import time
import random
import multiprocessing as mp
from multiprocessing.pool import ThreadPool

BURL = 'http://127.0.0.1:8000'

def create_and_get(query_type, query_params):
	q = {'query_type':query_type, 
		'query_params':query_params}
	r = requests.post(BURL+'/query', params=q)
	r2 = requests.get(BURL+f'/query/{query_type}',
	params={'query_params':query_params})
	r2.raise_for_status()
	query = r2.json()

	if len(query)==0:
		print(query_type, query_params)
		raise ValueError('query not created or returned!')

	return query

def log_query(userid, query):
	qhash = query[0]['queryhash']
	params = {'queryhash':qhash, 'userid':userid, 'rows_returned':-1}
	r = requests.post(BURL+'/log', params=params)
	r.raise_for_status()
	return r

def cache_query(query):
	query = query[0]
	qhash = query['queryhash']
	query_result = pd.DataFrame([(1,2),(3,4)], columns=['a','b'])
	cache_file = f'./query_cache/{qhash}.csv'
	query_result.to_csv(cache_file)
	query['cache_file'] = cache_file
	query['cached'] = True
	qtype = query.pop('query_type')
	r = requests.put(BURL+f'/query/{qtype}', params=query)
	r.raise_for_status()
	return r

def save_query(userid, query, alerts):
	qhash = query[0]['queryhash']
	params = {'queryhash':qhash, 'userid':userid,
				'alerts':alerts}
	r = requests.post(BURL+f'/save', params=params)
	r.raise_for_status()
	return r

def submit_query(userid, query_type, query_params, save, alerts):
	query = create_and_get(query_type, query_params)
	r = log_query(userid, query)
	if save:
		r = save_query(userid, query, alerts)
	already_cached = query[0]['cached']
	if not already_cached:
		r = cache_query(query)
	return query

def get_query(userid, qhash):
	try:
		df = pd.read_csv(f'./query_cache/{qhash}.csv')
		rows_returned = len(df)
		params={'queryhash':qhash, 'rows_returned':rows_returned}
		r = requests.put(BURL+f'/log/{userid}',params=params)
		r.raise_for_status()
		return df
	except FileNotFoundError:
		return 'Not ready yet!'


def simulate_user(userid):
	times = []
	query_types = [f'query{i}' for i in range(10000)]
	query_params = '{test:test}'
	for _ in range(100):
		t = time.time()
		qt = random.choice(query_types)
		save = random.choice([True,False])
		alerts = random.choice([True,False])
		try:
			query = submit_query(userid, qt, query_params, save, alerts)
			df = get_query(userid, query[0]['queryhash'])
		except Exception as e:
			print(f'submit_query error {e}')
		times.append(time.time() - t)

	return times

if __name__ == "__main__":
	nu = 5
	users = list(range(nu))
	with ThreadPool(nu) as tp:
		times = tp.map(simulate_user, users)
	
