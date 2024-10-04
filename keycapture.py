from readchar import readkey,key

run = True

while run == True:
    k = readkey()

    if k == "a":
        print("Showing the number of applicants")
    if k == "b":
        print("b")
    if k == key.ESC:
        print("exiting the program")
        break
    
run == False
quit()