from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from core.constans import (INGREDIENT_LENGTH, MEASUREMENT_LENGTH,
                           MIN_VALIDATOR_VALUE, RECIPE_LENGTH,
                           SHORT_LINK_LENGTH, TAG_LENGTH)

User = get_user_model()


class Tag(models.Model):
    """
    Класс для описания тегов рецептов.

    Атрибуты:
        name (str): Наименование тега.
        slug (str): Slug тега.
    """

    name = models.CharField(
        verbose_name='Наименование',
        max_length=TAG_LENGTH,
    )
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=TAG_LENGTH,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        """Возвращает строковое представление тега."""
        return self.slug


class Ingredient(models.Model):
    """
    Класс для описания ингредиентов рецептов.

    Атрибуты:
        name (str): Наименование ингредиента.
        measurement_unit (str): Единица измерения ингредиента.
    """

    name = models.CharField(
        verbose_name='Наименование',
        max_length=INGREDIENT_LENGTH
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=MEASUREMENT_LENGTH
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        """Возвращает строковое представление ингредиента."""
        return self.name


class Recipe(models.Model):
    """
    Класс для описания рецептов.

    Атрибуты:
        name (str): Название рецепта.
        author (User): Автор рецепта.
        image (ImageField): Фото рецепта.
        text (str): Описание рецепта.
        cooking_time (int): Время приготовления рецепта в минутах.
        tags (Tag): Теги, связанные с рецептом.
        ingredients (Ingredient): Ингредиенты, используемые в рецепте.
        is_favorited (bool): Статус нахождения рецепта в избранном.
        is_in_shopping_cart (bool): Статус нахождения рецепта в корзине.
        short_link (str): Короткая ссылка на рецепт.
        pub_date (datetime): Дата и время публикации рецепта.
    """

    name = models.CharField(
        verbose_name='Название',
        max_length=RECIPE_LENGTH
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='recipes/',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления в минутах',
        validators=[
            MinValueValidator(
                MIN_VALIDATOR_VALUE,
                message=f'Минимальное значение поля - {MIN_VALIDATOR_VALUE}.')
        ]
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes',
        through='IngredientInRecipe'
    )
    is_favorited = models.BooleanField(
        verbose_name='Рецепт находится в избранном',
        blank=True,
        default=False
    )
    is_in_shopping_cart = models.BooleanField(
        verbose_name='Рецепт находится в корзине',
        blank=True,
        default=False
    )
    short_link = models.CharField(
        verbose_name='Короткая ссылка на рецепт',
        max_length=SHORT_LINK_LENGTH,
        unique=True,
        blank=True,
        null=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        """Возвращает строковое представление рецепта."""
        return self.name


class IngredientInRecipe(models.Model):
    """
    Класс для описания ингредиентов в рецепте.

    Атрибуты:
        recipe (Recipe): Рецепт, к которому относится ингредиент.
        ingredient (Ingredient): Ингредиент, который используется в рецепте.
        amount (int): Количество ингредиента в рецепте.
    """

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='ingredients_in',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='in_recipes',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                MIN_VALIDATOR_VALUE,
                message=('Количество не может быть меньше '
                         f'{MIN_VALIDATOR_VALUE}.'))
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self) -> str:
        """Возвращает строковое представление ингредиента в рецепте."""
        return f'{self.recipe.name}: {self.amount} {self.ingredient.name}'
