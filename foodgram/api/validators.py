import re

from django.core.exceptions import ValidationError


def validate_ingredients(ingredients_list, val_model):
    """
    Метод проверяет существуют ли указанные ингредиенты
    и правильно ли задано их количество.
    Если нет - выбрасывает ValidationError.
    Вместе с ingredients_list передаем модель Ingredient,
    чтобы избежать circular import.
    """
    if len(ingredients_list) < 1:
        raise ValidationError(
            'Блюдо должно содержать хотя бы 1 ингредиент')
    unique_list = []
    for ingredient in ingredients_list:
        if not ingredient.get('id'):
            raise ValidationError('Укажите id ингредиента')
        ingredient_id = ingredient.get('id')
        if not val_model.objects.filter(pk=ingredient_id).exists():
            raise ValidationError(
                f'{ingredient_id}- ингредиент с таким id не найден')
        if id in unique_list:
            raise ValidationError(
                f'{ingredient_id}- дублирующийся ингредиент')
        unique_list.append(ingredient_id)
        ingredient_amount = ingredient.get('amount')
        if int(ingredient_amount) < 1:
            raise ValidationError(
                f'Количество {ingredient} должно быть больше 1')


def validate_tags(tags_list, val_model):
    """
    Метод проверяет существует ли указанный тег.
    Если нет - выбрасывает ValidationError.
    Вместе с tags_list передаем модель Tag,
    чтобы избежать circular import.
    """
    for tag in tags_list:
        if not val_model.objects.filter(pk=tag).exists():
            raise ValidationError(f'{tag} - Такого тэга не существует')


def validate_cooking_time(value):
    """
    Метод проверяет корректно ли указанное времени приготовления.
    Если нет - выбрасывает ValidationError.
    """
    if not value or int(value) < 1:
        raise ValidationError({
            'cooking_time': 'Укажите время приготовления'})


def validate_ingredient_name(value):
    """
    Метод проверяет соответствует ли название ингредиента
    заданному регулярному выражению.
    Название может содержать %,-"«»&() и
    русские и английские буквы.
    Если нет - выбрасывает ValidationError.
    """
    reg = r'^[\w%,"\'«»&()]+\Z'
    listik = value.split()
    for item in listik:
        if not re.fullmatch(reg, item):
            raise ValidationError({
                'Недопустимое значение имени {item}'})


def validate_hex(value):
    """
    Метод проверяет соответствует ли код цвета
    возможному
    Если нет - выбрасывает ValidationError.
    """
    regex = "^#([A-Fa-f0-9]{3,6})$"
    hehex = re.compile(regex)
    if not re.search(hehex, value):
        raise ValidationError({
            'Недопустимое значение цвета'})


def validate_username(value):
    """
    Метод проверяет соответствует username ожиданиям.
    Если нет - выбрасывает ValidationError.
    """
    if value.lower() == 'me':
        raise ValidationError({
            f'Username не может быть {value}'})


def validate_real_name(value):
    """
    Метод проверяет соответствует ли имя и фамилия
    пользователя заданному регулярному выражению.
    Если нет - выбрасывает ValidationError.
    """
    reg = r'^[\w-]+\Z'

    if not re.fullmatch(reg, value):
        raise ValidationError({
            'Недопустимое значение имени {value}'})
