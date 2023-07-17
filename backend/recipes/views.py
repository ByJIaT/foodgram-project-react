import io

from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from core.filters import IngredientFilter, RecipeFilter
from core.mixins import CreateMixin, DeleteMixin
from core.pagination import LimitPageNumberPagination
from recipes.models import (Tag, Ingredient, Recipe, Favorite, ShoppingCart)
from recipes.serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer,
    RecipeMiniFieldSerializer,
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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(CreateMixin, DeleteMixin, ModelViewSet):
    queryset = (Recipe.objects.all().select_related('author')
                .prefetch_related('ingredients', 'tags')
                )
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorAdminOrReadOnly,)
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(('post',), detail=True, permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        fields = {
            'user': request.user,
            'recipe': get_object_or_404(Recipe, pk=pk),
        }
        return self.created(model=Favorite,
                            serializer=RecipeMiniFieldSerializer,
                            instance=fields['recipe'],
                            error_message='Recipe already in favorites',
                            **fields,
                            )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        fields = {
            'user': request.user,
            'recipe': get_object_or_404(Recipe, pk=pk),
        }
        return self.deleted(model=Favorite,
                            error_message='Recipe are not in favorites',
                            **fields,
                            )

    @action(('post',), detail=True, permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        fields = {
            'user': request.user,
            'recipe': get_object_or_404(Recipe, pk=pk),
        }
        return self.created(model=ShoppingCart,
                            serializer=RecipeMiniFieldSerializer,
                            instance=fields['recipe'],
                            error_message='Recipe already in shopping cart',
                            **fields,
                            )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        fields = {
            'user': request.user,
            'recipe': get_object_or_404(Recipe, pk=pk),
        }
        return self.deleted(model=ShoppingCart,
                            error_message='Recipe are not in shopping cart',
                            **fields,
                            )

    @action(('get',), detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = (
            Ingredient.objects
            .filter(recipes__shopping_carts__user=request.user)
            .values('name', 'measurement_unit')
            .annotate(amount=Sum('recipe_ingredients__amount'))
        )
        buffer = io.BytesIO()
        pdfmetrics.registerFont(TTFont('FreeSans', 'fonts/FreeSans.ttf'))
        pdf = canvas.Canvas(buffer, pagesize=(350, 400),
                            initialFontName='FreeSans', initialFontSize=12)

        y = 380
        for ingredient in ingredients:
            pdf.drawString(20, y, f'{ingredient["name"]}:'
                                  f' {ingredient["amount"]}'
                                  f' {ingredient["measurement_unit"]}')
            y -= 20
            if y <= 20:
                pdf.showPage()
                y = 380

        pdf.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename='shopping_cart.pdf')
