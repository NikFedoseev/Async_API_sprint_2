import time

from enricher import PostgresEnricher
from loader import ElasticsearchLoader
from merger import PostgresMerger
from producer import PostgresProducer
from state import JsonFileStorage, State
from transformer import Transformer
from utils import get_postges_connection, logger

from settings import settings


def main():
    logger.info("etl process started")
    with get_postges_connection() as conn:
        state = State(storage=JsonFileStorage(file_path=settings.etl.STORAGE_FILE_PATH))
        producer = PostgresProducer(conn=conn, extract_size=settings.etl.EXTRACT_SIZE)
        enricher = PostgresEnricher(conn=conn)
        merger = PostgresMerger(conn=conn)
        transformer = Transformer()
        loader = ElasticsearchLoader(host=settings.elastic.HOST, port=settings.elastic.PORT)

        while True:
            filmwork_updates = producer.check_filmwork_updates(
                last_updated_time=state.get_state("movies_modified") or settings.etl.START_TIME
            )

            for updated_table, updated_entities, modified in filmwork_updates:
                index_name = "movies"
                enriched_entities = enricher.enrich(table=updated_table, entity_ids=updated_entities)
                merged_entities = merger.merge(enriched_entities, for_index=index_name)
                transformed_entities = transformer.transform_for_movie_index(merged_entities)
                loader.upload(index_name=index_name, entities=transformed_entities)
                state.set_state(key=f"{index_name}_modified", value=modified.strftime("%Y-%m-%d %H:%M:%S.%f %z"))

                logger.info(
                    f"{len(transformed_entities)} updates uploaded to {index_name} index, slepping {settings.etl.ITERATION_SLEEP_TIME} seconds"
                )
                time.sleep(settings.etl.ITERATION_SLEEP_TIME)

            person_updates = producer.check_person_updates(
                last_updated_time=state.get_state("persons_modified") or settings.etl.START_TIME
            )

            for updated_entities, modified in person_updates:
                index_name = "persons"
                merged_entities = merger.merge(updated_entities, for_index=index_name)
                transformed_entities = transformer.transform_for_person_index(merged_entities)
                loader.upload(index_name=index_name, entities=transformed_entities)
                state.set_state(key=f"{index_name}_modified", value=modified.strftime("%Y-%m-%d %H:%M:%S.%f %z"))
                logger.info(
                    f"{len(transformed_entities)} updates uploaded to {index_name} index, slepping {settings.etl.ITERATION_SLEEP_TIME} seconds"
                )
                time.sleep(settings.etl.ITERATION_SLEEP_TIME)

            genre_updates = producer.check_genre_updates(
                last_updated_time=state.get_state("genres_modified") or settings.etl.START_TIME
            )

            for updated_entities, modified in genre_updates:
                index_name = "genres"
                merged_entities = merger.merge(updated_entities, for_index=index_name)
                transformed_entities = transformer.transform_for_genre_index(merged_entities)
                loader.upload(index_name=index_name, entities=transformed_entities)
                state.set_state(key=f"{index_name}_modified", value=modified.strftime("%Y-%m-%d %H:%M:%S.%f %z"))
                logger.info(
                    f"{len(transformed_entities)} updates uploaded to {index_name} index, slepping {settings.etl.ITERATION_SLEEP_TIME} seconds"
                )
                time.sleep(settings.etl.ITERATION_SLEEP_TIME)

            logger.info(f"no updates found, slepping {settings.etl.CHECKING_UPDATES_SLEEP_TIME} seconds")
            time.sleep(settings.etl.CHECKING_UPDATES_SLEEP_TIME)


if __name__ == "__main__":
    main()
