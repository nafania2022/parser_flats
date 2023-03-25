import psycopg2
import time
import logging
import traceback
import sentry.sentry_logger as sentry_logger
from datetime import datetime

DBNAME = 'postgres'
USER = 'postgresql'
PASSWORD = 'postgresql'
HOST = '127.0.0.1'


def create_flats_table():
    try:    
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                CREATE TABLE IF NOT EXISTS flats (
                    id serial PRIMARY KEY,
                    link CHARACTER VARYING(300) UNIQUE NOT NULL,
                    reference CHARACTER VARYING(30),
                    price INTEGER,
                    price_meter INTEGER,
                    city CHARACTER VARYING(30),
                    title CHARACTER VARYING(1000),
                    description CHARACTER VARYING(3000),
                    date TIMESTAMP WITH TIME ZONE,
                    photo_links TEXT,
                    is_tg_posted BOOLEAN,
                    is_archive BOOLEAN
                    )''')
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {create_flats_table.__name__} : {traceback.format_exc()}')    
                
            
def create_city_table():
    try:    
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                CREATE TABLE IF NOT EXISTS cities (
                    id serial PRIMARY KEY,
                    city CHARACTER VARYING(30) UNIQUE NOT NULL
                    )''')
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {create_city_table.__name__} : {traceback.format_exc()}')


def create_subscriptions_table():  
    try:
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                CREATE TABLE IF NOT EXISTS user_subscriptions (
                    id serial PRIMARY KEY,
                    user_id BIGINT UNIQUE NOT NULL,
                    sort_price BOOLEAN,
                    sort_city BOOLEAN,
                    date TIMESTAMP WITHOUT TIME ZONE
                    )''')
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {get_flats_less_price.__name__} : {traceback.format_exc()}')
        
            
def add_user_subscriptions(user_id, sort_price, sort_city ):
    try:
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO user_subscriptions (user_id, sort_price, sort_city, date) VALUES (%s, %s, %s, %s)  
                    ON CONFLICT (user_id) DO UPDATE
                    SET
                    user_id = EXCLUDED.user_id,
                    sort_price = EXCLUDED.sort_price, 
                    sort_city = EXCLUDED.sort_city, 
                    date = EXCLUDED.date 
                            ''',
                        (user_id, sort_price, sort_city, datetime.now())   
                            )
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {add_user_subscriptions.__name__} : {traceback.format_exc()}')     
          
            
def check_subscriptions():
    try:
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    DELETE FROM user_subscriptions 
                    WHERE
                    DATE_PART('day', %(date)s - date ) >= 31     
                            ''',
                            {"date":datetime.now()}
                            
                            )
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {check_subscriptions.__name__} : {traceback.format_exc()}')   
             
            
def insert_flat(flat):
    try:    
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO flats (link, reference, price, price_metre, city, title, description, date, photo_links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    ON CONFLICT (link) DO UPDATE 
                    SET 
                    link = EXCLUDED.link, 
                    price = EXCLUDED.price,
                    price_meter = EXCLUDED.price_meter,
                    city = EXCLUDED.city,
                    title = EXCLUDED.title, 
                    description = EXCLUDED.description, 
                    date = EXCLUDED.date
                    ''',
                            (flat.link, flat.reference, flat.price, flat.price_meter, flat.city, flat.title, flat.description, flat.date,
                            ','.join(flat.images))
                            )
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {insert_flat.__name__} : {traceback.format_exc()}')    
                
            
def insert_cities():
    try:    
        cityes = [city for city in get_city_from_flats()]  
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM cities")
                cur.executemany('''
                    INSERT INTO cities (city) VALUES (%s) 
                    ON CONFLICT (city) DO UPDATE 
                    SET 
                    city = EXCLUDED.city
                    ''', cityes
                            )
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {insert_cities.__name__} : {traceback.format_exc()}')
            
                     
def insert_all_flats(flats):
    time_start = time.time()
    all_flats = []
    for flat in flats:
        fl = []      
        fl.append(flat.link)
        fl.append(flat.reference)
        fl.append(flat.price)
        fl.append(flat.price_meter)
        fl.append(flat.city)
        fl.append(flat.title)
        fl.append(flat.description)
        fl.append(flat.date)
        fl.append(','.join(flat.images))
        all_flats.append(tuple(fl))
    
    try:    
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.executemany('''
                        INSERT INTO flats (link, reference, price, price_meter, city, title, description, date, photo_links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (link) DO UPDATE
                        set
                        link = EXCLUDED.link, 
                        price = EXCLUDED.price,
                        price_meter = EXCLUDED.price_meter,
                        city = EXCLUDED.city,
                        title = EXCLUDED.title, 
                        description = EXCLUDED.description, 
                        date = EXCLUDED.date
                        ''', all_flats)
                time_end = time.time() - time_start
                print("Все загружено в бд", time_end)
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {insert_all_flats.__name__} : {traceback.format_exc()}')
        

def get_all_not_posted_flats(parser_types):
    try:    
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                        SELECT link, reference, price, price_meter, city, title, description, date, photo_links, id FROM flats
                        WHERE (is_tg_posted = false or is_tg_posted IS NULL) 
                        and reference IN %(parser_types)s
                    ''',
                            {'parser_types': tuple(parser_types)}
                            )
                return cur.fetchall()
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {get_all_not_posted_flats.__name__} : {traceback.format_exc()}')
        

def update_is_posted_state(ids):
    try:    
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                        UPDATE flats SET
                        is_tg_posted = true
                        WHERE id = ANY(%s)
                    ''',
                            [ids, ]
                            )
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {update_is_posted_state.__name__} : {traceback.format_exc()}')      
              
            
def get_flats_not_archive(link):
    try:    
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                        SELECT link, reference, price, price_meter, city, title, description, date, photo_links, id FROM flats
                        WHERE (is_archive = false or is_archive IS NULL) 
                        and link NOT IN %(parser_link)s
                    ''',
                            {'parser_link': tuple(link)}
                            )
                return cur.fetchall()
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {get_flats_not_archive.__name__} : {traceback.format_exc()}')  
          
        
def get_flats_less_price(price):
    try:   
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                        SELECT link, reference, price, price_meter, city, title, description, date, photo_links, id FROM flats
                        WHERE (is_archive = false or is_archive IS NULL) 
                        and price_meter < %(price)s
                    ''',
                            {'price': price}
                            )
                return cur.fetchall()
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {get_flats_less_price.__name__} : {traceback.format_exc()}')
        
        
           
def update_is_archive_state(ids):
    try:    
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                        UPDATE flats SET
                        is_archive = true
                        WHERE id = ANY(%s)
                    ''',
                            [ids, ]
                        )
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {update_is_archive_state.__name__} : {traceback.format_exc()}')      
              

def get_filter_flats_city(city): 
    try:       
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                        SELECT link, reference, price, price_meter, city, title, description, date, photo_links, id FROM flats
                        WHERE (is_archive = false or is_archive IS NULL) and city = %(city)s 
                    ''',
                            {'city': city}
                            )
                return cur.fetchall()
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {get_filter_flats_city.__name__}')
    
    
def get_city_from_flats():
    try:    
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                            SELECT city FROM flats
                            WHERE is_archive = false or is_archive IS NULL
                            
                            ''')
                return cur.fetchall()
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {get_city_from_flats.__name__} : {traceback.format_exc()}')
        

def get_city():
    try:   
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT city FROM cities")
                return cur.fetchall()
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {get_city.__name__}')
        

def get_user_id_subscriotions():
    try:
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id FROM user_subscriptions")
                return cur.fetchall()
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {get_user_id_subscriotions.__name__} : {traceback.format_exc()}')    
        
        
def get_subscriotions_user(user_id):
    try:
        with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT sort_price, sort_city FROM user_subscriptions
                    WHERE user_id  = %(user_id)s
                            ''',
                            {"user_id": user_id}
                            )
                
                return cur.fetchall()
    except Exception as e:
        logging.error(f'Возникла ошибка {e} в {get_subscriotions_user.__name__} : {traceback.format_exc()}')  
          
# create_city_table()
# create_flats_table()
# create_subscriptions_table()
insert_cities()