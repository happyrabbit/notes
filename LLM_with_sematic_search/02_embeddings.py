# !pip install cohere umap-learn altair datasets
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
import cohere
co = cohere.Client(os.environ['COHERE_API_KEY'])
import pandas as pd

# Word Embeddings
three_words = pd.DataFrame({'text':
  [
      'joy',
      'happiness',
      'potato'
  ]})

three_words
three_words_emb = co.embed(texts=list(three_words['text']),
                           model='embed-english-v2.0').embeddings

# Sentence Embeddings
sentences = pd.DataFrame({'text':
  [
   'Where is the world cup?',
   'The world cup is in Qatar',
   'What color is the sky?',
   'The sky is blue',
   'Where does the bear live?',
   'The bear lives in the the woods',
   'What is an apple?',
   'An apple is a fruit',
  ]})

sentences

emb = co.embed(texts=list(sentences['text']),
               model='embed-english-v2.0').embeddings

# Explore the 10 first entries of the embeddings of the 3 sentences:
for e in emb:
    print(e[:3])

#import umap
#import altair as alt

# hide the warnings that would appear when importing the UMAP library
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

from utils import umap_plot

chart = umap_plot(sentences, emb)
chart.interactive()

# Articles Embeddings
import pandas as pd
wiki_articles = pd.read_pickle('wikipedia.pkl')
wiki_articles

import numpy as np
from utils import umap_plot_big

articles = wiki_articles[['title', 'text']]
embeds = np.array([d for d in wiki_articles['emb']])

chart = umap_plot_big(articles, embeds)
chart.interactive()
