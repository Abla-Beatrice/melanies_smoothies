# -----------------------------------------
# Import required Python packages
# -----------------------------------------
import streamlit as st
import requests  
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# -----------------------------------------
# App title and instructions
# -----------------------------------------
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# -----------------------------------------
# Capture user input
# -----------------------------------------
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# -----------------------------------------
# Connect to Snowflake using Streamlit secrets
# -----------------------------------------
connection_parameters = st.secrets["connections"]["snowflake"]
session = Session.builder.configs(connection_parameters).create()

# -----------------------------------------
# Load available fruit options from Snowflake
# -----------------------------------------
my_dataframe = (
    session.table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
)

# Convert Snowpark DataFrame to a Python list for Streamlit multiselect
fruit_rows = my_dataframe.collect()
fruit_list = [row["FRUIT_NAME"] for row in fruit_rows]

# Display available fruits
st.dataframe(my_dataframe.to_pandas(), use_container_width=True)

# -----------------------------------------
# Allow user to select up to 5 ingredients
# -----------------------------------------
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# -----------------------------------------
# Process order when user selects ingredients
# -----------------------------------------
if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    if st.button("Submit Order"):
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")


smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)
