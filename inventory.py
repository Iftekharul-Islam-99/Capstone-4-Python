
from tabulate import tabulate


#This contains all the relevant data for each object that is fed to to it.
class Shoes():
    
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
        
    def get_cost(self):
        self.cost
        
    def get_quanty(self):
        self.quantity
        
    def __repr__(self):
        return f"{self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity}"
        

#Reads the file 'inventory.txt' and copies that data to the class 'Shoes'.
#This also appends to the global variables 'shoes_list' and 'mod_shoes_list'.
def read_shoes_data():
    try:
        inv = open('inventory.txt','r')
    except FileNotFoundError:
        print("The file 'inventory.txt' could not be found\n")
        inv.close()
    
    for line in inv:
        line = line.split(',')
        product_entry = Shoes(line[0], line[1], line[2], line[3], line[4])
        shoes_list.append(product_entry)
        mod_shoes_list.append(product_entry)
        
    del mod_shoes_list[0]
    

#Allows the user to manualy enter new items to the database.    
def capture_shoes():
    country = str(input("Entr the details below:\nCountry: "))
    code = str(input("Product code: "))
    product = str(input("Product name: "))
    
    while True:
        try:
            cost = int(input("Cost: £"))
            quantity = int(input("Quantity: "))
            if (cost < 0) or (quantity < 0):
                print("Incorrect input. Try again.\n")
                continue
            break
        except ValueError:
            print("Incorrect input. Try again.\n")
            
    manual_product_entry = Shoes(country, code, product, str(cost), str(quantity))
    shoes_list.append(manual_product_entry)
    mod_shoes_list.append(manual_product_entry)


#Generates a table of data of the database.    
def view_all(): 
    data_list = []
    for line in shoes_list:
        line = str(line)
        line = line.replace('\n','')
        line = line.split(', ')
        data_list.append(line)
    
    #Used this a referance for generating tables using 'tabulate'.
    #https://www.askpython.com/python-modules/tabulate-tables-in-python
    print(tabulate(data_list, headers='firstrow', tablefmt='fancy_grid'))
   

#This funtion displays the products with the lowest stock.
#The user is given the option to add items to the stock of that item.
#This info is then update in the system and the file.    
def re_stock():
    all_data = ''
    count = 0
    low_shoes_list = []
    lowest = []
    
    for line in mod_shoes_list:
        line = line.quantity
        line = line.replace('\n','')
        lowest.append(int(line))
    low = min(lowest)
    
    for line in mod_shoes_list:
        if low == int(line.quantity.replace('\n','')):
            count += 1
            print(count, ": ", str(line).replace('\n',''), '\n')
            low_shoes_list.append(line)
    
    while True:
        while True:
            try:
                choice = int(input("If you wish to update the stock on these shoes"
                                   "enter the number corresponding to the shoe.\n"
                                   "Or enter '-1' to exit\n"))
                if choice <= 0 and choice != -1:
                    print("Incorrect input. Please try again\n")
                    continue
                break
            except ValueError:
                print("Incorrect input. Please try again\n")
            
        choice -= 1
        if choice in range(0,len(low_shoes_list)):
            print(f"chosen:\n{low_shoes_list[choice]}\n")
            while True:
                try:
                    add_quant = int(input("Enter the quantity of shoes you wish to"
                                         "add to stock: "))
                    if add_quant <= 0:
                        print("Incorrect input. Please try again\n")
                        continue
                    break
                except ValueError:
                    print("Incorrect input. Please try again\n")
            
            new_quant = int(low_shoes_list[choice].quantity) + add_quant
            low_shoes_list[choice].quantity = str(new_quant) + '\n'
    
            for line in shoes_list:
                line = str(line).replace('\n','')
                line = line + '\n'
                all_data += line

            all_data = all_data.replace(' ','')
            with open('inventory.txt', 'w') as inv_w:
                inv_w.write(all_data)
            break
        
        elif choice == -2:
            break
        else:
            print("znThat was not one of the options. Try again.\n")


#This takes in an input from the user and prints the corresponding product info.
#This info is printed only if the input matches the product id.
def search_shoes():
    code_list =[]
    
    while True:
        search = str(input("Enter the code of the product: ")).strip()
        for line in shoes_list:
            line = str(line.code).strip()
            line = line.replace('\n', '')
            code_list.append(line)

        if search in code_list:
            index = code_list.index(search)
            print(shoes_list[index], '\n')
            break
        else:
            print("product does not exist. Try another code\n")


#This funtion takes all the objects in the class 'Shoes' and
#generates a table of stock value of each product.
def value_per_item():
    header = ['Product', 'Stock value']
    product_list = []
    graph_list = []
    values_list = []
    
    #This generates 2 lists.
    #1st list contains all the product name
    #2nd list contains all the stock value of each procduct.
    for line in mod_shoes_list:
        value_item = int(line.cost) * int(line.quantity)
        values_list.append(value_item)
        line = str(line.product).strip()
        line = line.replace('\n', '')
        product_list.append(line)
        
    for line1,line2 in zip(product_list, values_list):
        combine = f"{line1},£{line2}"
        graph_list.append(combine.split(','))
    
    print(tabulate(graph_list, headers=header, tablefmt='fancy_grid'))


#This funtion finds the 'object' highest 'quantity' value and
#prints the corresponding product name and that the product is on sale.
def highest_qty():
    largest = []
    
    for line in mod_shoes_list:
        line = line.quantity
        line = line.replace('\n','')
        largest.append(int(line))
    high = max(largest)
    
    for line in mod_shoes_list:
        if high == int(line.quantity.replace('\n','')):
            print(f"{line.product.strip()} is on SALE!\n")


#Global variables that are used troughout in multiple functions.
shoes_list = []
mod_shoes_list = []
glob_count = 0
#Generating the class database at the start of the programme to initialise global variables.
read_shoes_data()

while True:
    menu = input("\nChoose from the menu below:\n"
                 "gd - Generate database\n"
                 "vd - View data\n"
                 "ap - Add product\n"
                 "s  - Search product\n"
                 "rs - Restock\n"
                 "v  - Value of stock\n"
                 "ps - Products on sale\n"
                 "e  - Exit\n->").lower().strip()
    
    if menu == 'gd':
        if glob_count >= 1:
            print("\nDatabase already generated.Choose another option.")
        else:    
            print("\nDatabase generated.\n")
            glob_count +=1
        
    elif menu == 'vd':
        view_all()
    elif menu == 'ap':
        capture_shoes()
    elif menu == 's':
        search_shoes()
    elif menu == 'rs':
        re_stock()
    elif menu == 'v':
        value_per_item()
    elif menu == 'ps':
        highest_qty()
    elif menu == 'e':
        break
    else:
        print("Incorrect choice. Try again\n")
     