from app.menu import menu
import os
import time


class Menue:
    list_obj=[]

    def __init__(self,name,parent):
        self.name = name
        self.parent = parent
        Menue.list_obj.append(self)

    # def __repr__(self) -> str:
    #     return self.name

    # def __str__(self) -> str:
    #     return f"{self.name},{self.parent}"
    
    @classmethod
    def find_obj(cls,name,parent_name):
        for obj in cls.list_obj:
            
            if obj.name == name and obj.parent.name==parent_name:
                return obj
            
   
    @staticmethod
    def print(enumerate_item):
        

                
                    enumerate_item=enumerate(enumerate_item)
                    for i , item in enumerate_item:

                        print(f"{str(i+1)}:{item['name']}")
    @staticmethod
    def match_number_to_name(enumerate_item,number):
        
        return enumerate_item[number]["name"]
    
    @staticmethod
    def input():
        number_choise=input("choose a number:\n if you want to go back please enter 'b' and exit 'e'\n  "  )
        return number_choise



class SubMenu(Menue):
    def __init__(self,name,parent,child_list):
        super().__init__(name,parent)
        self.child_list =child_list

   
    

class ActionMenu(Menue):

    def __init__(self,name,parent,list_action_func):
         super().__init__(name,parent)
         self.list_action_func=list_action_func



def generate_obj(menue,parent=None):
   


    for item in menue:


        if "action" in item:
            obj=ActionMenu(item["name"],parent,item["action"])
           
        
        elif "children" in item:
            
            obj=SubMenu(item["name"],parent,item["children"])
           
           
            generate_obj(item["children"],obj)


def display(obj):
    try:
        
            
            
            os.system('cls')

            if 'function' in obj.child_list[0]:
                
                if not  obj.child_list[0]['function'][0]():
                     
                     display(obj.parent)
                     
               
                 
        
            Menue.print(obj.child_list)
            number_choise=Menue.input()
        
            name_choise=Menue.match_number_to_name(obj.child_list,int(number_choise)-1)
            
            new_obj=Menue.find_obj(name_choise,obj.name)
        
            display(new_obj)
    except AttributeError:
            
            for func in obj.list_action_func:
                func()
    except (ValueError,IndexError):
            if number_choise=="b":
                if obj.parent==None:
                    print( "end")
                else:
                    display(obj.parent)
            if number_choise=="e":
                print("have good day! ")
                exit()
                 
            else:
                    print ("your choise is not valid\n please enter a correct number")
                    time.sleep(8)
                    display(obj)



generate_obj(menu.enter)
display(Menue.list_obj[0])