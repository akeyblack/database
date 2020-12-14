import psycopg2
import time

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
import logging

# dbname=reviews user=postgres password=12345

con = psycopg2.connect("dbname=reviews user=postgres password=12345")
cur = con.cursor()

Base = declarative_base()

engine = create_engine('postgresql://postgres:12345@localhost:5432/reviews')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()


films_categories_association = Table('film_category', Base.metadata,
                                     Column('film_id', Integer, ForeignKey('films.id')),
                                     Column('category_id', Integer, ForeignKey('categories.id'))
                                     )

films_review_association = Table('film_review', Base.metadata,
                                     Column('film_id', Integer, ForeignKey('films.id')),
                                     Column('review_id', Integer, ForeignKey('reviews.id'))
                                     )

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    ava_url = Column(String)

    def __init__(self, username, password, ava_url):
        self.username = username
        self.password = password
        self.ava_url = ava_url



class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    films = relationship("Film", secondary=films_categories_association, back_populates="categories")

    def __init__(self, name):
        self.name = name


class Film(Base):
    __tablename__ = "films"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    director = Column(String)
    categories = relationship("Category", secondary=films_categories_association, back_populates="films")
    reviews = relationship("Review", secondary=films_review_association)

    def __init__(self, name, director):
        self.name = name
        self.director = director

class Review(Base):
    __tablename__ = "reviews"
    comment = Column(String)
    id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")

    def __init__(self, comment, rating, user_id):
        self.comment = comment
        self.rating = rating
        self.user_id = user_id



def set_data_base(string):
    global con
    global cur
    con = psycopg2.connect(string)
    cur = con.cursor()


def close_database():
    cur.close()
    con.close()
    session.close()


def add_category(name):
    try:
        session.add(Category(name))
        session.commit()
        return "Completed"
    except Exception as error:
        return str(error)


def add_user(username, password, ava_url):
    try:
        session.add(User(username,password,ava_url))
        session.commit()
        return "Completed"
    except Exception as error:
        return str(error)


def add_film(name, director):
    try:
        session.add(Film(name,director))
        session.commit()
        return 'Completed'
    except Exception as error:
        return str(error)


def add_film_category(film_id, category_id):
    try:
        film = session.query(Film)\
            .filter(Film.id == film_id)\
            .first()
        category = session.query(Category)\
            .filter(Category.id == category_id)\
            .first()
        film.categories.append(category)
        session.commit()
        return 'Completed'
    except Exception as error:
        return str(error)


def add_review(comment, rating, user_id, film_id):
    try:
        review = Review(comment, rating, user_id)
        user = session.query(User)\
            .filter(User.id == user_id)\
            .first()
        if user is None:
            raise Exception('Cant find user with this id')
        film = session.query(Film) \
            .filter(Film.id == film_id) \
            .first()
        film.reviews.append(review)
        review.user=user
        session.commit()
        return 'Completed'
    except Exception as error:
        return str(error)


def edit_category(item_id, name):
    try:
        category = session.query(Category)\
            .filter(Category.id == item_id)\
            .first()
        category.name = name;
        session.commit();
        return "Completed"
    except Exception as error:
        return str(error)


def edit_user(item_id, username, password, ava_url):
    try:
        user = session.query(User).get(item_id)
        user.username = username
        user.password = password
        user.ava_url = ava_url
        session.commit();
        return "Completed"
    except Exception as error:
        return str(error)


def edit_film(item_id, name, director):
    try:
        film = session.query(Film).get(item_id)
        film.name = name
        film.director = director
        session.commit();
        return 'Completed'
    except Exception as error:
        return str(error)


def edit_review(item_id, comment, rating, user_id):
    try:
        review = session.query(Review).get(item_id)
        user = session.query(User).get(user_id)
        review.user = user;
        review.user_id = user_id;
        review.comment = comment;
        review.rating = rating;
        session.commit()
        return 'Completed'
    except Exception as error:
        return str(error)


def remove_category(item_id):
    try:
        category = session.query(Category).get(item_id)
        session.delete(category)
        session.commit()
        return "Completed"
    except Exception as error:
        return str(error)


def remove_user(item_id):
    try:
        user = session.query(User).get(item_id)
        session.delete(user)
        session.commit()
        return "Completed"
    except Exception as error:
        return str(error)


def remove_film(item_id):
    try:
        film = session.query(Film).get(item_id)
        session.delete(film)
        session.commit()
        return "Completed"
    except Exception as error:
        return str(error)


def remove_review(item_id):
    try:
        review = session.query(Review).get(item_id)
        session.delete(review)
        session.commit()
        return "Completed"
    except Exception as error:
        return str(error)


def remove_film_category(film_id, category_id):
    try:
        film = session.query(Film).get(film_id)
        category = session.query(Category).get(category_id)
        film.categories.remove(category)
        category.films.remove(film)
        session.commit()
        return 'Completed'
    except Exception as error:
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
        cur.execute("SELECT * FROM films ORDER BY id DESC".format())
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