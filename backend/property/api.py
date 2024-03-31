from django.http import JsonResponse

from rest_framework.decorators import authentication_classes, permission_classes, api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from .models import Property
from .serializers import PropertiesListSerializer

@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
@parser_classes((FormParser, MultiPartParser)) #use parser_classes
def properties_list(request):
    
    properties = Property.objects.all()
    print("properties: ", properties[0])
    serializer = PropertiesListSerializer(properties, many=True)

    return JsonResponse({
        'data': serializer.data
    })

