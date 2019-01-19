from flask import *
from requests_oauthlib import OAuth1
import requests, datetime, time, re

class Variable():
	def __init__(self):
		self.nb_max_hastag = 100
		self.nb_iteration = 3
		self.blacklist_h = []


global_variable = Variable()

class Tlist():

	def __init__(self, name, lst, t):
		self.name = name
		self.prev = None
		self.type = t
		self.add_lst(lst)
		self.node_user_user = None
		self.node_user_hast = None
		self.node_hast_user = None
		self.node_hast_hast = None
		self.next = None

	def get_json(self):
		ret = []
		i = 0
		tmp = self
		while (tmp):
			tmp2 = {}
			tmp2["name"] = tmp.name
			if (tmp.ret != None):
				tmp2["type_@1_#2"] = tmp.type
				tmp2["liste_return"] = tmp.ret
				tmp2["nombre_delement"] = tmp.len_ret
				if (tmp.node_user_user != None):
					tmp2["BRANCHE_user_user"] = tmp.node_user_user.get_json()
				if (tmp.node_user_hast != None):
					tmp2["BRANCHE_user_hast"] = tmp.node_user_hast.get_json()
				if (tmp.node_hast_user != None):
					tmp2["BRANCHE_hast_user"] = tmp.node_hast_user.get_json()
				if (tmp.node_hast_hast != None):
					tmp2["BRANCHE_hast_hast"] = tmp.node_hast_hast.get_json()
			ret.append(tmp2)
			tmp = tmp.next
		return ret

	def get_csv_by_relation(self, path):
		file = open(path, "w")
		c = csv.writer(file)
		c.writerow([self.ret[0], "si direct", "nb lien", "nb"])
		tmp = self.node_user_user
		while (tmp):
			c = tmp.get_row_relation(c)
			tmp = tmp.next
		file.close()

	def get_row_relation(self, c):
		for value in self.ret:
			c.writerow([value, 1, self.ret.count(value)])
		tmp = self.node_user_user
		while (tmp):
			for value in tmp.ret:
				c.writerow([value, 0, tmp.ret.count(value)])
			tmp = tmp.next
		return (c)

	def add_next(self, value):
		tmp = self.get_end()
		tmp.next = value
		value.prev = tmp

	def add_lst(self, value):
		self.ret = value
		self.len_ret = len(value) if value else 0

	def get_start(self):
		if (self.prev == None):
			return self
		return self.prev.get_start()

	def get_begin(self):
		if (self.node == None):
			return self
		return self.node.get_begin()

	def del_one(self):
		if (self.next == None and self.prev == None):
			return None
		if (self.prev == None):
			self.next.prev = None
			return self.next
		if (self.next == None):
			self.prev.next == None
			return None
		self.next.prev = self.prev
		self.prev.next = self.next
		return self.next

	def get_end(self):
		if (self.next == None):
			return self
		return self.next.get_end()

	def do_node_user_user(self, value, lst):
		if (self.node_user_user == None):
			self.node_user_user = Tlist(value, lst, 1)
		else:
			self.node_user_user.add_next(Tlist(value, lst, 1))

	def do_node_user_hast(self, value, lst):
		if (self.node_user_hast == None):
			self.node_user_hast = Tlist(value, lst, 2)
		else:
			self.node_user_hast.add_next(Tlist(value, lst, 2))

	def do_node_hast_user(self, value, lst):
		if (self.node_hast_user == None):
			self.node_hast_user = Tlist(value, lst, 1)
		else:
			self.node_hast_user.add_next(Tlist(value, lst, 1))

	def do_node_hast_hast(self, value, lst):
		if (self.node_hast_hast == None):
			self.node_hast_hast = Tlist(value, lst, 2)
		else:
			self.node_hast_hast.add_next(Tlist(value, lst, 2))

def read_json(name):
	with open(name, encoding='utf-8') as data_file:
		data = json.loads(data_file.read())
	return (data)

def save_new_json(name, value):
	with open(name, 'w', encoding='utf8') as outfile:
		json.dump(value, outfile)

def save_json(path, di):
	jsonn = json.dumps(di)
	f = open(path,"w")
	f.write(jsonn)
	f.close()

def save(path, txt):
	fichier = open(path, "w")
	fichier.write(txt)
	fichier.close()

def supprimer_dooublon(lst):
	for key,value in lst:
		while (lst.count() > 1):
			lst.remove(value)
	return (lst)

def count_in_list(lst):  
	count = {} 
	for ii in lst: 
		if (ii in count): 
			count[ii] += 1
		else: 
			count[ii] = 1
	count = sorted(count.items(),reverse=True, key=lambda t: t[1])
	return (count)

def rqtt(url, plus):
	auth = OAuth1("PvzeEvDvTXhyRtPxFXFCSOx4U","nix6GtK0Q4HS67BKZHu0VyytMJY6Ecue84t8gEMIqGGotgoVZt","1081910144391368704-LpBgTAo33rIpBT94e0SEr62NLkhGBU","AaRIIJ2KcvhB2j23SP3UybabQ8ZzL4pAAUJAaTIkbwP6z")
	try:
		r = requests.get(url + plus, auth=auth)
	except Exception as e:
		print("rqttt")
		print (e)
	r.encoding = 'ISO-8859-1'
	return (r)

def get_tweets_by_hastag(hastag):
	try:
		url = "https://api.twitter.com/1.1/search/tweets.json?q="
		requette = rqtt(url, "%23" + hastag  + "&tweet_mode=extended")
		json_ret = requette.json().get('statuses')
		return (json_ret)
	except Exception as e:
		print ("get_tweets_by_hast")
		print (e)

def get_tweets_by_hastag_if_count(hastag):
	try:
		url = "https://api.twitter.com/1.1/search/tweets.json?q="
		requette = rqtt(url, "%23" + hastag)
		json_ret = requette.json()
		if (json_ret == None):
			print(requette)
			return None
		if (json_ret.get("search_metadata").get("count") < global_variable.nb_max_hastag):
			return json_ret.get('statuses')
		return None
	except Exception as e:
		print ("get_tweets_by_hastag_if_count,hastag = " + hastag + "RQT CODE" + str(requette) + " ERROR = " + str(e))
		if (requette.json().get("errors")[0].get("code") == 88):
			print ("waiiiiiiit")
			time.sleep(20)
			return get_tweets_by_hastag_if_count(hastag)
	return None 

def get_usr_info(usr):
	tweets = get_tweets_by_usr(usr)
	text = []
	if type(tweets) == list:
		for i in tweets:
			text += find_hast(i.get("full_text"))
	info = {'name' : usr, 'hastag' : count_in_list(text)}
	return (info)

def get_tweets_by_usr(usr):
	try:
		url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="
		requette = rqtt(url, "%40" + usr + "&tweet_mode=extended&exclude_replies=false")
		print (requette)
		json_ret = requette.json()
		return (json_ret)
	except Exception as e:
		print ("get_tweets_by_usr")
		print (e)
		if (requette.json().get("errors")[0].get("code") == 88):
			print ("waiiiiiiit")
			time.sleep(5)
			return get_tweets_by_usr(usr)

def get_follow_by_usr(usr):
	try:
		url = "https://api.twitter.com/1.1/followers/list.json?screen_name="
		requette = rqtt(url, usr)
		json_ret = requette.json()
	except Exception as e:
		print (e)
	return (json_ret)

def find_hast(tweet):
	ret = []
	if tweet == None:
		return None
	try:
		ret = re.findall("#([A-Za-z0-9_]+)", tweet)
		# ret = supprimer_dooublon(ret)
	except Exception as e:
		print ("find hast")
		print (e)
		print (tweet)
	return (ret)

def find_usr(tweet):
	ret = []
	if tweet == None:
		return None
	try:
		ret = re.findall("@([A-Za-z0-9_]+)", tweet)
		#ret = supprimer_dooublon(ret)
	except Exception as e:
		print ("find user")
		print (e)
		print (tweet)
	return (ret)

def get_user(usr):
	url = "https://api.twitter.com/1.1/users/show.json?screen_name="
	r = rqtt(url, usr)
	stt = r.json()
	return (stt)

def check_usr_cerf(usr):
	try:
		url = "https://api.twitter.com/1.1/users/show.json?screen_name="
		r = rqtt(url, usr)
		stt = r.json().get("verified")
		return (stt)
	except Exception as e:
		print (e)
		print ("check usr cert")
	return (False)

def put_without_double(lst_dst, lst_src):
	lst_double = []
	for i in lst_src:
		if i not in lst_dst:
			lst_double.append(i)
	return (lst_double)

def filter(ret):
	tmp = {"user" : [], "hastag" : []}
	tmp['user'] = filtre_user(ret.get('user'))
	tmp['hastag'] = filtre_hastag(ret.get('hastag'))
	return tmp

def filtre_hastag(lst_hastag):
	tmp = []
	for value in lst_hastag:
		if get_tweets_by_hastag_if_count(value) < global_variable.nb_max_hastag:
			tmp.append(value)
	return tmp

def filtre_user(lst_user):
	tmp = []
	for value in lst_user:
		if not check_usr_cerf(value):
			tmp.append(value)
	return tmp

def find_by_usr_special(usr):
	ret = {"user" : [], "hastag" : []}
	json_ret = get_tweets_by_usr(usr)
	if json_ret != None:
		json_ret = json_ret
		for row in json_ret:
			if (type(row) == dict):
				lst_hastag = find_hast(row.get("full_text"))
				lst_usr = find_usr(row.get("full_text"))
				if lst_hastag != None:
					for value in lst_hastag:
						print ("		hastag = " + value)
						ret['hastag'].append(value)
				if lst_usr != None:
					for value in lst_usr:
							if not check_usr_cerf(value):
								print ("		user = " + value)
								ret['user'].append(value)
		return ret

def find_by_usr(usr):
	ret = {"user" : [], "hastag" : []}
	json_ret = get_tweets_by_usr(usr)
	if json_ret != None:
		json_ret = json_ret
		for row in json_ret:
			if (type(row) == dict):
				lst_hastag = find_hast(row.get("full_text"))
				lst_usr = find_usr(row.get("full_text"))
				if lst_hastag != None:
					for value in lst_hastag:
						print ("		hastag = " + value)
						ret['hastag'].append(value)
				if lst_usr != None:
					for value in lst_usr:
						if not check_usr_cerf(value):
							print ("		user = " + value)
							ret['user'].append(value)
		print (ret)
		return ret

def find_by_hast(hastag):
	ret = {"user" : [], "hastag" : []}
	json_ret = get_tweets_by_hastag_if_count(hastag)
	if json_ret != None:
		for row in json_ret:
			if (type(row) == dict):
				lst_hastag =find_hast(row.get("full_text"))
				lst_usr = find_usr(row.get("full_text"))
				if lst_hastag != None:
					for value in lst_hastag:
						print ("		hastag = " + value)
						ret['hastag'].append(value)
				if lst_usr != None:
					lst_usr.append(row.get("user").get("screen_name"))
					for value in lst_usr:
						if not check_usr_cerf(value):
							print ("		user = " + value)
							ret['user'].append(value)
		return ret

def module_de_recherche_by_user(start, i):
	if i <= 0:
		return
	print ("user i = " + str(i))
	for value in list(set(start.ret)):
		tmp = find_by_usr(value)
		if (tmp == None):
			print("Rien Trouvé pour l'user " + value)
		else :
			start.do_node_user_user(value, tmp.get("user"))
			start.do_node_user_hast(value, tmp.get("hastag"))
			node = start.node_user_user
			while (node):
				module_de_recherche_by_user(node, i - 1)
				node = node.next
			node = start.node_user_hast
			while (node):
				module_de_recherche_by_hastag(node, i - 1)
				node = node.next
			node = start.node_hast_user
			while (node):
				module_de_recherche_by_user(node, i - 1)
				node = node.next
			node = start.node_hast_hast
			while (node):
				module_de_recherche_by_hastag(node, i - 1)
				node = node.next

def module_de_recherche_by_hastag(start, i):
	if i == 0:
		return
	print ("hastag i = " + str(i))
	for value in list(set(start.ret)):
		tmp = find_by_hast(value)
		if (tmp == None):
			print("Rien Trouvé pour l'hastag " + value)
		else :
			start.do_node_hast_user(value, tmp.get("user"))
			start.do_node_hast_hast(value, tmp.get("hastag"))
			node = start.node_user_user
			while (node):
				print (node.name)
				module_de_recherche_by_user(node, i - 1)
				node = node.next
			node = start.node_user_hast
			while (node):
				module_de_recherche_by_hastag(node, i - 1)
				node = node.next
			node = start.node_hast_user
			while (node):
				module_de_recherche_by_user(node, i - 1)
				node = node.next
			node = start.node_hast_hast
			while (node):
				module_de_recherche_by_hastag(node, i - 1)
				node = node.nex

def relation_entre_tweet(inpuut, i):
	start = Tlist("algo", [inpuut] , 0)
	if (i == 0):
		for value in start.ret:
			tmp = find_by_usr_special(value)
			print (tmp)
			if (tmp == None):
				print("Rien Trouvé pour l'user " + value)
			else :
				start.do_node_user_user(value, tmp.get("user"))
				start.do_node_user_hast(value, tmp.get("hastag"))
				node = start.node_user_user
				while (node):
					module_de_recherche_by_user(node, 2)
					node = node.next
				node = start.node_user_hast
				while (node):
					module_de_recherche_by_hastag(node, 2)
					node = node.next
				node = start.node_hast_user
				while (node):
					module_de_recherche_by_user(node, 2)
					node = node.next
				node = start.node_hast_hast
				while (node):
					module_de_recherche_by_hastag(node, 2)
					node = node.next
	else:
		for value in start.ret:
			print ("value")
			tmp = find_by_hast(value)
			print (tmp)
			if (tmp == None):
				print("Rien Trouvé pour l'user " + value)
			else :
				start.do_node_hast_user(value, tmp.get("user"))
				start.do_node_hast_hast(value, tmp.get("hastag"))
				node = start.node_user_user
				while (node):
					module_de_recherche_by_user(node, 2)
					node = node.next
				node = start.node_user_hast
				while (node):
					module_de_recherche_by_hastag(node, 2)
					node = node.next
				node = start.node_hast_user
				while (node):
					module_de_recherche_by_user(node, 2)
					node = node.next
				node = start.node_hast_hast
				while (node):
					module_de_recherche_by_hastag(node, 2)
					node = node.next
	return (start)

def get_relation(data):
	ret = {}
	tout_1 = []
	tout_2 = []
	plus_plus = []
	plus_plus_plus = []
	start = data[0].get("BRANCHE_user_user")[0]
	user = data[0].get("liste_return")[0]
	file = []
	file.append([sys.argv[1], "+++", "++", "1", "2", "3"])
	if start.get("BRANCHE_user_user") != None:
		for node in start.get("BRANCHE_user_user"):
			tmp = node.get("liste_return")
			if user in tmp:
				plus_plus_plus.append(node.get("name"))
			tout_1 += tmp
			if node.get("BRANCHE_user_user") != None:
				for node_2 in node.get("BRANCHE_user_user"):
					tmp_2 = node_2.get("liste_return")
					if user in tmp_2:
						plus_plus.append(node_2.get("name"))
					tout_2 += tmp_2
	tout = start.get("liste_return")
	total = list(set(tout + tout_1 + tout_2))
	for value in total:			
		ret[value] = [value, 0, 0, 0, 0, 0]
		if value in plus_plus:
			ret.get(value)[2] += 1
		if value in plus_plus_plus:
			ret.get(value)[1] += 1
	for value in tout:
		if (value != sys.argv[1]):
			ret.get(value)[3] += 1
	for value in tout_1:
		if (value != sys.argv[1]):
			ret.get(value)[4] += 1
	for value in tout_2:
		if (value != sys.argv[1]):
			ret.get(value)[5] += 1
	for value in total:
		# print (ret.get(value))
		file.append(ret.get(value))
	return (file)

def get_tweets_by_usr_2(usr, nb):
	try:
		print ("by user")
		url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="
		requette = rqtt(url, "%40" + usr + "&tweet_mode=extended&count=" + str(nb))
		json_ret = requette.json()
		return (json_ret)
	except Exception as e:
		print (e)
		# if (type(requette) != "undefined"):
		# 	if (requette.json().get("errors")[0].get("code") == 88):
		# 		time.sleep(5)
		# 		return get_tweets_by_usr(usr)
		return None

def get_tweets_by_hastag_2(hastag, nb):
	try:
		print ("by hastag")
		url = "https://api.twitter.com/1.1/search/tweets.json?q="
		requette = rqtt(url, "%23" + hastag  + "&tweet_mode=extended&count=" + str(nb))
		json_ret = requette.json()
		return (json_ret)
	except Exception as e:
		print (e)
		# if (requette.json().get("errors")[0].get("code") == 88):
		# 	time.sleep(5)
		# 	return get_tweets_by_hastag_2(hastag)
		return None

def get_user(value, typee, nb):
	if (typee):
		tweets = get_tweets_by_hastag(value, nb)
	else:
		tweets = get_tweets_by_user(value, nb)

def date_to_int(date):
	return (time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()))

def data_twitter(data):
	return time.mktime(time.strptime(data,'%a %b %d %H:%M:%S +0000 %Y'))
