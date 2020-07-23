from django.core.exceptions import ObjectDoesNotExist
from dateutil.parser import isoparse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from collections import Counter
from .models import *
from .serializers import *

models_dict = {'user': User, 'post': Post, 'like':Like}
serializers_dict = {'user': UserSerializer, 'post': PostSerializer, 'like':LikeSerializer}

# Create your views here.



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all(request, model):
	Model = models_dict[model] #class
	Serializer = serializers_dict[model] #class

	objects = Model.objects.all() #instances
	serializer = Serializer(objects, many=True) #instance

	return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get(request, model, pk):
	Model = models_dict[model] #class
	Serializer = serializers_dict[model] #class

	try:
		objects = Model.objects.get(pk=pk) #instance
	except ObjectDoesNotExist:
		return Response('ObjectDoesNotExist', status=404)

	serializer = Serializer(objects, many=False) #instance

	return Response(serializer.data)

@api_view(['POST'])
def create(request, model):
	if model == 'user':
		resp = create_obj(request, model)
		return Response(resp[0], status=resp[1])
	else:
		if request.user.is_authenticated:
			resp = create_obj(request, model)
			return Response(resp[0], status=resp[1])
		else:
			return Response('Not authenticated', status=401)


#Standart for updating is PUT method but as I'm using obvious naming I think it's ok to use POST
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update(request, model, pk):
	Model = models_dict[model] #class
	Serializer = serializers_dict[model] #class

	try:
		objects = Model.objects.get(pk=pk) #instance
	except ObjectDoesNotExist:
		return Response('ObjectDoesNotExist', status=404)

	serializer = Serializer(instance=objects, data=request.data) #instance

	if serializer.is_valid():
		serializer.save()
		
		return Response(serializer.data)
	else:
		print(serializer.errors)
		return Response(serializer.errors, status=500)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated]) 
def delete(request, model, pk):

	Model = models_dict[model]

	try:
		objects = Model.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response('ObjectDoesNotExist', status=404)

	response = objects.delete()

	return Response(response)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytic(request):
	likes = Like.objects.filter(date_created__gte=request.GET['date_from'],
							    date_created__lte=request.GET['date_to'])
	
	serializer = LikeSerializer(likes, many=True)
	
	#Maybe time formating isn't that good(short), but this method allows to form any strig format needed 
	likes_list = [isoparse(each['date_created']).date().strftime('%Y/%m/%d') for each in serializer.data]

	#Using Counter to aggregate likes by day
	return Response(Counter(likes_list))


def create_obj(request, model):
	Serializer = serializers_dict[model] #class

	serializer = Serializer(data=request.data) #instance

	if serializer.is_valid():
		serializer.save()
		
		return (serializer.data, 200)
	else:
		return (serializer.errors, 500)