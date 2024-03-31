from collections import deque
from collections.abc import Callable, Sequence
from dataclasses import fields
from typing import Any, Mapping
from django.contrib import admin, messages
from django import forms
from django.contrib.admin.views.main import ChangeList
from django.core.files.base import File
from django.db.models import ForeignKey, Model
from django.db.models.fields.related import RelatedField
from django.db.models.query import QuerySet
from django.forms.utils import ErrorDict, ErrorList
from django.http import HttpRequest
from django.http.response import HttpResponse
from django_jsonform.widgets import JSONFormWidget
from django.forms import ValidationError
from requests import options
from .serializers import ProductTypeSerializer
from .models import Product, ProductType, schema, product_schema
import json
# Register your models here.

class ProductTypeChangeForm(forms.ModelForm):
  name = forms.CharField(max_length=255)
  properties = forms.JSONField(widget=JSONFormWidget(schema=schema))

  def __init__(self, *args, **kwargs):
    super(ProductTypeChangeForm, self).__init__(*args, **kwargs)
    self.__important_fields = ['name', 'properties']
    for field in self.__important_fields:
      setattr(self, '__original_%s' % field, getattr(self.instance, field))

  def clean(self) -> Any:
    # check change
    try:
      old_properties = getattr(self, "__original_properties")["properties"]
      new_properties = self.cleaned_data["properties"]["properties"]
    except:
      return
    else:
      changed = False
      q = deque([(old_properties, new_properties)])
      while len(q) > 0:
        p, n = q.popleft()
        if len(p) < len(n):
          p, n = n, p
        for property in p:
          if isinstance(p[property], dict) and p[property] != {}:
            if property not in n:
              print("property not same: ", property)
              changed = True
              break
            else:
              print("property same: ", property)
              print("p property: ", p[property])
              print("n property: ", n[property])
              q.append((p[property], n[property]))
        if changed:
          break

      if not changed:
        self.add_error("properties", "not changed still be same properties previous")

  def clean_properties(self) -> Any:
    print("clean properties")
    properties = self.cleaned_data["properties"]
    try:
      ProductTypeSerializer.model_validate(properties)
    except ValidationError as err:
      #print("error properties: ", err)
      self.add_error('properties', f'error message: {err}')
      #raise ValidationError("invalid properties", code="invalid")
    else:
      print("properties valid: ", self.cleaned_data["properties"])
      return self.cleaned_data["properties"]
    

class ProductTypeAdmin(admin.ModelAdmin):
  form = ProductTypeChangeForm

  list_display = [
    "id",
    "name"
  ]

  search_fields = ["name"]

from django.conf import settings
def dynamic_admin_fields(form: forms.ModelForm, obj) -> dict:
  
  return json.loads(obj.properties)

class ProductForm(forms.ModelForm):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    v = dynamic_admin_fields(self, self.instance)
    self.base_fields["properties"] = forms.JSONField(widget=JSONFormWidget(schema=v))
    self.fields["properties"] = forms.JSONField(widget=JSONFormWidget(schema=v))
    

  class Meta:
    model = Product
    fields = ["product_type", "name", "properties"]

class ProductAdmin(admin.ModelAdmin):
  form = ProductForm
  
  #def get_form(self, request, obj, change=False, **kwargs):
  #  return ProductForm
  def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
    query = super().get_queryset(request)
    v = query.select_related("product_type")
    return v
  
  def get_product_type_name(self, obj):
    return obj.product_type.name
    

  get_product_type_name.short_description = "Type Product"
  list_display = [
    "id",
    "name",
    "get_product_type_name",
  ]

  autocomplete_fields = [
    "product_type"
  ]

  pass

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)