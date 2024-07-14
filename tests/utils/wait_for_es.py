import backoff
import logging

from elasticsearch import Elasticsearch

from settings import test_settings


def handle_backoff(details):
    logging.error("Backing off {wait:0.1f} seconds after {tries} tries. Calling function {targer}".format(**details))


@backoff.on_exception(
    backoff.expo,
    (ConnectionError,),
    on_backoff=handle_backoff,
)
def setup_elastic_connection():
    es_client = Elasticsearch(hosts=test_settings.es.url)
    if not es_client.ping():
        raise ConnectionError("Could not connect to elasticsearch")
    return es_client


if __name__ == "__main__":
    es_client = setup_elastic_connection()
