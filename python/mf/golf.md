### assign ###

變數給初始值

	# beginner python
	a = 0
	b = 0
	c = 0

	# proper python
	a, b, c = 0, 0, 0

	# code golf
	a = b = c = 0

	# beginner python
	a = 'a'
	b = 'b'
	c = 'c'

	# proper python
	a, b, c = 'a', 'b', 'c'

	# code golf
	a, b, c= 'abc'


### if else ###

	# beginner python
	if a < 0:
		b = 2 * a
	else:
		b = 3 * a

	# proper python
	b = 2 * a if a < 0 else 3 * a

	# code golf 1
	b = a < 0 and 2 * a or 3 * a
	# code golf 2 
	b = a * (3, 2)[a<0]


### reverse list ###

[1, 2, 3, 4] => [4, 3, 2, 1]

	l = [1, 2, 3, 4]
	l[::-1] # 只有回傳值改變, 但變數本身不變
	l.reverse() # 回傳值和變數本身皆改變


### combine two list ###

[a, b, c, d] + [1, 2, 3, 4] => [a1, b2, c3, d4]

	a = list("abcd")
	b = list("1234")

	[x+y for x, y in zip(a,b)]
	map(lambda x, y: x+y, a, b)
	map("".join, zip(a, b))
	map(str.__add__, a, b)


### 2D list ###

[[1, 2, 3], [4, 5, 6], [7, 8, 9]] => [[1, 4, 7], [2, 5, 8], [3, 6, 9]]


	# beginner python
	l1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	l2 = []
	for col in range(len(l1[0])):
		tmp = []
		for raw in l1:
			tmp.append(raw[col])
		l2.append(tmp)

	# proper python
	l1 = [[1+ x + 3 * y for x in range(3)] for y in range(3)]
	l2 = [[row[col] for row in l1] for col in range(len(l1[0]))]

	# code golf
	l1 = [[1+ x + 3 * y for x in range(3)] for y in range(3)]
	l2 = map(list, zip(*l1))


### function loop ###

	l1 = [1,2,3]
	l2 = [4,5,6]

	def f1(x):
		return 10 * x

	def f2(x,y):
		return 10 * x + y

	# beginner python
	tmp = []
	for x in l1:
		tmp.append(f1(x))
	print tmp

	tmp = []
	for i in range(len(l1)):
		tmp.append(f2(l1[i], l2[i]))
	print tmp

	# proper python
	print [f1(x) for x in l1]
	print [f2(l1[_], l2[_]) for _ in range(len(l1))]

	# code golf
	print map(f1, l1)
	print map(f2, l1, l2)

	print map(lambda x: 10 * x, l1)
	print map(lambda x, y: 10 * x + y, l1, l2)
