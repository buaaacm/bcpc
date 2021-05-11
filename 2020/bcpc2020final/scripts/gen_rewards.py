import requests

from common import get_head


host = 'http://172.17.238.138'
cid = 1

rank_reward = {
	range(1, 2): ('冠军', '#FEE94D'),
	range(2, 3): ('亚军', '#E6E6EB'),
	range(3, 4): ('季军', '#D1A17B'),
	range(4, 10): ('一等奖', '#FFFFFF'),
	range(10, 27): ('二等奖', '#EFEFEF'),
	range(27, 60): ('三等奖', '#DFDFDF'),
}

head = f'''
{get_head('决赛获奖名单', 0)}

<div class="container">
<div class="row justify-content-md-center">
<div class="col-md-auto">

<h1 style="margin-top: 0.5em;">BCPC 2020 决赛获奖名单</h1>

<div class="float-end">
<a class="text-muted" href="bcpc2020final-rewards.xlsx">XLSX 格式</a>
</div>

<table class="table">
<thead>
<tr>
<th scope="col">排名</th>
<th scope="col">学号</th>
<th scope="col">姓名</th>
<th scope="col">奖项</th>
</tr>
</thead>
<tbody>
'''
tail = '''
</tbody>
</table>
</div>
</div>
</div>
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

def gen_info_cells(team_stat):
	def f(x):
		if f.first:
			f.first = False
			return '<th scope="row">%s</th>' % x
		return '<td>%s</td>' % x
	f.first = True
	bg_color = team_stat['bg']
	info = map(team_stat.get, ['rank', 'student_id', 'name', 'reward'])
	info = ''.join(map(f, info))
	if bg_color:
		return '<tr style="background-color: %s;">%s</tr>' % (bg_color, info)
	return '<tr>%s</tr>' % info


def main():
	global host, cid, rank_background, head, tail

	session = requests.Session()

	teams = get_teams(session, host, cid)
	scoreboard = get_scoreboard(session, host, cid)

	team_names = {i['id']: i['name'] for i in teams}

	for r in scoreboard['rows']:
		r['team_name'] = team_names[r['team_id']]
		r['student_id'], r['name'] = r['team_name'].split('-')
		for k, v in rank_reward.items():
			if r['rank'] in k:
				r['reward'], r['bg'] = v
				break

	print(head)

	for r in scoreboard['rows']:
		if r.get('reward', None):
			print(gen_info_cells(r))

	print(tail)


if __name__ == '__main__':
	main()
