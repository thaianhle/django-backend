
from ast import Dict
import asyncio
from collections import deque
from threading import Lock
from typing import Annotated, List, Protocol
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import concurrent.futures
def notify():
  pass

async def worker(q: deque, cond: asyncio.Condition):
  pass

def on_hook(type, func):
  pass


def register_publisher():
  pass
def register_subscriber():
  pass

def unregister_publisher():
  pass


key_partition = ["get", "create", "delete", "filter", "update"]


def worker(publisher_name: str, subscriber: str, new_data: any, id_new, id_old, observer):
  old_data, observer_func = observer
  print("old address: ", id_old, " new address: ", id_new)
  if old_data != new_data and id_old == id_new:
    observer_func(publisher_name, subscriber, new_data)
  return
def new_system(cpu_core: int=2):
  executor = ProcessPoolExecutor(max_workers=cpu_core)
  def publisher(publisher_name: str):
    map_subscriber = {}
    lock_map_subscriber = Lock()
    """
    register_subscriber
    """
    def register_subscriber(subscriber_name: str, observers):
      with lock_map_subscriber:
        if subscriber_name not in map_subscriber:
          map_subscriber[subscriber_name] = []
        
        for observer in observers:
          address_old_data = id(observer[0])
          map_subscriber[subscriber_name].append((worker, address_old_data, observer))

  
    def update_data(data_address, func_update):
      #print("update")
      new_data = func_update(data_address)
      with executor as exc:
        futures = []
        for subscriber in map_subscriber:
          for stream in map_subscriber[subscriber]:
            worker_func, old_address, observer = stream
            futures.append(exc.submit(worker_func, publisher_name, subscriber, new_data, id(data_address), old_address, observer))
          
        for future in concurrent.futures.as_completed(futures):
          future.result()
      return
    def unregister_subscriber(name: str):
      pass
    return (register_subscriber, unregister_subscriber, update_data)
  return publisher

def on_listen(publisher, subscriber, data: any):
  v = f"[Subscriber-{subscriber}] received from [Publisher-{publisher}], new_data: {data}"
  print(v)

system = new_system(cpu_core=2)
product_publisher = system("product")
data1 = {"data": 5}
data2 = {"data": 10}
print("address data 1:" , id(data1))
product_publisher[0]("product_type", [(data1, on_listen)])
product_publisher[0]("aggregate_price", [(data2, on_listen)])
n = 10


with ThreadPoolExecutor(max_workers=100) as exec:
  while True:
    new_futures = []
    for i in range(n, n+5):
      futures = exec.submit(product_publisher[2], data1, lambda event: {"data": event["data"] + i})

  

    for new_future in concurrent.futures.as_completed(new_futures):
      new_future.result()
    n += 5
    #print(n)

