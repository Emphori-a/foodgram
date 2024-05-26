# Generated by Django 3.2.3 on 2024-05-26 16:16

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_ingredientinrecipe_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AddField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата и время публикации'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Количество не может быть меньше 1.')], verbose_name='Количество'),
        ),
    ]