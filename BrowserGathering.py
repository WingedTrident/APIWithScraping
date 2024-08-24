#IMPORTS
import requests
import webbrowser
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import END, Text, Listbox
from tkinter.ttk import Button

#SETUP
root = tk.Tk()
root.title('API + Scraping Practice')
root.geometry('400x400')
root.resizable(False, False)

#uses the quotable website api to directly get json information
def get_quote():
    try:
        r = requests.get('https://api.quotable.io/random')
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    data = r.json()
    quote = data['content']
    
    text_box.delete('1.0', END) #delete the previous quote
    
    text_box.insert(END, quote) #insert the new quote

#uses a mock careers website made to practice webscraping
def get_jobs():
    global urls
    URL = "https://realpython.github.io/fake-jobs/"
    try: 
        page = requests.get(URL)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    soup = BeautifulSoup(page.content, "html.parser") #parses the page's html

    results = soup.find(id="ResultsContainer") #narrows content to certain ids

    python_jobs = results.find_all( #looks for h2 elements with python in them
        "h2", string=lambda text: "python" in text.lower()
    )

    python_job_elements = [ #broadens the scope out to access all elements of the listing
        h2_element.parent.parent.parent for h2_element in python_jobs
    ]
    
    all_python_jobs = [job.find("h2", class_="title") for job in python_job_elements] #gets the listing job titles only
    all_python_job_urls = [job.find_all("a")[1]['href'] for job in python_job_elements] #get the urls for the jobs only (same order)
    urls = all_python_job_urls
    
    list_box.delete(0, END) #clear previous results 
    
    for job in all_python_jobs: #inserts all listing found one by one
        list_box.insert(END, job.text.strip())

#uses the urls gathered from the scraping to link to the selected job in the list        
def goto_job():    
    selected = list_box.curselection() #checks what list element is selected
    if len(selected) == 0: #if no item selected do nothing
        return
    webbrowser.open(urls[selected[0]]) #otherwise open up the link with webbrowser
    
#GLOBAL (no class used for this application)
urls = None  
   
#LAYOUT    
text_box = Text(root, height=10, width=100)
get_quote_button = Button(root, text="Get Quote", command=get_quote)

list_box = Listbox(root) 
get_job_button = Button(root, text="Get Python related jobs", command=get_jobs)
goto_job_button = Button(root, text="Job Link", command=goto_job)

#BUILD
text_box.pack()
get_quote_button.pack()
list_box.pack(fill=tk.BOTH)
get_job_button.pack()
goto_job_button.pack()

#MAIN LOOP
root.mainloop()
