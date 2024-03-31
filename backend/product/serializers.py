from typing_extensions import Unpack
from django.forms import ValidationError
from pydantic import BaseModel as TypeClass, ConfigDict, field_validator
from typing import Any, List, Dict, Union
from pydantic import UUID4
from django.forms import ValidationError

# Create your models here.
from rest_framework import serializers


from pydantic import BaseModel as TypeClass

class OptionValueField(TypeClass):
    id: Union[int, str] =-1
    soft_deleted: bool = False

class ProductTypeField(TypeClass):
    id: Union[int, str] = -1
    options: Dict[str, OptionValueField]
    required: bool

    @field_validator("options")
    @classmethod
    def check_options(cls, value: Dict[str, OptionValueField]):
        if value == {}:
            raise ValidationError("missing options", "invalid")
        
        return value
    def transform(self):
        index = 1
        for option_name in self.options:
            self.options[option_name].id = index
            index += 1
        return self
    
class ProductTypeSerializer(TypeClass):
    properties: Dict[str, ProductTypeField]

      
    @field_validator("properties")
    @classmethod
    def check_properties(cls, value: Dict[str, ProductTypeField]):
        if value == {}:
            raise ValidationError("missing properties", "invalid")
        

        return value
    
    
    def _transform(self):
        index = 1
        for property_name in self.properties:
            self.properties[property_name].id = index
            self.properties[property_name].transform()
            index += 1
        
        return self
    def transform_and_to_object(self):
        return self._transform().model_dump()

    def transform_and_to_json(self):
        return self._transform().model_dump_json()
        #try:
        #    data = v.model_dump_json()
        #except BaseException as err:
        #    print("error dump json: ", err)
        #else:
        #    return data



    def get_model(self, transform_type=None):
        if transform_type is not None:
            if  transform_type == "object":
                return self.transform_and_to_object()
            if  transform_type == "json":
                return self.transform_and_to_json()


