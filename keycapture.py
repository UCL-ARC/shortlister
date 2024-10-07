from readchar import readchar,readkey,key
from controller import Controller

run = True
control = Controller("test_role")
control.show_boot_message()

while run == True:
    options = {"a":control.show_applicants,
               "b":control.show_boot_message,
               "c":control.show_criteria,
               "r":control.show_role_info,
               "s":control.show_shortlist,} 
    
    k = readkey()
    output = options.get(k)
    if output is not None:
        output()
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

# put keypress and controller functions in key:value pair in a dictionary
# check if k == any of the keys 
# if it does, access the function stored in value