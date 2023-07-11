from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from config.settings import TEXT_LENGTH

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_('Tag name'),
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        null=True,
        verbose_name=_('Tag color'),
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        null=True,
        verbose_name=_('Tag slug'),
    )

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        indexes = [
            models.Index(fields=('name',))
        ]

    def __str__(self):
        return f'{self.name[:TEXT_LENGTH]}'


class OrderedIngredientManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by(Lower('name'))


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_('Ingredient name'),
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name=_('Measurement unit'),
    )

    objects = OrderedIngredientManager()

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')
        indexes = [
            models.Index(fields=('name',))
        ]

    def __str__(self):
        return f'{self.name[:TEXT_LENGTH]}'


class RecipeManager(models.Manager):
    def get_recipes(self):
        return self.all().select_related('author')

    def get_recipes_count(self):
        return self.all().count()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name=_('Recipe author'),
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name=_('Recipe ingredients'),
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        related_name='recipes',
        verbose_name=_('Recipe tags'),
    )
    name = models.CharField(max_length=200, verbose_name=_('Recipe name'))
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name=_('Recipe image'),
    )
    text = models.TextField(verbose_name=_('Recipe description'), )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1, message=_('Must be more then 1 minute')),
        ],
        help_text=_('Cooking time in minutes'),
        verbose_name=_('Cooking time'),
    )

    objects = RecipeManager()

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        indexes = [
            models.Index(fields=('name',))
        ]

    def __str__(self):
        return f'{self.name[:TEXT_LENGTH]}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name=_('Ingredients'),
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name=_('Recipes'),
    )
    amount = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(1, message=_('Must be more then 1')),
        ],
        help_text=_('Amount of ingredients'),
        verbose_name=_('Ingredient amount'),
    )

    class Meta:
        verbose_name = _('RecipeIngredient')
        verbose_name_plural = _('RecipeIngredients')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='%(app_label)s_%(class)s',
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class RecipeTag(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name=_('Tags'),
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name=_('Recipes'),
    )

    class Meta:
        verbose_name = _('RecipeTag')
        verbose_name_plural = _('RecipeTags')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='%(app_label)s_%(class)s',
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class ShoppingCartManager(models.Manager):
    def is_in_shopping_cart(self, user, recipe):
        return self.filter(user=user, recipe=recipe).exists()

    def delete(self, user, recipe):
        return self.filter(user=user, recipe=recipe).delete()


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcarts',
        verbose_name=_('ShoppingCart users'),
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcarts',
        verbose_name=_('ShoppingCart recipes'),
    )

    objects = ShoppingCartManager()

    class Meta:
        verbose_name = _('ShoppingCart')
        verbose_name_plural = _('ShoppingCarts')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='%(app_label)s_%(class)s',
            )
        ]
        indexes = [
            models.Index(fields=('user',))
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class FavoriteManager(models.Manager):
    def is_favorited(self, user, recipe):
        return self.filter(user=user, recipe=recipe).exists()

    def delete(self, user, recipe):
        return self.filter(user=user, recipe=recipe).delete()


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=_('Favorite users'),
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name=_('Favorite recipes'),
    )

    objects = FavoriteManager()

    class Meta:
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='%(app_label)s_%(class)s',
            )
        ]
        indexes = [
            models.Index(fields=('user',))
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'
