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
product_publisher[2](data2, lambda data_event: {"data": data_event["data"] + 100})
while True:
  pass