import os
import pickle
from utils import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as font
from tkinter import Checkbutton,Canvas
from tkinter.messagebox import askyesno,askquestion,showinfo

if not os.path.exists('repos'):
	os.mkdir('repos')

if os.path.exists('saved_session.pickle'):
	pickle_in = open('saved_session.pickle',"rb")
	saved_session = pickle.load(pickle_in)
else:
	saved_session = {}
	update_session_file(saved_session)

root = Tk()

width_of_window = 650
height_of_window = 480

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width/2)-(width_of_window/2)
y = (screen_height/2)-(height_of_window/2)

root.geometry("%dx%d+%d+%d"%(width_of_window,height_of_window,x,y))

# <----------------functions------------------>
def init_repo():
	url_value = url.get()
	repo_name = init_local_repo(url_value)
	saved_session['repo_name'] = repo_name
	update_session_file(saved_session)

# <----------------Notebook------------------>
note = ttk.Notebook(root)

home = ttk.Frame(note)
tab1 = ttk.Frame(note)
tab2 = ttk.Frame(note)

note.add(home,text="Add Github url")
note.add(tab1, text = "Your envs")
note.add(tab2, text = "Envs on Github", state="disabled")
note.pack(expand = 1, fill = "both")


# <----------------Home------------------>
canvas_home = Canvas(home,bg='#398FFF')
canvas_home.pack(expand=True,fill=BOTH)

url = Entry(canvas_home,width=40)
url['font']=font.Font(size=15)

enter_url_button = Button(canvas_home, text="Enter Url",command=init_repo)
enter_url_button['font']=font.Font(size=15)

url.place(relx=0.5, rely=0.4, anchor=CENTER)
enter_url_button.place(relx=0.5, rely=0.5, anchor=CENTER)


# <----------------tab1------------------>

canvas_tab1 = Canvas(tab1,bg='#398FFF')
canvas_tab1.pack(expand=True,fill=BOTH)

envs = get_envs()
env_list = Listbox(canvas_tab1,width = 50,bg='#85144B',fg='white')
env_list.pack(side=LEFT,fill=Y)
env_list.config(border=2,relief=FLAT,font=("Courier", 9))
for env in envs:
	env_list.insert(END,"      "+env)
scroll = Scrollbar(canvas_tab1,orient=VERTICAL,command=env_list.yview)
scroll.pack(side=LEFT,fill=Y)

env_list['yscrollcommand'] = scroll.set

def show_info_backup(env_name,version):
	showinfo(title="Backedup successfully!", message=env_name+" backedup successfully to version"+version)

def get_env_name_from_selection():
	print('env_list.curselection()',env_list.curselection())
	item = list(map(int, env_list.curselection()))
	print('item',item)
	env_name = env_list.get(item)
	# env_name = env_list.get(ANCHOR)

	env_name = env_name.split(' ')[-1]
	print('env_name :: ',env_name)
	return env_name

def check_backup():
	print('saved_session["repo_name"]',saved_session['repo_name'])
	env_name = get_env_name_from_selection()
	path_to_env = os.path.join('repos',saved_session['repo_name'],env_name)
	if not os.path.exists(path_to_env):
		answer = askyesno('Not backedup',env_name+" is not backedup. Do u wish to backup?")
		if answer:
			version = save_env(env_name,saved_session['repo_name'],os.path.join('repos',saved_session['repo_name']))
			show_info_backup(env_name,version)
	else:
		backed_up = check_prev_backup(path_to_env,env_name)
		if backed_up:
			showinfo(title="Backedup!", message=env_name+"is backedup")
		else:
			answer = askyesno('Backedup outdated',env_name+" has changed since the last backup. Do u wish to backup again?")
			if answer:
				version = save_env(env_name,saved_session['repo_name'],os.path.join('repos',saved_session['repo_name']))
				show_info_backup(env_name,version)

def backup_env():
	env_name = get_env_name_from_selection()
	version = save_env(env_name,saved_session['repo_name'],os.path.join('repos',saved_session['repo_name']))
	show_info_backup(env_name,version)
	

def delete_env():
	env_name = get_env_name_from_selection()
	backed_up = check_prev_backup(path_to_env,env_name)
	if backed_up:
		remove_env(env_name)
		showinfo(title="Removed!", message=env_name+"is removed from ur local machine")
		env_list.delete(env_list.curselection())
	else:
		showwarning()
		answer = askquestion ("Env not backed up!!",env_name+"has not been backed up or has been modified afterwards, are you sure you want to remove it?",icon = 'warning')
		if answer=="yes":
			remove_env(env_name)
			showinfo(title="Removed!", message=env_name+"is removed from ur local machine")
			env_list.delete(env_list.curselection())


check = Button(canvas_tab1, text="Check if backedup",command=check_backup,relief=FLAT,padx=20,pady=10,fg='blue',bd=2)
check.pack(side=TOP,pady=90)
check['font']=font.Font(size=15)


backup = Button(canvas_tab1, text="Backup env", command=backup_env,relief=FLAT,padx=20,pady=10,fg='blue',bd=2)
backup.pack(side=TOP,pady=10)
backup['font']=font.Font(size=15)


delete = Button(canvas_tab1, text="Delete env", command=delete_env,relief=FLAT,padx=20,pady=10,fg='blue',bd=2)
delete.pack(side=TOP,pady=10)
delete['font']=font.Font(size=15)


# <----------------tab2------------------>
# if 'repo_name' in saved_session.keys():
# 	if not saved_session['repo_name'] == None:
# 		note.tab(0, state="normal")

# 		canvas = Canvas(tab2,bg='#398FFF')
# 		canvas.pack(expand=True,fill=BOTH)

# 		envs = envs_in_repo(saved_session['repo_name'])
# 		env_list = Listbox(canvas,width = 50,bg='#85144B',fg='white')
# 		env_list.pack(side=LEFT,fill=Y)
# 		env_list.config(border=2,relief=FLAT,font=("Courier", 9))
# 		for env in envs:
# 			env_list.insert(END,"      "+env)
# 		scroll = Scrollbar(canvas,orient=VERTICAL,command=env_list.yview)
# 		scroll.pack(side=LEFT,fill=Y)

# 		env_list['yscrollcommand'] = scroll.set




if __name__ == "__main__":
	root.mainloop()






# canvas = Canvas(tab1 ,bg='green')#, width=200, height=400
# scroll = Scrollbar(tab1, command=canvas.yview)
# canvas.config(yscrollcommand=scroll.set, scrollregion=(0,0,100,1000))
# canvas.pack(side=LEFT, fill=BOTH, expand=True)
# scroll.pack(side=RIGHT, fill=Y)

# frame = Frame(canvas, bg='red')
# canvas.create_window(90, 450, window=frame)

# frame2 = Frame(canvas,bg="red")
# canvas.create_window(2000, 550, window=frame2)