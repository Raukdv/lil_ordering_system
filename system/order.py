from os import system, name
import time
from datetime import date
#Custom loader
from loader.custome import (
    PAYMENTS, 
    TRANSLATION, 
    BATH_ITEMS, 
    BATH_ITEMS_PRICE
)

class PorchOrder():

    def __init__(self, *args, **kwargs):
        #others values
        self.__first_welcome = False
        self.__first_instruction = False
        self.__done = False
        self.__customer = None
        #For user odering - This will be the total amount and price to paid at the end of the operation
        self.ordered_items = []
        self.total_ordered = []
        self.payment_selected = None

        #BIG CUSTOM LOADING FOR THE SYSTEM.
        if 'fromfile' in kwargs and kwargs.get('fromfile', None):
            self.payments = PAYMENTS
            self.translation = TRANSLATION
            self.bath_items = BATH_ITEMS
            self.bath_items_price = BATH_ITEMS_PRICE
        else:
            self.payments = {
                '1':'PagoMovil',
                '2':'Efectivo (Bs)',
                '3':'Efectivo (Divisas)',
                '4':'Transferencia'
            } 
            #Translate thing - idk dude, i just messing around
            self.translation = {
                'burge_normal': 'Hamburguesa normnale',
                'burge_spceial': 'Hamburguesa Especial',
                'burger_super_special': 'Hamburguesa Super Especial',
                'small_soda':'Refresco Pequeño',
                'big_soda': 'Refresco Grande',
                }
            #Default items
            self.bath_items = {
                'burge_normal': 10,
                'burge_spceial': 10,
                'burger_super_special': 10,
                'small_soda': 10,
                'big_soda': 10,
                }
            #Default items price
            self.bath_items_price = {
                'burge_normal': 3,
                'burge_spceial': 5,
                'burger_super_special': 10,
                'small_soda': 1,
                'big_soda': 3,
            }

    def _wait(self, seconds: int):
        time.sleep(seconds)

    def __call__(self):
        try:
            return self.handle()
        except Exception as err:
            print(err)
            self._wait(10)
        finally:
            pass

    def handle(self):
        self.do_ordering()
    
    #defin our request customer name
    def __add_customer(self):
        self.__customer = input('Su nombre y apellido por favor: ')

    # define our clear function
    def __clear_terminal(self):
        #for windows is nt and for mac and linux(here, os.name is 'posix')
        cleaned = system('clear' if name == 'posix' else 'cls')
        #if you have problem with system use subprocess call instaed, like this
        #from subprocess import call
        #cleaned = call('clear' if os.name == 'posix' else 'cls')

    def __wellcome_template(self):
        self.__clear_terminal()
        template = f'''
        Hola! Este es un sistema bien endogeno creado por alguien sin mucho que hacer despues el trabajo.

        En el menu hay disponibilidad de;
        
        0) Hamburguesas normnales a 3$
        1) Hamburguesas Especiales a 5$
        2) Hamburguesas Super Especiales a 10$
        3) Refresco Pequeño a 1$
        4) Refresco Grande a 3$

        '''
        print(template)
    
    def __check_menu(self):
        self.__clear_terminal()
        template = f''' bien {self.__customer} aqui tienes el menu:
        0) Hamburguesas normnales a 3$
        1) Hamburguesas Especiales a 5$
        2) Hamburguesas Super Especiales a 10$
        3) Refresco Pequeño a 1$
        4) Refresco Grande a 3$

        '''
        print(template)
    
    def __instructions(self):
        self.__clear_terminal()
        instructions = f'''
        Estimado {self.__customer} note que debe ingresar sus opciones de la siguiente forma:
        option cantidad
        ejemplo: 1 2

        si colocas ayuda, se te monstrara este mensaje de nuevo.
        si colocas menu, se te monstrara nuevamente las opciones del menu.
        si colocas disponibles, se te mostrara la cantidad disponible para comprar, si se agotan, no podras efecutar dicha opcion.
        si colocas revisar, se te monstrara la cantidad que llevas en tu orden.
        si colocas seguir, se te mostrara tu total ordenado y factura.
        si colocas salir, saldras del sistema y se cerrara.
        '''
        print(instructions)

    def __check_stock(self):
        self.__clear_terminal()
        for item, in_stock in self.bath_items.items():
            print(f'Quedan {in_stock} unidades de {self.translation[item]}')

    def __load_total(self, load: bool):
        #This will check the total in self.ordered_items to generate self.total_ordered if load is True
        keys = list(self.bath_items.keys())
        for key in keys:
            total_ordered = sum(item.get(key, 0) for item in self.ordered_items)
            if load:
                if total_ordered != 0:
                    self.total_ordered.append({key:total_ordered})
            else:
                if total_ordered != 0:
                    print(f"Se ha añadido a tu orden {total_ordered} unidades de {self.translation[key]}")
    #Thanks to Thierry Husson
    def printTable(self, myDict, colList=None):
        #Check https://stackoverflow.com/questions/17330139/python-printing-a-dictionary-as-a-horizontal-table-with-headers for more options
        """ Pretty print a list of dictionaries (myDict) as a dynamically sized table.
        If column names (colList) aren't specified, they will show in random order.
        Author: Thierry Husson - Use it as you want but don't blame me.
        """
        if not colList: colList = list(myDict[0].keys() if myDict else [])
        myList = [colList] # 1st row = header
        for item in myDict: myList.append([str(item[col] if item[col] is not None else '') for col in colList])
        colSize = [max(map(len,col)) for col in zip(*myList)]
        formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
        myList.insert(1, ['-' * i for i in colSize]) # Seperating line
        for item in myList: print(formatStr.format(*item))
    
    def __check_invoice(self):
        #Load you order
        self.__load_total(load=True)
        list_dict = []
        total_to_pay = 0
        #this will do the list dict for print pretty table and also calculate your total
        for data in self.total_ordered:
            key, value = list(data.items())[0]
            list_dict.append({'Productos':self.translation[key], 'Total':value, 'PrecioPorUnidad':self.bath_items_price[key]})
            total_to_pay += value * self.bath_items_price[key]
        
        template_haeder = f'''

        {date.today()} -- Ordering Site 1.0v --
        {self.__customer} haz seleccionado pagar con {self.payment_selected} los siguientes productos:

        '''
        print(template_haeder)
        self.printTable(list_dict, ['Productos','Total','PrecioPorUnidad'])
        print('-------')
        print(f'Tu total a pagar es de: {total_to_pay}$')
        print('-------')
        self.__done = True
    
    def __first_step_order(self):

        if not self.__first_instruction:
            self.__instructions()
            self.__first_instruction = True

        choice = input("¿Que desea hacer?: ")
        if choice == 'menu':
            self.__check_menu()
        elif choice == 'disponibles':
            self.__check_stock()
        elif choice == 'ayuda':
            self.__instructions()
        elif choice == 'revisar':
            self.__load_total(load=False)
        elif choice == 'seguir':
            self.__second_step_order()
        elif choice == 'salir':
            self.__done = True
        else:
            #Is better if you check formatting input first, instaed of run into the exact input, for example what happen if you put 12.
            #The current format its one list of two (2) element, if you can admit more elements to split and process you have to change the valitation of those line
            packed = choice.split(' ')
            if len(packed) > 1 and len(packed) <= 2:
                order = packed[0]
                amount = packed[1]
                #load keys for positions:
                #Validate int inputs too
                if order.isnumeric() and amount.isnumeric():
                    #Transfor dict_keys into list to get the corresponding dictionary value according to option
                    keys = list(self.bath_items.keys())
                    #get the exact value
                    key = keys[int(order)]
                    
                    #add data into your invoicing, first check if not key in dict, if it exists just update it, update the bath and check if you have stock in.
                    if self.bath_items[key] > 0:
                        #First add all the customer request.
                        self.ordered_items.append({key:int(amount)})

                        #Update your self.bath_items as stock
                        new_bath_amount = self.bath_items[key] - int(amount)
                        self.bath_items.update({key:new_bath_amount})
                    else:
                        print(f'No hay unidades disponibles para: {self.translation[key]}, tendra que escoger otra opcion')
 
            else:
                print("Your input is wrong, use opcion cantidad format to process")
    
    def __second_step_order(self):
        print('--- Se requiere que seleccione un metodo de pago ---')
        for key, value in self.payments.items():
            print(f'Marque {key} para pagar con {value}')
        
        payment = input(f'{self.__customer} introduzca un su metodo de pago: ')
        self._wait(2)
        self.payment_selected = self.payments[payment]
        self.__check_invoice()

    #System code
    def do_ordering(self):
        
        while not self.__done:
            #Do the welcome :D just one.
            if not self.__first_welcome:
                self.__wellcome_template()
                self.__first_welcome = True
            #Request the customer name
            if not self.__customer:
                self.__add_customer()
            
            #Do the fist step of order
            self.__first_step_order()
            
            

            

        