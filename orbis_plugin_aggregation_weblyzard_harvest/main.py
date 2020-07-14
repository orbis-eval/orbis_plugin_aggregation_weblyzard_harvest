# -*- coding: utf-8 -*-

import requests
import html
import json
from urllib.parse import unquote_plus

from orbis_eval.core.base import AggregationBaseClass
# from orbis_plugin_aggregation_dbpedia_entity_types import Main as dbpedia_entity_types

import logging
logger = logging.getLogger("Weblyzard_Harvest")


class Main(AggregationBaseClass):

    def query(self, item):
        service_url = 'http://localhost:5000/extract_from_html'

        print(item['url'])
        data = {'url': item['url'], 'html': item['corpus'], 'text': item['corpus_modified']}

        try:
            response = requests.post(service_url, json=data)
        except Exception as exception:
            print(f"Query failed: {exception}")
            response = None

        response_dict = json.loads(response.text)
        # print(f"Response: {response_dict['entities']}")
        return response_dict

    def map_entities(self, response, item):
        file_entities = []

        if not response:
            return None
        for entity, entity_data in response["entities"].items():
            for doc in entity_data:
                print(doc)
                """
                'doc_id': doc_id,
                    'type': item,
                    'surface_form'
                result['  '][doc_id]
                """
                # print(f"\n{doc['type']}")
                # print(f"Surface_form {doc['surface_form']}")
                # print(doc['type'])

                doc['key'] = doc['doc_id']
                doc["entity_type"] = doc['type']
                if doc.get("surface_form"):
                    doc["surfaceForm"] = doc['surface_form']
                    doc["document_start"] = doc.get("start", item['corpus_modified'].find(doc['surface_form']))
                    doc["document_end"] = doc.get("end", doc["document_start"] + len(doc['surface_form']))
                    file_entities.append(doc)
        return file_entities
