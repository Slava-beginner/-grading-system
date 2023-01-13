from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv
import math



root = Tk()
# рейтинг -  оценка от 1 до 5, выставляется среднее арифметическое

familia = ''
review = ''
entry_rating = ''
entry_comment = ''
current_review = ''

trees = Frame(bd=1,width=650,height=600,padx=50)

trees.place(x=0,y=27)
tree = ''
def getRatingForTree(s):
    s = s.rstrip()
    obj = {
    '☆':0.5,
    '★':1,
    '★ ☆':1.5,
    '★ ★':2,
    '★ ★ ☆':2.5,
    '★ ★ ★':3,
    '★ ★ ★ ☆':3.5,
    '★ ★ ★ ★':4,
    "★ ★ ★ ★ ☆":4.5,
    "★ ★ ★ ★ ★":5
    }
    return obj[s]
def getRating(count):
    obj = {
    0.5:'☆',
    1:'★',
    1.5:'★ ☆',
    2:'★ ★',
    2.5:'★ ★ ☆',
    3:'★ ★ ★',
    3.5:'★ ★ ★ ☆',
    4:'★ ★ ★ ★',
    4.5:"★ ★ ★ ★ ☆",
    5:"★ ★ ★ ★ ★"

    }
    return obj[count]
def getData():
    if db.data != []:
        return [i[0] for i in db.data]
    return ['']
class DB:
    def __init__(self):
        self.data = self.getData()
        self.reviews = self.getReviews()
    
    def updateData(self):
        try:
            newArr = [["Преподователь","Кол-во отзывов","Рейтинг","Звёзды"]] + self.data
            newArr2 = self.reviews
            with open('db.csv',mode="w",encoding="utf-8") as F:
                r = csv.writer(F,lineterminator="\r")
                r.writerows(newArr)
            with open('reviews.csv',mode="w",encoding="utf-8") as F:
                r = csv.writer(F,lineterminator="\r")
                r.writerows(newArr2)
            self.data = self.getData()
            self.reviews = self.getReviews()
            disable_tree()
            makeTree()
            return

        except:
            print('Error')
            return
        
    
    def getPerson(self,fam):

        for i in range(len(self.reviews)):
            if fam in self.reviews[i][0]:
                return self.reviews[i][1:]
        return False
    def getReviews(self):
        r = csv.reader(open('reviews.csv',mode="r",encoding="utf-8"))
        arr = [i for i in list(r) if i != []]
        return arr
    def getData(self):
        r = csv.reader(open('db.csv',mode="r",encoding="utf-8"))
        arr = []
        for i in list(r)[1:]:
            if i != []:
                if '.' in i[2]:
                    i[2] = float(i[2])
                else:
                    i[2] = int(i[2])
                arr.append(i)
        print(arr,'getData')
        return arr
     
    
    
 
db = DB()



def btn_add_person():
    global familia,entry_rating,entry_comment
    newRoot = Tk()
    newRoot.title('Добавить')
    newRoot.geometry('400x250+400+300')
    newRoot.resizable(False, False)
    
   

    title = Label(newRoot,text='Добавить отзыв',bg='#d5d5d5',font=20)
    title.place(x=85, y=10)
  

   
    label_familia = Label(newRoot,text='Выберите ФИО преподавателя\nМожно добваить нового')
    label_familia.config(justify=LEFT)
    label_familia.place(x=25,y=50)



    label_rating= Label(newRoot, text='Оцените работу\nПреподователя от 1 до 5',justify=LEFT)
    label_rating.place(x=35, y=100)
        
    label_comment  = Label(newRoot, text='Напишите небольшой\nкомментарий\n\nЭто необязательно')
    label_comment.place(x=10, y=150)

    familia = ttk.Combobox(newRoot,values=getData())
    familia.current(0)
    familia.place(x=200,y=50)
    


    entry_rating = ttk.Combobox(newRoot, values=[u'1', u'2',u'3',u'4',u'5'])
    entry_rating.current(0)
    entry_rating.place(x=200, y=110,width=40)
    
    entry_comment  = Text(newRoot)
    entry_comment.place(x=200, y=150,height=55,width=150)

    btn_cancel = Button(newRoot, text='Закрыть', command=newRoot.destroy)
    btn_cancel.place(x=300, y=210)

    def add_person():
        global familia,entry_rating,entry_comment
        fam = familia.get()
        rat = float(entry_rating.get())
        comm = entry_comment.get("1.0",END)
        if rat < 1 or rat > 5:
            newRoot.destroy()
            return messagebox.showinfo(message='Неправильно выбрали рейтинг')
        if fam == '' or fam == ' '  or len(fam.split()) == 1 or len(fam.split()[1]) != 2:
            newRoot.destroy()
            return messagebox.showinfo(message='Неверно указали фамилию или инициалы')
        
        if any(i for i in db.data  if fam in i[0]):
            prepod = [i for i in db.data if fam in i[0]][0]
            print(prepod,'prepod')
            ind = [db.data.index(i) for i in db.data if fam in i[0]][0]
            count = str(int(prepod[1]) + 1)
            print(rat,'rating')
            print(prepod[2],'current')
            print(prepod[2]+rat,'newRate')
            newRate =  prepod[2]+rat
            print(newRate)
            if newRate % int(count) == 0:
                t = float(newRate/int(count))
            elif newRate % int(count) <= 5:
                t = float(str(int(newRate//int(count)))+'.5')
            elif newRate % int(count) > 5:
                t = float(round(newRate/int(count)))
           
            if t > 5:
                t = 5
            elif t < 0.5:
                t = 0.5
            prepod[1] = count
            prepod[2] = newRate
            prepod[3] = getRating(t)
            db.data[ind] = prepod
            if comm != ' ' and comm != '' and comm.split() != []:
                ind2 = [db.reviews.index(i) for i in db.reviews if prepod[0] in i[0]][0]
                db.reviews[ind2].append(comm)
          
        else:
            prep = [fam,'1',rat,getRating(rat)]
            db.data.append(prep)
            db.reviews.append([fam,comm])
        db.updateData()
        newRoot.destroy()
        
    btn_ok = Button(newRoot, text='Добавить',command=add_person)
    btn_ok.place(x=220, y=210)

    newRoot.focus_set()


def reset_person():
    global familia
    familia.delete(0,END)
    familia.config(state=NORMAL)



def prev_preview():
    global review,familia
    
    arr = [i for i in db.reviews if familia.get() in i][0]
    s = review.get("1.0",END).replace('\n','')
    review.config(state=NORMAL)
    if s == arr[1]:
        review.replace("1.0", END,arr[-1])
    else:
        review.delete("1.0",END)
        review.replace("1.0",END, arr[arr.index(s)-1])
    review.config(state=DISABLED)

def  next_review():
    global review,familia
    arr = [i for i in db.reviews if familia.get() in i[0]][0]
    
    s = review.get("1.0",END).replace('\n','')
    review.config(state=NORMAL)
    if s == arr[-1]:
        review.replace("1.0", END,arr[1])
    else:
        review.delete("1.0",END)
        review.replace("1.0",END, arr[arr.index(s)+1])

    review.config(state=DISABLED)
    
def btn_search_person():
    global familia

    newRoot = Tk()
    newRoot.title('Поиск')
    newRoot.geometry('400x220+400+300')
    newRoot.resizable(False, False)
    
   

    title = Label(newRoot,text='Поиск преподавателя',bg='#d5d5d5',font=20)
    title.place(x=85, y=10)

    label_familia = Label(newRoot,text='Выберите ФИО преподавателя')
    label_familia.place(x=25,y=50)

   
    familia = ttk.Combobox(newRoot,values=getData())
    familia.current(0)
    familia.place(x=200,y=50)
    
   

    def find_person():
        global familia,review

    
        value = familia.get()
        if value == '' or value == ' ':
            newRoot.destroy()
            return messagebox.showerror(message='Неверно указана Фамилия')
        r = db.getPerson(value)
        if type(r) == bool:
            newRoot.destroy()
            return messagebox.showerror(message='Такого преподавателя нет в базе')
        if len(r) == 0:
             newRoot.destroy()
             return messagebox.showinfo(message='К сожалению, пока нет отзывов на этого преподавателя')
        familia.config(state=DISABLED)
        review = Text(newRoot)
        
        review.insert("1.0",r[0])
        review.config(state=DISABLED,wrap='word')
        review.place(x=135,y=80,width=170,height=80)  


        messagebox.showinfo(message='Кол-во отзывов на этого преподавателя ' + str(len(r)))
        newRoot.focus_set()
        if len(r) > 1:
            btn_next = Button(newRoot, text='Следующий',command=next_review)
            btn_next.place(x=315, y=120)
            btn_prev = Button(newRoot, text='Предыдущий',command=prev_preview)
            btn_prev.place(x=40, y=120)
        
           
       
           


    btn_cancel = Button(newRoot, text='Закрыть', command=newRoot.destroy)
    btn_cancel.place(x=300, y=170)

    btn_ok = Button(newRoot, text='Поиск',command=find_person,width=10)
    btn_ok.place(x=210, y=170)
    
    btn_reset = Button(newRoot, text='Сброс',command=reset_person)
    btn_reset.place(x=350, y=45)
    newRoot.focus_set()


def btn_edit_person():
    global familia
    newRoot = Tk()
    newRoot.title('Редактировать данные')
    newRoot.geometry('500x280+350+300')
    newRoot.resizable(False, False)

    title = Label(newRoot,text='Редактировать данные',bg='#d5d5d5',font=20)
    title.place(x=85, y=10)

    label_familia = Label(newRoot,text='Выберите ФИО преподавателя')
    label_familia.place(x=25,y=50)
    
            
    def find_person():
        global familia,review

    
        value = familia.get()
        if value == '' or value == ' ':
            newRoot.destroy()
            return messagebox.showerror(message='Неверно указана Фамилия')
        r = db.getPerson(value)
        if type(r) == bool:
            newRoot.destroy()
            return messagebox.showerror(message='Такого преподавателя нет в базе')
        familia.config(state=DISABLED)
        review = Text(newRoot)
        
        review.insert("1.0",r[0])
        review.config(state=DISABLED,wrap='word')
        review.place(x=135,y=120,width=240,height=80)  
        
        def delete_person():
            global familia
            v = familia.get()
            m = messagebox.askyesno(title='Подтверждение операции',message ='Вы уверены?')
            if m:
                for k in db.data:
                    if v in k[0]:
                        db.data.remove(k)
                        break
                for k in db.reviews:
                    if v in k[0]:
                        db.reviews.remove(k)
                        break
                db.updateData()
                newRoot.destroy()
                return messagebox.showinfo(message='Успешно удалён из базы')
            return messagebox.showinfo(message='Отмена удаления')

        def delete_review():
            global review
            v = review.get("1.0",END).replace('\n','')
            
            m = messagebox.askyesno(title='Подтверждение операции',message ='Вы уверены?')
            if m:

                for k in db.reviews:
                    if v in k:
                        k.remove(v)
                        break
                db.updateData()
                newRoot.destroy()
                return messagebox.showinfo(message='Отзыв успешно удалён')

            return messagebox.showinfo(message='Отмена удаления')


        btn_delete_person = Button(newRoot,text='Удалить преподавателя',command=delete_person,bg='white')
        btn_delete_person.place(x=185,y=85)

        btn_edit_review = Button(newRoot,text='Редактировать отзыв',command=edit_review,bg='white')
        btn_edit_review.place(x=70,y=210)

        btn_save_review= Button(newRoot,text='Сохранить',command=save_review,bg='white')
        btn_save_review.place(x=70,y=240)

        if len(r) >= 1:
            btn_delete_review = Button(newRoot,text='Удалить отзыв',command=delete_review,bg='white')
            btn_delete_review.place(x=220,y=210)

        messagebox.showinfo(message='Кол-во отзывов на этого преподователя ' + str(len(r)))
        newRoot.focus_set()
        if len(r) > 1:
            btn_next = Button(newRoot, text='Следующий',command=next_review)
            btn_next.place(x=390, y=145)
            btn_prev = Button(newRoot, text='Предыдущий',command=prev_preview)
            btn_prev.place(x=35, y=145)   

       
    
    
   

   

    familia = ttk.Combobox(newRoot,values=getData())
    familia.current(0)
    familia.place(x=200,y=50)
    

    btn_cancel = Button(newRoot, text='Закрыть', command=newRoot.destroy)
    btn_cancel.place(x=400, y=250)
    
    btn_ok = Button(newRoot, text='Поиск',command=find_person,width=10)
    btn_ok.place(x=300, y=250)
    
    btn_reset = Button(newRoot, text='Сброс',command=reset_person)
    btn_reset.place(x=350, y=45)
    newRoot.focus_set()

def save_review():
    global review
    r = review.get("1.0",END).replace('\n','')
    if r == current_review or current_review == '':
        messagebox.showinfo(message='Нужно внести изменения в отзыв')
        return
    for i in db.reviews:
        if current_review in i:
            i[i.index(current_review)] = r
    review.config(state=DISABLED)
    db.updateData()
    messagebox.showinfo(message='Новый отзыв сохранён')

def edit_review():
    global review,current_review
    r = review.get("1.0",END).replace('\n','')
    current_review = r
    review.config(state=NORMAL)
    review.focus_set()
 

def btn_delete_all():
    m = messagebox.askyesno(message='Вы уверены?',title='Подтверждение действия')
    if m:
        db.data = []
        db.reviews = []
        db.updateData()
        disable_tree()
        makeTree()
        return messagebox.showinfo(message='База очищена')
     
    return messagebox.showinfo(message='Отмена операции')

def makeTree():
    global tree
    tree = ttk.Treeview(trees, columns=('init','count','rating','stars'), height=20,show='headings')
    elems = []
    for i in db.data:
        elems.append(i.copy())
    for k in elems:
        k[2] = getRatingForTree(k[-1])
        elems[elems.index(k)] = k
    arr = sorted(elems,key=lambda x: x[2])
    arr = list(reversed(arr))
    for i in range(len(arr)):
        elem = arr[i]
        tree.insert('', END,values=elem)
     
     
 

    tree.column('init', width=150, anchor=CENTER)
    tree.heading('init', text='Преподаватели')

    tree.column('count', width=125, anchor=CENTER)
    tree.heading('count', text='Кол-во отзывов')

    tree.column('rating',width=100,anchor=CENTER)
    tree.heading('rating', text='Рейтинг')

    tree.column('stars',width=110,anchor=CENTER)
    tree.heading('stars', text='Звёзды')

    tree.pack()
def disable_tree():
   global tree
   return tree.destroy()



def Main():
    global tree
    toolbar = Frame(bg='#d7d8e0', bd=2)
    toolbar.pack(side=TOP, fill=X)

    
    
    root.title("Система оценки качества преподователей")
    root.geometry("600x450+300+200")
   
    btn_add = Button(toolbar, text='Добавить отзыв', width=20,command=btn_add_person, bg='yellow',bd=1,compound=TOP)
    btn_search = Button(toolbar, text='Найти преподователя',width=20, command=btn_search_person, bg='yellow',bd=1,compound=TOP)
    btn_correct = Button(toolbar, text='Редактировать данные',width=20, command=btn_edit_person, bg='yellow',bd=1,compound=TOP)
    btn_delete = Button(toolbar, text='Очистить базу',width=20, command=btn_delete_all, bg='yellow',bd=1,compound=TOP)
    btn_add.pack(side=LEFT)
    btn_search.pack(side=LEFT)
    btn_correct.pack(side=LEFT)
    btn_delete.pack(side=LEFT)
    makeTree() 

def start():
    Main()
    root.mainloop()

start()
    