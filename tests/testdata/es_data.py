import random
import uuid

import faker

fake = faker.Faker()

es_data_the_star_60 = [
    {
        "id": str(uuid.uuid4()),
        "imdb_rating": 8.5,
        "title": "The Star",
        "description": "New World",
        "genres": ["Action", "Sci-Fi"],
        "directors_names": ["Stan"],
        "actors_names": ["Ann", "Bob"],
        "writers_names": ["Ben", "Howard"],
        "actors": [
            {"id": "ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95", "name": "Ann"},
            {"id": "fb111f22-121e-44a7-b78f-b19191810fbf", "name": "Bob"},
        ],
        "writers": [
            {"id": "caf76c67-c0fe-477e-8766-3ab3ff2574b5", "name": "Ben"},
            {"id": "b45bd7bc-2e16-46d5-b125-983d356768c6", "name": "Howard"},
        ],
        "directors": [],
    }
    for _ in range(60)
]

es_data_fake_10 = [
    {
        "id": str(uuid.uuid4()),
        "imdb_rating": round(random.uniform(0, 10), 1),
        "title": "Doctor Who",
        "description": fake.text(100),
        "genres": ["Sci-Fi"],
        "directors_names": [fake.first_name()],
        "actors_names": [fake.first_name(), fake.first_name()],
        "writers_names": [fake.first_name(), fake.first_name()],
        "actors": [
            {"id": str(uuid.uuid4()), "name": fake.name()},
            {"id": str(uuid.uuid4()), "name": fake.name()},
        ],
        "writers": [
            {"id": str(uuid.uuid4()), "name": fake.name()},
            {"id": str(uuid.uuid4()), "name": fake.name()},
        ],
        "directors": [],
    }
    for _ in range(10)
]
