import asyncio
import timeit
import os
import threading
import requests

def delim():
    print("-----------------------------------------------------------")

def synchronous_requests(urls, responses):
    for i in range(len(urls)):
        responses[i] = requests.get(urls[i])
    return responses

def get(url):
    print("For URL: {0} PID: {1} TID: {2}\n".format( url, os.getpid(), threading.get_ident() ))
    return requests.get(url)

async def asynchronous_requests(urls, data):
    loop = asyncio.get_event_loop()
    futures = [ loop.run_in_executor(None, get, url) for url in urls ]
    for future in futures:
        asyncio.ensure_future(future)
    data = [ None for future in futures ]
    for iter in range(len(futures)):
        data[iter] = await futures[iter]
    return data

urls = [ 'http://localhost:10998/2' for x in range(1) ]
responses = [ 0 for x in range(len(urls))]
start = timeit.default_timer()
responses = synchronous_requests(urls, responses)
end = timeit.default_timer()
print("Time elapsed:",end-start)
for iter in range(len(responses)):
    print("URL: {0} \t Content-Type: {1}".format( urls[iter], responses[iter].headers['Content-Type'] ))

delim()

loop = asyncio.get_event_loop()
responses = []
start = timeit.default_timer()
responses = loop.run_until_complete(asynchronous_requests(urls, responses))
end = timeit.default_timer()
print("Time elapsed:",end-start)
for iter in range(len(responses)):
    print("URL: {0} \t Content-Type: {1}".format( urls[iter], responses[iter].headers['Content-Type'] ))
