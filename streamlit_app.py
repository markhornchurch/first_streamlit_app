import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#just add a title, text or header
streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas will allow me to normalize the text file provided into a table.
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#streamlit.dataframe(my_fruit_list) chekck what index set does.
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)


#don't run anything past here while we troubleshoot.
#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_chioice):
      fruityvice_response = requests.get("https://Fruityvice.com/api/fruit/" + fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalized

#New Section to display api responses
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

    
streamlit.write('The user entered ', fruit_choice)


#don't run anything past here while we troubleshoot.
streamlit.stop()


#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list cotains:")
streamlit.dataframe(my_data_rows)


second_choice = streamlit.text_input('What fruit would you like to add?','Kiwi again')
streamlit.write('thanks for adding ', second_choice)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
