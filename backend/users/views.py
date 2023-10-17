from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api import pagintation

from .models import Subscribe, User
from .serializers import (CustomUserSerializer, SubscribeListSerializer,
                          SubscribeSerializer)


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    pagination_class = pagintation.CustomPagination

    @action(['get'], detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(['post'], detail=True,
            url_path=r'subscribe',
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        serializer = SubscribeSerializer(
            context={'request': request},
            data={'user': user.id,
                  'author': author.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def subscribtion_delete(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if User.objects.filter(id=author.id).exists():
            if not Subscribe.objects.filter(
                user=user.id, author=author.id
            ).exists():
                return Response({"detail': Subscription doesn't exists"},
                                status=status.HTTP_400_BAD_REQUEST)
        subscription = get_object_or_404(
            Subscribe, user=user.id, author=author.id)
        subscription.delete()
        return Response({'detail': 'Subscription was deleted'},
                        status=status.HTTP_204_NO_CONTENT)

    @action(['get'], detail=False,
            url_path=r'subscriptions',
            permission_classes=(IsAuthenticated,),
            pagination_class=pagintation.CustomPagination)
    def subscriptions(self, request):
        authors = User.objects.filter(subscribing__user=request.user)
        paginated_authors = self.paginate_queryset(authors)
        serializer = SubscribeListSerializer(
            paginated_authors,
            context={'request': request,
                     'user': request.user},
            many=True)
        return self.get_paginated_response(serializer.data)
