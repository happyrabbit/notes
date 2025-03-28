# !pip install cohere 
# !pip install weaviate-client Annoy
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

import cohere
co = cohere.Client(os.environ['COHERE_API_KEY'])

import weaviate
auth_config = weaviate.auth.AuthApiKey(
    api_key=os.environ['WEAVIATE_API_KEY'])

client = weaviate.Client(
    url=os.environ['WEAVIATE_API_URL'],
    auth_client_secret=auth_config,
    additional_headers={
        "X-Cohere-Api-Key": os.environ['COHERE_API_KEY'],
    }
)
client.is_ready() #check if True

def dense_retrieval(query, 
                    results_lang='en', 
                    properties = ["text", "title", "url", "views", "lang", "_additional {distance}"],
                    num_results=5):
    """
    Perform dense retrieval of articles from a Weaviate database based on a query.

    Args:
        query (str): The search query.
        results_lang (str): Language filter for the results (default is 'en').
        properties (list): List of properties to retrieve for each result.
        num_results (int): Number of results to return.

    Returns:
        list: Retrieved articles matching the query.
    """

    # Define the search concepts for the query
    nearText = {"concepts": [query]}
    
    # Define a filter to restrict results to a specific language
    where_filter = {
        "path": ["lang"],  # The property to filter by
        "operator": "Equal",  # The comparison operator
        "valueString": results_lang  # The value to match
    }
    
    # Perform the query on the Weaviate database
    response = (
        client.query
        .get("Articles", properties)  # Specify the class and properties to retrieve
        .with_near_text(nearText)  # Add the nearText search condition
        .with_where(where_filter)  # Apply the language filter
        .with_limit(num_results)  # Limit the number of results
        .do()  # Execute the query
    )

    # Extract the results from the response
    result = response['data']['Get']['Articles']

    return result

from utils import print_result

# Basic query
query = "Who wrote Hamlet?"
dense_retrieval_results = dense_retrieval(query)
print_result(dense_retrieval_results)

# Medium query
query = "What is the capital of Canada?"
dense_retrieval_results = dense_retrieval(query)
print_result(dense_retrieval_results)

# Complicated query
query = "What is the average temperature in the Sahara Desert in summer?"
dense_retrieval_results = dense_retrieval(query)
print_result(dense_retrieval_results)

# Building Semantic Search from Scratch
from annoy import AnnoyIndex
import numpy as np
import pandas as pd
import re

text = """
Interstellar is a 2014 epic science fiction film co-written, directed, and produced by Christopher Nolan.
It stars Matthew McConaughey, Anne Hathaway, Jessica Chastain, Bill Irwin, Ellen Burstyn, Matt Damon, and Michael Caine.
Set in a dystopian future where humanity is struggling to survive, the film follows a group of astronauts who travel through a wormhole near Saturn in search of a new home for mankind.

Brothers Christopher and Jonathan Nolan wrote the screenplay, which had its origins in a script Jonathan developed in 2007.
Caltech theoretical physicist and 2017 Nobel laureate in Physics[4] Kip Thorne was an executive producer, acted as a scientific consultant, and wrote a tie-in book, The Science of Interstellar.
Cinematographer Hoyte van Hoytema shot it on 35 mm movie film in the Panavision anamorphic format and IMAX 70 mm.
Principal photography began in late 2013 and took place in Alberta, Iceland, and Los Angeles.
Interstellar uses extensive practical and miniature effects and the company Double Negative created additional digital effects.

Interstellar premiered on October 26, 2014, in Los Angeles.
In the United States, it was first released on film stock, expanding to venues using digital projectors.
The film had a worldwide gross over $677 million (and $773 million with subsequent re-releases), making it the tenth-highest grossing film of 2014.
It received acclaim for its performances, direction, screenplay, musical score, visual effects, ambition, themes, and emotional weight.
It has also received praise from many astronomers for its scientific accuracy and portrayal of theoretical astrophysics. Since its premiere, Interstellar gained a cult following,[5] and now is regarded by many sci-fi experts as one of the best science-fiction films of all time.
Interstellar was nominated for five awards at the 87th Academy Awards, winning Best Visual Effects, and received numerous other accolades"""

# Split into a list of sentences
texts = text.split('.')
# Clean up to remove empty spaces and new lines
texts = np.array([t.strip(' \n') for t in texts])

# # Split into a list of paragraphs
# texts = text.split('\n\n')
# # Clean up to remove empty spaces and new lines
# texts = np.array([t.strip(' \n') for t in texts])

title = 'Interstellar (film)'
texts = np.array([f"{title} {t}" for t in texts])

# Get the embeddings
response = co.embed(
    texts=texts.tolist()
).embeddings

embeds = np.array(response)
embeds.shape

# Create the search index
search_index = AnnoyIndex(embeds.shape[1], 'angular')
# Add all the vectors to the search index
for i in range(len(embeds)):
    search_index.add_item(i, embeds[i])

search_index.build(10) # 10 trees
search_index.save('test.ann')

pd.set_option('display.max_colwidth', None)

def search(query):

  # Get the query's embedding
  query_embed = co.embed(texts=[query]).embeddings

  # Retrieve the nearest neighbors
  similar_item_ids = search_index.get_nns_by_vector(query_embed[0],
                                                    3,
                                                  include_distances=True)
  # Format the results
  results = pd.DataFrame(data={'texts': texts[similar_item_ids[0]],
                              'distance': similar_item_ids[1]})

  print(texts[similar_item_ids[0]])
    
  return results