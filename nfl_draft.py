from bs4 import BeautifulSoup as bs
import urllib.request
import pandas as pd
import numpy as np # for NaN

"http://www.pro-football-reference.com/play-index/draft-finder.cgi?request=1&year_min=2000&year_max=2016&team_id=dal&draft_round_min=1&draft_round_max=30&draft_slot_min=1&draft_slot_max=500&pick_type=overall&pos=qb&pos=rb&pos=wr&pos=te&pos=e&pos=t&pos=g&pos=c&pos=ol&pos=dt&pos=de&pos=dl&pos=ilb&pos=olb&pos=lb&pos=cb&pos=s&pos=db&pos=k&pos=p&college_id=all&conference_id=any&show=all&order_by=default"

team_list = ['crd','atl','rav','buf','car','chi','cin','cle','dal','den','det','gnb','htx','clt','jax','kan','mia','min','nwe','nor','nyg','nyj','rai','phi','pit','sdg','sea','sfo','ram','tam','oti','was']


def make_url(team, start=2000,end=2016):

	head = 'http://www.pro-football-reference.com/play-index/draft-finder.cgi?request=1&'

	yr_min = 'year_min=' + str(start) + '&'
	yr_max = 'year_max=' + str(end) + '&'
	team = 'team_id=' + team + '&'

	tail = 'draft_round_min=1&draft_round_max=30&draft_slot_min=1&draft_slot_max=500&pick_type=overall&pos=qb&pos=rb&pos=wr&pos=te&pos=e&pos=t&pos=g&pos=c&pos=ol&pos=dt&pos=de&pos=dl&pos=ilb&pos=olb&pos=lb&pos=cb&pos=s&pos=db&pos=k&pos=p&college_id=all&conference_id=any&show=all&order_by=default'

	return head + yr_min + yr_max + team + tail


def get_team_draft(team,start=1994,end=2016):

	team_url = make_url(team,start,end)
	response = urllib.request.urlopen(team_url)
	html = response.read()
	page = bs(html, 'html.parser')
	draft_table = page.tbody
	temp_str = str(draft_table)
	temp_str = temp_str.replace('data-stat', 'datastat')
	draft_table = bs(temp_str, 'html.parser')
	# print(draft_table.get_text())
	pick_list = draft_table.find_all('tr')
	# print(pick_list[0])

	ranker = []
	player_link = []
	
	year_id = []
	draft_round = []
	draft_pick = []
	player = []
	pos = []
	draft_age = []
	year_min = []
	year_max = []
	all_pros_first_team = []
	pro_bowls = []
	years_as_primary_starter = []
	career_av = []
	g = []
	gs = []
	qb_rec = []
	pass_cmp = []
	pass_att = []
	pass_yds = []
	pass_td = []
	pass_int = []
	rush_att = []
	rush_yds = []
	rush_td = []
	rec = []
	rec_yds = []
	rec_td = []
	def_int = []
	sacks = []
	college_id = []
	college_link = []

	td_fields = [year_id, draft_round, draft_pick, player, pos, draft_age, year_min,
				 year_max, all_pros_first_team, pro_bowls, years_as_primary_starter, career_av, g, 
				 gs, qb_rec, pass_cmp, pass_att, pass_yds, pass_td, pass_int, rush_att, rush_yds, 
				 rush_td, rec, rec_yds, rec_td, def_int, sacks, college_id, college_link]

	td_field_names = ['year_id', 'draft_round', 'draft_pick', 'player', 'pos', 'draft_age', 'year_min',
					  'year_max', 'all_pros_first_team', 'pro_bowls', 'years_as_primary_starter', 'career_av', 'g', 
					  'gs', 'qb_rec', 'pass_cmp', 'pass_att', 'pass_yds', 'pass_td', 'pass_int', 'rush_att', 'rush_yds', 
					  'rush_td', 'rec', 'rec_yds', 'rec_td', 'def_int', 'sacks', 'college_id', 'college_link']

	ranker = [s.get_text() for s in draft_table.find_all('th', datastat='ranker')]
	ranker = [y for y in ranker if y != 'Rk']
	player_link = [l.find('a',href=True)['href'] if l.find('a',href=True) is not None else '' for l in draft_table.find_all('td', datastat='player')]	

	# for l in draft_table.find_all('td', datastat='player'):
	# 	print(l.find('a',href=True)['href'])


	for f in range(0,len(td_fields)):
		# td_fields[f] = draft_table.find_all('td', datastat=td_field_names[f])
		td_fields[f] = [s.get_text() for s in draft_table.find_all('td', datastat=td_field_names[f])]

	# print(td_fields[3])
	# print(ranker)
	# print(player_link)
	# for f in td_fields:
	# 	print(len(f), f)
	# print(player)
	# print(len(td_fields[0]))
	# print(len(ranker), ranker)
	# print(len(player_link))
	# print(len(college_id), college_id)

	df = pd.DataFrame(td_fields)
	df = df.transpose()
	df.columns = td_field_names

	df['team'] = team
	# print('team works')
	df['order'] = ranker
	# print('ranker works')
	df['player_link'] = player_link
	# print('player link works')

	# df = pd.DataFrame({'ranker':ranker,
	# 				   'team':team,
	# 				   'draft_year':year_id})
					   # 'draft_round':draft_round,
					   # 'draft_pick':draft_pick,
					   # 'player':player,
					   # 'player_link':player_link,
					   # 'position':pos,
					   # 'draft_age':draft_age,
					   # 'career_start':year_min,
					   # 'career_end':year_max,
					   # '1st_team_all_pro':all_pros_first_team,
					   # 'pro_bowls':pro_bowls,
					   # 'years_as_primary_starter':years_as_primary_starter,
					   # 'career_avg_value':career_av,
					   # 'games_played':g,
					   # 'games_started':gs,
					   # 'qb_record':qb_rec,
					   # 'pass_cmp':pass_cmp,
					   # 'pass_att':pass_att,
					   # 'pass_yds':pass_yds,
					   # 'pass_tds':pass_td,
					   # 'pass_int':pass_int,
					   # 'rush_att':rush_att,
					   # 'rush_yds':rush_yds,
					   # 'rush_tds':rush_td,
					   # 'receptions':rec,
					   # 'rec_yds':rec_yds,
					   # 'rec_tds':rec_td,
					   # 'def_int':def_int,
					   # 'sacks':sacks,
					   # 'college':college_id})

	# print(df.describe())
	# print(df.head())

	return df


def get_all_teams(start, end, filename=None):
	
	first = True
	for t in team_list:
		print(t)
		if first:
			df = get_team_draft(t, start, end)
			first = False
			# print(df.head())
			continue
		
		df2 = get_team_draft(t, start, end)
		df = pd.concat([df, df2])

	if filename:
		df.to_csv(filename, index=True)
		return None

	return df


# get_team_draft('atl',2000,2016)
get_all_teams(2000, 2016, 'draft_history.csv')