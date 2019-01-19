from algo import *

app = Flask(__name__)

@app.route("/")
def get_home():
	return (render_template("index.html"))

@app.route("/tweet_hast/<hastag>/<nb>")
def get_last_tweet_by_h(hastag, nb):
	ret = {"return" : []}
	if (json_ret == None):
		return Response(response=json.dumps({"errors": "jsp"}), status=401, mimetype='application/json')
	json_ret = get_tweets_by_hastag_2(hastag, nb)
	for tweet in json_ret.get('status'):
		tmp = {}
		tmp['id'] = tweet.get("id")
		tmp['name'] = tweet.get("user").get("name")
		tmp['screnn_name'] = tweet.get("user").get("screnn_name")
		tmp['date'] = tweet.get("created_at")
		ret.append(tweet.get("full_text"))
	ret['next'] = json_ret.get('search_metadata').get("refresh_url")
	return Response(response=json.dumps(ret), status=200, mimetype='application/json')
 
@app.route("/tweet_user/<user>/<nb>")
def get_last_tweet_by_user(user, nb):
	ret = {"return" : []}
	json_ret = get_tweets_by_usr_2(user, nb)
	if (json_ret == None):
		return Response(response=json.dumps({"errors": "jsp"}), status=401, mimetype='application/json')
	for tweet in json_ret:
		print (tweet)
		tmp = {"id" : "", "name" : "", "screnn_name" : "", "date" : "", "return" : ""}
		tmp['idd'] = tweet.get("id")
		tmp['name'] = tweet.get("user").get("name")
		tmp['screnn_name'] = tweet.get("user").get("screnn_name")
		tmp['date'] = tweet.get("created_at")
		ret['return'].append(tweet.get("full_text"))
	return Response(response=json.dumps(ret), status=200, mimetype='application/json')

@app.route("/relation/<value>/<typee>")
def relation(value, typee):
	ret = relation_entre_tweet(value, int(typee)).get_json()
	print (ret)
	return Response(response=json.dumps(ret), status=200, mimetype='application/json')

@app.route("/graph_value/<value>/<typee>/<nb>")
def graph_value(value, typee, nb):
	nb = int(nb)
	tout = {"return" : []}
	data = {"labels" : [], "data" : []}
	ret = []
	i = 0
	if (typee == "1"):
		tweets = get_tweets_by_usr_2(value, nb)
	else :
		tweets = get_tweets_by_hastag_2(value, nb)
		if (tweets != None):
			tweets = tweets.get("statuses")
	if (tweets == None):
		print ("SALOPEEEE")
		return Response(response=json.dumps({"errors": "jsp"}), status=401, mimetype='application/json')
	date = data_twitter(tweets[0].get("created_at"))
	for tweet in tweets:
		tmp = {"id" : "", "name" : "", "screnn_name" : "", "date" : "", "return" : ""}
		tmp['idd'] = tweet.get("id")
		tmp['name'] = tweet.get("user").get("name")
		tmp['screnn_name'] = tweet.get("user").get("screnn_name")
		tmp['t_date'] = tweet.get("created_at")
		tmp['date'] = data_twitter(tweet.get("created_at"))
		tmp['return'] = tweet.get("full_text")
		i += 1
		tout['return'].append(tmp)
	a = i / 20
	date_end = data_twitter(tweets[-1].get("created_at"))
	t = (date - date_end) / a
	print (" 		a = "  + str(a))
	print (" 		t = "  + str(t))
	print (" 		date = "  + str(date))
	print (" 		date_end = "  + str(date_end))
	value = 0
	tmp_2 = []
	while (value < a):
		data['labels'].append(value)
		value += 1
	value = 0
	for tweet in tout.get("return"):
		print ("comparer value = " + str(tweet.get("date")) + " value 2 = " + str(date + (t * value)))
		if (tweet.get("date") < (date_end + (t * value))):
			tmp_2.append(tweet)
		else :
			t += 1
			data["data"].append(len(tmp_2))
			# print (tmp_2)
			tmp_2 = []
			tmp_2.append(tweet)
			value += 1
	# print (tmp_2)
	print (data)
	return Response(response=json.dumps({"errors": "jsp"}), status=402, mimetype='application/json')

@app.route("/research/<value>")
def research(value):
	data = read_json("json.json")
	start = data[0].get("BRANCHE_user_user")[0]
	if start.get("BRANCHE_user_user") != None:
		for node in start.get("BRANCHE_user_user"):
			tmp = node.get("liste_return")
			tout_1 += tmp
			if node.get("BRANCHE_user_user") != None:
				for node_2 in node.get("BRANCHE_user_user"):
					tmp_2 = node_2.get("liste_return")
					tout_2 += tmp_2
	tout = start.get("liste_return")
	total = list(set(tout + tout_1 + tout_2))

print (__name__)
if __name__ == '__main__':
	app.run(debug=True)