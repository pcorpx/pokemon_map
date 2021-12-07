import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        add_pokemon(
            folium_map,
            pokemon.lat,
            pokemon.lon,
            request.build_absolute_uri(pokemon.pokemon.photo.url)
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(
                pokemon.photo.url
            ),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        chosen_pokemon = Pokemon.objects.get(id=pokemon_id)
        pokemon_entities = chosen_pokemon.pokemon_entities.all()
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon = {}
    pokemon['title_ru'] = chosen_pokemon.title
    pokemon['title_en'] = chosen_pokemon.title_en
    pokemon['title_jp'] = chosen_pokemon.title_jp
    pokemon_img_url = request.build_absolute_uri(chosen_pokemon.photo.url)
    pokemon['img_url'] = pokemon_img_url
    pokemon['description'] = chosen_pokemon.description

    parent_pokemon = chosen_pokemon.previous_evolution
    if parent_pokemon:
        pokemon['previous_evolution'] = {}
        pokemon['previous_evolution']['pokemon_id'] = parent_pokemon.id
        pokemon['previous_evolution']['title_ru'] = parent_pokemon.title
        pokemon['previous_evolution']['img_url'] = parent_pokemon.photo.url

    child_pokemon = chosen_pokemon.next_evolution.first()
    if child_pokemon:
        pokemon['next_evolution'] = {}
        pokemon['next_evolution']['pokemon_id'] = child_pokemon.id
        pokemon['next_evolution']['title_ru'] = child_pokemon.title
        pokemon['next_evolution']['img_url'] = child_pokemon.photo.url

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_img_url
        )
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
