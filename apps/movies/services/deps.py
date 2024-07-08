from typing import Annotated

from cache import RedisCache as _RedisCache
from fastapi import Depends
from storages.film import ElasticSearchFilmStorage as _ElasticSearchFilmStorage
from storages.genre import ElasticSearchGenreStorage as _ElasticSearchGenreStorage
from storages.person import ElasticPersonFilmStorage as _ElasticPersonFilmStorage

RedisCache = Annotated[_RedisCache, Depends(_RedisCache)]
ElasticSearchFilmStorage = Annotated[_ElasticSearchFilmStorage, Depends(_ElasticSearchFilmStorage)]
ElasticSearchGenreStorage = Annotated[_ElasticSearchGenreStorage, Depends(_ElasticSearchGenreStorage)]
ElasticPersonFilmStorage = Annotated[_ElasticPersonFilmStorage, Depends(_ElasticPersonFilmStorage)]
