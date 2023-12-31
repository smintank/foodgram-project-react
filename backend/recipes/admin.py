from django.contrib import admin
from django.db.models import Count

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    verbose_name = 'ингредиент'
    verbose_name_plural = 'Ингредиенты'
    fields = ('ingredient', 'amount')


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('name', 'author', 'favorite_count')
    list_filter = ('tags', )
    search_fields = ('name',)
    filter_horizontal = ('tags',)
    date_hierarchy = 'pub_date'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _favorite_count=Count("favorites", distinct=True),
        )
        return queryset

    @admin.display(description='В избранном')
    def favorite_count(self, obj):
        count = obj._favorite_count
        if count == 0:
            return 'нет'
        return f'{count}'

    favorite_count.admin_order_field = '_favorite_count'


class IngredientsAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_display_links = ('user',)
    list_filter = ('user', 'recipe')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_display_links = ('user',)
    list_filter = ('user', 'recipe')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientsAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Tag)
