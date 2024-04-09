from django.contrib import messages
from django.db import models
import uuid
from typing import Any, Iterable
import json
from django_jsonform.models.fields import JSONField as JSONFORMFIELD
from pydantic import ValidationError

from .serializers import ProductTypeSerializer

#json_data = {"fields": [{"name": "color", "options": [{"value": "red"}, {"value": "blue", "required": True}]}]}
#v = ProductFields(**json_data)
#breakpoint()

cache = {}
class ProductTypeJSONFIELDCUSTOM(models.JSONField):
    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        db_val = super().from_db_value(value, expression, connection)
        if db_val is None:
            return ""
        
        #print("get db_val here: ", db_val)
        #print("get json db_val here:, ", db_val)
        return json.loads(db_val)
      
schema = {
  "type": "object",
  "keys": {
    "properties": {
      "type": "object",
      "title": "From Create Properties Here",
      "keys": {},
      "additionalProperties": {
        "type": "object", 
        "keys": {
          "id": {
            "type": "string",
            "widget": "hidden"
          },
          "required": {
            "type": "boolean",
            "widget": "select",
            "default": True,
            "choices": [
              {
                "title": "Yes",
                "value": True,
              },
              {
                "title": "No",
                "value": False
              }
            ]
          },
          "options": {
            "type": "object",
            "keys": {},
            "additionalProperties": {
              "type": "object",
              "keys": {
                "id": {
                  "type": "string",
                  "widget": "hidden"
                }
              }
            }
          }
        }
      }
    }
  }
}


class ProductType(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    properties = ProductTypeJSONFIELDCUSTOM(null=False, default=None)
    product_schema_render = ProductTypeJSONFIELDCUSTOM(null=True, default=None)
    def save(self, *args, **kwargs):
        # before save transform for id
        properties = ProductTypeSerializer.model_validate(self.properties)
        self.product_schema_render = json.dumps(self.construct_product_schema_render())
        self.properties = properties.get_model(transform_type="json")
        super(ProductType, self).save(*args, **kwargs)

    def construct_product_schema_render(self):
      try:
        properties = self.properties["properties"]
        new_schema = product_schema.copy()
        keys = new_schema["keys"]["properties"]["keys"]
        for property in properties:
          id = properties[property]["id"]
          keys[str(id)] = {
            "type": "string",
            "title": property,
            "choices": []
          }
          options = properties[property]
          #print("options: ", options)
          for option in options["options"]:
            option_id = options["options"][option]["id"]
            keys[str(id)]["choices"].append({
              "title": option,
              "value": str(option_id)
            })
            #print("keys: ", keys)
        new_schema["keys"]["properties"]["keys"] = keys
      except BaseException as err:
        raise err
      else:
        return new_schema
      
    def __str__(self):
      return self.name
product_schema = {
  "type": "object",
  "keys": {
    "properties": {
      "type": "object",
      "keys": {
      }    
    }
  }
}

class ProductProperties(models.JSONField):
  def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
    db_val = super().from_db_value(value, expression, connection)
    if db_val is None:
        return ""
     
    #print("get db_val here: ", db_val)
    #print("get json db_val here:, ", db_val)
    return json.loads(db_val)
class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(ProductType, related_name='products', on_delete=models.CASCADE, 
    null=True, default=None)
    #added_properties = models.BooleanField(default=False)
    properties = models.JSONField(null=True, default=None)




    print("schema_json: ", properties)
    def product_type_name(self):
      return self.product_type.name
    
    def dynamic_schema(self):
      return self.properties
    def save(self, *args, **kwargs):
      print("properties: ", self.properties)
      
      super().save(*args, **kwargs)

    

    