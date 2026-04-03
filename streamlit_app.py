import streamlit as st
import requests  
from snowflake.snowpark.functions import col

# Page setup
st.set_page_config(page_title="Melanie's Smoothies", page_icon="🥤")

# Title and instructions
st.title("🥤 Customize Your Smoothie!")
st.write("Choose up to 5 fruits for your custom smoothie.")

# Connect to Snowflake using the Streamlit connection in secrets
cnx = st.connection("snowflake")
session = cnx.session()

# Load fruit options from Snowflake
fruit_df = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
)

# Convert Snowpark DataFrame to a simple Python list for Streamlit widgets
fruit_list = [row["FRUIT_NAME"] for row in fruit_df.collect()]

# User input
name_on_order = st.text_input("Name on Smoothie:")
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Optional preview table
st.dataframe(fruit_df.to_pandas(), width="stretch")

# Submit order
if st.button("Submit Order"):
    if not name_on_order.strip():
        st.warning("Please enter a name for the order.")
    elif not ingredients_list:
        st.warning("Please choose at least one ingredient.")
    else:
        ingredients_string = ", ".join(ingredients_list)

        # Simple insert for the app
        insert_sql = f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{ingredients_string}', '{name_on_order.strip()}')
        """
        session.sql(insert_sql).collect()

        st.success(f"Order placed for {name_on_order.strip()}!")
        st.write("Ingredients:", ingredients_string)


# New section to display smoothiefroot nutrition information

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
st.text(smoothiefroot_response)
