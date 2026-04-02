# -----------------------------------------
# Import required Python packages
# -----------------------------------------
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# -----------------------------------------
# App Title and Instructions
# -----------------------------------------
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")


# -----------------------------------------
# Capture user input (name on the order)
# -----------------------------------------
name_on_order = st.text_input("Name on Smoothie:")

# Display confirmation of entered name
st.write("The name on your Smoothie will be:", name_on_order)


# -----------------------------------------
# Connect to Snowflake session
# -----------------------------------------
session = get_active_session()


# -----------------------------------------
# Load available fruit options from Snowflake
# -----------------------------------------
my_dataframe = (
    session
    .table("smoothies.public.fruit_options")  # Source table
    .select(col('FRUIT_NAME'))               # Select only fruit names
)

# Display available fruits in the UI
st.dataframe(data=my_dataframe, use_container_width=True)


# -----------------------------------------
# Allow user to select up to 5 ingredients
# -----------------------------------------
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)


# -----------------------------------------
# Process order when user selects ingredients
# -----------------------------------------
if ingredients_list:

    # Convert selected ingredients into a single string
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # Build SQL insert statement
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')
    """

    # Button to submit order
    time_to_insert = st.button('Submit Order')

    # Execute insert when button is clicked
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        # Success message to user
        st.success('Your Smoothie is ordered!', icon="✅")
