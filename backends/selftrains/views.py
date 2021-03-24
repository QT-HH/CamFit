from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import  TrainListSerializer, TrainDetailSerializer
from .models import SelfTrain

@api_view(['GET','POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def train_list_create(request):
    if request.method == 'GET':
        trains = SelfTrain.objects.order_by('-pk')
        serializer = ArticleSerializer(articles, many =True)
        return Response(serializer.data)
    else:
        if request.user.is_superuser:
            serializer = ArticleSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user= request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def train_detail(request, train_pk):
    train = get_object_or_404(SelfTrain, pk=selftrain_pk)
    serializer = TrainDetailSerializer(train)
    return Response(serializer.data)

@api_view(['PUT','DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def train_update_delete(request,article_pk):
    train = get_object_or_404(SelfTrain, pk=selftrain_pk)

    if not request.user.train.filter(pk=selftrain_pk).exists():
        return Response({'detail': '권한이 없습니다.'})
    
    if request.method == 'PUT':
        serializer = TrainDetailSerializer(train, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user= request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        train.delete()
        return Response({'id': selftrain_pk}, status=status.HTTP_204_NO_CONTENT)

