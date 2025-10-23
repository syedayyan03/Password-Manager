# ---------------------------- PASSWORD GENERATOR ------------------------------- #
from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip
import json

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    num_letters = randint(8, 10)
    num_symbols  = randint(2, 4)
    num_numbers = randint(2, 4)

    password_letters= [choice(letters) for _ in range(num_letters)]
    password_symbols= [choice(symbols) for _ in range(num_symbols)]
    password_numbers= [choice(numbers) for _ in range(num_numbers)]

    password_list = password_symbols + password_numbers + password_letters
    shuffle(password_list)

    password= "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password= password_entry.get()

    new_data = {
        website:{
            "email": email,
            "password": password,
        }
    }

    if len(password)==0 or len(email)==0 or len(password)==0:
        messagebox.showinfo(title="Oops", message="Please don't leave any field empty!")

    else:
        # is_ok= messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail:{email}"
        #                             f"\nPassword:{password} \nIs it ok to save")
        # if is_ok:
        # with open("data.txt", "a") as data_file:
        try:
            with open("data.json", "r") as data_file:
                # data_file.write(f"{website} | {email} | {password}\n")
                data= json.load(data_file) # read the json data
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                #Saving the updated data
                json.dump(new_data, data_file, indent= 4) # it is used to add data into json file for the first time

        else:
            data.update(new_data)  # updating the old data with new data
            with open("data.json", "w") as data_file:
                #Saving the updated data
                json.dump(data, data_file, indent= 4)

        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)
#----------------------------- FIND PASSWORD ---------------------------#
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data= json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")

    else:
            if website in data:
                email= data[website]["email"]
                password= data[website]["password"]
                messagebox.showinfo(title= website, message=f"Email: {email}\nPassword:{password}")
            else:
                messagebox.showinfo(title= "Error", message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
window= Tk()
window.title("Password Manager")
window.config(padx= 50, pady= 50)

canvas= Canvas(width= 200, height= 200)
logo_img= PhotoImage(file= "logo.png")
canvas.create_image(100, 100, image= logo_img)
canvas.grid(column= 1, row= 0)

website_label= Label(text= "Website:", font=("Arial", 10))
website_label.grid(column= 0 , row= 1)

website_entry= Entry(width= 21)
website_entry.grid(column= 1 , row= 1)

email_label= Label(text= "Email/Username:", font=("Arial", 10))
email_label.grid(column= 0 , row= 2)

email_entry= Entry(width= 32)
email_entry.grid(column= 1 , row= 2)

password_label= Label(text= "Password:", font=("Arial", 10))
password_label.grid(column= 0 , row= 3)

password_entry= Entry(width= 21)
password_entry.grid(column= 1 , row= 3)

generate_password_button = Button(text= "Generate Password", highlightthickness=0, command= generate_password)
generate_password_button.grid(column= 2, row= 3)

add_button= Button(text= "Add", width= 36, highlightthickness=0, command= save)
add_button.grid(column= 1, row= 4)

search_button= Button(text= "Search", highlightthickness=0, width= 13, command= find_password)
search_button.grid(column= 2, row= 1)

window.mainloop()