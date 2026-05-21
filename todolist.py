todo_list=[]
def addList():
    item = input("Enter a new Task :")
    todo_list.append(item)
    print(f"{item} added to todo list")
def displayList():
    print("___________________________")
    print("To Do List")
    print("___________________________")
    for index, item in enumerate(todo_list,start=1):
        print(f"{index}-{item}")
def removeList():
    displayList()
    index = int(input("Enter the item number to remove : "))-1
    
    if 0<= index < len(todo_list):
      removed_item=todo_list.pop(index)
      print(f"{removed_item} removed from the list")
    else:
        print("Invalid item number")

def markComplete():
    displayList()
    index = int(input("Enter the item number to mark as complete : "))-1
    
    if 0<= index < len(todo_list):
      if "[Completed]" not in todo_list[index]:
          todo_list[index] += " [Completed]"
          print("Task marked as complete")
      else:
          print("Task is already marked as complete")
    else:
        print("Invalid item number")

while True:

    print("###########################")
    print("To Do List App")
    print("###########################")
    print("1- Add to List")
    print("2- View List")
    print("3- Mark tasks as Complete")
    print("4- Delete from List")
    print("5- Exit")
    print("###########################")

    option= input("Select your option : ")
    if option =="1":
        addList()
    elif option =="2":
        displayList()
    elif option =="3":
        markComplete()
    elif option =="4":
        removeList()
    elif option =="5":
        print("Exit")
        break
    else:
        print("Invalid option")