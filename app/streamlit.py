# -*- coding: utf-8 -*-

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py

import pickle
import streamlit as st

c1, c2 = st.columns([0.32, 2])

with c1:
    st.image( "images/The Punch logo.jpg", widh = 85)

with c2:
    st.title("THE PUNCH Newspaper Recommender App")
    st.subheader("What PUNCH article should you read next?")
    st.text("Get a list of 10 newspaper articles similar to your last PUNCH article")

############ SIDEBAR CONTENT ############

st.sidebar.write('')


# For elements to be displayed in the sidebar, we need to add the sidebar element in the widget.

# We create a text input field for users to enter the link to their last PUNCH article.

st.sidebar.text_input(
    'Enter the link to your last PUNCH article',
    help = "Go to your last online PUNCH article and copy the link from the search bar and paste it here"
)


st.sidebar.markdown("---")

# Let's add some info about the app to the sidebar.

st.sidebar.write(
    """
    App created by [Olomo Ayooluwaposi] (https://github.com/posi-olomo) using [Streamlit] (https://streamlit.io/)
    """


"""## Recommender"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from google.colab import drive
drive.mount('/content/drive')

data = pd.read_excel('/content/drive/MyDrive/Punch Project/The Punch Cleaned File BackUp.xlsx')

# Create the TfidfVectorizer Object
tfidf = TfidfVectorizer(max_features = 2000)

# Create a matrix of word vectors
tfidf_matrix = tfidf.fit_transform(data['CLEANED DATA'])

print(tfidf_matrix.toarray())

"""Cosine Similarity"""

# Let's look at the similarities between each article
cosine_sim = cosine_similarity(tfidf_matrix,tfidf_matrix)

print(cosine_sim)

# Map article links to their indices(index)
indices = pd.Series(data.index, index=data['URL'])
indices

# Map article links to their indices(index)
indices = pd.Series(data.index, index=data['URL'])

def get_recommendation(link, cosine_sim, indices):
  idx = indices[link]

  # Create a list of tuples where the first element is the index of the article and
  # the second element is the cosine similarity of the article with the article above
  sim_scores = list(enumerate(cosine_sim[idx]))

  # Sort the article not by the index but the second element in the tuple which is the cosine similarity
  # Reverse is True because it will sort the values from highest to lowest
  sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)

  # Show only the top 10 similar articles
  # We start from 1 because the article with the highest cosine similarity (1) is the article itself
  sim_scores = sim_scores[1:11]
  print(sim_scores)

  # Get the article indices
  article_indices = [i[0] for i in sim_scores]

  # Map the article indices to the article link
  top_10 = data['URL'].iloc[article_indices]

  return top_10

url = 'https://punchng.com/presidential-inauguration-obi-didnt-call-for-boycott-postponement-lp/'
get_recommendation(url, cosine_sim, indices)

import pickle

#Let  us save the tfidf Vectorizer and the cosine similarity matrix
pickle.dump(tfidf, open('tfidf.pickle', 'wb'))
pickle.dump(cosine_sim, open('cosine_sim.pickle', 'wb'))

