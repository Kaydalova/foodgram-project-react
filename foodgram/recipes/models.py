from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.validators import validate_hex, validate_ingredient_name
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тэг',
        max_length=settings.TAG_MAX_LENGTH,
        unique=True,
        validators=[UnicodeUsernameValidator])
    slug = models.CharField(
        verbose_name='Слаг',
        max_length=settings.TAG_MAX_LENGTH,
        unique=True)
    color = models.CharField(
        verbose_name='Цвет', max_length=7,
        default='#C71585', unique=True,
        validators=[validate_hex])

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.INGREDIENT_MAX_LENGTH,
        validators=[validate_ingredient_name])
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=settings.INGREDIENT_MAX_LENGTH)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор', related_name='recipe')
    name = models.CharField(
        verbose_name='Название', max_length=200,
        validators=[validate_ingredient_name])
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
        verbose_name='Фотография блюда')
    text = models.TextField(
        verbose_name='Описание')
    tags = models.ManyToManyField(
        Tag, verbose_name='Тэги')
    cooking_time = models.PositiveSmallIntegerField(
        default=1, blank=False,
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(1, 'Должно быть больше 0'),
            MaxValueValidator(600, 'Превышен лимит времени приготовления')])
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        ordering = ['-pub_date', ]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(fields=['author', 'name'],
                                    name='unique_author_recipename')
        ]

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='+')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт')
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество в рецепте',
        validators=[
            MinValueValidator(1, 'Должно быть больше 0'),
            MaxValueValidator(2000, 'Максимальное количество - 2000')])

    def __str__(self):
        return self.recipe.name

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='+')
    recipe_lover = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Добавил в избранное',
        related_name='favorite')

    class Meta:
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'


class ShoppingCart(models.Model):
    cart_owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Владелец списка покупок',
        related_name='shopping_cart')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='+')

    def __str__(self):
        return self.recipe.name

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
