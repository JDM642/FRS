import streamlit as st
import pickle
import pandas as pd
from serpapi import GoogleSearch


#iving title
st.title('Swiggy Recommender System')

#Loading food list
food_dict= pickle.load(open('food_dict.pkl','rb'))
food= pd.DataFrame(food_dict)

#Making item_similarity
item_similarity= pickle.load(open('item_similarity.pkl','rb'))

#Making a Drop down box
selected_food_name = st.selectbox(
'What do you want to eat',
food.index.values)

#Fetching Poster
def fetch_poster(x):
    params = {
        "api_key": "dea32cc0aa99122da38af3f3d38901f54261593e5a55fcb84927d6bd5f09fb55",
        "engine": "google_images",
        "google_domain": "google.co.in",
        "q": "{}".format(x),
        "hl": "hi",
        "gl": "in",
        "location": "Maharashtra, India"
    }
    search = GoogleSearch(params)
    image_results = []
    results = search.get_dict()  # JSON -> Python dictionary
    for image in results["images_results"]:
        image_results.append(image["original"])
        break
    for results in image_results:
        return results

def foodprediction(selected_item):
    item_index =food.index.get_loc(selected_item) # Find the item's index in the user-item matrix
    item_similarities = item_similarity[item_index] # Calculate item-item similarities for the selected item
    top_similar_items = item_similarities.argsort()[::-1][1:6] # Find the top N similar items (excluding the selected item itself)
    recommended_items = food.index[top_similar_items]
    recommended_movie_posters=[]
    for item in recommended_items:
        recommended_movie_posters.append(fetch_poster(item))
    return recommended_items,recommended_movie_posters

#Inserting recommend button
if st.button('Recommend', type="primary"):
    names,posters= foodprediction(selected_food_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown("<h1 style='font-size: 24px;'>{}</h1>".format(names[0]), unsafe_allow_html=True)
        st.image(posters[0])

    with col2:
        st.markdown("<h1 style='font-size: 24px;'>{}</h1>".format(names[1]), unsafe_allow_html=True)
        st.image(posters[1])

    with col3:
        st.markdown("<h1 style='font-size: 24px;'>{}</h1>".format(names[2]), unsafe_allow_html=True)
        st.image(posters[2])

    with col4:
        st.markdown("<h1 style='font-size: 24px;'>{}</h1>".format(names[3]), unsafe_allow_html=True)
        st.image(posters[3])

    with col5:
        st.markdown("<h1 style='font-size: 24px;'>{}</h1>".format(names[4]), unsafe_allow_html=True)
        st.image(posters[4])
