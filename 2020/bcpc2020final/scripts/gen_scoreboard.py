import requests

from common import get_head


host = 'http://172.17.238.138'
cid = 1

rank_background = {
	range(1, 10): '#FEE94D',
	range(10, 27): '#E6E6EB',
	range(27, 60): '#D1A17B',
}

head = f'''
{get_head('决赛校内榜单', 1)}

<h1 style="margin-top: 0.5em; text-align: center;">BCPC 2020 决赛校内榜单</h1>

<p id="date">2020 年 12 月 6 日 13:00 — 17:00</p>

<table id="scoreboard">
<caption>榜单</caption>
'''
tail = '''
</table>
</body>
</html>
'''

def get_scoreboard(session, host, cid):
	url = f'{host}/api/v4/contests/{cid}/scoreboard'
	scoreboard = session.get(url)
	return scoreboard.json()

def get_teams(session, host, cid):
	url = f'{host}/api/v4/contests/{cid}/teams'
	teams = session.get(url)
	return teams.json()

def gen_info_cells(team_stat, first_background=None):
	def f(x):
		if f.first:
			f.first = False
			if first_background:
				return '<td style="background: %s;">%s</td>' % (first_background, x)
		return '<td>%s</td>' % x
	f.first = True
	info = [team_stat['rank'], team_stat['team_name'], team_stat['score']['num_solved'], team_stat['score']['total_time']]
	return ''.join(map(f, info))

def gen_prob_cell(prob_stat):
	assert prob_stat['num_pending'] == 0
	stat = ''
	if prob_stat['solved']:
		attempt = f'+{prob_stat["num_judged"] - 1}' if prob_stat['num_judged'] - 1 else '+'
		stat = f'<span class="accepted">{attempt}</span><br />{prob_stat["time"]}'
	elif prob_stat['num_judged']:
		stat = f'<span class="failed">-{prob_stat["num_judged"]}</span>'
	return ''.join([
		'<td style="background: #90EE90;">' if prob_stat['first_to_solve'] else '<td>',
		stat,
		'</td>',
	])

def gen_row(stat, first_background=None):
	res = [gen_info_cells(stat, first_background=first_background)]
	for ps in stat['problems']:
		res.append(gen_prob_cell(ps))
	return '<tr>%s</tr>' % ''.join(res)

def gen_head_row(problems):
	info = ['#', 'Who', '=', 'Penalty', *sorted(problems)]
	return ''.join(map(lambda x: '<th>%s</th>' % x, info))

def main():
	global host, cid, rank_background, head, tail

	session = requests.Session()

	teams = get_teams(session, host, cid)
	scoreboard = get_scoreboard(session, host, cid)

	team_names = {i['id']: i['name'] for i in teams}

	for r in scoreboard['rows']:
		r['team_name'] = team_names[r['team_id']]

	problems = set()

	for r in scoreboard['rows']:
		for p in r['problems']:
			p['label'] = p['label'].upper().strip()
			if p['label'] == 'Z':
				continue
			problems.add(p['label'])

	for r in scoreboard['rows']:
		r['problems'] = sorted(
			filter(
				lambda i: i['label'] in problems,
				r['problems']
			),
			key=lambda i: ord(i['label'])
		)

	print(head)

	print('<thead>')
	print(gen_head_row(problems))
	print('</thead>')

	print('<tbody>')
	for r in scoreboard['rows']:
		bg = None
		for k, v in rank_background.items():
			if r['rank'] in k:
				bg = v
				break
		print(gen_row(r, bg))
	print('</tbody>')

	print(tail)


if __name__ == '__main__':
	main()
