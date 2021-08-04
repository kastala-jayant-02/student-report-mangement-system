import sys
import pandas as p
import mysql.connector as sql
import time
import random as RN

#DATABASE CONNECTION
Storehouse=sql.connect(host='localhost',user='root',passwd='jayant1234')
mycursor=Storehouse.cursor()

#CLASS FOR LIVE DATA STORING
class SQL():

    #STUDENTS REAL AND NOMINAL MARKS REPORT 
    def CreateTB(Student_name):
        try:
            mycursor.execute('use DataHouse')
            try:                
                mycursor.execute('CREATE TABLE %s(Subject_Name varchar(50),Periodic_One varchar(50),Half_Yearly varchar(50),Periodic_Two varchar(50),Annual_Test varchar(50));'\
                                 %(Student_name))
                mycursor.execute('CREATE TABLE %s(Subject_Name varchar(50),Periodic_One varchar(50),Half_Yearly varchar(50),Periodic_Two varchar(50),Annual_Test varchar(50));'\
                                 %(Student_name.title()+"_Real_values"))
            except:
                print("The table of this student already exists.The data storing...")
            Storehouse.commit()
        except:
            Storehouse.rollback()
            mycursor.execute("CREATE DATABASE %s;"%('DataHouse'))
            mycursor.execute('use DataHouse')
            mycursor.execute('CREATE TABLE %s(Subject_Name varchar(50),Periodic_One varchar(50),Half_Yearly varchar(50),Periodic_Two varchar(50),Annual_Test varchar(50));'\
                             %(Student_name))
            mycursor.execute('CREATE TABLE %s(Subject_Name varchar(50),Periodic_One varchar(50),Half_Yearly varchar(50),Periodic_Two varchar(50),Annual_Test varchar(50));'\
                             %(Student_name.title()+"_Real_values"))
            Storehouse.commit()
            
    #STUDENTS RESULT REPORT 
    def CreateRTB():
            try:
                mycursor.execute('use DataHouse')
                mycursor.execute('CREATE TABLE STUDENT_RESULT(Admin_No varchar(50),Student_name varchar(50),Stream varchar(50),Marks varchar(50),Marks_percentage \
                varchar(50),Status varchar(50))')
            except:
                print("The Result Table already exists,proceeding to recording data...")
                Storehouse.rollback()
            Storehouse.commit()
            
    #LIVE DATA RECORD FOR STUDENT REPORT
    def RecRTB(admin,Student_name,Stream,marks,percentage,status):
        mycursor.execute("use datahouse")
        mycursor.execute('insert into STUDENT_RESULT(Admin_no,Student_name,Stream,Marks,Marks_percentage,Status) values("%s","%s","%s","%s","%s","%s")'\
                         %(admin,Student_name,Stream,marks,percentage,status))
        Storehouse.commit()

    #SHOW REPORT DATA FROM RECORDS
    def SHRTB():
        try:
            Data_mark=[]
            Data_adm=[]
            Data_name=[]
            Data_markp=[]
            Data_stat=[]
            Data_Str=[]
            mycursor.execute('use DataHouse')
            mycursor.execute('select * from student_result;')
            record=mycursor.fetchall()
            for rec in record:
                Data_adm.append(rec[0])
                Data_name.append(rec[1])
                Data_Str.append(rec[2])
                Data_mark.append(rec[3])
                Data_markp.append(rec[4])
                Data_stat.append(rec[5])
            Table_data={'Admin_no':Data_adm,"Student_Name":Data_name,"Stream":Data_Str,"Nominal_Marks":Data_mark,"Marks_%age":Data_markp,"Status":Data_stat}
            Table=p.DataFrame(Table_data)
            print(Table)
            Storehouse.commit()
        except:
            print("There are no Records to show")
            Storehouse.rollback()

    #-----------------------------------------------CONFIGRATION OF DATA-----------------------------------

    #DELETION OF RECORD
    def delrec(Student_name):
        try:
            mycursor.execute('use DataHouse')
            mycursor.execute('DELETE FROM student_result where Student_name="%s";'%(Student_name))
            mycursor.execute('drop table %s'%(Student_name))
            mycursor.execute('drop table %s'%(Student_name+'_Real_values'))
            Storehouse.commit()
        except:
            Storehouse.rollback()

    #UPDATE MARKS IN RESULT
    def UPMark(Student_name,marks):
        try:
            mycursor.execute('use DataHouse')
            mycursor.execute('UPDATE student_result SET Marks="%s" where Student_name ="%s"'%(marks,Student_name))
            Storehouse.commit()
        except:
            Storehouse.rollback()

    #UPDATE NAME IN THE RECORDS
    def UPN(Student_name,New_name,admin):
        try:
            mycursor.execute('use DataHouse')
            mycursor.execute('update student_result set Student_name="%s" where Admin_no =%i;'%(New_name,admin))
            mycursor.execute('alter table %s rename to %s'%(Student_name,str(New_name)))
            mycursor.execute('alter table %s rename to %s'%(Student_name+"_Real_values",str(New_name)+"_Real_values"))
            Storehouse.commit()
        except:
            Storehouse.rollback()
        

    #UPDATE MARKS IN PERCENTAGE IN RESULT
    def UPMK(Student_name,marks):
        try:
            mycursor.execute('use DataHouse')
            mycursor.execute('UPDATE student_result SET Marks_percentage="%s" where Student_name ="%s"'%(marks,Student_name))
            Storehouse.commit()
        except:
            Storehouse.rollback()

    #UPDATE ADMIMISION NUMBER IN RESULT
    def UPAdm(Student_name,admin):
        try:
            mycursor.execute('use DataHouse')
            mycursor.execute('UPDATE student_result SET Admin_No="%s" where Student_name ="%s"'%(admin,Student_name))
            Storehouse.commit()
        except:
            Storehouse.rollback()

    #UPDATE STATUS OF STATUS OF RESULT IN RESULT
    def UPST(Student_name,stat):
        try:
            mycursor.execute('use DataHouse')
            mycursor.execute('UPDATE student_result SET Status="%s" where Student_name ="%s"'%(stat,Student_name))
            Storehouse.commit()
        except:
            Storehouse.rollback()

    #SEARCH FOR ADMISSION AND NAME OF THE STUDENTS ALREADY EXISTS IN RECORDS
    def SHAN():
        try:
            Data_adm=[]
            Data_name=[]
            mycursor.execute('use DataHouse')
            mycursor.execute('select * from student_result;')
            record=mycursor.fetchall()
            for rec in record:
                Data_adm.append(rec[0])
                Data_name.append(rec[1])
            Table_data={'Admin_no':Data_adm,"Student_Name":Data_name}
            Table=p.DataFrame(Table_data)
            print(Table)
            Storehouse.commit()
        except:
            print("There are no Records to show")
            Storehouse.rollback()
    
    #SEARCH FOR NAMES OF STUDENTS ALREADY EXISTS IN RECORDS
    def SearchRTB():
        Total_name=[]
        Name_Src=[]
        mycursor.execute("use datahouse;")
        mycursor.execute("select * from student_result;")
        record=mycursor.fetchall()
        for row in record:
            Name_Src.append(row[1])
            Total_name.append(row[1])
        Table_Data={'Existing_Students':Total_name}
        Table=p.DataFrame(Table_Data)
        print(Table)
        
    #SEARCH FOR NOMINAL MARKS THROUGH DATABASE
    def SearchRec(Student_name):
        Data_sub=[]
        Data_PTO=[]
        Data_HF=[]
        Data_PTT=[]
        Data_AE=[]
        mycursor.execute("use datahouse;")
        mycursor.execute("select * from %s"%Student_name)
        records=mycursor.fetchall()
        for row in records:
            Data_sub.append(row[0])
            Data_PTO.append(row[1])
            Data_HF.append(row[2])
            Data_PTT.append(row[3])
            Data_AE.append(row[4])
        Table_data={'Subject_name':Data_sub,"Periodic_Test-1":Data_PTO,"Half_Yearly":Data_HF,"Periodic_Test-2":Data_PTT,"Annual_Year":Data_AE}
        Table=p.DataFrame(Table_data)
        print(Table)
        Storehouse.commit()
        
    #SEARCH FOR REAL MARKS THROUGH DATABASE
    def SearchReal(Student_name):
        Data_sub=[]
        Data_PTO=[]
        Data_HF=[]
        Data_PTT=[]
        Data_AE=[]
        mycursor.execute("use datahouse;")
        mycursor.execute("select * from %s"%Student_name.title()+"_Real_values")
        records=mycursor.fetchall()
        for row in records:
            Data_sub.append(row[0])
            Data_PTO.append(row[1])
            Data_HF.append(row[2])
            Data_PTT.append(row[3])
            Data_AE.append(row[4])
        Table_data={'Subject_name':Data_sub,"Periodic_Test-1":Data_PTO,"Half_Yearly":Data_HF,"Periodic_Test-2":Data_PTT,"Annual_Year":Data_AE}
        Table=p.DataFrame(Table_data)
        print(Table)
        Storehouse.commit()

    #LIVE DATA RECORD OF NOMINAL MARKS
    def RecDB(Student_name,sub_name,sub1,sub2,sub3,sub4):
        mycursor.execute("insert into %s values('%s','%s','%s','%s','%s')"%(Student_name,sub_name,sub1,sub2,sub3,sub4))
        Storehouse.commit()

    #LIVE DATA RECORD OF REAL MARKS 
    def RecReal(Student_name,sub_name,sub1,sub2,sub3,sub4):
        mycursor.execute("insert into %s values('%s','%s','%s','%s','%s')"%(Student_name+"_Real_values",sub_name,sub1,sub2,sub3,sub4))
        Storehouse.commit()

    #NAME GENERATOR FOR DATABASE 
    def Replace_spc(string): 
        return string.replace(' ', '_') 

#CLASS FOR HOUSE CLEANING
class Restrict():
    
    #FUNCTOIN FOR RESTRICTING CHARACTER INPUT ONLY
    def limitchar(content):
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*~'''
        values=''
        count=3
        while True:
            variable_space=input("%s"%content)
            if variable_space!=0:
                for val in variable_space:
                    if val not in punctuations:
                        values=values+val
                return values
                break
            else:
                count=count-1
                if count in[3,2,1]:
                    print("Invalid Data type found")
                    print("Remaing retry of above entry:%s"%count)
                else:
                    pass
                if count==0:
                    print("Remaing retry of above entry:%s"%count)            
                    print("We are sorry you have exhausted all retry's")
                    break
                continue
            
    #FUNCTION FOR RESTRICTING INTERGER INPUT ONLY
    def limitnum(content):
        alphabets=['a','q','e','w','r','t','y','u','i','o','p','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        alphabets.extend(punctuations)
        values=''
        count=3
        while True:
            try:
                _input=input('%s'%content)
                for val in _input:
                    if val not in alphabets:
                        values=values+val
                        values=int(values)
                        return values
                break
            except ValueError:
                count=count-1
                if count in[3,2,1]:
                    print("Invalid Data type found")
                    print("Remaing retry of above entry:%s"%count)
                else:
                    pass
                if count==0:
                    print("Remaing retry of above entry:%s"%count)            
                    print("We are sorry you have exhausted all retry's")
                    break
    #CLASSICAL NUMERIC RESSTRICTION
    def num(content):
        count=3
        while True:
            try:
                var=int(input('%s'%content))
                return var
                break
            except ValueError:
                count=count-1
                if count in[3,2,1]:
                    print("Invalid Data type found")
                    print("Remaing retry of above entry:%s"%count)
                else:
                    pass
                if count==0:
                    print("Remaing retry of above entry:%s"%count)            
                    print("We are sorry you have exhausted all retry's")
                    break
    
    #FUNCTION FOR RESTRICTING ALPHA-NUMERIC ONLY
    def limitalnum(content):
        punctuations =['!','(',')','-','[',']','{','}',';',':',"'",'"',"\\",',','<','>','.','/','?','@','#','$','%','^','&','*','_','~']
        count=3
        while True:
            ask_input=input("%s"%content)
            if ask_input.isalnum()==False:
                count=count-1
                if count in[3,2,1]:
                    print("Sorry only alphabets and numeric are acceptable")
                    print("Remaing retry of above entry:%s"%count)
                else:
                    pass
                if count==0:
                    print("Remaing retry of above entry:%s"%count)            
                    print("We are sorry you have exhausted all retry's")
                    break
                continue
            else:
                return ask_input 
                break

#CREATING CLASS FOR COMMERCE STREAM

class Commerce():
    
    #FUNCTION FOR COMMERRCE STREAM TO GET MARKS OF PERIODIC TESTS EXAMINATIONS
    def Entry(_sub, test):
        while True:
            if _sub==_sub:
                try:
                    print("Enter marks of ", _sub, "in", test, end="=>")
                    x = int(input())
                except:
                    print("Invalid input")
                    continue
                if x in range(0, 41):
                    return x
                    break

                else:
                    print("Marks exceded, please try again ")
            else:
                print("Invalid marks")
                continue
        

    #FUNCITON TO GET MARKS FOR COMPUTER SCIENCE/INFORMATICS PRACTICS MARKS
    def AHFComputer(test,_sub="IP"):
        while True:
            try:
                print("Enter marks of ", _sub, "in", test, end="=>")
                x: int = int(input())
            except:
                print("Invalid input")
                continue
            if x in range(0, 71):
                return x
                break
            else:
                print("Marks exceded, please try again")

    #FUNCTION FOR COMMERRCE STREAM TO GET HALF YEARLY  AND ANNUAL EXAMINATIONS MARKS            
    def AHYEntry(_sub, test):
        while True:
            if _sub == "Maths" or "Business Studies" or "Accounts" or "Economics" or "Physical Education" or "English":
                try:
                    print("Enter marks of ", _sub, "in", test, end="=>")
                    x = int(input())
                except:
                    print("Invalid input")
                    continue
                if x in range(0, 81):
                    return x
                    break

                else:
                    print("Marks exceded, please try again ")
            else:
                print("Invalid marks")
                continue
#-------------------------------------COMMERCE VARIABLES START--------------------------------
#PERIODIC TEST MARKS VARIABLES
        
BST_PT_MARKS=0
ENG_PT_MARKS=0
IP_PT_MARKS=0
MATHS_PT_MARKS=0
ECO_PT_MARKS=0
ACC_PT_MARKS=0
PY_PT_MARKS=0
HI_PT_MARKS=0

#HALF YEAR TEST MARKS VARIABLES

BST_HF_MARKS=0
ENG_HF_MARKS=0
HI_HF_MARRKS=0
IP_HF_MARKS=0
MATHS_HF_MARKS=0
ECO_HF_MARKS=0
ACC_HF_MARKS=0
PY_HF_MARKS=0

#PERIODIC TEST - 2 TEST MARKS VARIABLES

BST_PT2_MARKS=0
ENG_PT2_MARKS=0
IP_PT2_MARKS=0
HI_PT2_MARKS=0
MATHS_PT2_MARKS=0
ECO_PT2_MARKS=0
ACC_PT2_MARKS=0
PY_PT2_MARKS=0

#ANNUAL EXAMINATION TEST MARKS VARIABLES

BST_AE_MARKS=0
ENG_AE_MARKS=0
HI_AE_MARKS=0
IP_AE_MARKS=0
MATHS_AE_MARKS=0
ECO_AE_MARKS=0
ACC_AE_MARKS=0
PY_AE_MARKS=0

#------------------------------------------COMMERCE VARIABLES END------------------------------

#------------------------------------------SCIENCE VARIABLES START-----------------------------
# PERIODIC TEST - 1 VARIABLES
chem_marks1 = 0
phy_marks1 = 0
math_marks1 = 0
pe_marks1 = 0
cs_marks1 = 0
eng_marks1 = 0

# HALF-YEARLY EXAM VARIABLES
chem_marks2 = 0
phy_marks2 = 0
math_marks2 = 0
pe_marks2 = 0
cs_marks2 = 0
eng_marks2 = 0

# PERIODIC TEST - 2 VARIABLES

chem_marks3 = 0
phy_marks3 = 0
math_marks3 = 0
pe_marks3 = 0
cs_marks3 = 0
eng_marks3 = 0

# FINAL EXAM VARIABLES

chem_marks4 = 0
phy_marks4 = 0
math_marks4 = 0
cs_marks4 = 0
eng_marks4 = 0
pe_marks4 = 0

#------------------------------------SCIENCE VARIABLES END------------------------

#------------------------------------ARTS VARIABLES START-------------------------

#PERIODIC TEST ONE VARIABLES

sco_marks1=0
hin_marks1=0
hist_marks1=0
geo_marks1=0

#HALF YEARLY EXAM VARIABLES

sco_marks2=0
hin_marks2=0
hist_marks2=0
geo_marks2=0

#PERIODIC TEST TWO VARIABLES
sco_marks3=0
hin_marks3=0
hist_marks3=0
geo_marks3=0

#FINAL EXAM VARIABLES

sco_marks4=0
hin_marks4=0
hist_marks4=0
geo_marks4=0

#----------------------------------ARTS VARIABLES END-----------------------------
#CONDITIONAL VARIABLE TO CHECK

Present_touch=[]

def Student_Record():
    #BASIC INFORMATION COLLECTION (start)

    Student_name=Restrict.limitchar("Enter your full name:")
    Class_In=Restrict.num("%s which class you are currently in:"%Student_name.title())
    if Class_In in [11]:
        pass
    else:
        print("Caution: This program is only use for 11th class")
        
    Student_admin=Restrict.num('Enter your admission number:')

    print("Welcome %s To Qualifier v1.0.1"%Student_name.title())
    try:
        SQL_Name=SQL.Replace_spc(Student_name)
    except:
        print("Failed to Create Database UserName(Conversion)")
    #STREAMS CATALOG
    print("""Streams available:
        1.Science
        2.Commerce
        3.Arts""")
    Stream_choice=Restrict.limitnum("Which Stream you are currently  pursuing %s:"%Student_name.title())
    Stream_option=Restrict()
    if Stream_choice ==2:
        
        #OPTIONAL SUBJECTS CATALOG
        print('''Optional Subjects available:
        1.Maths
        2.Informatics Practices
        3.Hindi''')
        Stream_option=Restrict.limitalnum("Enter Which optional subject you have opted:")
        
        Student_Report=SQL()

        #STOREHOUSE
        try:
            SQL.CreateTB(SQL_Name)
            SQL.CreateRTB()
        except:
            print("Failed to Create Database")

        #GETTING MARKS OF THE STUDENT
        while True:
            for i in range(1,5):
                if i==1:
                    #--------------------------------PERIODIC TEST-1 START-----------------------------------

                    print("The Periodic Test-1 Fill Fourm")
                    #REDUNDANCY CHECK UP REGARDING
                    Present_touch.append(1) 
                             
                    #OPTIONAL SUBJECTS
                    
                    if Stream_option=='1':
                        MATHS_PT_MARKS=Commerce.Entry("Maths","Periodic Test-1")
                    elif Stream_option == '2':
                        IP_PT_MARKS=Commerce.Entry("IP","Periodic Test-1")
                    elif Stream_option == '3':
                        HI_PT_MARKS = Commerce.Entry("Hindi","Periodic Test-1")

                    #BUSINESS STUDIES SUBJECT
                         
                    BST_PT_MARKS=Commerce.Entry("Business Studies","Periodic Test-1")

                    #ENGLISH SUBJECT
                         
                    ENG_PT_MARKS=Commerce.Entry("English","Periodic Test-1")

                    #ECONOMICS SUBJECT
                         
                    ECO_PT_MARKS=Commerce.Entry("Economics","Periodic Test-1")

                    #ACCOUNTS SUBJECT
                         
                    ACC_PT_MARKS=Commerce.Entry("Accounts","Periodic Test-1")

                    #PYSICAL EDUCATION SUBJECT
                         
                    PY_PT_MARKS=Commerce.Entry("Physical Education","Periodic Test-1")
                    
                    #----------------------------------PERIODIC TEST-1 END-------------------------------------
                    continue

                if i==2:
                    #----------------------------------HALF YEARLY EXAMINATON START----------------------------

                    print("The Half Year Exam Fill Fourm")
                    
                    #REDUNDANCY CHECK UP REGARDING
                    Present_touch.append(2)

                    #OPTIONAL SUBJECTS
                    
                    if Stream_option=='1':
                        MATHS_HF_MARKS=Commerce.AHYEntry("Maths","Half Yearly Examination")
                    elif Stream_option == '2':
                        IP_HF_MARKS=Commerce.AHFComputer("Half Yearly Examination")
                    elif Stream_option == '3':
                        HI_HF_MARKS = Commerce.AHYEntry("Hindi","Half Yearly Examination")
                        
                    #ACCOUNTS SUBJECT

                    ACC_HF_MARKS=Commerce.AHYEntry("Accounts","Half Yearly Examination")

                    #ENGLISH SUBJECT

                    ENG_HF_MARKS=Commerce.AHYEntry("English","Half Yearly Examination")

                    #ECONOMICS SUBJECT

                    ECO_HF_MARKS=Commerce.AHYEntry("Economics","Half Yearly Examination")

                    #BUSINESS STUDIES SUBJECT

                    BST_HF_MARKS=Commerce.AHYEntry("Business Studies","Half Yearly Examination")

                    #PHYISCAL EDUCATION SUBJECT

                    PY_HF_MARKS=Commerce.AHFComputer("Half Yearly Examination","Phyiscal Education")

                    #---------------------------HALF YEARLY EXAMINATION END------------------------------------
                    continue
                if i==3:
                    #---------------------------PERIODIC TEST-2 START-------------------------------------------
                    
                    print('The Periodic Test Two Fill Form')

                    #RDUNDANCY CHECK UP REGARDING
                    Present_touch.append(3)

                    #OPTIONAL SUBJECTS
                        
                    if Stream_option=='1':
                        MATHS_PT2_MARKS=Commerce.Entry("Maths","Periodic Test-2")
                    elif Stream_option == '2':
                        IP_PT2_MARKS=Commerce.Entry("IP","Periodic Test-2")
                    elif Stream_option == '3':
                        HI_PT2_MARKS = Commerce.Entry("Hindi","Periodic Test-2")

                    #BUSINESS STUDIES SUBJECT
                         
                    BST_PT2_MARKS=Commerce.Entry("Business Studies","Periodic Test-2")

                    #ENGLISH SUBJECT
                         
                    ENG_PT2_MARKS=Commerce.Entry("English","Periodic Test-2")

                    #ECONOMICS SUBJECT
                         
                    ECO_PT2_MARKS=Commerce.Entry("Economics","Periodic Test-2")

                    #ACCOUNTS SUBJECT
                         
                    ACC_PT2_MARKS=Commerce.Entry("Accounts","Periodic Test-2")

                    #PYSICAL EDUCATION SUBJECT
                         
                    PY_PT2_MARKS=Commerce.Entry("Physical Education","Periodic Test-2")

                    #-----------------------------PERIODIC TEST-2 END-------------------------------------------
                    continue
                if i==4:
                    #-----------------------------ANNUAL EXAMINATION START--------------------------------------
                    print("The Annual Examination Fill Fourm")
                    
                    #REDUNDANCY CHECK UP REGARDING
                    Present_touch.append(4)

                    #OPTIONAL SUBJECTS

                    if Stream_option=='1':
                        MATHS_AE_MARKS=Commerce.AHYEntry("Maths","Annual Examination")
                    elif Stream_option == '2' :
                        IP_AE_MARKS=Commerce.AHFComputer("Annual Examination")
                    elif Stream_option == '3':
                        HI_AE_MARKS = Commerce.AHYEntry("Hindi","Annual Examination")

                    #ACCOUNTS SUBJECT

                    ACC_AE_MARKS=Commerce.AHYEntry("Accounts","Annual Examination")

                    #ENGLISH SUBJECT

                    ENG_AE_MARKS=Commerce.AHYEntry("English","Annual Examination")

                    #ECONOMICS SUBJECT

                    ECO_AE_MARKS=Commerce.AHYEntry("Economics","Annual Examination")

                    #BUSINESS STUDIES SUBJECT

                    BST_AE_MARKS=Commerce.AHYEntry("Business Studies","Annual Examination")

                    #PHYISCAL EDUCATION SUBJECT

                    PY_AE_MARKS=Commerce.AHFComputer("Annual Examination","Phyiscal Education")
            break
        #STOREHOUSE
        if Stream_option=='1':
            try:
                SQL.RecDB(SQL_Name,'Maths',str(MATHS_PT_MARKS),str(MATHS_HF_MARKS),str(MATHS_PT2_MARKS),str(MATHS_AE_MARKS))
                SQL.RecDB(SQL_Name,'Economics',str(ECO_PT_MARKS),str(ECO_HF_MARKS),str(ECO_PT2_MARKS),str(ECO_AE_MARKS))
                SQL.RecDB(SQL_Name,'Business Studies',str(BST_PT_MARKS),str(BST_HF_MARKS),str(BST_PT2_MARKS),str(BST_AE_MARKS))
                SQL.RecDB(SQL_Name,'English',str(ENG_PT_MARKS),str(ENG_HF_MARKS),str(ENG_PT2_MARKS),str(ENG_AE_MARKS))
                SQL.RecDB(SQL_Name,'Accounts',str(ACC_PT_MARKS),str(ACC_HF_MARKS),str(ACC_PT2_MARKS),str(ACC_AE_MARKS))
                SQL.RecDB(SQL_Name,'Physical Education',str(PY_PT_MARKS),str(PY_HF_MARKS),str(PY_PT2_MARKS),str(PY_AE_MARKS))
                print("Nomial Marks succesfully stored for Commerce!!")
            except:
                print("Nomial Marks Failed stored for Commerce!!")
        
        elif Stream_option=='2':
            try:
                SQL.RecDB(SQL_Name,'Informatic Practics',str(IP_PT_MARKS),str(IP_HF_MARKS),str(IP_PT2_MARKS),str(IP_AE_MARKS))
                SQL.RecDB(SQL_Name,'Economics',str(ECO_PT_MARKS),str(ECO_HF_MARKS),str(ECO_PT2_MARKS),str(ECO_AE_MARKS))
                SQL.RecDB(SQL_Name,'Business Studies',str(BST_PT_MARKS),str(BST_HF_MARKS),str(BST_PT2_MARKS),str(BST_AE_MARKS))
                SQL.RecDB(SQL_Name,'English',str(ENG_PT_MARKS),str(ENG_HF_MARKS),str(ENG_PT2_MARKS),str(ENG_AE_MARKS))
                SQL.RecDB(SQL_Name,'Accounts',str(ACC_PT_MARKS),str(ACC_HF_MARKS),str(ACC_PT2_MARKS),str(ACC_AE_MARKS))
                SQL.RecDB(SQL_Name,'Physical Education',str(PY_PT_MARKS),str(PY_HF_MARKS),str(PY_PT2_MARKS),str(PY_AE_MARKS))
                print("Nomial Marks succesfully stored for Commerce!!")
            except:
                print("Nomial Marks Failed stored for Commerce!!")
                 
        elif Stream_option=='3':
            try:
                SQL.RecDB(SQL_Name,'Hindi',str(HI_PT_MARKS),str(HI_HF_MARKS),str(HI_PT2_MARKS),str(HI_AE_MARKS))
                SQL.RecDB(SQL_Name,'Economics',str(ECO_PT_MARKS),str(ECO_HF_MARKS),str(ECO_PT2_MARKS),str(ECO_AE_MARKS))
                SQL.RecDB(SQL_Name,'Business Studies',str(BST_PT_MARKS),str(BST_HF_MARKS),str(BST_PT2_MARKS),str(BST_AE_MARKS))
                SQL.RecDB(SQL_Name,'English',str(ENG_PT_MARKS),str(ENG_HF_MARKS),str(ENG_PT2_MARKS),str(ENG_AE_MARKS))
                SQL.RecDB(SQL_Name,'Accounts',str(ACC_PT_MARKS),str(ACC_HF_MARKS),str(ACC_PT2_MARKS),str(ACC_AE_MARKS))
                SQL.RecDB(SQL_Name,'Physical Education',str(PY_PT_MARKS),str(PY_HF_MARKS),str(PY_PT2_MARKS),str(PY_AE_MARKS))
                print("Nomial Marks succesfully stored for Commerce!!")
            except:
                print("Nomial Marks Failed stored for Commerce!!")
        #TABLE FORMATION FOR MARKS OBTAINED BY STUDENT NOMINAL VALUES
        Nominal_Values=input('Do you want to see results (in table format)(y/n):')
        if Nominal_Values =='y':
            if Stream_option=='1':
                print("""
                ===============================================================================      
                                            The Marks Scored in the Current Year
                ===============================================================================      """)

                #COLLECTION OF MARKS IN A VARIABLE FOR TABLE PRESENTATION 
                                
                PT1=[MATHS_PT_MARKS,ECO_PT_MARKS,BST_PT_MARKS,ENG_PT_MARKS,ACC_PT_MARKS,PY_PT_MARKS]

                HF=[MATHS_HF_MARKS,ECO_HF_MARKS,BST_HF_MARKS,ENG_HF_MARKS,ACC_HF_MARKS,PY_HF_MARKS]

                PT2=[MATHS_PT2_MARKS,ECO_PT2_MARKS,BST_PT2_MARKS,ENG_PT2_MARKS,ACC_PT2_MARKS,PY_PT2_MARKS]

                AE=[MATHS_AE_MARKS,ECO_AE_MARKS,BST_AE_MARKS,ENG_AE_MARKS,ACC_AE_MARKS,PY_AE_MARKS]

                #RESHAPING THE VARIABLES INTO A 2D TABLE

                Data_Table={"Periodic One":PT1,"Half Yearly":HF,"Periodic Two":PT2,"Annual Test":AE}
                Table_shape=p.DataFrame(Data_Table,index=["Maths","Economics","Business Studies","English",'Accounts','Physical Education'])
                print(Table_shape)
                                    
            elif Stream_option == '2':
                print("""
                ===============================================================================      
                                            The Marks Scored in the Current Year
                ===============================================================================      """)

                #COLLECTION OF MARKS IN A VARIABLE FOR TABLE PRESENTATION 
                                
                PT1=[IP_PT_MARKS,ECO_PT_MARKS,BST_PT_MARKS,ENG_PT_MARKS,ACC_PT_MARKS,PY_PT_MARKS]

                HF=[IP_HF_MARKS,ECO_HF_MARKS,BST_HF_MARKS,ENG_HF_MARKS,ACC_HF_MARKS,PY_HF_MARKS]

                PT2=[IP_PT2_MARKS,ECO_PT2_MARKS,BST_PT2_MARKS,ENG_PT2_MARKS,ACC_PT2_MARKS,PY_PT2_MARKS]

                AE=[IP_AE_MARKS,ECO_AE_MARKS,BST_AE_MARKS,ENG_AE_MARKS,ACC_AE_MARKS,PY_AE_MARKS]

                #RESHAPING THE VARIABLES INTO A 2D TABLE

                Data_Table={"Periodic One":PT1,"Half Yearly":HF,"Periodic Two":PT2,"Annual Test":AE}
                Table_shape=p.DataFrame(Data_Table,index=["IP","Economics","Business Studies","English",'Accounts','Physical Education'],\
                columns=['Periodic One','Half Yearly','Periodic Two','Annual Test'])
                print(Table_shape)
                                    
            elif Stream_option == '3':
                print("""
                ===============================================================================      
                                            The Marks Scored in the Current Year
                ===============================================================================      """)

                #COLLECTION OF MARKS IN A VARIABLE FOR TABLE PRESENTATION 
                                
                PT1=[HI_PT_MARKS,ECO_PT_MARKS,BST_PT_MARKS,ENG_PT_MARKS,ACC_PT_MARKS,PY_PT_MARKS]

                HF=[HI_HF_MARKS,ECO_HF_MARKS,BST_HF_MARKS,ENG_HF_MARKS,ACC_HF_MARKS,PY_HF_MARKS]

                PT2=[HI_PT2_MARKS,ECO_PT2_MARKS,BST_PT2_MARKS,ENG_PT2_MARKS,ACC_PT2_MARKS,PY_PT2_MARKS]

                AE=[HI_AE_MARKS,ECO_AE_MARKS,BST_AE_MARKS,ENG_AE_MARKS,ACC_AE_MARKS,PY_AE_MARKS]

                #RESHAPING THE VARIABLES INTO A 2D TABLE

                Data_Table={"Periodic One":PT1,"Half Yearly":HF,"Periodic Two":PT2,"Annual Test":AE}
                Table_shape=p.DataFrame(Data_Table,index=["Hindi","Economics","Business Studies","English",'Accounts','Physical Education'])
                print(Table_shape)
        else:
            print("Okay no problem")
            
        #CALCLUATION OF MARKS VARIABLES 
        #-----------------------------------#
        #PERIODIC ONE ACUTAL MARKS
            
        PTO_ENGLISH=ENG_PT_MARKS/4

        if Stream_option=='3':
            PTO_HINDI=HI_PT_MARKS/4

        if Stream_option=='1':
            PTO_MATHS=MATHS_PT_MARKS/4

        if Stream_option=='2':
            PTO_IP=IP_PT_MARKS/4

        PTO_ECO=ECO_PT_MARKS/4
        PTO_BST=BST_PT_MARKS/4
        PTO_ACC=ACC_PT_MARKS/4
        PTO_PY=PY_PT_MARKS/4

        #PERIODIC  TWO ACUTAL MARKS
        
        PTT_ENGLISH=ENG_PT2_MARKS/4

        if Stream_option=='3':
            PTT_HINDI=HI_PT2_MARKS/4

        if Stream_option=='1':
            PTT_MATHS=MATHS_PT2_MARKS/4

        if Stream_option=='2':
            PTT_IP=IP_PT2_MARKS/4

        PTT_ECO=ECO_PT2_MARKS/4
        PTT_BST=BST_PT2_MARKS/4
        PTT_ACC=ACC_PT2_MARKS/4
        PTT_PY=PY_PT2_MARKS/4

        #HALF YEARLY ACUTUAL MARKS
        
        HF_ENGLISH=(ENG_HF_MARKS/80)*30

        if Stream_option=='3':
            HF_HINDI=(HI_HF_MARKS/80)*30

        if Stream_option=='1':
            HF_MATHS=(MATHS_HF_MARKS/80)*30

        if Stream_option=='2':
            HF_IP=(IP_HF_MARKS/70)*30

        HF_ECO=(ECO_HF_MARKS/80)*30
        HF_BST=(BST_HF_MARKS/80)*30
        HF_ACC=(ACC_HF_MARKS/80)*30
        HF_PY=(PY_HF_MARKS/70)*30

        #ANNUAL EXAM ACTUAL MARKS 

        AE_ENGLISH=(ENG_AE_MARKS/80)*30

        if Stream_option=='3':
            AE_HINDI=(HI_HF_MARKS/80)*30

        if Stream_option=='1':
            AE_MATHS=(MATHS_AE_MARKS/80)*30

        if Stream_option=='2':
            AE_IP=(IP_AE_MARKS/70)*30

        AE_ECO=(ECO_AE_MARKS/80)*30
        AE_BST=(BST_AE_MARKS/80)*30
        AE_ACC=(ACC_AE_MARKS/80)*30
        AE_PY=(PY_AE_MARKS/70)*30

        #MARKS OBTAINED BY STUDENT IN YEAR

        FM_ACC=PTT_ACC+HF_ACC+PTO_ACC+AE_ACC
        FM_BST=PTT_BST+PTO_BST+HF_BST+AE_BST
        FM_ECO=PTT_ECO+PTO_ECO+HF_ECO+AE_ECO
        FM_ENG=PTT_ENGLISH+PTO_ENGLISH+HF_ENGLISH+AE_ENGLISH
        FM_PY=PTT_PY+PTO_PY+HF_PY+AE_PY

        if Stream_option=='3':
            FM_HINDI=AE_HINDI+PTO_HINDI+PTT_HINDI+HF_HINDI
        if Stream_option=='1':
            FM_MATHS=HF_MATHS+PTO_MATHS+PTT_MATHS+AE_MATHS
        if Stream_option=='2':
            FM_IP=AE_IP+PTO_IP+PTT_IP+HF_IP

        #STOREHOUSE
        if Stream_option=='1':
            try:
                SQL.RecReal(SQL_Name,'Maths',str(PTT_MATHS),str(HF_MATHS),str(PTO_MATHS),str(AE_MATHS))
                SQL.RecReal(SQL_Name,'Economics',str(PTT_ECO),str(HF_ECO),str(PTO_ECO),str(AE_ECO))
                SQL.RecReal(SQL_Name,'Business Studies',str(PTT_BST),str(HF_BST),str(PTO_BST),str(AE_BST))
                SQL.RecReal(SQL_Name,'English',str(PTT_ENGLISH),str(HF_ENGLISH),str(PTO_ENGLISH),str(AE_ENGLISH))
                SQL.RecReal(SQL_Name,'Accounts',str(PTT_ACC),str(HF_ACC),str(PTO_ACC),str(AE_ACC))
                SQL.RecReal(SQL_Name,'Physical Education',str(PTT_PY),str(HF_PY),str(PTO_PY),str(AE_PY))
                print("Real Marks succesfully stored for Commerce!!")
            except:
                print("Real Marks Failed to stored for Commerce!!")
        elif Stream_option=='2':
            try:
                SQL.RecReal(SQL_Name,'Information practics',str(PTT_IP),str(HF_IP),str(PTO_IP),str(AE_IP))
                SQL.RecReal(SQL_Name,'Economics',str(PTT_ECO),str(HF_ECO),str(PTO_ECO),str(AE_ECO))
                SQL.RecReal(SQL_Name,'Business Studies',str(PTT_BST),str(HF_BST),str(PTO_BST),str(AE_BST))
                SQL.RecReal(SQL_Name,'English',str(PTT_ENGLISH),str(HF_ENGLISH),str(PTO_ENGLISH),str(AE_ENGLISH))
                SQL.RecReal(SQL_Name,'Accounts',str(PTT_ACC),str(HF_ACC),str(PTO_ACC),str(AE_ACC))
                SQL.RecReal(SQL_Name,'Physical Education',str(PTT_PY),str(HF_PY),str(PTO_PY),str(AE_PY))
                print("Real Marks succesfully stored for Commerce!!")
            except:
                print("Real Marks Failed to stored for Commerce!!")
        elif Stream_option=='3':
            try:
                SQL.RecReal(SQL_Name,'Hindi',str(PTT_HINDI),str(HF_HINDI),str(PTO_HINDI),str(AE_HINDI))
                SQL.RecReal(SQL_Name,'Economics',str(PTT_ECO),str(HF_ECO),str(PTO_ECO),str(AE_ECO))
                SQL.RecReal(SQL_Name,'Business Studies',str(PTT_BST),str(HF_BST),str(PTO_BST),str(AE_BST))
                SQL.RecReal(SQL_Name,'English',str(PTT_ENGLISH),str(HF_ENGLISH),str(PTO_ENGLISH),str(AE_ENGLISH))
                SQL.RecReal(SQL_Name,'Accounts',str(PTT_ACC),str(HF_ACC),str(PTO_ACC),str(AE_ACC))
                SQL.RecReal(SQL_Name,'Physical Education',str(PTT_PY),str(HF_PY),str(PTO_PY),str(AE_PY))
                print("Real Marks succesfully stored for Commerce!!")
            except:
                print("Real Marks Failed to stored for Commerce!!")
            
        #REPORT CARD
        if Stream_option =='1':
            Total_FM=FM_MATHS+FM_ACC+FM_BST+FM_ECO+FM_ENG+FM_PY
        if Stream_option == '2':
            Total_FM=FM_IP+FM_ACC+FM_BST+FM_ECO+FM_ENG+FM_PY
        if Stream_option == '3':
            Total_FM=FM_HINDI+FM_ACC+FM_BST+FM_ECO+FM_ENG+FM_PY
        
        if Stream_option =='1':
            Total_PCT=(Total_FM/470)*100
        if Stream_option == '2':
            Total_PCT=(Total_FM/460)*100
        if Stream_option == '3':
            Total_PCT=(Total_FM/470)*100
        
        if Stream_option =='1':
            Marks_box=[FM_MATHS+FM_ACC+FM_BST+FM_ECO+FM_ENG+FM_PY]
        if Stream_option == '2':
            Marks_box=[FM_IP+FM_ACC+FM_BST+FM_ECO+FM_ENG+FM_PY]
        if Stream_option =='3':
            Marks_box=[FM_HINDI+FM_ACC+FM_BST+FM_ECO+FM_ENG+FM_PY]

        Box_len=len(Marks_box)
        Status_pass="Pass"
        Status_fail="Failed"
        Marks_floor=33
        for sub in Marks_box:
            if sub>= Marks_floor:
                if sub ==Marks_box[Box_len-1]:
                    try:
                        SQL.RecRTB(str(Student_admin),SQL_Name,'Commerce',str(Total_FM),str(Total_PCT),str(Status_pass))
                    except:
                        print("Data Failed to Store.Please check the script")
            elif sub<Marks_floor:
                try:
                    SQL.RecRTB(str(Student_admin),SQL_Name,'Commerce',str(Total_FM),str(Total_PCT),str(Status_fail))
                except:
                    print("Data Failed to Store.Please check the script")
                    
                break

        #ACUTALL MARKS SCORED BY THE STUDENT
        Post_Values=Restrict.limitchar('Do you want to see the acutal results (in table format)(y/n):')
        if Post_Values.lower() =='y':
            if Stream_option=='1':
                print("""
                ===============================================================================      
                                            The Actual Marks Scored in the Current Year
                ===============================================================================      """)

                #COLLECTION OF MARKS IN A VARIABLE FOR TABLE PRESENTATION 
                                
                PT1=[PTO_MATHS,PTO_ECO,PTO_BST,PTO_ENGLISH,PTO_ACC,PTO_PY]

                HF=[HF_MATHS,HF_ECO,HF_BST,HF_ENGLISH,HF_ACC,HF_PY]

                PT2=[PTT_MATHS,PTT_ECO,PTT_BST,PTT_ENGLISH,PTT_ACC,PTT_PY]

                AE=[AE_MATHS,AE_ECO,AE_BST,AE_ENGLISH,AE_ACC,AE_PY]

                #RESHAPING THE VARIABLES INTO A 2D TABLE

                Data_Table={"Periodic One":PT1,"Half Yearly":HF,"Periodic Two":PT2,"Annual Test":AE}
                Table_shape=p.DataFrame(Data_Table,index=["Maths","Economics","Business Studies","English",'Accounts','Physical Education'])
                print(Table_shape)
                                    
            elif Stream_option == '2':
                print("""
                ===============================================================================      
                                            The Actual Marks Scored in the Current Year
                ===============================================================================      """)

                #COLLECTION OF MARKS IN A VARIABLE FOR TABLE PRESENTATION 
                                
                PT1=[PTO_IP,PTO_ECO,PTO_BST,PTO_ENGLISH,PTO_ACC,PTO_PY]

                HF=[HF_IP,HF_ECO,HF_BST,HF_ENGLISH,HF_ACC,HF_PY]

                PT2=[PTT_IP,PTT_ECO,PTT_BST,PTT_ENGLISH,PTT_ACC,PTT_PY]

                AE=[AE_IP,AE_ECO,AE_BST,AE_ENGLISH,AE_ACC,AE_PY]

                #RESHAPING THE VARIABLES INTO A 2D TABLE

                Data_Table={"Periodic One":PT1,"Half Yearly":HF,"Periodic Two":PT2,"Annual Test":AE}
                Table_shape=p.DataFrame(Data_Table,index=["IP","Economics","Business Studies","English",'Accounts','Physical Education'],\
                columns=['Periodic One','Half Yearly','Periodic Two','Annual Test'])
                print(Table_shape)
                                    
            elif Stream_option == '3':
                print("""
                ===============================================================================      
                                            The Actual Marks Scored in the Current Year
                ===============================================================================      """)

                #COLLECTION OF MARKS IN A VARIABLE FOR TABLE PRESENTATION 
                                
                PT1=[PTO_HINDI,PTO_ECO,PTO_BST,PTO_ENGLISH,PTO_ACC,PTO_PY]

                HF=[HF_HINDI,HF_ECO,HF_BST,HF_ENGLISH,HF_ACC,HF_PY]

                PT2=[PTT_HINDI,PTT_ECO,PTT_BST,PTT_ENGLISH,PTT_ACC,PTT_PY]

                AE=[AE_HINDI,AE_ECO,AE_BST,AE_ENGLISH,AE_ACC,AE_PY]

                #RESHAPING THE VARIABLES INTO A 2D TABLE

                Data_Table={"Periodic One":PT1,"Half Yearly":HF,"Periodic Two":PT2,"Annual Test":AE}
                Table_shape=p.DataFrame(Data_Table,index=["Hindi","Economics","Business Studies","English",'Accounts','Physical Education'])
                print(Table_shape)
            else:
                pass
            
        else:
            print('MARKS ARE ONLY SHOWN THROUGH MENU ONLY')
            
    elif Stream_choice == 1:
        
        Student_Report=SQL()

        #OPTIONAL SUBJECTS CATALOG
        print('''Optional Subjects available:
        1.Computer Science 
        2.Biology''')

        Stream_option=Restrict.limitalnum("Enter Which optional subject you have opted:")

        #STOREHOUSE
        try:
            SQL.CreateTB(SQL_Name)
            SQL.CreateRTB()
        except:
            print("Failed to Create Database")
        while True:                
            for i in range(5):
                if i == 1:
                    print("The Periodic Test-1 Fill Fourm")

                    # CHEMISTRY
                    chem_marks1 = Commerce.Entry("Chemistry", "Periodic Test - 1")

                    # PHYSICS
                    phy_marks1 = Commerce.Entry("Physics", "Periodic Test - 1")
                    
                    # MATHS
                    math_marks1 = Commerce.Entry("Maths", "Periodic Test - 1")
                    
                    #OPTINAL SUBJECTS
                    if Stream_option=='1':
                        cs_marks1 = Commerce.Entry("Computer Science", "Periodic test - 1")
                    elif Stream_option=='2':
                        bio_marks1=Commerce.Entry("Biololgy","Periodic Test - 1")
                    
                    # PE
                    pe_marks1 = Commerce.Entry("Physical Education", "Periodic Test -1")
                    
                    # ENG
                    eng_marks1 = Commerce.Entry("English", "Periodic Test -1")

                    continue

                # PERIODIC TEST - 1 END

                # HALF YEARLY - BEGINS
                if i == 2:
                    print("The Half Year Exam Fill Fourm")

                    # CHEMISTRY
                    chem_marks2 = Commerce.AHFComputer("Half-Yearly","Chemistry")

                    # PHYSICS
                    phy_marks2 = Commerce.AHFComputer("Half-yearly","Physics")
                    
                    #OPTIONAL SUBJECTS
                    if Stream_option=='1':
                        cs_marks2 = Commerce.AHFComputer("Half-Yearly","Computer Science")
                    elif Stream_option=='2':
                        bio_marks2=Commerce.AHFComputer("Half-Yearly","Biology")

                    # PE
                    pe_marks2 = Commerce.AHFComputer("Half-Yearly","Physical education")
                    
                    # Maths
                    math_marks2 = Commerce.AHYEntry("Maths", "Half-yearly")

                    # ENGLISH
                    eng_marks2 = Commerce.AHYEntry("English", "Half-yearly")

                    continue

                # HALF - YEARLY COMPLETED

                # PERIODIC TEST - 3 STARTS

                if i == 3:
                    print('The Periodic Test Two Fill Form')
                    
                    # CHEMISTRY
                    chem_marks3 = Commerce.Entry("Chemistry", "Periodic Test - 2")
                    
                    # PHYSICS
                    phy_marks3 = Commerce.Entry("Physics", "Periodic Test - 2")
                    
                    # MATHS
                    math_marks3 = Commerce.Entry("Maths", "Periodic Test - 2")
                    
                    #OPTOINAL SUBJECTS
                    if Stream_option=='1':
                        cs_marks3 = Commerce.Entry("Computer Science", "Periodic Test - 2")
                    elif Stream_option=='2':
                        bio_marks3=Commerce.Entry("Biology","Periodic Test -2")
                
                    # PE
                    pe_marks3 = Commerce.Entry("Physical Education", "Periodic Test -2")
                
                    # ENG
                    eng_marks3 = Commerce.Entry("English", "Periodic Test -2")
                    
                    continue
                # PERIODIC TEST - 2 ENDS

                # SESSION ENDING EXAMINATION STARTS

                if i == 4:
                    print("The Annual Examination Fill Fourm")

                    # CHEMISTRY
                    chem_marks4 = Commerce.AHFComputer("Session Ending Examination","Chemistry")

                    # PHYSICS
                    phy_marks4 = Commerce.AHFComputer("Session Ending Examination","Physics")
                    
                    # MATHS
                    math_marks4 = Commerce.AHYEntry("Session Ending Examination","Maths")
                    
                    # ENGLISH
                    eng_marks4 = Commerce.AHYEntry("English", "Session Ending Examination")
                    
                    #OPTOINAL SUBJECTS
                    if Stream_option=='1':
                        cs_marks4 = Commerce.AHFComputer("Session Ending Examination","Computer Science")
                    elif Stream_option=='2':
                        bio_marks4=Commerce.AHFComputer("Session Ending Examination","Biology")


                    # PE
                    pe_marks4 = Commerce.AHFComputer("Session Ending Examination","Physical Education")
                    # SESSION ENDING EXAMINATION ENDS

            break
        
        #STORAGE FOR NOMINAL MARK OF THE STUDENT
        try:
            SQL.RecDB(SQL_Name,'Chemistry',str(chem_marks1),str(chem_marks2),str(chem_marks3),str(chem_marks4))
            SQL.RecDB(SQL_Name,"Physics",str(phy_marks1),str(phy_marks2),str(phy_marks3),str(phy_marks4))
            SQL.RecDB(SQL_Name,'Maths',str(math_marks1),str(math_marks2),str(math_marks3),str(math_marks4))
            SQL.RecDB(SQL_Name,'English',str(eng_marks1),str(eng_marks2),str(eng_marks3),str(eng_marks4))
            if Stream_option==1:
                SQL.RecDB(SQL_Name,'Computer Science',str(cs_marks1),str(cs_marks2),str(cs_marks3),str(cs_marks4))
            elif Stream_option==2:
                SQL.RecDB(SQL_Name,'Biology',str(bio_marks1),str(bio_marks2),str(bio_marks3),str(bio_marks4))
            SQL.RecDB(SQL_Name,'Physical Education',str(pe_marks1),str(pe_marks2),str(pe_marks3),str(pe_marks4))
            print("Nominal marks of the student is successfully stored for science!!")
        except:
            print("Nominal marks of the student failed to stored for science!!")

        Nominal_Values=input('Do you want to see results (in table format)(y/n):')
        if Nominal_Values.lower()=='y':
            print("""
                ===============================================================================      
                                            The Marks Scored in the Current Year
                ===============================================================================      """)

            #COLLECTION OF MARKS IN A VARIABLE FOR TABLE PRESENTATION 
                                
            PT1=[chem_marks1,phy_marks1,math_marks1,eng_marks1,cs_marks1,pe_marks1]

            HF=[chem_marks2,phy_marks2,math_marks2,eng_marks2,cs_marks2,pe_marks2]

            PT2=[chem_marks3,phy_marks3,math_marks3,eng_marks3,cs_marks3,pe_marks3]

            AE=[chem_marks4,phy_marks4,math_marks4,eng_marks4,cs_marks4,pe_marks4]

            #RESHAPING THE VARIABLES INTO A 2D TABLE

            Data_Table={"Periodic One":PT1,"Half Yearly":HF,"Periodic Two":PT2,"Annual Test":AE}
            Table_shape=p.DataFrame(Data_Table,index=["Chemistry","Physics","Maths","English",'Computer Science','Physical Education'],\
            columns=['Periodic One','Half Yearly','Periodic Two','Annual Test'])
            print(Table_shape)
        else:
            print('Okay no problem!!')
        if Nominal_Values.lower() != 'y':
            print('MARKS ARE ONLY SHOWN THROUGH MENU ONLY')
    
        #CALCLUATION OF MARKS VARIABLES 
        #-----------------------------------#
        #PERIODIC TEST ONE REAL MARKS

        SCI_CHEM_PTO=(chem_marks1)/4
        SCI_PHY_PTO=(phy_marks1)/4
        SCI_MA_PTO=(math_marks1)/4
        SCI_EN_PTO=(eng_marks1)/4
        SCI_CS_PTO=(cs_marks1)/4
        SCI_PE_PTO=(pe_marks1)/4
        #HALF YEARLY REAL MARKS

        SCI_CHEM_HF=(chem_marks2/70)*30
        SCI_PHY_HF=(phy_marks2/70)*30
        SCI_MA_HF=(math_marks2/80)*30
        SCI_EN_HF=(eng_marks2/80)*30
        SCI_CS_HF=(cs_marks2)*30
        SCI_PE_HF=(pe_marks2/70)*30

        #PERIODIC TEST TWO REAL MARKS

        SCI_CHEM_PTT=(chem_marks3)/4
        SCI_PHY_PTT=(phy_marks3)/4
        SCI_MA_PTT=(math_marks3)/4
        SCI_EN_PTT=(eng_marks3)/4
        SCI_CS_PTT=(cs_marks3)/4
        SCI_PE_PTT=(pe_marks3)/4

        #ANNUAL YEAR REAL MARKS

        SCI_CHEM_AE=(chem_marks4/70)*30
        SCI_PHY_AE=(phy_marks4/70)*30
        SCI_MA_AE=(math_marks4/80)*30
        SCI_EN_AE=(eng_marks4/80)*30
        SCI_CS_AE=(cs_marks4)*30
        SCI_PE_AE=(pe_marks4/70)*30
        
        #SCIENCE ACTUAL MARKS OF EACH SUBJECT
        SCI_CHEM_FM=SCI_CHEM_AE+SCI_CHEM_HF+SCI_CHEM_PTO+SCI_CHEM_PTT
        SCI_PHY_FM=SCI_PHY_AE+SCI_PHY_HF+SCI_PHY_PTO+SCI_PHY_PTT
        SCI_MA_FM=SCI_MA_AE+SCI_MA_HF+SCI_MA_PTO+SCI_MA_PTT
        SCI_EN_FM=SCI_EN_AE+SCI_EN_HF+SCI_EN_PTO+SCI_EN_PTT
        SCI_CS_FM=SCI_CS_AE+SCI_CS_HF+SCI_CS_PTO+SCI_CS_PTT
        SCI_PE_FM=SCI_PE_AE+SCI_PE_HF+SCI_PE_PTO+SCI_PE_PTT

        #STOREAGE OF REAL MARKS
        try:
            SQL.RecReal(SQL_Name,'Chemistry',str(SCI_CHEM_PTO),str(SCI_CHEM_HF),str(SCI_CHEM_PTT),str(SCI_CHEM_AE))
            SQL.RecReal(SQL_Name,'Physics',str(SCI_PHY_PTO),str(SCI_PHY_HF),str(SCI_PHY_PTT),str(SCI_PHY_AE))
            SQL.RecReal(SQL_Name,'Maths',str(SCI_MA_PTO),str(SCI_MA_HF),str(SCI_MA_PTT),str(SCI_MA_AE))
            SQL.RecReal(SQL_Name,'English',str(SCI_EN_PTO),str(SCI_EN_HF),str(SCI_EN_PTT),str(SCI_EN_AE))
            SQL.RecReal(SQL_Name,'Computer Science',str(SCI_CS_PTO),str(SCI_CS_HF),str(SCI_CS_PTT),str(SCI_CS_AE))
            SQL.RecReal(SQL_Name,'Physical Education',str(SCI_PE_PTO),str(SCI_PE_HF),str(SCI_PE_PTT),str(SCI_PE_AE))
            print("Real values of the student is succesfully stored for science")
        except:
            print("Real values of the student failed to stored for science")

        #REPORT CARD
        Total_FM=SCI_CHEM_FM+SCI_PHY_FM+SCI_MA_FM+SCI_EN_FM+SCI_CS_FM+SCI_PE_FM
        Total_PCT=(Total_FM/440)*100
        Marks_box=[SCI_CHEM_FM+SCI_PHY_FM+SCI_MA_FM+SCI_EN_FM+SCI_CS_FM+SCI_PE_FM]
        Box_len=len(Marks_box)
        Status_pass="Pass"
        Status_fail="Failed"
        Marks_floor=33
        for sub in Marks_box:
            if sub>= Marks_floor:
                if sub ==Marks_box[Box_len-1]:
                    try:
                        SQL.RecRTB(str(Student_admin),SQL_Name,'Science',str(Total_FM),str(Total_PCT),str(Status_pass))
                    except:
                        print("Data Failed to Store.Please check the script")
            elif sub<Marks_floor:
                try:
                    SQL.RecRTB(str(Student_admin),SQL_Name,'Science',str(Total_FM),str(Total_PCT),str(Status_fail))
                except:
                    print("Data Failed to Store.Please check the script")
                    
                break

        #ACUTALL MARKS SCORED BY THE STUDENT
        Post_Values=Restrict.limitchar('Do you want to see the acutal results (in table format)(y/n):')
        if Post_Values=='y' or 'yes':
            print("""
                ===============================================================================      
                                            The Actual Marks Scored in the Current Year
                ===============================================================================      """)

            #COLLECTION OF MARKS IN A VARIABLE FOR TABLE PRESENTATION 

            PT1=[SCI_CHEM_PTO,SCI_PHY_PTO,SCI_MA_PTO,SCI_EN_PTO,SCI_CS_PTO,SCI_PE_PTO]

            HF=[SCI_CHEM_HF,SCI_PHY_HF,SCI_MA_HF,SCI_EN_HF,SCI_CS_HF,SCI_PE_HF]

            PT2=[SCI_CHEM_PTT,SCI_PHY_PTT,SCI_MA_PTT,SCI_EN_PTT,SCI_CS_PTT,SCI_PE_PTT]

            AE=[SCI_CHEM_AE,SCI_PHY_AE,SCI_MA_AE,SCI_EN_AE,SCI_CS_AE,SCI_PE_AE]

            #RESHAPING THE VARIABLES INTO A 2D TABLE

            Data_Table={"Periodic One":PT1,"Half Yearly":HF,"Periodic Two":PT2,"Annual Test":AE}
            Table_shape=p.DataFrame(Data_Table,index=["Chemistry","Physics","Maths","English",'Computer Science','Physical Education'])
            print(Table_shape)

        if Post_Values.lower()!='y':
            print('okay no problem')        
        
    elif Stream_choice == 3:

        Student_Report=SQL()

        #STOREHOUSE
        try:
            SQL.CreateTB(SQL_Name)
            SQL.CreateRTB()
        except:
            print("Failed to Create Database")
        while True:
            for i in range(5):
                if i==1:

                    print("The Periodic Test-1 Fill Fourm")

                    #SOCIOLOGY SUBJECT
                    sco_marks1=Commerce.Entry('Sociology','Periodic Test-1')

                    #ENGLISH SUBJECT
                    eng_marks1=Commerce.Entry("English","Periodic Test-1")

                    #HISTORY SUBJECT
                    hist_marks1=Commerce.Entry("History",'Periodic Test-1')

                    #HINDI SUBJECT
                    hin_marks1=Commerce.Entry('Hindi','Periodic Test-1')

                    #PHYSICAL EDUCATION SUBJECT
                    pe_marks1=Commerce.Entry("Physical Education","Periodic Test-1")

                    #GEOGRAPHY SUBJECT
                    geo_marks1=Commerce.Entry("Geography","Periodic Test-1")

                if i==2:

                    print("The Half Year Exam Fill Fourm")
                    
                    #SOCIOLOGY SUBJECT
                    sco_marks2=Commerce.AHYEntry('Sociology','Half Yearly Examination')

                    #ENGLISH SUBJECT
                    eng_marks2=Commerce.AHYEntry("English","Half Yearly Examinatione")

                    #HISTORY SUBJECT
                    hist_marks2=Commerce.AHYEntry("History",'Half Yearly Examination')

                    #HINDI SUBJECT
                    hin_marks2=Commerce.AHYEntry('Hindi','Half Yearly Examination')

                    #PHYSCIAL EDUCATION SUBJECT
                    pe_marks2=Commerce.AHYEntry("Physical Education","Half Yearly Examination")

                    #GEOGRAPHY SUBJECT
                    geo_marks2=Commerce.AHFComputer("Half Yearly Examination","Geography")

                if i==3:
                    
                    print('The Periodic Test Two Fill Form')

                    #SOCIOLOGY SUBJECT
                    sco_marks3=Commerce.Entry('Sociology','Periodic Test-2')

                    #ENGLISH SUBJECT
                    eng_marks3=Commerce.Entry("English","Periodic Test-2")

                    #HISTORY SUBJECT
                    hist_marks3=Commerce.Entry("History",'Periodic Test-2')

                    #HINDI SUBJECT
                    hin_marks3=Commerce.Entry('Hindi','Periodic Test-2')

                    #PHYSICAL EDUCATION SUBJECT
                    pe_marks3=Commerce.Entry("Physical Education","Periodic Test-2")

                    #GEOGRAPHY SUBJECT
                    geo_marks3=Commerce.Entry("Geography","Periodic Test-2")

                if i==4:
                    
                    print("The Annual Examination Fill Fourm")

                    #SOCIOLOGY SUBJECT
                    sco_marks4=Commerce.AHYEntry('Sociology','Annual Examination')

                    #ENGLISH SUBJECT
                    eng_marks4=Commerce.AHYEntry("English","Annual Examination")

                    #HISTORY SUBJECT
                    hist_marks4=Commerce.AHYEntry("History",'Annual Examination')

                    #HINDI SUBJECT
                    hin_marks4=Commerce.AHYEntry('Hindi','Annual Examination')

                    #PHYSCIAL EDUCATION SUBJECT
                    pe_marks4=Commerce.AHYEntry("Physical Education","Annual Examination")

                    #GEOGRAPAHY SUBJECT
                    geo_marks4=Commerce.AHFComputer('Annual Examination',"Geography")
            break

        #STORAGE FOR NOMINAL VALUES
        try:
            SQL.RecDB(SQL_Name,'Sociology',str(sco_marks1),str(sco_marks2),str(sco_marks3),str(sco_marks4))
            SQL.RecDB(SQL_Name,'English',str(eng_marks1),str(eng_marks2),str(eng_marks3),str(eng_marks4))
            SQL.RecDB(SQL_Name,'History',str(hist_marks1),str(hist_marks2),str(hist_marks3),str(hist_marks4))
            SQL.RecDB(SQL_Name,'Hindi',str(hin_marks1),str(hin_marks2),str(hin_marks3),str(hin_marks4))
            SQL.RecDB(SQL_Name,'Geography',str(geo_marks1),str(geo_marks2),str(geo_marks3),str(geo_marks4))
            SQL.RecDB(SQL_Name,'Physical Education',str(pe_marks1),str(pe_marks2),str(pe_marks3),str(pe_marks4))
            print("Nominal values of the student is succesfully stored for Arts")
        except:
            print("Nominal values of the student failed to stored for Arts")

        #NOMINAL MARKS IN TABLE FORM
        Nominal_Values=input('Do you want to see results (in table format)(y/n):')
        if Nominal_Values=='y' or 'yes':
            print("""
                ===============================================================================      
                                            The Marks Scored in the Current Year
                ===============================================================================      """)

            #COLLECTION OF MARKS IN A VARIABLE FOR TABLE PRESENTATION 
                                
            PT1=[sco_marks1,eng_marks1,hist_marks1,hin_marks1,geo_marks1,pe_marks1]

            HF=[sco_marks2,eng_marks2,hist_marks2,hin_marks2,geo_marks2,pe_marks2]

            PT2=[sco_marks3,eng_marks3,hist_marks3,hin_marks3,geo_marks3,pe_marks3]

            AE=[sco_marks4,eng_marks4,hist_marks4,hin_marks4,geo_marks4,pe_marks4]

            #RESHAPING THE VARIABLES INTO A 2D TABLE

            Data_Table={"Periodic One":PT1,"Half Yearly":HF,"Periodic Two":PT2,"Annual Test":AE}
            Table_shape=p.DataFrame(Data_Table,index=["Scoiology","English","History","Hindi",'Geography','Physical Education'],\
            columns=['Periodic One','Half Yearly','Periodic Two','Annual Test'])
            print(Table_shape)
        if Nominal_values.lower()!='y':
            print("okay no problem")
            

        #CALCLUATION OF MARKS VARIABLES 
        #-----------------------------------#
        #PERIODIC TEST 1 REAL MARKS ARTS

        AR_SCO_PTO=(sco_marks1)/4
        AR_EN_PTO=(eng_marks1)/4
        AR_HIST_PTO=(hist_marks1)/4
        AR_HIN_PTO=(hin_marks1)/4
        AR_GEO_PTO=(geo_marks1)/4
        AR_PE_PTO=(pe_marks1)/4

        #HALF YEARLY EXAMINATION REAL MARKS  OF ARTS

        AR_SCO_HF=(sco_marks2/80)*30
        AR_EN_HF=(eng_marks2/80)*30
        AR_HIST_HF=(hist_marks2/80)*30
        AR_HIN_HF=(hin_marks2/80)*30
        AR_GEO_HF=(geo_marks2/70)*30
        AR_PE_HF=(pe_marks2/80)*30

        #PERIODIC TEST 2 REAL MARKS OF ARTS

        AR_SCO_PTT=(sco_marks3)/4
        AR_EN_PTT=(eng_marks3)/4
        AR_HIST_PTT=(hist_marks3)/4
        AR_HIN_PTT=(hin_marks3)/4
        AR_GEO_PTT=(geo_marks3)/4
        AR_PE_PTT=(pe_marks3)/4

        #FINAL EXAMINATION TEST REAL MARKS OF ARTS

        AR_SCO_AE=(sco_marks4/80)*30
        AR_EN_AE=(eng_marks4/80)*30
        AR_HIST_AE=(hist_marks4/80)*30
        AR_HIN_AE=(hin_marks4/80)*30
        AR_GEO_AE=(geo_marks4/70)*30
        AR_PE_AE=(pe_marks4/80)*30

        #SUM OF TOTAL ACUTALLY SCORED OF ARTS

        AR_SCO_FM=AR_SCO_AE+AR_SCO_HF+AR_SCO_PTO+AR_SCO_PTT
        AR_EN_FM=AR_EN_AE+AR_EN_HF+AR_EN_PTO+AR_EN_PTT
        AR_GEO_FM=AR_GEO_AE+AR_GEO_HF+AR_GEO_PTO+AR_GEO_PTT
        AR_HIST_FM=AR_HIST_AE+AR_HIST_HF+AR_HIST_PTO+AR_HIST_PTT
        AR_HIN_FM=AR_HIN_AE+AR_HIN_HF+AR_HIN_PTO+AR_HIN_PTT
        AR_PE_FM=AR_PE_AE+AR_PE_HF+AR_PE_PTO+AR_PE_PTT

        #STORAGE OF REAL VALUES OF ARTS
        try:
            SQL.RecReal(SQL_Name,'Sociology',str(AR_SCO_PTO),str(AR_SCO_HF),str(AR_SCO_PTT),str(AR_SCO_AE))
            SQL.RecReal(SQL_Name,'English',str(AR_EN_PTO),str(AR_EN_HF),str(AR_EN_PTT),str(AR_EN_AE))
            SQL.RecReal(SQL_Name,'History',str(AR_HIST_PTO),str(AR_HIST_HF),str(AR_HIST_PTT),str(AR_HIST_AE))
            SQL.RecReal(SQL_Name,'Hindi',str(AR_HIN_PTO),str(AR_HIN_HF),str(AR_HIN_PTT),str(AR_HIN_AE))
            SQL.RecReal(SQL_Name,"Geography",str(AR_GEO_PTO),str(AR_GEO_HF),str(AR_GEO_PTT),str(AR_GEO_AE))
            SQL.RecReal(SQL_Name,"Physical Education",str(AR_PE_PTO),str(AR_PE_HF),str(AR_PE_PTT),str(AR_PE_AE))
            print("Real values of the student is succesfully stored for Arts")
        except:
            print("The Real values of the student Failed to store for Arts")

        #REPORT CARD
        Total_FM=AR_SCO_FM+AR_HIN_FM+AR_HIST_FM+AR_EN_FM+AR_GEO_FM+AR_PE_FM
        Total_PCT=(Total_FM/470)*100
        Marks_box=[AR_SCO_FM,AR_HIN_FM,AR_HIST_FM,AR_EN_FM,AR_GEO_FM,AR_PE_FM]
        Box_len=len(Marks_box)
        Status_pass="Pass"
        Status_fail="Failed"
        Marks_floor=33
        for sub in Marks_box:
            if sub>= Marks_floor:
                if sub ==Marks_box[Box_len-1]:
                    try:
                        SQL.RecRTB(str(Student_admin),SQL_Name,'Arts',str(Total_FM),str(Total_PCT),str(Status_pass))
                        break
                    except:
                        print("Data Failed to Store.Please check the script")
            elif sub<Marks_floor:
                try:
                    SQL.RecRTB(str(Student_admin),SQL_Name,'Arts',str(Total_FM),str(Total_PCT),str(Status_fail))
                    break
                except:
                    print("Data Failed to Store.Please check the script")
                break
    
            
        #ACUTALL MARKS SCORED BY THE STUDENT
        Post_Values=Restrict.limitchar('Do you want to see the acutal results (in table format)(y/n):')
        if Post_Values=='y' or 'yes':
            print("""
                ===============================================================================      
                                            The Actual Marks Scored in the Current Year
                ===============================================================================      """)

            #COLLECTION OF MARKS IN A VARIABLE FOR TABLE PRESENTATION 

            PT1=[AR_SCO_PTO,AR_EN_PTO,AR_HIST_PTO,AR_HIN_PTO,AR_GEO_PTO,AR_PE_PTO]

            HF=[AR_SCO_HF,AR_EN_HF,AR_HIST_HF,AR_HIN_HF,AR_GEO_HF,AR_PE_HF]

            PT2=[AR_SCO_PTT,AR_EN_PTT,AR_HIST_PTT,AR_HIN_PTT,AR_GEO_PTT,AR_PE_PTT]

            AE=[AR_SCO_AE,AR_EN_AE,AR_HIST_AE,AR_HIN_AE,AR_GEO_AE,AR_PE_AE]

            #RESHAPING THE VARIABLES INTO A 2D TABLE

            Data_Table={"Periodic One":PT1,"Half Yearly":HF,"Periodic Two":PT2,"Annual Test":AE}
            Table_shape=p.DataFrame(Data_Table,index=["Scoiology","English","History","Hindi",'Geography','Physical Education'],\
            columns=['Periodic One','Half Yearly','Periodic Two','Annual Test'])
            print(Table_shape)

        if Post_Values.lower()!='y':
            print("okay no problem")
        
    else:
        print("Sorry this Stream is currently not available.Please select from (1-3) stream.")
    
    print("Thank you for being paitent.")

#FACE OF THE PROGRAM
def main():
    #SOFTWARE NAME OUTPUT
    print("""==================================================================\n                           Qualifier v1.0.1\n======\
============================================================""")
    print('1.RECORD STUDENT SCORE               2.VIEW STUDENT SCORES')
    print("3.MANAGE STUDENT RECORD              4.VIEW STUDENT RESULTS")
    Main_ask=Restrict.num('Enter desired option from above:')
    if Main_ask == 1:
        Student_Record()
    elif  Main_ask ==2:
        print("""==================================================================\n                           STUDENTS RESULT\n======\
============================================================""")
        print("1.NOMINAL RECORDS             2.REAL RECORDS")
        try:
            User_rec=Restrict.num("Enter which Record to show of the student:")
        except:
            print("There are no Records to View/Modify")
            
        try:
            SQL.SearchRTB()

            if User_rec==1:
                User_ask=input("Enter Name to get Student Nominal Record:")
                try:
                    time.sleep(1)
                    SQL.SearchRec(User_ask)
                except:
                    print("The name should be Written as shown only,try again through menu")
                
            elif User_rec==2:
                User_ask=input("Enter Name to get Student Real Record:")
                try:
                    time.sleep(1)
                    SQL.SearchReal(User_ask)
                except:
                    print("The name should be Written as shown only,try again through menu")
        except:
            print("There are no Records to View/Modify")
            
        
                
    elif Main_ask ==3:
        print("""==================================================================\n                           DATA ALTERATION\n========\
==========================================================""")
        print("1.REMOVE RECORD              2.UPDATE RECORD")
        try:
            User_rec=Restrict.num("Enter options from above for Record Configration:")
            if User_rec==1:
                SQL.SearchRTB()
                User_ask=input('Enter Name of student to remove:')
                try:
                    SQL.delrec(User_ask)
                except:
                    print("The Function did not work.Try again")
                
            elif User_rec==2:
                SQL.SearchRTB()
                User_ask=input("Enter Name of the Student to config:")
                print("""==================================================================\n                           RECORD CONFIGRATIONS\n======\
============================================================""")
                print("1.NAME                   2.MARKS")
                print("3.STATUS                 4.MARKS%")
                print("5.ADMIN NO")
                try:
                    User_req=Restrict.num("Enter options from above to modify:")
                except:
                    print("sorry that option is not available")
                if User_req==5:
                    Admin_new=Restrict.num("Enter new Adminssion No of %s:"%(User_ask))
                    try:
                        SQL.UPAdm(User_ask,str(Admin_new))
                        print("Data Modified Successfully")
                    except:
                        print("Data Modified Failed")
                        
                if User_req==2:
                    Marks_new=float(input('Enter New Total marks of %s:'%(User_ask)))
                    try:
                        SQL.UPMark(User_ask,str(Marks_new))
                        print("Data Modified Successfully")
                    except:
                        print("Data Modified Failed")
                        
                if User_req==3:
                    Stat_new=input("Enter Status of %s (fail/pass):")
                    Log_box=['Fail','Pass','pass','fail']
                    if Stat_new in Log_box:
                        try:
                            SQL.UPST(User_ask,Stat_new.title())
                            print("Data Modified Successfully")
                        except:
                            print("Data Modified Failed")
                    else:
                        Eor='Error'
                        try:
                            SQL.UPST(User_ask,str(Eor))
                            print("Data Modified Successfully")
                        except:
                            print("Data Modified Failed")
                if User_req==1:
                    print('                                        (Enter a to check admission no)')
                    admin=input("Enter admission number of %s:"%(User_ask))
                    if admin=='a':
                        try:
                            SQL.SHAN()
                            admin_no=Restrict.num("Enter admission number of %s:"%(User_ask))
                            Name_new=input("Enter New name of %s:"%(User_ask))
                            Name_sq=SQL.Replace_spc(Name_new)
                            SQL.UPN(User_ask,Name_sq,admin_no)
                
                        except:
                            print("Function failed to run")
                    else:
                        Name_new=input("Enter New name of %s:"%(User_ask))
                        Name_sq=SQL.Replace_spc(Name_new)
                        admin_i=int(admin)
                        SQL.UPN(User_ask,Name_sq,admin_i)
                        print("Data Modified Successfully")
                    
                if User_req == 4:
                    MarkP_new=Restrict.num("Enter New Percentage of %s:"%(User_ask))
                    try:
                        SQL.UPMK(User_ask,MarkP_new)
                        print("Data Modified Successfully")
                    except:
                        print("Data Modified Failed")

        except:
            print("There are no Records to View/Modify")
            
    elif Main_ask==4:
        time.sleep(1)
        print("""==================================================================\n                           STUDENTS FINAL SCORE\n\
==================================================================""")
        try:
            SQL.SHRTB()
        except:
            print("Function failed to run")
    else:
        print("Please enter within options available")
    Restart()    
    
#FUNCTION TO RESTART THE PROGRAM
def Restart():
    print("(Enter any keyword to exit)")
    Run_again=input('Press Enter to go to Menu:')
    if Run_again.lower() == '':
        sec=RN.randrange(0,4)
        print(sec,'Seconds remaning to restart...')
        for i in range(sec-1,0,-1):
            time.sleep(1)
            print(i,'Seconds remaing to restart...')
        print('')
        main()
    elif Run_again!='':
        print('Exit Dialogue opening...')
        time.sleep(1)
        exit()

#FUNCTION TO CLOSE THE PROGRAM SUCESSFULLY WITH DATABASE        
def Main():
    main()
    Storehouse.close()
Main()






