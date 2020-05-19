import os
import pickle
import webbrowser
from utils import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as font
from tkinter import filedialog,Checkbutton,Canvas
from tkinter.messagebox import askyesno,askquestion,showinfo,showerror

REPOS = 'repos'

if not os.path.exists(REPOS):
	os.mkdir(REPOS)

root = Tk()
url,repo = StringVar(root),StringVar(root) 

flag = False

if os.path.exists("url.txt"):
	flag = True # for disabling home
	with open("url.txt",'r') as f:
		url.set(f.readline())
	repo.set(get_repo_name_from_url(url.get()))
	update_local_repo(repo.get())  # if repo exists. update it.

root.wm_iconbitmap("assets/icon.ico")
root.title("env2repo")


width_of_window = 650
height_of_window = 480

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width/2)-(width_of_window/2)
y = (screen_height/2)-(height_of_window/2)

root.geometry("%dx%d+%d+%d"%(width_of_window,height_of_window,x,y))
root.resizable(width=False, height=False)

# <----------------functions------------------>
def init_repo():
	url.set(url_entry.get())
	if url.get().split('/')[-1].split('.')[-1] == 'git':
		with open("url.txt",'w') as f:
			f.write(url.get())
		repo.set(init_local_repo(url.get()))
		print('repo from init_local_repo',repo.get())
	else:
		showerror("INVALID URL!","The url you have entered is invalid. Try again")

# <----------------Notebook------------------>
note = ttk.Notebook(root)

home = ttk.Frame(note)
tab1 = ttk.Frame(note)
tab2 = ttk.Frame(note)
about = ttk.Frame(note)

if flag:
	note.add(home,text="Add Github url",state="disabled")
else:
	note.add(home,text="Add Github url")

note.add(tab1, text = "Your envs")
note.add(tab2, text = "Envs on Github", state="disabled")
note.add(about, text = "About")

note.pack(expand = 1, fill = "both")


# <----------------Home(tab0)------------------>
## <--canvas_home-->	
canvas_home = Canvas(home,bg='#398FFF')
canvas_home.pack(expand=True,fill=BOTH)

## <--url-->	
url_entry = Entry(canvas_home,width=40)
url_entry['font']=font.Font(size=15)

enter_url_button = Button(canvas_home, text="Enter Url",command=init_repo)
enter_url_button['font']=font.Font(size=15)

url_entry.place(relx=0.5, rely=0.4, anchor=CENTER)
enter_url_button.place(relx=0.5, rely=0.5, anchor=CENTER)


# <----------------tab1------------------>
## <--canvas1-->	
canvas_tab1 = Canvas(tab1,bg='#398FFF')
canvas_tab1.pack(expand=True,fill=BOTH)

## <--add envs-->	
envs = get_envs()
env_list = Listbox(canvas_tab1,width = 50,bg='#85144B',fg='white')
env_list.pack(side=LEFT,fill=Y)
env_list.config(border=2,relief=FLAT,font=("Courier", 9))
for env in envs:
	env_list.insert(END,"      "+env)

## <--scrollbar-->	
scroll = Scrollbar(canvas_tab1,orient=VERTICAL,command=env_list.yview)
scroll.pack(side=LEFT,fill=Y)
env_list['yscrollcommand'] = scroll.set

## <--functions for buttons-->	
def show_info_backup(env_name,version):
	showinfo(title="Backedup successfully!",
	 message=env_name+" backedup successfully to version: "+version)

def get_env_name_from_selection():
	env_name = env_list.get(env_list.curselection())
	env_name = env_name.split(' ')[-1]
	return env_name

def check_backup():
	env_name = get_env_name_from_selection()
	path_to_env = os.path.join(REPOS,repo.get(),env_name)
	if not os.path.exists(path_to_env):
		answer = askyesno('Not backedup',
			env_name+" is not backedup. Do u wish to backup?")
		if answer:
			version = save_env(env_name,repo.get())
			show_info_backup(env_name,version)
	else:
		backed_up = check_prev_backup(path_to_env,env_name)
		if backed_up:
			showinfo(title="Backedup!", message=env_name+" is backedup")
		else:
			answer = askyesno('Backedup outdated',
				env_name+" has changed since the last backup. Do u wish to backup again?")
			if answer:
				version = save_env(env_name,repo,get())
				show_info_backup(env_name,version)

def backup_env():
	env_name = get_env_name_from_selection()
	version = save_env(env_name,repo.get())
	show_info_backup(env_name,version)
	

def delete_env():
	env_name = get_env_name_from_selection()
	backed_up = check_prev_backup(repo.get(),env_name)
	if backed_up:
		remove_env(env_name)
		showinfo(title="Removed!", message=env_name+" is removed from ur local machine")
		env_list.delete(env_list.curselection())
	else:
		answer = askquestion ("Env not backed up!!",
			env_name+" has not been backed up or has been modified afterwards, are you sure you want to remove it?",
			icon = 'warning')
		if answer=="yes":
			remove_env(env_name)
			showinfo(title="Removed!", message=env_name+" is removed from ur local machine")
			env_list.delete(env_list.curselection())

## <--buttons-->	
check = Button(canvas_tab1, text="Check if backedup",
	command=check_backup,relief=FLAT,padx=20,pady=10,fg='blue',bd=2,state='disabled')
check.pack(side=TOP,pady=90)
check['font']=font.Font(size=15)


backup = Button(canvas_tab1, text="Backup env",
	command=backup_env,relief=FLAT,padx=20,pady=10,fg='blue',bd=2,state='disabled')
backup.pack(side=TOP,pady=10)
backup['font']=font.Font(size=15)


delete = Button(canvas_tab1, text="Delete env",
	command=delete_env,relief=FLAT,padx=20,pady=10,fg='blue',bd=2,state='disabled')
delete.pack(side=TOP,pady=10)
delete['font']=font.Font(size=15)


#<----------------tab2------------------>

## <--canvas2-->	
canvas_tab2 = Canvas(tab2,bg='#398FFF')
canvas_tab2.pack(expand=True,fill=BOTH)

## <--functions for getting env name-->	
def get_env_name_from_selection_tab2():
	env_name = env_list_tab2.get(env_list_tab2.curselection())
	env_name = env_name.split(' ')[-1]
	print('env_name :: ',env_name)
	return env_name

## <--add envs-->	
env_list_tab2 = Listbox(canvas_tab2,width = 50,bg='#85144B',fg='white')
env_list_tab2.pack(side=LEFT,fill=Y)
env_list_tab2.config(border=2,relief=FLAT,font=("Courier", 9))

envs = envs_in_repo(repo.get())
print(envs)
for env in envs:
	env_list_tab2.insert(END,"      "+env)

## <--scrollbar-->	
scroll = Scrollbar(canvas_tab2,orient=VERTICAL,command=env_list_tab2.yview)
scroll.pack(side=LEFT,fill=Y)
env_list_tab2['yscrollcommand'] = scroll.set

## <--functions for buttons-->	
def open_env(): 
	env_name = get_env_name_from_selection_tab2()
	filename = filedialog.askopenfilename(initialdir = os.path.join(REPOS,repo.get(),
		env_name),
		title = env_name, filetypes = (("Yml files","*.yml*"),("all files","*.*"))) 
	if not filename == '':
		webbrowser.open('file://' + os.path.realpath(filename))

def delete_backup_env():
	env_name = get_env_name_from_selection_tab2()
	answer = askquestion ("You sure about that?",
		"\""+env_name+"\" will be permanently removed from your local and remote backups, are you sure you want to remove it?",
		icon = 'warning')
	
	if answer=="yes":
		update_github(env_name,repo.get(),"remove env backup")
		showinfo(title="Removed!", message="\""+env_name+"\" is removed from your local and remote backup.")
		env_list_tab2.delete(env_list_tab2.curselection())	

## <--buttons-->	
open_ = Button(canvas_tab2, text="Open",command=open_env,relief=FLAT,padx=20,pady=10,fg='blue',bd=2)
open_.pack(side=TOP,pady=90)
open_['font']=font.Font(size=15)

delete_env = Button(canvas_tab2, text="Delete env", 
	command=delete_backup_env,relief=FLAT,padx=20,pady=10,fg='blue',bd=2)
delete_env.pack(side=TOP,pady=10)
delete_env['font']=font.Font(size=15)

#<----------------enable tab1 & tab2's buttons------------------>
def check_file():
	print('checking file')
	if os.path.exists("url.txt"):
		with open("url.txt",'r') as f:
			url.set(f.readline())
		repo.set(get_repo_name_from_url(url.get()))
		note.tab(2, state="normal")

		##<---enable tab1 buttons--->
		check ["state"] = "normal"
		backup["state"] = "normal"
		delete["state"] = "normal"

	else:
		root.after(1, check_file)

root.after(1, check_file)

#<----------------About Page------------------>

## <--canvas3-->	
canvas_tab3 = Canvas(about,bg='#398FFF')
canvas_tab3.pack(expand=True,fill=BOTH)

with open("LICENSE.txt") as f:
    LICENSE = f.read()
license = Label(canvas_tab3,text = LICENSE)
license.place(relx=.5, rely=.5, anchor="center")

if __name__ == "__main__":
	root.mainloop()
