# -*- coding: utf-8 -*-

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image

st.set_page_config(layout="wide")

col1, col2, col3 = st.columns((0.7, 2, 0.7))
with col2:
     st.image(Image.open("images/The Punch logo.jpg"), width = 300) #use_container_width = True)

st.markdown(("## THE PUNCH Newspaper Recommender App"))
st.markdown("### *What PUNCH article should you read next?*")

st.markdown("""
1. **Get Started:**
            
    Use the dataset linked below to select a newspaper article, which can be used to find similar newspaper articles
2. **How to Use the Dataset**
            
    - Open the file using the link provided
    - Look through the URLs in the "URL" column
    - If you’re unsure which URL to pick, refer to the 'Tags' column for guidance on relevance
        - There are URLs on the following Tags: [ *News*, *Business*, *Metro Plus*, *General Health*, *Sport*, *Politics*, *Editorial*]
    - Copy the link to an article that interests you

3. **Next Step:**
            
    Paste the URL you selected into the search bar below to view the top 10 recommended newspaper articles tailors for you
            """)

# We create a text input field for users to enter the link to their last PUNCH article.
st.link_button("Excel File (URLs List)", "https://docs.google.com/spreadsheets/d/1dV_OY4kbTefQrQc9SGc752wJqK6NdiFH4wkHwN-gHFI/edit?usp=sharing", help = "Click this link to open the Excel file containing a list of URLs")

url = st.text_input(
    'Enter the link to your selected PUNCH article'
)
 

############ SIDEBAR CONTENT ############

st.sidebar.write('')


# For elements to be displayed in the sidebar, we need to add the sidebar element in the widget.



st.sidebar.image(Image.open("../images/tired_jet_lag.gif"), width = 300)
st.sidebar.markdown(
            """
            <div style="text-align: center">
                <div style="margin-top: -10px;">
                    <a href="https://giphy.com/gifs/computer-tired-jAe22Ec5iICCk" 
                    style="text-decoration: none; color: #2b7bba; font-size: 14px;" 
                    target="_blank">
                    Source: giphy.com
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.sidebar.markdown("---")
# Let's add some info about the app to the sidebar.

st.sidebar.write(
    """
    App created by [Olomo Ayooluwaposi] (https://github.com/posi-olomo) using [Streamlit] (https://streamlit.io/)
    """
)

def get_recommendation(url, cosine_sim, indices):
      
      if url not in indices:
            st.error("The provided link is not in the dataset.")
            return []

      # Get the index of the URL
      idx = indices[url]
    
      # cosine_sim[idx] == 1 row from the N by N dataframe showing the cosine similaries of every newspaper 
      # with this particular newspaper(url)
      # list(enumerate(cosine_sim[idx])) == a tuple "(newspaper index, similarity score)" of each newspaper's index
      # and it's similarity score
      # Remember that this is 1 row representing the selected newspaper, therefore the tuple shows the index and 
      # similarity score of every newspaper compared to the selected newspaper
      # Then convert this to a list
      sim_scores = list(enumerate(cosine_sim[idx]))
    
      # Sort the article not by the index but the second element in the tuple which is the cosine similarity
      # Reverse is True because it will sort the values from highest to lowest
      sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    
      # Show only the top 10 similar articles
      # We start from 1 because the article with the highest cosine similarity (1) is the article itself
      sim_scores = sim_scores[1:11]
    
      # Get the article indices
      # It is still a tuple and we want the indices, so we selected the 1st value in the tuple
      article_indices = [i[0] for i in sim_scores]
    
      # Map the article indices to the article link
      top_10 = data['URL'].iloc[article_indices]
    
      return top_10

if url:

    col1, col2, col3 = st.columns((0.7, 2, 0.7))

    with col2:
        st.image("../images/muhammad-taha-ibrahim-SUYgiqO2wAE-unsplash.jpg")

        st.markdown(
            """
            <div style="text-align: center">
                <p>A Black man reading The PUNCH newspaper</p>
                <div style="margin-top: -10px;">
                    <a href="https://unsplash.com/photos/man-in-black-shirt-sitting-beside-table-SUYgiqO2wAE?utm_content=creditShareLink&utm_medium=referral&utm_source=unsplash" 
                    style="text-decoration: none; color: #2b7bba; font-size: 14px;" 
                    target="_blank">
                    Credit: Photo by Muhammad-Taha Ibrahim
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.divider()
    c1, c2 = st.columns(2, gap ='large')

    with c1:

        st.markdown(r"$\underline{\text{Your PUNCH article is about:}}$")

    # Read the data file    
    data = pd.read_excel('../data/The Punch Cleaned File BackUp.xlsx')
    
    tag = data[data["URL"]==url]["TAGS"]

    # OUTPUT THE LABEL OF THE URL
    if not tag.empty:
        st.text(tag.values[0])
    else:
        st.error("URL not found in the Database. Try again with another URL.")

    # Labels that can be predicted
    labels = [ 'News', 'Business',  'Metro Plus', 'General Health', 'Sport', 'Politics', 'Editorial']

    st.divider()

    st.markdown('''
                #### :red[Newspaper Recommendations]''')
    
    # Create the TfidfVectorizer Object
    tfidf = TfidfVectorizer(max_features = 2000)
    
    # Create a matrix of word vectors
    tfidf_matrix = tfidf.fit_transform(data['CLEANED DATA'])

    # Cosine Similarities
    # Let's look at the similarities between each article
    #cosine_sim is a matrix of N by N, where N is the number of articles
    cosine_sim = cosine_similarity(tfidf_matrix,tfidf_matrix)

    # Map article links to their indices(index)
    indices = pd.Series(data.index, index=data['URL'])
    
    top_10 = get_recommendation(url, cosine_sim, indices)


    # Back to the Streamlit app
    st.table(top_10)

    # print(cosine_sim)

