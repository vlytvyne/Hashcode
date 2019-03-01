def read_input(file):
	horizontal = []
	vertical = []
	i = 0
	with open(file, 'r') as f:
		f.readline()
		for line in f:
			tokens = line.split(' ')
			item = {}
			item['id'] = i
			item['tags'] = tokens[2:]
			item['tags'][-1] = item['tags'][-1].strip()
			item['tags'] = set(item['tags'])
			if tokens[0] == 'H':
				item['isHorizontal'] = True
				horizontal.append(item)
			else:
				vertical.append(item)
			i += 1
	return horizontal, vertical

def generate_pairs(vertical):
	result = []
	i = 0
	length = len(vertical)
	while i < length:
		j = i + 1
		while j < length:
			item = {}
			item['isHorizontal'] = False
			item['elems'] = [vertical[i], vertical[j]]
			item['tags'] = vertical[i]['tags'].union(vertical[j]['tags'])
			result.append(item)
			j += 1
		i += 1
	return result

def get_score(slide1, slide2):
	s1 = slide1['tags']
	s2 = slide2['tags']
	inter = len(s1.intersection(s2))
	diff1 = len(s1.difference(s2))
	diff2 = len(s2.difference(s1))
	return min(inter, diff1, diff2)

def find_biggest_score(slide, unsed_slides):
	score = 0
	target = slide
	for sl in unsed_slides:
		score_now = get_score(slide, sl)
		if score < score_now:
			score = score_now
			target = sl
	return score, target

def remove_slide(slide, unsed_slides):
	if slide['isHorizontal']:
		unsed_slides.remove(slide)
	else:
		for sl in unsed_slides:
			if sl is slide:
				unsed_slides.remove(sl)

def get_id(slide):
	if slide['isHorizontal']:
		return slide['id']
	else:
		return [slide['elems'][0]['id'], slide['elems'][1]['id']]

def print_result(result):
	print(len(result))
	for ids in result:
		if type(ids) is list:
			print("{} {}".format(ids[0], ids[1]))
		else:
			print(ids)

horizontal, vertical = read_input('a.txt')
pairs = generate_pairs(vertical)
unsed_slides = horizontal
unsed_slides.extend(pairs)

result = []
left_slide = unsed_slides[0]
score_r, right_slide = find_biggest_score(left_slide, unsed_slides)
result.append(get_id(left_slide))
result.append(get_id(right_slide))
remove_slide(left_slide, unsed_slides)
remove_slide(right_slide, unsed_slides)

while len(unsed_slides) > 0:
	score_l, ls = find_biggest_score(left_slide, unsed_slides)
	score_r, rs = find_biggest_score(right_slide, unsed_slides)
	if score_l > score_r:
		remove_slide(ls, unsed_slides)
		result.append(get_id(ls))
		left_slide = ls
	else:
		remove_slide(rs, unsed_slides)
		result.append(get_id(rs))
		right_slide = rs
		
print_result(result)