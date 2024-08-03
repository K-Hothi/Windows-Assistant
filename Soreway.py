import shutil
import os
import re
import time
from tkinter import *
import tkinter as tk
from tkinter.filedialog import askdirectory
import csv
import os.path
import hashlib
from pathlib import Path
import subprocess


xpad = 50
ypad = 50
bbg = '#DEFCF9'    
menu = Tk()
menu.title("Main Menu")
menu.configure(background='#C3BEF0', highlightbackground="Grey", highlightthickness=4)
menu.iconbitmap('KH_LOGO.ico')


s = 1
e = 5
listbox_tk = None
scrollbar1 = None
#----------------------------------------find file------------------------------------------------------------------------
def find_file():
    global lod1
    findbg = '#a4ccf9'
    findbg2 = '#a4d5f9'
    
    def Back_():
        find_top.destroy()
        menu.deiconify()
           
    
    menu.withdraw()
    find_top = Toplevel()
    find_top.geometry('740x250')
    find_top.configure(background=findbg, highlightbackground="Grey", highlightthickness=4)

  
    find_top.title('Find file, Please allow a few moments to find files')
    btton = Button(find_top, text='back', command=lambda: Back_(), font= ("Courier", 8))
    btton.pack(side=TOP, anchor=NW, )
    btton.configure(width=8, height=1, background = bbg)


        
    def Find_File(file):
        global listbox_tk
        global scrollbar1
        global lod1

        try:
            listbox_tk.destroy()
            scrollbar1.destroy()
        except:
            pass
        lod1 = Label(find_top, text='Searching...', font= ("Courier", 10), background=findbg)
        lod1.pack()
        
        nums = 1
        try:
            find_top.update()
        except:
            pass

        cmd = subprocess.Popen(f'where /r C: *{file}*', shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out,err = cmd.communicate()
        string = out.decode('utf-8')
        spl = string.split('\n')
        find_top.update()

        try:
            listbox_tk.destroy()
            scrollbar1.destroy()
        except:
            pass
        
        lod1.destroy()  
        scrollbar1 = Scrollbar(find_top)
        scrollbar1.pack( side = RIGHT, fill = Y )
        listbox_tk = Listbox(find_top, yscrollcommand=scrollbar1.set, background=findbg2, font= ("Courier", 8))
     
        for x in spl:
            listbox_tk.insert(END, f'{nums})  {x}')
            nums += 1
        
        listbox_tk.pack(fill=BOTH, side = BOTTOM)
        scrollbar1.config(command=listbox_tk.yview)
        find_top.update()
     
        

           
            

 
    input1 = Entry(find_top, width=28, font=('Helvetica 14 bold'))
    input1.pack()
    button_entry = tk.Button(find_top, text='Enter', command=lambda: Find_File(input1.get()))
    button_entry.pack(pady=4)
    button_entry.configure(width=24)
    find_top.mainloop()

 
 
    

#-------------Dupe Files-----------------------------------------------------------------------
def dupe_check():

    menu.withdraw()
    find_top4 = Toplevel()
    find_top4.geometry('500x200')
    find_top4.configure(background='#a4c6f9', highlightbackground="Grey", highlightthickness=4)

    scrollbar1 = Scrollbar(find_top4)
    scrollbar1.pack( side = RIGHT, fill = Y )
    listbox_tk = Listbox(find_top4, yscrollcommand=scrollbar1.set, background='#b7d2fa')
    find_top4.title('Duplicate file checker, (This process may take a few minutes depending on directory size)')
   
    file_path = askdirectory(title='Choose where to check for duplicate files')
    loading1 = Label(find_top4, text='Loading...', background='#a4c6f9', font= ("Courier", 20))
    loading1.pack()
   
    find_top4.update()
    def walk_level(some_dir, level=3):
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]

    all_files = walk_level(file_path)
    unique_files = []
    delete_files = []
    n = 0
    for root, folders, files in all_files:
        
        n += 1
        for file in files:
            file_path = Path(root, file)
            try:
                Hash_file = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
            except:
                continue

            if Hash_file not in unique_files:
                unique_files.append(Hash_file)
            else:
                delete_files.append(file_path)
    
    loading1.destroy()
    find_top4.update()
    if len(delete_files) >= 1:
        find_top4.geometry('700x300')
        find_top4.update()
        i = 0
        nums = 1
        for x in delete_files:
            i += 1
            listbox_tk.insert(END, f'{nums})  {x}')
            nums += 1
        listbox_tk.pack(fill=BOTH)
        scrollbar1.config(command=listbox_tk.yview)    
        a1 = Button(find_top4, text='Delete files', command= lambda: del_or_not('y'))
        a1.pack(expand=True,side=tk.BOTTOM)
        a2 = Button(find_top4, text='Keep files', command= lambda: del_or_not('n'))
        a2.pack(expand=True,side=tk.BOTTOM)

        a1.configure(width=14, height=1, background = '#DEFCF9')
        a2.configure(width=14, height=1, background = '#DEFCF9')
    else:
        Label(find_top4, text='No duplicate files found', background='#a4c6f9', font= ("Courier", 18)).pack()
        find_top4.update()
        time.sleep(2)
        find_top4.withdraw()
        menu.deiconify()
        
        
    def del_or_not(dt):
        if dt == 'y':
            Label(find_top4, text='Removing duplicate files', background='#a4c6f9', font= ("Courier", 10)).pack()
            for files in delete_files:
                os.remove(files)
            find_top4.update()
            time.sleep(2)
            find_top4.withdraw()
            menu.deiconify()
            
            
        elif dt == 'n':
            
            Label(find_top4, text='Files not removed', background='#a4c6f9', font= ("Courier", 10)).pack()
            find_top4.update()
            find_top4.geometry('400x300')
            time.sleep(2)
            find_top4.withdraw()
            menu.deiconify()
            
        
    find_top4.mainloop()
 
#------    NEW USER   -------------------------------------------------------------------------------------------------------------------------------------------------------------------

def New():

    sort_file_location = askdirectory(title='Select where to place your sorting bin(Desktop)')
    os.mkdir(sort_file_location + '/Sort_Bin')
    full_bin_location = sort_file_location + '/Sort_Bin'
    each = os.listdir(sort_file_location + '/Sort_Bin')


    phototarget = askdirectory(title='Select directory for your photos 1/4') 
    exetarget = askdirectory(title='Select directory for your exe files 2/4') 
    musictarget = askdirectory(title='Select directory for your music 3/4')
    doctarget = askdirectory(title='Select directory for your documents 4/4')

    
    with open('user_info_main.csv', 'w') as file:
         csv_writer = csv.DictWriter(file, fieldnames=['Bin_Location', 'photo_location', 'exe_location', 'music_location', 'document_location'])
         csv_writer.writeheader()
         csv_writer.writerow({'Bin_Location': full_bin_location, 'photo_location': phototarget, 'exe_location': exetarget, 'music_location': musictarget, 'document_location': doctarget})
        
    sta = Label(menu, text='Please restart app to begin', font= ("Courier", 15))
    sta.pack()
    
   
#----------    SORTER BIN    --------------------------------------------------------------------------------------------------------------------------------------------------------------
counter = 0
def sorter():
    global counter
    counter = 0
    
    def check(file):
        if re.search('.jpg', file) or re.search('.tif', file) or re.search('.png', file) or re.search('.gif', file) or re.search('.jpeg', file) or re.search('.PNG', file):
            return 'photo'
        elif re.search('.exe', file) or re.search('.lnk', file) or re.search('.msi', file):
            return 'exe'
        elif re.search('.mp3', file) or re.search('.mp4', file):
            return 'music'
        elif re.search('.zip', file):
            return 'zip'
        elif re.search('.pdf', file) or re.search('.docx', file) or re.search('.doc', file) or re.search('.txt', file):
            return 'doc'
        elif re.search('.apk', file):
            return 'apk'
        else:
            return 'other'


    def sort():
        global counter

        with open('user_info_main.csv', 'r') as file:
        
            csv_reader = csv.DictReader(file)
            for line in csv_reader:
                sort_file_location = line['Bin_Location']
                phototarget = line['photo_location']
                exe_target = line['exe_location']
                music_target = line['music_location']
                doctarget = line['document_location']
                
        each = os.listdir(sort_file_location)
        
        for x in each:
            counter += 1
        
            if check(x) == 'photo':
                y = sort_file_location + '/' + x
                try:
                    shutil.move(y, phototarget)
                except:
                    continue
            elif check(x) == 'exe':
                y = sort_file_location + '/' + x
                try:
                    shutil.move(y, exe_target)
                except:
                    continue
            elif check(x) == 'music':
                y = sort_file_location + '/' + x
                try:
                    shutil.move(y, music_target)
                except:
                    continue
            elif check(x) == 'other':
                y = sort_file_location + '/' + x
                try:
                    shutil.move(y, doctarget)
                except:
                    continue
            elif check(x) == 'zip':
                y = sort_file_location + '/' + x
                try:
                    shutil.move(y, doctarget)
                except:
                    continue
            elif check(x) == 'doc':
                y = sort_file_location + '/' + x
                try:
                    shutil.move(y, doctarget)
                except:
                    continue
            elif check(x) == 'apk':
                y = sort_file_location + '/' + x
                try:
                    shutil.move(y, doctarget)
                except:
                    continue
            else:
                continue

     
    sort();
    sort_file_bg = '#CADEFC'   
    find_top2 = Toplevel()
    find_top2.title('Sorting Bin (Sort all files in your sorting bin!)')
    find_top2.geometry('400x100')
    find_top2.configure(background=sort_file_bg, highlightbackground="Grey", highlightthickness=3)
    
    Label(find_top2, text='Done!', background=sort_file_bg, font= ("Courier", 15)).pack()
    Label(find_top2, text=f'{counter} files sorted', background=sort_file_bg, font= ("Courier", 15)).pack()
    find_top2.update()
    time.sleep(3)
    find_top2.destroy()

    find_top2.mainloop()
 

    

#-----------    SORT ALL    --------------------------------------------------------------------------------------------------------------------------------------------------------------

def sort_all():
    counter_all = 0
    def test():
        print('')
    find_top3 = Toplevel()
    find_top3.title('Sort out an entire directory! Please allow a few minutes for larger directories to be sort')
    find_top3.geometry('400x100')
    find_top3.configure(background='#CADEFC', highlightbackground="Grey", highlightthickness=4)
    menu.withdraw()
    lab1 = Label(find_top3, text='Select which directory you would \n like to clean', font= ("Courier", 15), background='#CADEFC')
    lab1.pack()
    with open('user_info_main.csv', 'r') as file:
        
        csv_reader = csv.DictReader(file)
        for line in csv_reader:
            sort_file_location = line['Bin_Location']
            phototarget = line['photo_location']
            exe_target = line['exe_location']
            music_target = line['music_location']
            doctarget = line['document_location']
            
    dir_clear = askdirectory(title='Select which directory to clean')
    lab1.config(text='Please allow a few moments for the procces to finish', font= ("Courier", 15))
    
    for file in os.listdir(dir_clear):
        
        counter_all += 1
        if re.search('.jpg', file) or re.search('.tif', file) or re.search('.png', file) or re.search('.gif', file) or re.search('.jpeg', file) or re.search('.PNG', file):
            y = dir_clear + '/' + file
            try:
                shutil.move(y, phototarget)
            except:
                continue
        elif re.search('.exe', file) or re.search('.lnk', file) or re.search('.msi', file):
            y = dir_clear + '/' + file
            try:
                shutil.move(y, exe_target)
            except:
                continue
        elif re.search('.mp3', file) or re.search('.mp4', file):
            y = dir_clear + '/' + file
            try:
                shutil.move(y, music_target)
            except:
                continue
        elif re.search('.zip', file):
            y = dir_clear + '/' + file
            try:
                shutil.move(y, doctarget)
            except:
                continue
        elif re.search('.pdf', file) or re.search('.docx', file) or re.search('.doc', file) or re.search('.txt', file):
            y = dir_clear + '/' + file
            try:
                shutil.move(y, doctarget)
            except:
                continue
        elif re.search('.apk', file):
            y = dir_clear + '/' + file
            try:
                shutil.move(y, doctarget)
            except:
                continue
        else:
            continue
    
    Label(find_top3, text='Done!', font= ("Courier", 15), background='#CADEFC').pack()
    lab1.config(text=f'{counter_all} files sorted', font= ("Courier", 15), background='#CADEFC')
    find_top3.update()
    time.sleep(2)
    find_top3.withdraw()
    menu.deiconify()
    
    

    find_top3.mainloop()
        
    
   
# --------------------    settings   ----------------------------------------------------------------------------------------------------

def settings1():
    def Back_():
        find_top8.destroy()
        menu.deiconify()
        
    def c1():
        new1 = askdirectory(title='Select new location')
    
        with open('user_info_main.csv', 'w') as file:
             csv_writer = csv.DictWriter(file, fieldnames=['Bin_Location', 'photo_location', 'exe_location', 'music_location', 'document_location'])
             csv_writer.writeheader()
             csv_writer.writerow({'Bin_Location': str(new1), 'photo_location': phototarget, 'exe_location': exe_target, 'music_location': music_target, 'document_location': doctarget})
        r1.configure(text=f'Sorter Bin Location:    {new1}')

    def c2():
        
        new2 = askdirectory(title='Select new location')
    
        with open('user_info_main.csv', 'w') as file:
             csv_writer = csv.DictWriter(file, fieldnames=['Bin_Location', 'photo_location', 'exe_location', 'music_location', 'document_location'])
             csv_writer.writeheader()
             csv_writer.writerow({'Bin_Location': sort_file_location, 'photo_location': str(new2), 'exe_location': exe_target, 'music_location': music_target, 'document_location': doctarget})
        r2.configure(text=f'Photo Location:    {new2}')            

    def c3():
        new3 = askdirectory(title='Select new location')
    
        with open('user_info_main.csv', 'w') as file:
             csv_writer = csv.DictWriter(file, fieldnames=['Bin_Location', 'photo_location', 'exe_location', 'music_location', 'document_location'])
             csv_writer.writeheader()
             csv_writer.writerow({'Bin_Location': sort_file_location, 'photo_location': phototarget, 'exe_location': str(new3), 'music_location': music_target, 'document_location': doctarget})
        r3.configure(text=f'Exe Location:    {new3}')            

    def c4():
        new4 = askdirectory(title='Select new location')
    
        with open('user_info_main.csv', 'w') as file:
             csv_writer = csv.DictWriter(file, fieldnames=['Bin_Location', 'photo_location', 'exe_location', 'music_location', 'document_location'])
             csv_writer.writeheader()
             csv_writer.writerow({'Bin_Location': sort_file_location, 'photo_location': phototarget, 'exe_location': exe_target, 'music_location': str(new4), 'document_location': doctarget})
        r4.configure(text=f'Music Location:    {new4}')            

    def c5():
        new5 = askdirectory(title='Select new location')
    
        with open('user_info_main.csv', 'w') as file:
             csv_writer = csv.DictWriter(file, fieldnames=['Bin_Location', 'photo_location', 'exe_location', 'music_location', 'document_location'])
             csv_writer.writeheader()
             csv_writer.writerow({'Bin_Location': sort_file_location, 'photo_location': phototarget, 'exe_location': exe_target, 'music_location': music_target, 'document_location': str(new5)})
        r5.configure(text=f'Document Location:    {new5}')            

    with open('user_info_main.csv', 'r') as file:
        
        csv_reader = csv.DictReader(file)
        for line in csv_reader:
            sort_file_location = line['Bin_Location']
            phototarget = line['photo_location']
            exe_target = line['exe_location']
            music_target = line['music_location']
            doctarget = line['document_location']
            
    co = '#CADEFC'
    find_top8 = Toplevel()
    find_top8.title('Settings')
    find_top8.geometry('400x200')
    find_top8.configure(background= co, highlightbackground="Grey", highlightthickness=4)
    menu.withdraw()
    find_top8.update()
    Back_button = Button(find_top8, text='back', command=Back_)
    Back_button.grid(row=0, column=0, sticky=W)
    
    e1 = Button(find_top8, text='change', command=c1)
    e1.grid(column=0, row=1, padx=2)
    r1 = Label(find_top8, text=f'Sorter Bin Location:    {sort_file_location}', background= co)
    r1.grid(row=1, column=1, sticky=W)

    e2 = Button(find_top8, text='change', command=c2)
    e2.grid(column=0, row=3, padx=2)
    r2 = Label(find_top8, text=f'Photo Location:    {phototarget}', background= co)
    r2.grid(row=3, column=1, sticky=W)

    e3 = Button(find_top8, text='change', command=c3)
    e3.grid(column=0, row=5, padx=2)
    r3 = Label(find_top8, text=f'Exe Location:    {exe_target}', background= co)
    r3.grid(row=5, column=1, sticky=W)

    e4 = Button(find_top8, text='change', command=c4)
    e4.grid(column=0, row=7, padx=2)
    r4 = Label(find_top8, text=f'Music Location:    {music_target}', background= co)
    r4.grid(row=7, column=1, sticky=W)

    e5 = Button(find_top8, text='change', command=c5)
    e5.grid(column=0, row=8, padx=2)
    r5 = Label(find_top8, text=f'Document Location:    {doctarget}', background= co)
    r5.grid(row=8, column=1, sticky=W)




    
    find_top8.mainloop()

#------------ More -------------------------------------------------------------------------------------------------------------------------------------
def more1():

    def Back_():
        find_top_more.destroy()
        menu.deiconify()
        
    co = '#CADEFC'
    find_top_more = Toplevel()
    find_top_more.title('')
    find_top_more.geometry('310x100')
    find_top_more.configure(background= co, highlightbackground="Grey", highlightthickness=4)
    menu.withdraw()
    find_top_more.update()
    Back_button = Button(find_top_more, text='back', command=Back_)
    Back_button.grid(row=0, column=0, sticky=W)
    Label(find_top_more, text="More Coming Soon!", font= ("Courier", 18), background=co).grid(row=1, column=1)

#----------    ENGINE    ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#if os.path.exists('user_info_main.csv'):
size = os.path.getsize('user_info_main.csv')
if size > 0:
    w = 15
    h = 1
    bbg_blue = '#68A7AD'
    bg_border_back = 5
    
    button1=tk.Button(menu, text="Sort Directory", command=sort_all, bd=bg_border_back)
    button1.grid(row=1,column=0, padx=xpad, pady=ypad)
    button1.configure(width=w, height=h, background = bbg)

    button2=tk.Button(menu, text="Duplicate file check", command=dupe_check, bd=bg_border_back)
    button2.grid(row=1,column=1, padx=xpad, pady=ypad)
    button2.configure(width=w, height=h, background = bbg)

    button3=tk.Button(menu, text="Sort Bin", command=sorter, bd=bg_border_back)
    button3.grid(row=1,column=2, padx=xpad, pady=ypad)
    button3.configure(width=w, height=h, background = bbg)

    button4=tk.Button(menu, text="Find File", command=find_file, bd=bg_border_back)
    button4.grid(row=2,column=0, padx=xpad, pady=ypad)
    button4.configure(width=w, height=h, background = bbg)
    
    button5=tk.Button(menu, text="Settings", bd=bg_border_back, command=settings1)
    button5.grid(row=2,column=1, padx=xpad, pady=ypad)
    button5.configure(width=w, height=h, background = bbg)

    buttonm=tk.Button(menu, text="More", bd=bg_border_back, command=more1)
    buttonm.grid(row=2,column=2, padx=xpad, pady=ypad)
    buttonm.configure(width=w, height=h, background = bbg)
 
else:
    New()
menu.mainloop()
