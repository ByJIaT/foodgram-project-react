from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from config.settings import TEXT_LENGTH

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True, )
    color = models.CharField(max_length=7, unique=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, null=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        indexes = [
            models.Index(fields=('name',))
        ]

    def __str__(self):
        return f'{self.name[:TEXT_LENGTH]}'


class Ingredient(models.Model):
    name = models.CharField(max_length=200, )
    measurement_unit = models.CharField(max_length=200, )

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
        return self.all().select_related('author').count()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='%(app_label)s_%(class)s',
    )
    tags = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(app_label)s_%(class)s',
    )
    name = models.CharField(max_length=200, verbose_name=_('recipe name'))
    image = models.ImageField(upload_to='recipes/images/', )
    text = models.TextField(verbose_name=_('description'), )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1, message=_('Must be more then 1 minute')),
        ],
        help_text=_('Cooking time in minutes'),
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
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
    )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(1, message=_('Must be more then 1')),
        ],
        help_text=_('Amount of ingredients'),
    )

    class Meta:
        verbose_name = _('RecipeIngredient')
        verbose_name_plural = _('RecipeIngredients')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredients'],
                name='%(app_label)s_%(class)s',
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.ingredients}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
    )

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


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s',
    )

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
