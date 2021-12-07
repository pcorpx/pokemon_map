from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя')
    title_en = models.CharField(
        max_length=200, blank=True, verbose_name='Имя по английски'
    )
    title_jp = models.CharField(
        max_length=200, blank=True, verbose_name='Имя по японски'
    )
    photo = models.ImageField(upload_to='pics', verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'self', related_name='next_evolution', null=True, blank=True,
        on_delete=models.PROTECT, verbose_name='Предшественник'
    )

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, related_name='pokemon_entities',
        verbose_name='Покемон'
    )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(
        null=True, blank=True, verbose_name='Появился'
    )
    disappeared_at = models.DateTimeField(
        null=True, blank=True, verbose_name='Исчез'
    )
    level = models.IntegerField(
        null=True, blank=True, verbose_name='Уровень'
    )
    health = models.IntegerField(
        null=True, blank=True, verbose_name='Здоровье'
    )
    strength = models.IntegerField(
        null=True, blank=True, verbose_name='Атака'
    )
    defence = models.IntegerField(
        null=True, blank=True, verbose_name='Защита'
    )
    stamina = models.IntegerField(
        null=True, blank=True, verbose_name='Выносливость'
    )
