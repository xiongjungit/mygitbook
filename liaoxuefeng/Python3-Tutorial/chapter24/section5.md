#24-5 Day 5 - 编写Web框架

在正式开始Web开发前，我们需要编写一个Web框架。

aiohttp已经是一个Web框架了，为什么我们还需要自己封装一个？

原因是从使用者的角度来说，aiohttp相对比较底层，编写一个URL的处理函数需要这么几步：

第一步，编写一个用@asyncio.coroutine装饰的函数：

	@asyncio.coroutine
		def handle_url_xxx(request):
		    pass
第二步，传入的参数需要自己从request中获取：

	url_param = request.match_info['key']
	query_params = parse_qs(request.query_string)
最后，需要自己构造Response对象：

	text = render('template', data)
	return web.Response(text.encode('utf-8'))
这些重复的工作可以由框架完成。例如，处理带参数的URL/blog/{id}可以这么写：

	@get('/blog/{id}')
	def get_blog(id):
	    pass
处理query_string参数可以通过关键字参数**kw或者命名关键字参数接收：

	@get('/api/comments')
	def api_comments(*, page='1'):
	    pass
对于函数的返回值，不一定是web.Response对象，可以是str、bytes或dict。

如果希望渲染模板，我们可以这么返回一个dict：

	return {
	    '__template__': 'index.html',
	    'data': '...'
	}
因此，Web框架的设计是完全从使用者出发，目的是让使用者编写尽可能少的代码。

编写简单的函数而非引入request和web.Response还有一个额外的好处，就是可以单独测试，否则，需要模拟一个request才能测试。

##@get和@post

要把一个函数映射为一个URL处理函数，我们先定义@get()：

	def get(path):
	    '''
	    Define decorator @get('/path')
	    '''
	    def decorator(func):
	        @functools.wraps(func)
	        def wrapper(*args, **kw):
	            return func(*args, **kw)
	        wrapper.__method__ = 'GET'
	        wrapper.__route__ = path
	        return wrapper
	    return decorator
这样，一个函数通过@get()的装饰就附带了URL信息。

@post与@get定义类似。

##定义RequestHandler

URL处理函数不一定是一个coroutine，因此我们用RequestHandler()来封装一个URL处理函数。

RequestHandler是一个类，由于定义了__call__()方法，因此可以将其实例视为函数。

RequestHandler目的就是从URL函数中分析其需要接收的参数，从request中获取必要的参数，调用URL函数，然后把结果转换为web.Response对象，这样，就完全符合aiohttp框架的要求：

	class RequestHandler(object):
	
	    def __init__(self, app, fn):
	        self._app = app
	        self._func = fn
	        ...
	
	    @asyncio.coroutine
	    def __call__(self, request):
	        kw = ... 获取参数
	        r = yield from self._func(**kw)
	        return r
再编写一个add_route函数，用来注册一个URL处理函数：

	def add_route(app, fn):
	    method = getattr(fn, '__method__', None)
	    path = getattr(fn, '__route__', None)
	    if path is None or method is None:
	        raise ValueError('@get or @post not defined in %s.' % str(fn))
	    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
	        fn = asyncio.coroutine(fn)
	    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
	    app.router.add_route(method, path, RequestHandler(app, fn))
最后一步，把很多次add_route()注册的调用：

	add_route(app, handles.index)
	add_route(app, handles.blog)
	add_route(app, handles.create_comment)
	...
变成自动扫描：

	# 自动把handler模块的所有符合条件的函数注册了:
	add_routes(app, 'handlers')
add_routes()定义如下：

	def add_routes(app, module_name):
	    n = module_name.rfind('.')
	    if n == (-1):
	        mod = __import__(module_name, globals(), locals())
	    else:
	        name = module_name[n+1:]
	        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
	    for attr in dir(mod):
	        if attr.startswith('_'):
	            continue
	        fn = getattr(mod, attr)
	        if callable(fn):
	            method = getattr(fn, '__method__', None)
	            path = getattr(fn, '__route__', None)
	            if method and path:
	                add_route(app, fn)
最后，在app.py中加入middleware、jinja2模板和自注册的支持：

	app = web.Application(loop=loop, middlewares=[
	    logger_factory, response_factory
	])
	init_jinja2(app, filters=dict(datetime=datetime_filter))
	add_routes(app, 'handlers')
	add_static(app)
##middleware

middleware是一种拦截器，一个URL在被某个函数处理前，可以经过一系列的middleware的处理。

一个middleware可以改变URL的输入、输出，甚至可以决定不继续处理而直接返回。middleware的用处就在于把通用的功能从每个URL处理函数中拿出来，集中放到一个地方。例如，一个记录URL日志的logger可以简单定义如下：

	@asyncio.coroutine
	def logger_factory(app, handler):
	    @asyncio.coroutine
	    def logger(request):
	        # 记录日志:
	        logging.info('Request: %s %s' % (request.method, request.path))
	        # 继续处理请求:
	        return (yield from handler(request))
	    return logger
而response这个middleware把返回值转换为web.Response对象再返回，以保证满足aiohttp的要求：

	@asyncio.coroutine
	def response_factory(app, handler):
	    @asyncio.coroutine
	    def response(request):
	        # 结果:
	        r = yield from handler(request)
	        if isinstance(r, web.StreamResponse):
	            return r
	        if isinstance(r, bytes):
	            resp = web.Response(body=r)
	            resp.content_type = 'application/octet-stream'
	            return resp
	        if isinstance(r, str):
	            resp = web.Response(body=r.encode('utf-8'))
	            resp.content_type = 'text/html;charset=utf-8'
	            return resp
	        if isinstance(r, dict):
	            ...
有了这些基础设施，我们就可以专注地往handlers模块不断添加URL处理函数了，可以极大地提高开发效率。

##参考源码

[day-05](https://github.com/michaelliao/awesome-python3-webapp/tree/day-05)