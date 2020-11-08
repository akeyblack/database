import backend


class Model(object):

    def __init__(self, db_string):
        self.db_string = db_string
        backend.set_data_base(db_string)

    def __del__(self):
        backend.close_database()

    def add_category(self, name):
        return backend.add_category(name)

    def add_user(self, username, password, ava_url):
        return backend.add_user(username, password, ava_url)

    def add_film(self, name, director):
        return backend.add_film(name, director)

    def add_review(self, comment, rating, user_id, film_id):
        return backend.add_review(comment, rating, user_id, film_id)

    def add_film_category(self, film_id, category_id):
        return backend.add_film_category(film_id, category_id)

    def edit_category(self, item_id, name):
        return backend.edit_category(item_id, name)

    def edit_user(self, item_id, username, password, ava_url):
        return backend.edit_user(item_id, username, password, ava_url)

    def edit_film(self, item_id, name, director):
        return backend.edit_film(item_id, name, director)

    def edit_review(self, item_id, comment, rating, user_id):
        return backend.edit_review(item_id, comment, rating, user_id)

    def remove_category(self, item_id):
        return backend.remove_category(item_id)

    def remove_user(self, item_id):
        return backend.remove_user(item_id)

    def remove_film(self, item_id):
        return backend.remove_film(item_id)

    def remove_review(self, item_id):
        return backend.remove_review(item_id)

    def remove_film_category(self, film_id, category_id):
        return backend.remove_film_category(film_id, category_id)

    def get_film_and_categories(self, film_id):
        return backend.get_film_and_categories(film_id)

    def get_reviews_to_film(self, film_id):
        return backend.get_reviews_to_film(film_id)

    def get_users(self):
        return backend.get_users()

    def get_films(self):
        return backend.get_films()

    def get_categories(self):
        return backend.get_categories()

    def special_find(self, name, director, category_name):
        return backend.special_find(name, director, category_name)

    def generate_random(self):
        return backend.generate_random()