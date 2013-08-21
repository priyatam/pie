import pystache

def hello_world(text):
    return "Hello %s from Frozen Pie" % text

def all_posts(text):
    posts = [ content for content in contents if content["type"] == "blog" ]
    return pystache.render(text, { "posts": posts })
