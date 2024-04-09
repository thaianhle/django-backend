import asyncio
from django.shortcuts import render
from rest_framework.decorators import authentication_classes, permission_classes, renderer_classes
from adrf.decorators import api_view
from pydantic import ValidationError
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import renderers
from pydantic import BaseModel
from typing import Any
from .serializers import ProductTypeSerializer
from .models import ProductType
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from collections import deque
from pydantic import BaseModel
from asgiref.sync import sync_to_async
from .models import Product
# Create your views here.

class CustomRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, BaseModel):
            response_data = data.model_dump_json()
            return super().render(response_data, accepted_media_type, renderer_context)
    
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
@renderer_classes([CustomRenderer])
async def create_product_type(request):

    try:
        product_type_request = await ProductTypeSerializer(**request.data)
        fields = product_type_request.transform_and_to_json()
    except ValidationError as err:
        print(err)
        error = repr(err.errors()[0]["type"])
        return Response(data={"error": "", "result": ""}, status=401)
    
    product_type = ProductType(name=product_type_request.name, fields=fields)
    product_type.save()
    product_type_request.id = product_type.id
    return Response(data=product_type_request, status=200)

@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
@renderer_classes([CustomRenderer])
async def get_product_by_id(request, product_id):
  try:
    #await asyncio.sleep(0.1)
    product = await get_product(product_id)
  except BaseException as err:
    #print("error: ", err)
    pass
  else:
    #print("product data: ", product)
    return Response(data=product, status=200)
  
cache = {}
lock = asyncio.Lock()
@sync_to_async  
def get_product(product_id):
  if product_id not in cache:
    cache[product_id] = Product.objects.get(id=product_id)
  return cache[product_id]