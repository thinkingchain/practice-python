
import requests  as req

url ="https://baidu.com/"

#本地代理
proxies = {'http' : '127.0.0.1:7890','https' : '127.0.0.1:7890'}
response  = req.get(url, proxies=proxies)

print(response.content)
