import io

from django.db.models import Sum
from django.http import FileResponse

from django.utils.translation import gettext_lazy as _
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from recipes.models import (Tag, Ingredient, Recipe, Favorite, ShoppingCart)
from recipes.serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer,
    RecipeReadSerializer,
)
from users.permissions import IsAdminOrReadOnly, IsAuthorAdminOrReadOnly


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('$name',)


class RecipeViewSet(ModelViewSet):
    queryset = (Recipe.objects.all().select_related('author')
                .prefetch_related('ingredients')
                )
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(('post',), detail=True, permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if Favorite.objects.is_favorited(user, recipe):
            return Response(
                {'errors': _('Recipe already in favorites')},
                status=status.HTTP_400_BAD_REQUEST
            )
        Favorite.objects.create(user=user, recipe=recipe)
        serializer = RecipeReadSerializer(recipe)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not Favorite.objects.is_favorited(user, recipe):
            return Response(
                {'errors': _('Recipe are not in favorites')},
                status=status.HTTP_400_BAD_REQUEST
            )
        Favorite.objects.delete(user, recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(('post',), detail=True, permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if ShoppingCart.objects.is_in_shopping_cart(user, recipe):
            return Response(
                {'errors': _('Recipe already in shopping cart')},
                status=status.HTTP_400_BAD_REQUEST
            )
        ShoppingCart.objects.create(user=user, recipe=recipe)
        serializer = RecipeReadSerializer(recipe)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @shopping_cart.mapping.delete
    def delete_from_shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not ShoppingCart.objects.is_in_shopping_cart(user, recipe):
            return Response(
                {'errors': _('Recipe are not in shopping cart')},
                status=status.HTTP_400_BAD_REQUEST
            )
        ShoppingCart.objects.delete(user, recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(('get',), detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = (
            Ingredient.objects.filter(
                recipeingredient_ingredients__recipe__shoppingcart_recipes__user=request.user)
            .values('name', 'measurement_unit')
            .annotate(amount=Sum('recipeingredient_ingredients__amount'))
        )

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf', 'UTF-8'))
        pdf.setFont('Vera', 20)
        pdf.drawString(200, 800, 'Shopping cart')
        pdf.setFont('Vera', 14)
        y = 750
        for ingredient in ingredients:
            pdf.drawString(20, y, f'{ingredient["name"]}: '
                                  f'{ingredient["amount"]} '
                                  f'{ingredient["measurement_unit"]}'
                           )
            y -= 25

        pdf.setTitle('Foodgram')
        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename='shopping cart.pdf')
