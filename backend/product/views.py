from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
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
def create_product_type(request):

    try:
        product_type_request = ProductTypeSerializer(**request.data)
        fields = product_type_request.transform_and_to_json()
    except ValidationError as err:
        print(err)
        error = repr(err.errors()[0]["type"])
        return Response(data={"error": "", "result": ""}, status=401)
    
    product_type = ProductType(name=product_type_request.name, fields=fields)
    product_type.save()
    product_type_request.id = product_type.id
    return Response(data=product_type_request, status=200)



