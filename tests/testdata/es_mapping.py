from settings import ESIndex


def get_index_config_by_name(index_name: ESIndex) -> dict | None:  # type: ignore
    if index_name == ESIndex.movies:
        return movie_index_config
    if index_name == ESIndex.genres:
        return genre_index_config
    if index_name == ESIndex.persons:
        return person_index_config


movie_index_config = {
    "settings": {
        "refresh_interval": "1ms",
        "analysis": {
            "filter": {
                "english_stop": {"type": "stop", "stopwords": "_english_"},
                "english_stemmer": {"type": "stemmer", "language": "english"},
                "english_possessive_stemmer": {"type": "stemmer", "language": "possessive_english"},
                "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                "russian_stemmer": {"type": "stemmer", "language": "russian"},
            },
            "analyzer": {
                "ru_en": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer",
                    ],
                }
            },
        },
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {"type": "keyword"},
            "imdb_rating": {"type": "float"},
            "genres": {"type": "keyword"},
            "title": {"type": "text", "analyzer": "ru_en", "fields": {"raw": {"type": "keyword"}}},
            "description": {"type": "text", "analyzer": "ru_en"},
            "directors_names": {"type": "text", "analyzer": "ru_en"},
            "actors_names": {"type": "text", "analyzer": "ru_en"},
            "writers_names": {"type": "text", "analyzer": "ru_en"},
            "directors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {"id": {"type": "keyword"}, "name": {"type": "text", "analyzer": "ru_en"}},
            },
            "actors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {"id": {"type": "keyword"}, "name": {"type": "text", "analyzer": "ru_en"}},
            },
            "writers": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {"id": {"type": "keyword"}, "name": {"type": "text", "analyzer": "ru_en"}},
            },
        },
    },
}

genre_index_config = {
    "settings": {
        "refresh_interval": "1ms",
        "analysis": {
            "filter": {
                "english_stop": {"type": "stop", "stopwords": "_english_"},
                "english_stemmer": {"type": "stemmer", "language": "english"},
                "english_possessive_stemmer": {"type": "stemmer", "language": "possessive_english"},
                "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                "russian_stemmer": {"type": "stemmer", "language": "russian"},
            },
            "analyzer": {
                "ru_en": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer",
                    ],
                }
            },
        },
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {"type": "keyword"},
            "name": {
                "type": "text",
                "analyzer": "ru_en",
            },
            "description": {
                "type": "text",
                "analyzer": "ru_en",
            },
            "films": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "title": {
                        "type": "text",
                        "analyzer": "ru_en",
                    },
                    "imdb_rating": {"type": "float"},
                },
            },
        },
    },
}

person_index_config = {
    "settings": {
        "refresh_interval": "1ms",
        "analysis": {
            "filter": {
                "english_stop": {"type": "stop", "stopwords": "_english_"},
                "english_stemmer": {"type": "stemmer", "language": "english"},
                "english_possessive_stemmer": {"type": "stemmer", "language": "possessive_english"},
                "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                "russian_stemmer": {"type": "stemmer", "language": "russian"},
            },
            "analyzer": {
                "ru_en": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer",
                    ],
                }
            },
        },
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {"type": "keyword"},
            "full_name": {
                "type": "text",
                "analyzer": "ru_en",
            },
            "films": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "title": {
                        "type": "text",
                        "analyzer": "ru_en",
                    },
                    "imdb_rating": {"type": "float"},
                    "roles": {
                        "type": "text",
                        "analyzer": "ru_en",
                    },
                },
            },
        },
    },
}
