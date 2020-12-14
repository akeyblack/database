import controller
import view
import model

c = controller.Controller(model.Model("dbname=reviews user=postgres password=12345"), view.View())
c.show_start_menu()