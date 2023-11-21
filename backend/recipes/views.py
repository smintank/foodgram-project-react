from rest_framework import viewsets, status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import (
    Recipe, Ingredient, Favorite, Tag, Subscription, ShoppingCart
)
from recipes.serializer import (
    RecipeSerializer, IngredientSerializer, FavoriteSerializer, TagSerializer,
    SubscriptionListSerializer, SubscribeSerializer,
    ShoppingCartSerializer, DownloadCartSerializer
)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = None


class FavoriteView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    path_arg = 'recipe'

    def create(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        request.data[self.path_arg] = self.kwargs.get('pk')
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not (instance := self.queryset.filter(
                {'user': self.request.user.id,
                 self.path_arg: self.kwargs.get('pk')}
        )):
            return Response({'error': 'Нельзя отписаться, вы не подписаны!'},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance.first())
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination

    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SubscribeView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)
    path_arg = 'subscription'

    def create(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        request.data[self.path_arg] = self.kwargs.get('pk')
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not (instance := self.queryset.filter(
                {'user': self.request.user.id,
                 self.path_arg: self.kwargs.get('pk')}
        )):
            return Response({'error': 'Нельзя отписаться, вы не подписаны!'},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance.first())
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionListView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionListSerializer
    permission_classes = (IsAuthenticated,)


class ShoppingCartView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer


class DownloadCartView(generics.RetrieveAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = DownloadCartSerializer
