class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_start_menu(self):
        self.view.clear()
        while 1:
            self.view.clear()
            self.view.show_start_menu()
            try:
                operation = int(input())
            except:
                continue
            if operation == 1:
                self.show_get_menu()
            elif operation == 2:
                self.show_insert_menu()
            elif operation == 3:
                self.show_update_menu()
            elif operation == 4:
                self.show_remove_menu()
            elif operation == 5:
                print(self.model.generate_random())
            elif operation == 6:
                self.show_special_search()
            elif operation == 0:
                return
            else:
                self.view.clear()
                continue

    def show_get_menu(self):
        self.view.clear()
        while 1:
            self.view.clear()
            self.view.show_get_menu()
            try:
                operation = int(input())
            except:
                continue
            if operation == 1:
                return self.show_get(1, 1)
            elif operation == 2:
                return self.show_get(2, 1)
            elif operation == 3:
                return self.show_get(3)
            elif operation == 4:
                return self.show_get(4)
            elif operation == 5:
                return self.show_get(5)
            elif operation == 0:
                return
            else:
                self.view.clear()
                continue

    def show_insert_menu(self):
        self.view.clear()
        while 1:
            self.view.clear()
            self.view.show_insert_menu()
            try:
                operation = int(input())
            except:
                continue
            return self.show_insert(operation)

    def show_update_menu(self):
        self.view.clear()
        while 1:
            self.view.clear()
            self.view.show_update_menu()
            try:
                operation = int(input())
            except:
                continue
            return self.show_update(operation)

    def show_remove_menu(self):
        self.view.clear()
        while 1:
            self.view.clear()
            self.view.show_remove_menu()
            try:
                operation = int(input())
            except:
                continue
            return self.show_remove(operation)

    def show_get(self, operation, item_id=-1):
        self.view.clear()
        try:
            while 1:
                self.view.clear()
                if item_id != -1:
                    self.view.show_input(["id"])
                    item_id = int(input())
                if operation == 1:
                    print(self.model.get_film_and_categories(item_id))
                    input()
                    return
                elif operation == 2:
                    print(self.model.get_reviews_to_film(item_id))
                    input()
                    return
                elif operation == 3:
                    print(self.model.get_users())
                    input()
                    return
                elif operation == 4:
                    print(self.model.get_films())
                    input()
                    return
                elif operation == 5:
                    print(self.model.get_categories())
                    input()
                    return
                elif operation == 0:
                    return
                else:
                    self.view.clear()
                    continue
        except:
            print("Bad input data")
            input()

    def show_insert(self, operation):
        self.view.clear()
        try:
            if operation == 1:
                self.view.show_input(["username", "password", "avaUrl"])
                print(self.model.add_user(input(), input(), input()))
                input()
            elif operation == 2:
                self.view.show_input(["name", "director"])
                print(self.model.add_film(input(), input()))
                input()
            elif operation == 3:
                self.view.show_input(["name"])
                print(self.model.add_category(input()))
                input()
            elif operation == 4:
                self.view.show_input(["comment", "rating", "user_id", "film_id"])
                print(self.model.add_review(input(), int(input()), int(input()), int(input())))
                input()
            elif operation == 5:
                self.view.show_input(["film_id", "category_id"])
                print(self.model.add_film_category(int(input()), int(input())))
                input()
            elif operation == 0:
                return
            else:
                return
        except:
            print("Bad data")
            input()
            return

    def show_update(self, operation):
        self.view.clear()
        try:
            if operation == 1:
                self.view.show_input(["id", "username", "password", "avaUrl"])
                print(self.model.edit_user(int(input()), input(), input(), input()))
                input()
            elif operation == 2:
                self.view.show_input(["id", "name", "director"])
                print(self.model.edit_film(int(input()), input(), input()))
                input()
            elif operation == 3:
                self.view.show_input(["id", "name"])
                print(self.model.edit_category(int(input()), input()))
                input()
            elif operation == 4:
                self.view.show_input(["id", "comment", "rating", "user_id"])
                print(self.model.edit_review(int(input()), input(), int(input()), int(input())))
                input()
            elif operation == 0:
                return
            else:
                return
        except:
            print("Bad data")
            input()
            return

    def show_remove(self, operation):
        self.view.clear()
        try:
            if operation == 1:
                self.view.show_input(["id"])
                print(self.model.remove_user(int(input())))
                input()
            elif operation == 2:
                self.view.show_input(["id"])
                print(self.model.remove_film(int(input())))
                input()
            elif operation == 3:
                self.view.show_input(["id"])
                print(self.model.remove_category(int(input())))
                input()
            elif operation == 4:
                self.view.show_input(["id"])
                print(self.model.remove_review(int(input())))
                input()
            elif operation == 0:
                return
            else:
                return
        except:
            print("Bad data")
            input()
            return

    def show_special_search(self):
        self.view.clear()
        try:
            self.view.show_special_search()
            print(self.model.special_find(input(), input(), input()))
            input()
            return
        except:
            print("Something wrong")
            input()
            return
