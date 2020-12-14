import os


class View(object):

    @staticmethod
    def show_start_menu():
        print('''Enter number of operation:
0.To return
1.Get data
2.Insert data
3.Update data 
4.Remove data 
5.Generate random
6.Special search''')

    @staticmethod
    def show_get_menu():
        print('''Enter number of operation:
0.To return
1.Get film and categories by id
2.Get reviews for film by id
3.Get users list
4.Get films
5.Get categories''')

    @staticmethod
    def show_insert_menu():
        print('''Enter number of operation:
0.To return
1.Insert user
2.Insert film
3.Insert category
4.Insert review
5.Insert category_to_film''')

    @staticmethod
    def show_update_menu():
        print('''Enter number of operation:
0.To return
1.Update user
2.Update film
3.Update category
4.Update review''')

    @staticmethod
    def show_remove_menu():
        print('''Enter number of operation:
0.To return
1.Remove user
2.Remove film
3.Remove category
4.Remove review''')

    @staticmethod
    def show_special_search():
        print('Enter film name, film director, category name')

    @staticmethod
    def show_input(array_of_attrs):
        string = 'Enter next attrs: '
        for item in array_of_attrs:
            string += item + " "
        print(string)

    @staticmethod
    def clear():
        os.system('cls')
