# Import python packages
import streamlit as st


# Write directly to the app
streamlit.title("My Parents New Healthy Diner")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    
    """
)  

from snowflake.snowpark.functions import col
cnx=st.connection("snowflake")
session=cnx.session()

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe
)
if ingredients_list:

    ingredients_string=''
    
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen +' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""
        
    time_to_insert=st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
