from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from foodgram import settings
from recipes.views import (DownloadCartView, IngredientViewSet, RecipeViewSet,
                           TagViewSet)
from users.views import SubscribeView, SubscriptionListView, UserView

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'tags', TagViewSet)
router.register(r'users', UserView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/users/subscriptions/', SubscriptionListView.as_view()),
    path('api/users/<int:pk>/subscribe/', SubscribeView.as_view()),
    path('api/recipes/download_shopping_cart/', DownloadCartView.as_view()),
    path('api/', include(router.urls))
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
