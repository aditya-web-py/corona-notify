import tkinter
from tkinter import ttk
from tkinter import messagebox
from win10toast import ToastNotifier
from bs4 import BeautifulSoup
import requests
import time

window = tkinter.Tk()
window.title('Coronavirus Notify')
window.iconbitmap(r'icon.ico')

labelOne = ttk.Label(window, text='Your state name:    ')
labelOne.grid(row=0, column=0)
stateName = tkinter.StringVar()
refresh = tkinter.IntVar()
stateEntry = ttk.Entry(window, width=26, textvariable=stateName)
stateEntry.grid(row=0, column=1)
labelTwo = ttk.Label(window, text='Refresh Time(Min): ')
labelTwo.grid(row=1, column=0)
refreshEntery = ttk.Entry(window, width=26, textvariable=refresh)
refreshEntery.grid(row=1, column=1)


def data_cleanup(array):
    L = []
    for i in array:
        i = i.replace("*", "")
        i = i.replace("-", "")
        if i == "":
            i = "0"
        L.append(i.strip())
    return L


def openFrame():
    window.withdraw()
    states = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
              "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands", "Chandigarh", "Delhi", "Puducherry"]
    state = stateName.get().title()
    if state not in states:
        messagebox.showerror("Error", "State not found.")
        window.quit()
    else:
        if state == 'Nagaland':
            state = 'Assam'
        country = ["India", state]
        notification_duration = 7
        refresh_time = refresh.get()  # minutes
        worldmetersLink = "https://www.mohfw.gov.in/"
        while True:
            try:
                html_page = requests.get(worldmetersLink)
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", e)
                window.quit()
                break
            bs = BeautifulSoup(html_page.content, 'html.parser')

            search = bs.select("div tbody tr td")
            start = -1
            for j in country:
                for i in range(len(search)):
                    if search[i].get_text().find(j) != -1:
                        start = i
                        break
                data = []
                for i in range(1, 4):
                    try:
                        data = data + [search[start+i].get_text()]
                    except:
                        data = data + ["0"]

                data = data_cleanup(data)
                message = "Total infected = {},  Recovered = {},  Deaths = {}".format(
                    *data)
                toaster = ToastNotifier()
                if j == 'Assam':
                    j = 'Assam & Nagaland'
                toaster.show_toast("Coronavirus {}".format(
                    j), message, duration=notification_duration, icon_path="icon.ico")
            time.sleep(refresh_time*60)


btn = ttk.Button(window, text='NotifyMe', command=openFrame)
btn.grid(row=0, column=2, rowspan = 2)
stateEntry.focus()
copy = ttk.Label(window, text='© Aditya Prakash Gupta')
copy.grid(row=2, column=0, columnspan = 3)
window.resizable(0, 0)
window.mainloop()
