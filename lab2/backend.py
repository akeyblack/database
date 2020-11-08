import psycopg2
import time

# dbname=reviews user=postgres password=12345

con = psycopg2.connect("dbname=reviews user=postgres password=12345")
cur = con.cursor()


def set_data_base(string):
    global con
    global cur
    con = psycopg2.connect(string)
    cur = con.cursor()


def close_database():
    cur.close()
    con.close()


def add_category(name):
    try:
        cur.execute("INSERT INTO categories (name) VALUES ('{0}')".format(name))
        con.commit()
        return "Completed"
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def add_user(username, password, ava_url):
    try:
        cur.execute("INSERT INTO users (username,password,ava_url) VALUES ('{0}','{1}','{2}') RETURNING id"
                    .format(username, password, ava_url))
        con.commit()
        return "Completed"
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def add_film(name, director):
    try:
        cur.execute("INSERT INTO films (name, director) VALUES ('{0}','{1}')"
                    .format(name, director))
        con.commit()
        return 'Completed'
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def add_film_category(film_id, category_id):
    try:
        cur.execute("SELECT 0 id from films WHERE id=({0})".format(film_id))
        is_exits = cur.fetchone()[0]
        if is_exits != 0:
            return "Can't find this film"
        cur.execute("SELECT 0 id from categories WHERE id=({0})".format(category_id))
        is_exits = cur.fetchone()[0]
        if is_exits != 0:
            return "Can't find this category"
        cur.execute("INSERT INTO film_category (film_id, category_id) VALUES ({0}, {1})"
                    .format(film_id, category_id))
        con.commit()
        return 'Completed'
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def add_review(comment, rating, user_id, film_id):
    try:
        cur.execute("SELECT 0 id from users WHERE id=({0})".format(user_id))
        if cur.fetchone() is None:
            return "Can't find this user"
        cur.execute("SELECT 0 id from films WHERE id=({0})".format(film_id))
        is_exits = cur.fetchone()[0]
        if is_exits != 0:
            return "Can't find this film"
        cur.execute("INSERT INTO reviews (comment, rating, user_id) VALUES ('{0}',{1},{2}) RETURNING id"
                    .format(comment, rating, user_id))
        last_id = cur.fetchone()[0]
        cur.execute("INSERT INTO film_review (film_id, review_id) VALUES ({0}, {1})"
                    .format(film_id, last_id))
        con.commit()
        return 'Completed'
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def edit_category(item_id, name):
    try:
        cur.execute("SELECT 0 id from categories WHERE id=({0})".format(item_id))
        if cur.fetchone() is None:
            return "Can't find this category"
        cur.execute("UPDATE categories SET name='{0}' WHERE id={1}".format(name, item_id))
        con.commit()
        return "Completed"
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def edit_user(item_id, username, password, ava_url):
    try:
        cur.execute("SELECT 0 id from users WHERE id=({0})".format(item_id))
        if cur.fetchone() is None:
            return "Can't find this user"
        cur.execute("""UPDATE users SET username='{0}', password='{1}', ava_url='{2}') 
                    VALUES ('{0}','{1}','{2}') WHERE id={3}"""
                    .format(username, password, ava_url, item_id))
        con.commit()
        return "Completed"
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def edit_film(item_id, name, director):
    try:
        cur.execute("SELECT 0 id from films WHERE id=({0})".format(item_id))
        if cur.fetchone() is None:
            return "Can't find this film"
        cur.execute("UPDATE films SET name='{0}', director='{1}' WHERE id={2}"
                    .format(name, director, item_id))
        con.commit()
        return 'Completed'
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def edit_review(item_id, comment, rating, user_id):
    try:
        cur.execute("SELECT 0 id from reviews WHERE id=({0})".format(item_id))
        if cur.fetchone() is None:
            return "Can't find this review"
        cur.execute("SELECT 0 id from users WHERE id=({0})".format(user_id))
        if cur.fetchone() is None:
            return "Can't find this user"
        cur.execute("UPDATE reviews SET comment='{0}', rating={1}, user_id={2} WHERE id={3}"
                    .format(comment, rating, user_id, item_id))
        con.commit()
        return 'Completed'
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def remove_category(item_id):
    try:
        cur.execute("SELECT 0 id from categories WHERE id=({0})".format(item_id))
        if cur.fetchone() is None:
            return "Can't find this category"
        cur.execute("DELETE FROM film_category WHERE category_id={0}".format(item_id))
        cur.execute("DELETE FROM categories WHERE id={0}".format(item_id))
        con.commit()
        return "Completed"
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def remove_user(item_id):
    try:
        cur.execute("SELECT 0 id from users WHERE id=({0})".format(item_id))
        if cur.fetchone() is None:
            return "Can't find this user"
        cur.execute("UPDATE reviews SET user_id=NULL WHERE user_id={0}".format(item_id))
        cur.execute("DELETE FROM users WHERE id={0}".format(item_id))
        con.commit()
        return "Completed"
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def remove_film(item_id):
    try:
        cur.execute("SELECT 0 id from films WHERE id=({0})".format(item_id))
        if cur.fetchone() is None:
            return "Can't find this film"
        cur.execute("DELETE FROM film_category WHERE film_id={0}".format(item_id))
        cur.execute("SELECT id FROM film_review WHERE film_id={0}".format(item_id))
        review_ids = cur.fetchall()
        cur.execute("DELETE FROM film_review WHERE film_id={0}".format(i1tem_id))
        for item in review_ids:
            cur.execute("DELETE FROM reviews WHERE id={0}".format(item[0]));
        cur.execute("DELETE FROM films WHERE id={0}".format(item_id))
        con.commit()
        return "Completed"
    except Exception as error:
        con.rollback()
        return str(error)


def remove_review(item_id):
    try:
        cur.execute("SELECT 0 id from reviews WHERE id=({0})".format(item_id))
        if cur.fetchone() is None:
            return "Can't find this review"
        cur.execute("DELETE FROM film_review WHERE review_id={0}".format(item_id))
        cur.execute("DELETE FROM reviews WHERE id={0}".format(item_id))
        con.commit()
        return "Completed"
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def remove_film_category(film_id, category_id):
    try:
        cur.execute("SELECT 0 id from films WHERE id=({0})".format(film_id))
        if cur.fetchone() is None:
            return "Can't find this film"
        cur.execute("SELECT 0 id from categories WHERE id=({0})".format(category_id))
        is_exits = cur.fetchone()[0]
        if is_exits != 0:
            return "Can't find this category"
        cur.execute("DELETE FROM film_category WHERE film_id={0} AND category_id={1}"
                    .format(film_id, category_id))
        con.commit()
        return 'Completed'
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def get_film_and_categories(film_id):
    try:
        string = ''
        cur.execute("SELECT * from films WHERE id={0}".format(film_id))
        item = cur.fetchone()
        if item is None:
            return "Cant find this film"
        for i in item:
            string += str(i) + " "
        cur.execute('''SELECT categories.id, categories.name from films JOIN film_category ON films.id=film_category.film_id
                JOIN categories ON film_category.category_id=categories.id WHERE films.id={0}'''.format(film_id))
        items = cur.fetchall()
        string += " with categories: "
        for item in items:
            for i in item:
                string += str(i) + ' '
        return string
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def get_reviews_to_film(film_id):
    try:
        cur.execute("SELECT * from films WHERE id={0}".format(film_id))
        item = cur.fetchone()
        if item is None:
            return "Cant find this film"
        string = "" + str(film_id) + ": \n"
        cur.execute('''SELECT reviews.id,reviews.rating,reviews.user_id,reviews.comment 
                FROM reviews LEFT JOIN film_review ON film_review.review_id=reviews.id 
                WHERE film_review.film_id = {0}'''.format(film_id))
        items = cur.fetchall()
        for item in items:
            for i in item:
                string += str(i) + ' '
            string += '\n'
        return string
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def get_users():
    try:
        string = "users: \n"
        cur.execute("SELECT * FROM users".format())
        items = cur.fetchall()
        if items is None:
            return "Cant find any user"
        for item in items:
            for i in item:
                string += str(i) + ' '
            string += '\n'
        return string
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def get_films():
    try:
        string = "films: \n"
        cur.execute("SELECT * FROM films".format())
        items = cur.fetchall()
        if items is None:
            return "Cant find any user"
        for item in items:
            for i in item:
                string += str(i) + ' '
            string += '\n'
        return string
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def get_categories():
    try:
        string = "categories: \n"
        cur.execute("SELECT * FROM categories".format())
        items = cur.fetchall()
        if items is None:
            return "Cant find any category"
        for item in items:
            for i in item:
                string += str(i) + ' '
            string += '\n'
        return string
    except psycopg2.ProgrammingError:
        con.rollback()
        return "Bad input data"
    except Exception as error:
        con.rollback()
        return str(error)


def special_find(name, director, category_name):
    try:
        start_time = time.time()
        query = '''
                SELECT films.name, films.director, categories.name
                FROM films 
                JOIN film_category ON films.id=film_category.film_id
                JOIN categories ON categories.id=film_category.category_id'''
        if name:
            query += " WHERE films.name LIKE '{0}'".format(name)
        if director and not name:
            query += " WHERE director LIKE '{0}' ".format(director)
        elif director:
            query += " AND director LIKE '{0}'".format(director)
        if category_name and not name and not director:
            query += " WHERE categories.name LIKE '{0}'".format(category_name)
        elif category_name:
            query += " AND categories.name LIKE '{0}'".format(category_name)
        cur.execute(query)
        string = ''
        items = cur.fetchall()
        if not items:
            return "no items"
        for item in items:
            for i in item:
                string += str(i) + ' '
            string += '\n'
        string += "\nTime:" + str((time.time() - start_time)*1000) + " milliseconds"
        return string
    except Exception as error:
        return str(error)


def generate_random():
    try:
        cur.execute('''
                INSERT INTO films (name,director)
                SELECT 
                chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int),
                chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int)
                FROM generate_series(1,100)''')
        cur.execute('''
                INSERT INTO categories (name)
                SELECT 
                chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int)
                FROM generate_series(1,100)''')
        cur.execute('''
                INSERT INTO users (username,password,ava_url)
                SELECT 
                chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int),
                chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int),
                chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int)
                FROM generate_series(1,100)''')
        cur.execute('''
                DO
                $$
                DECLARE
                    i record;
                BEGIN
                FOR i_num_count IN 1 .. 100 BY 1
                    LOOP
                        INSERT INTO film_category (film_id,category_id) VALUES (
                        (SELECT id FROM films
                        ORDER BY random()
                        LIMIT 1),
                        (SELECT id FROM categories
                        ORDER BY random()
                        LIMIT 1)
                        );
                    END LOOP;
                END;
                $$
                ;''')
        con.commit()
        return "Complete"
    except:
        con.rollback()
        return "Failed"