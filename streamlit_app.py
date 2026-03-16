
# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write("Choose the fruit you want in your custom Smoothie!")

# Use Streamlit connection backed by secrets
cnx = st.connection('snowflake')
session = cnx.session()

name_of_order = st.text_input("Name on Smoothie:")
st.write("The name of the smoothie will be:", name_of_order)

# Get list of fruits
fruit_df = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
           .select(col('FRUIT_NAME'))
           .to_pandas()
)
fruit_list = fruit_df['FRUIT_NAME'].tolist()

ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_list, max_selections=5)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = (
        "insert into SMOOTHIES.PUBLIC.ORDERS(name_on_order, ingredients) "
        "values ('" + name_of_order + "', '" + ingredients_string + "')"
    )

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        if not name_of_order:
            st.error("Please enter a name for the smoothie before submitting.")
        else:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon='✅')
