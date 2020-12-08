nav = [
	('rewards.html', '决赛获奖名单'),
	('scoreboard.html', '决赛校内榜单'),
	('scoreboard_extern.html', '决赛校外榜单'),
]

def get_nav_content(active_index):
	res = []
	for i in range(len(nav)):
		href, text = nav[i]
		if i == active_index:
			res.append(f'''
<li class="nav-item">
<a class="nav-link active" aria-current="page" href="#">{text}</a>
</li>
''')
		else:
			res.append(f'''
<li class="nav-item">
<a class="nav-link" aria-current="page" href="{href}">{text}</a>
</li>
''')
	return ''.join(res)

def get_head(title, active_index):
	nav_content = get_nav_content(active_index)
	head = f'''
<!DOCTYPE html>
<html lang="zh-cn">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>BCPC 2020 决赛 - {title}</title>

  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
  <link rel="stylesheet" href="scoreboard.css">

</head>
<body>

<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container">
    <a class="navbar-brand" href="https://buaaacm.com/bcpc/">BCPC 2020</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav ms-auto">
      	{nav_content}
      </ul>
    </div>
  </div>
</nav>
'''
	return head
