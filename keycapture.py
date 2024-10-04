from readchar import readchar,readkey,key
from controller import *

run = True
control = Controller("test_role")
control.show_boot_message()

while run == True:
    k = readchar()
    if k == "a":
        print(k)
        control.show_applicants()
        print("(`oAo)")
    if k == "b":
        control.show_boot_message()
        print("(=v=)b")
    if k == "c":
        control.show_criteria()
    if k == "r":
        control.show_role_info()
    if k == "s":
        control.show_shortlist()
    if k == "o":
        print("(´⊙ω⊙`)!")
    if k == key.CTRL_U:
        print("ctrl u")
    if k == key.ESC:
        print("exiting the program...")
        break
    
run == False
quit()


"""Learning Notes"""
#readchar() / readkey() both returns a string
#key.sepecial_key makes it easier comparing keys like ENTER, Ctrl+A ,TAB
#? difference between read char and read key

"""code improvement"""
#could perhaps put all the keypress options in a list or set to avoid using hundreds if statements?
