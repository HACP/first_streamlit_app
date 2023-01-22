import streamlit
import pandas
import requests

# adding connector - needs requirement.txt file
import snowflake.connector

# quering data from Snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from fruit_load_list")
#my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
#streamlit.dataframe(my_data_row)
streamlit.dataframe(my_data_rows)

streamlit.text("What fruit would you like to add")
# adding a search box for text
snowflake_fruit_choice = streamlit.text_input('What fruit would you like to add','jackfruit')
streamlit.write('The user entered ', snowflake_fruit_choice)


# formating the page
streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# reading data from an S3 bucket
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

# definining selected fruits
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# display table
#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

# New section to display fruityvice api fruityvice_response
streamlit.header("Fruityvice Fruit Advice!")

# adding a search box for text
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

# Adding a response from the API
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json())

# formatting to the response from the API
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display normalized table
streamlit.dataframe(fruityvice_normalized)
