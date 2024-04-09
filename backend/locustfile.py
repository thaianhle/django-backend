from locust import HttpUser, task

class ProductAPITest(HttpUser):
  
  @task
  def get_all_product_type(self):
    self.client.get(
      url="/api/product_type/get/8ce67ba5-b607-45eb-98d4-004ecd9c9cdd")
      #url="/api/cms/context/vehicle_type/get/vehicle_type/get")