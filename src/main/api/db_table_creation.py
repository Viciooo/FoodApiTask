from src.main.api.dbService import open_db

conn, cursor = open_db()

cursor.execute("""create table MEALS
(
    meal_id       integer not null
        primary key
        unique,
    search_id     TEXT    not null,
    name          varchar not null,
    picture       varchar,
    carbs         float,
    carbs_unit    varchar,
    proteins      float,
    proteins_unit varchar,
    calories      float,
    calories_unit varchar
);""")

cursor.execute("""create table MISSING_INGREDIENTS
(
    meal_id integer not null
        references MEALS
            on delete cascade,
    name    varchar
);
                """)

cursor.execute("""create table PRESENT_INGREDIENTS
(
    meal_id integer not null
        references MEALS
            on delete cascade,
    name    varchar
);""")


conn.commit()
conn.close()
