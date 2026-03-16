# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw: ")
st.write(  """Choose the fruit you want in your custom Smoothie!  """)


import streamlit as st

cnx = st.connection('snowflake')
session = cnx.session()

name_of_order = st.text_input("Name on Smoothie:")
st.write("The name of the smoothie will be:", name_of_order)

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list= st.multiselect('Choose upto 5 ingradients:' , my_dataframe ,max_selections=5)

if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order,ingredients)
                    values ('""" + name_of_order + """', '""" + ingredients_string + """')"""

    st.write(my_insert_stmt)
  
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")

import requests  
smoothiefroot_response = requests.get("https://sturdy-bassoon-pqe9swv7g6z2rP6.8000.app.github.dev/api/fruit/watermelon")  
st.text(smoothiefroot_response)

