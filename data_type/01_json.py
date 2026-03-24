import json

s = """
{
    "sites": [
        {"name": "菜鸟教程", "url": "www.runoob.com"},
        {"name": "google", "url": "www.google.com"},
        {"name": "weibo", "url": "www.weibo.com"}
    ]
}

"""

d = json.loads(s)
print(type(d))
print(d['sites'])
print(d['sites'][0])
print(d['sites'][0]['url'])