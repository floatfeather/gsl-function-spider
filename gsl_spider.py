from bs4 import BeautifulSoup
import requests
import Queue

components = ['Complex Numbers', 'Polynomials', 'Special Functions', 'Linear Algebra', 
'Eigensystems', 'Fast Fourier Transforms', 'Numerical Integration', 'Statistics',
'Discrete Hankel Transforms', 'Least-Squares Fitting', 'Nonlinear Least-Squares Fitting', 'Basis Splines']
com_set = set(components)

gsl_home = 'http://www.gnu.org/software/gsl/manual/html_node/'
work_list = Queue.Queue()
func_map = {}

def parse_home_table(table):
	for entry in table :
		label = entry.td.a.string
		if label in com_set :
			url_part2 = entry.td.a['href']
			new_url = gsl_home + url_part2
			work_list.put({'url': new_url, 'comp': label})

def parse_table(label, table):
	for entry in table :
		url_part2 = entry.td.a['href']
		new_url = gsl_home + url_part2
		work_list.put({'url': new_url, 'comp': label})

r = requests.get(url=gsl_home)
top = BeautifulSoup(r.text, 'html.parser');

# Get list
l = top.find_all('tr')
parse_home_table(l)

while not work_list.empty() :
	cur_ele = work_list.get()
	cur_url = cur_ele['url']
	print(cur_url)
	r = requests.get(url = cur_url)
	cur = BeautifulSoup(r.text, 'html.parser')
	menu = cur.find_all('table', 'menu')
	for each_menu in menu:
		parse_table(cur_ele['comp'], each_menu.find_all('tr'))
	function_lists = cur.find_all('dl')
	for function_list in function_lists:
		function_group = function_list.find_all('dt')
		for func in function_group:
			if func.strong == None:
				break
			name = func.strong.string
			others = func.find_all('em')
			if len(others) != 2:
				break
			rettype = others[0].string
			params = ''
			for param in others[1].contents:
				params += param.string
			func_decl = rettype + ' ' + name + params
			if not func_map.has_key(cur_ele['comp']):
				func_map[cur_ele['comp']] = []
			func_map[cur_ele['comp']].append(func_decl)

for comp in components:
	if func_map.has_key(comp):
		f = open(comp + '.txt', 'a')
		for func_decl in func_map[comp]:
			f.write(func_decl + '\n')
		f.close()
	





