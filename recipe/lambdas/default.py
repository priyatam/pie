import pystache


def hello_world(text):
    return "Hello %s from Frozen Pie" % text

def posts(text):
    data = [ {
               'post_date': '2010-01-01',
               'name': 'test-name-1',
               'title': 'Test Name 1' },
               {
               'post_date': '2011-01-01',
               'name': 'test-name-1',
               'title': 'Test Name 1' }
           ]
    return pystache.render(text, data)