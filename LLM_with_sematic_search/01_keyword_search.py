# Setup

import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

import weaviate
auth_config = weaviate.auth.AuthApiKey(
    api_key=os.environ['WEAVIATE_API_KEY'])

# https://cohere-demo.weaviate.network/v1
# 10 million records from wikipedia
# each row is a paragraph from wikipedia
# they are in different languages
# we can choose which language to query

client = weaviate.Client(
    url=os.environ['WEAVIATE_API_URL'],
    auth_client_secret=auth_config,
    additional_headers={
        "X-Cohere-Api-Key": os.environ['COHERE_API_KEY'],
    }
)

# is true, it means our local Weaviate client is connected to the remote Weaviate database
# we are able to do a keyword search on this database
client.is_ready() 
#> True

# Keyword Search
def keyword_search(query, 
                   results_lang='en',
                   properties = ["title","url","text"],
                   num_results=3):
    # properties: list of properties to return in the response
    where_filter = {
    "path": ["lang"],
    "operator": "Equal",
    "valueString": results_lang
    }

    response = (
        client.query.get("Articles", properties)
        .with_bm25(query = query) # BM25 search
        .with_where(where_filter)
        .with_limit(num_results)
        .do()
    )
    result = response['data']['Get']['Articles']
    return result

query = "What is the most viewed televised event?"
keyword_search_results = keyword_search(query)
print(keyword_search_results)

def print_result(result):
    """ Print results with colorful formatting """
    for i,item in enumerate(result):
        print(f'item {i}')
        for key in item.keys():
            print(f"{key}:{item.get(key)}")
            print()
        print()

# change language and properties
properties = ["text", "title", "url", 
             "views", "lang"]

query = "What is the most viewed televised event?"
keyword_search_results = keyword_search(query, results_lang='de', properties = properties)
print_result(keyword_search_results)