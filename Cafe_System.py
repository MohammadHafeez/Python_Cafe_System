# imports
import pyfirmata
from time import sleep
board = pyfirmata.Arduino("COM3")
iterator =pyfirmata.util.Iterator(board) #overflow or buffer to prevent overloading of servo
iterator.start()
Xmotor = board.get_pin('d:6:s')
Xmotor.write(0)
# functions
def printMenu(menu_data):
    x = 0
    print("{0:^31}\n-------------------------------".format("Welcome To Starbarks Cafe"))
    print(" {0} {1:20} {2}\n-------------------------------".format("", "Item", "price"))
    for key in menu_data:
        print("\n  {0}\n===============================".format(key))
        for subkey in menu_data[key]:
            x += 1
            print("{0:>3} {1:<18} {2}".format(x, subkey, "$"+str(menu_data[key][subkey]["Price"])))

def redLight(board):
    red_led.write(1)
    board.pass_time(0.5)
    red_led.write(0)

def greenLight(board):
    green_led.write(1)
    board.pass_time(0.5)
    green_led.write(0)

def AddItems():
    super_cart = []
    while True:
        cart = []
        item_choice = input("Which item would you like to purchase (0-9). 0 to stop choosing: ")
        if item_choice == "0":
            break

        while item_choice.isalpha():
            item_choice = input("Please Select a number (0-9): ")
        while int(item_choice) > 9 or int(item_choice) < 0:
            item_choice = input("Please Select a valid number (0-9): ")
        cart.append(int(item_choice))

        if int(item_choice) % 2 == 0:
            redLight(board)
        elif int(item_choice) % 2 != 0:
            greenLight(board)


        item_qty = input("Enter the amount you would like to puchase: ")
        while item_qty.isalpha():
            item_qty = input("Please Select a valid input: ")
        cart.append(int(item_qty))

        super_cart.append(cart)

    for i in super_cart:
        for key in menu_data:
            for subkey in menu_data[key]:
                if menu_data[key][subkey]["Index"] == i[0]:
                    menu_data[key][subkey]["Qty"] += i[1]

    return super_cart

def removeItem():
    dict_list = []
    x = 0
    print("\n{0:^36}\n------------------------------------".format("Purchased Items"))
    print(" {0} {1:20} {2:7} {3}\n------------------------------------".format("", "Item", "price", "Qty"))
    for key in menu_data:
        print("\n  {0}\n====================================".format(key))
        for subkey in menu_data[key]:
            if menu_data[key][subkey]["Qty"] > 0:
                x += 1
                print("{0:>3} {1:<18} {2:7} {3:>3}".format(x, subkey, "$" + str(menu_data[key][subkey]["Price"]),
                                                           menu_data[key][subkey]["Qty"]))
                dict_list.append({menu_data[key][subkey]["Index"]: {"Desc": subkey,
                                                                    "Price": menu_data[key][subkey]["Price"],
                                                                    "Qty": menu_data[key][subkey]["Qty"]}})

    user_option = input("\nSelect the item you wish to reduce (1-{0}): ".format(len(dict_list)))
    while user_option.isalpha():
        user_option = input("Please Select a number (1-{0}): ".format(len(dict_list)))
    while int(user_option) > len(dict_list) or int(user_option) <= 0:
        user_option = input("Please Select a valid number (1-{0}): ".format(len(dict_list)))

    amount_reducable = input("\nSelect the amount you wish to reduce the item by: ")
    while user_option.isalpha():
        amount_reducable = input("Please Select a number: ")

    for index in dict_list[int(user_option) - 1]:
        for key in menu_data:
            for subkey in menu_data[key]:
                if menu_data[key][subkey]["Index"] == index:
                    dict = menu_data[key][subkey]
                    while int(amount_reducable) > dict["Qty"] or int(amount_reducable) < 0:
                        amount_reducable = input("Please Select a valid amount: ")
                    menu_data[key][subkey]["Qty"] -= int(amount_reducable)

def calcCost(menu_data):
    total = 0
    for key in menu_data:
        for subkey in menu_data[key]:
            if menu_data[key][subkey]["Qty"] > 0:
                total += menu_data[key][subkey]["Qty"] * menu_data[key][subkey]["Price"]

    purchase_disc = 0
    member_disc = 0

    if total >= 10:
        purchase_disc = total * 0.05

    is_member = input("\nAre you a member of starbarks cafe (Y/N): ").lower()
    while is_member != "y" and is_member != "n":
        is_member = input("Please select valid input (Y/N): ").lower()

    if is_member == "y":
        member_disc = (total-purchase_disc) * 0.15

    gst = (total-purchase_disc-member_disc) * 0.07
    net_total = total - purchase_disc - member_disc + gst

    return [total, purchase_disc, member_disc, gst, net_total]

def printReceipt(menu_data):
    costDesc = ["Total Amount", "Purchase Disc.", "Member Disc.", "GST", "Net Total"]
    calcList = calcCost(menu_data)
    x = 0

    print("\n{0:^36}\n------------------------------------".format("Starbarks Cafe Receipt"))
    print(" {0} {1:20} {2:7} {3}\n------------------------------------".format("", "Item", "price", "Qty"))
    for key in menu_data:
        print("\n  {0}\n====================================".format(key))
        for subkey in menu_data[key]:
            if menu_data[key][subkey]["Qty"] > 0:
                x += 1
                print("{0:>3} {1:<18} {2:7} {3:>3}".format(x, subkey, "$"+str(menu_data[key][subkey]["Price"]),menu_data[key][subkey]["Qty"]))
    print("\n------------------------------------")
    for i in range(len(costDesc)):
        print("  {0:20} {1}".format(costDesc[i], "$"+str(round(calcList[i],2))))

def changeOrder(menu_data):
    for i in range(len(option_list)):
        print("({0}) {1}".format(i + 1, option_list[i]))
    user_choice = input("What would you like to do (1 or 2): ")

    while user_choice.isalpha():
        user_choice = input("Please Select a number (1 or 2): ")
    while int(user_choice) > 2 or int(user_choice) < 1:
        user_choice = input("Please Select a valid number (1 or 2): ")

    if user_choice == "1":
        printMenu(menu_data)
        AddItems()
    elif user_choice == "2":
        removeItem()

def setServoAngle(angle):
    Xmotor.write(angle)
    sleep(0.015)

def rotateServo():
    while True:
        for i in range(0,180):
            setServoAngle(i)

        board.exit()
        break

# data
menu_data = {
    "Drinks": {
        "Coffee":{ "Index": 1, "Price": 4.00, "Qty": 0 },
        "Tea":{ "Index": 2, "Price": 3.00, "Qty": 0 },
        "Coca-Cola":{ "Index": 3, "Price": 2.00, "Qty": 0 },
        "Bubble Tea":{ "Index": 4, "Price": 3.66, "Qty": 0 },
    },
    "Food": {
        "Scone":{ "Index": 5, "Price": 2.45, "Qty": 0 },
        "Spicy Nugget":{ "Index": 6, "Price": 3.42, "Qty": 0 },
        "Truffle Fries":{ "Index": 7, "Price": 4.56, "Qty": 0 },
        "Fried Chicken":{ "Index": 8, "Price": 3.65, "Qty": 0 },
        "Fried Rice":{ "Index": 9, "Price": 10.34, "Qty": 0 },
    }
}
option_list = ["Add items", "Remove items"]
super_cart = []
red_led = board.get_pin('d:11:o')
green_led = board.get_pin("d:13:o")
iter = pyfirmata.util.Iterator(board)

# main code
while True:
    printMenu(menu_data)
    print("")
    super_cart = AddItems()
    printReceipt(menu_data)
    while True:
        is_satisfied = input("\nDo you wish to make changes? (Y/N): ").lower()
        while is_satisfied != "y" and is_satisfied != "n":
            is_satisfied = input("Please select valid input (Y/N): ").lower()
        print("")
        if is_satisfied == "y":
            changeOrder(menu_data)
            printReceipt(menu_data)
        else:
            print("Thank you for purchasing from Starbarks")
            rotateServo()
            break
    break