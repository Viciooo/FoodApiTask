import sqlite3

conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE MEAL (
                meal_id integer not null UNIQUE primary key ,
                search_id TEXT not null,
                present_ingredients_list_id integer not null UNIQUE ,
                missing_ingredients_list_id integer not null UNIQUE ,
                name varchar not null,
                picture varchar,
                carbs float,
                carbs_unit varchar,
                proteins float,
                proteins_unit varchar,
                calories float,
                calories_unit varchar
                )""")

cursor.execute("""CREATE TABLE PRESENT_INGREDIENTS_LIST (
                present_ingredients_list_id integer primary key ,
                meal_name varchar not null
                )""")

cursor.execute("""CREATE TABLE MISSING_INGREDIENTS_LIST (
                missing_ingredients_list_id integer primary key ,
                meal_name varchar not null
                )""")

cursor.execute("""CREATE TABLE INGREDIENT (
                present_ingredients_list_id integer ,
                missing_ingredients_list_id integer ,
                name varchar
                )""")

conn.commit()
conn.close()
