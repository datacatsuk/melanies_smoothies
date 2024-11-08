import streamlit as st
from snowflake.snowpark.functions import col

st.title("Customise Your Somoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want for your sommothie
    """
)

name_on_order = st.text_input("Name on smoothie:")
#st.write(name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect("Choose up to 5 ingredients"
                                    , my_dataframe
                                    , max_selections = 5
                                 )

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')
            """

    #st.write(my_insert_stmt)
    time_to_insert = st.button("Insert Order")

    if ingredients_string and time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
