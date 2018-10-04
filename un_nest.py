def un_nest(l):
	for el in l:
		if isinstance(el, int):
			yield el
		elif isinstance(el, list):
			yield from un_nest(el)