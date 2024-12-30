from config import *
from opensearchpy import helpers


def wrap_doc(doc):
    new_doc = {}
    new_doc.update({"_index": INDEX_NAME})
    new_doc.update({"_source": doc})

    return new_doc


def post_doc(client, doc):
    response = client.index(index=INDEX_NAME, body=doc)
    print(response)


def post_docs(client, docs):
    response = helpers.bulk(client, docs)
    print("Bulk insertion completed: ", response)
