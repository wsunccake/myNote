### class ###

使用不方式宣告 class

	class C1:
		def __init__(self):
			self.x = 4

		y = 5

		def z(self, word):
			return 'Hi {}'.format(word)

	def say(self, word):
		return 'Hi {}'.format(word)

	C2 = type('C2', (), {'x': 4, 'y': 5, 'z': say})
	C3 = type('C3', (), dict(x=4, y=5, z=say))

	c1 = C1()
	c2 = C2()
	c3 = C3()


### getattr, setattr ###

getattr, setattr 能更動態的設定 class method 或 attribute

	class Person:
		def __init__(self, name):
			self.name = name

		def getName(self):
			return self.name

	def setName(self, name):
		self.name = name

	person = Person('Tim')

	# setattr
	setattr(person, 'age', 10) 
	print person.age

	setattr(Person, 'setName', setName)
	p = Person('John')
	print p.name
	p.setName('Johnie')
	print p.name

	# getattr
	print getattr(Person, 'getName')

	print getattr(person, 'getName')
	print getattr(person, 'name')
	print person.name
	print getattr(person, 'getName')()
	print person.getName()


### instancecheck, subclasshook ###

subclasshook 和 instancecheck 是 python 用來定義 isinstance 的 method, subclasshook 是用來檢查 instance 是否為自定義 sub class. instancecheck 則是檢查 instance 為自定義 class

	import abc

	class Foo(object):
		__metaclass__ = abc.ABCMeta

		@classmethod
		def __instancecheck__(cls, instance):
			print "run instance"
			return hasattr(instance, 'x')

		__metaclass__.__instancecheck__ = __instancecheck__

		@classmethod
		def __subclasshook__(cls, instance):
			print "run subclasshook"
			return hasattr(instance, 'y')

		def x(self): return 5

	class Bar(object):
		def x(self): return 5
		def y(self): return 7

	class Ash(Foo):
		def z(self): return 0

	f = Foo()
	b = Bar()
	a = Ash()

	print "f, Foo"
	print isinstance(f, Foo)
	print issubclass(f, Foo)

	print "b, Foo"
	print isinstance(b, Foo)
	print issubclass(b, Foo)

	print "a, Foo"
	print isinstance(a, Foo)
	print issubclass(a, Foo)

other example

	import abc
	def interface(*attributes):
		def decorator(Base):

			def checker(Other):
				return all(hasattr(Other, a) for a in attributes)

			def __subclasshook__(cls, Other):
				print "run shbclasshook"
				if checker(Other):
					return True
				return NotImplemented

			def __instancecheck__(cls, Other):
				print "run installcheck"
				return checker(Other)

			Base.__subclasshook__ = classmethod(__subclasshook__)
			Base.__metaclass__.__instancecheck__ = classmethod(__instancecheck__)
			return Base

		return decorator

	@interface("x", "y")
	class Foo(object):
		__metaclass__ = abc.ABCMeta
		def x(self): return 5
		def y(self): return 10

	class Bar(object):
		def x(self): return "blah"
		def y(self): return "blah"

	class Baz(object):
		def __init__(self):
			self.x = "blah"
			self.y = "blah"

	class attrdict(dict):
		def __getattr__(self, attr):
			return self[attr]

	f = Foo()
	b = Bar()
	z = Baz()
	t = attrdict({"x":27.5, "y":37.5})

	print isinstance(f, Foo)
	print isinstance(b, Foo)
	print isinstance(z, Foo)
	print isinstance(t, Foo)

metaclass 則是用 instancecheck


### with ###

在 with block 裡面, 開始會執行 __enter__, 最後會執行 __exit__, 即使有 exception, 仍然會執行 __exit__

`with 範例`

	class Foo(object):
		def __init__(self):
			print "init"
		def __enter__(self):
			print "enter"
		def __exit__(self, type, value, traceback):
			print "exit"

	with Foo():
		print "with"
		raise Exception

`with as 範例`

	class Foo(object):
		def __init__(self):
			pass

		def __enter__(self):
			print "setting count to 0"
			self.count = 0
			return self

		def __exit__(self, type, value, traceback):
			print "count is now: %d" % self.count
	
		def incr(self):
			self.count += 1

	with Foo() as baz:
		print baz
		for i in range(4):
			baz.incr()


### iterator ###

iterator 用來自定義 class 迭代方式

	class PowTwo:
		def __init__(self, max=0):
			self.max = max

		def __iter__(self):
			self.n = 0
			return self

		def next(self): # for python 2.x
		# def __next__(self): # for python 3.x
			if self.n <= self.max:
				result = 2 ** self.n
				self.n += 1
				return result
			else:
				raise StopIteration

	my_class = PowTwo(3)
	for i in my_class:
		print i


### decorator ###

	import functools
	
	def greet(function):
		@functools.wraps(function)
		def wrapper(name):
			print 'Hello'
			return function(name)
		return wrapper

	def greet_someone1(someone):
		print someone
	greet_someone1 = greet(greet_someone1)

	@greet
	def greet_someone2(someone):
		print someone

	def greet_something(word):
		def decorator(function):
			@functools.wraps(function)
			def wrapper(name):
				print word
				return function(name)
			return wrapper
		return decorator

	def greet_someone3(someone):
		print someone
	tmp_function = greet_something('Hey')
	greet_someone3 = tmp_function(greet_someone3)

	@greet_something('Hi')
	def greet_someone4(someone):
		print someone

	greet_someone1('John')
	print greet_someone1.func_name
	greet_someone2('Mary')
	print greet_someone2.func_name
	greet_someone3('Bill')
	print greet_someone3.func_name
	greet_someone4('Jean')
	print greet_someone4.func_name

greet 為不帶參數的 function (而參數中的 function, 是要做 decorator), 因為回傳 closure function. greet_someone1 為一般使用方式; greet_some2 使用 python 特有的 syntax. greet_something 是帶參數的 function (參數中的 someone是要帶入的參數, 真的做 decorator 為內部另外定義 decorator)


### property ###

	class Ball1: 
		def __init__(self, radius): 
			self.setRadius(radius) 

		def getRadius(self): 
			return self.__radius 

		def setRadius(self, radius): 
			if radius <= 0: 
				raise ValueError('{} must be positive'.format(radius)) 
			self.__radius = radius 

	class Ball2: 
		def __init__(self, radius): 
			self.setRadius(radius) 

		def getRadius(self): 
			return self.__radius 

		def setRadius(self, radius): 
			if radius <= 0: 
				raise ValueError('{} must be positive'.format(radius)) 
			self.__radius = radius 

		def delRadius(self): 
			del self.__radius 

		radius = property(getRadius, setRadius, delRadius, 'radius property') 

	class Ball3: 
		def __init__(self, radius): 
			self.__radius = radius 

		@property 
		def radius(self): 
			return self.__radius 

		@radius.setter 
		def radius(self, radius): 
			if radius <= 0: 
				raise ValueError('{} must be positive'.format(radius)) 
			self.__radius = radius 

		@radius.deleter 
		def radius(self): 
			del self.__radius 

	print ('b1: ') 
	b1 = Ball1(1) 
	print (b1.getRadius()) 
	b1.setRadius(5) 
	print (b1.getRadius()) 

	print ('b2: ') 
	b2 = Ball2(1) 
	print ('get: {}, {}'.format(b2.getRadius(), b2.radius)) 
	b2.setRadius(5) 
	print ('get: {}, {}'.format(b2.getRadius(), b2.radius)) 
	b2.radius = 4 
	print ('get: {}, {}'.format(b2.getRadius(), b2.radius)) 

	print ('b3: ') 
	b3 = Ball3(1) 
	print b3.radius 
	# b3.radius = -1 # 帶入負值會錯誤

property 是 decorator, 用以簡化 getter, setter, delter method 使用方式
