import streamlit as st
from snowflake.snowpark.functions import col

# Title
st.title("🥤 Customize Your Smoothie!")

# User input
name_on_order = st.text_input("Name on Smoothie:")

# ✅ NEW connection method (matches your image)
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit data
fruit_df = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col("FRUIT_NAME"))

# Convert to list
fruit_list = [row["FRUIT_NAME"] for row in fruit_df.collect()]

# Display
st.dataframe(fruit_df.to_pandas(), width="stretch")

# Select fruits
ingredients = st.multiselect("Choose up to 5 ingredients:", fruit_list, max_selections=5)

# Submit
if st.button("Submit Order"):
    if not name_on_order or not ingredients:
        st.warning("Enter a name and pick at least one fruit.")
    else:
        ingredients_string = ", ".join(ingredients)

        session.sql(f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """).collect()

        st.success("Order placed!")
