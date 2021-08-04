def Eng_marks(E_Mks):
    while True:
        try:
            E_Mks = int(input("Enter English marks: "))
        except ValueError:
                print("Data type is not Invalid")
                continue        
        if E_Mks in range (0,41):
            break
        else:
            print("Marks Exceeded.Please try again later")
        
def IP_marks():
    ip_mark=int(input("Enter IP Marks:"))
    if ip_mark>40:
        print("Marks Exceeded.Please try again later")
    else:
        pass
def Ac_marks():
    ac_mark=int(input("Enter Accounts marks:"))
    if ac_mark>40:
        print("Marks Exceeded.Please try again later")
    else:
        pass
def Eco_marks():
    eco_mark=int(input("Enter Economics:"))
    if eco_mark>40:
        print("Marks Exceeded.Please try again later")
    else:
        pass
def Bst_mars():
    bst_mark=int(input("Enter Business studies marks:"))
    if bst_mark>40:
        print("Marks Exceeded.Please try again later")
    else:
        pass
def Phy_marks():
    Ph_mark=int(input("Enter Physical Education marks:"))
    if Ph_mark > 40:
        print("Marks exceeded.Please try again later")
    else:
        pass

        
        
        
        
        
        
        
        
   



    

    
        
 
        
    
    
    
     
        

    
