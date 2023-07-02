from tkinter import *
import іnterpolation as interpol
from tkinter import messagebox
from tkinter import scrolledtext

from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter.filedialog import *

class Application:
    def __init__(self):
        self.root = Tk()
        self.root.title("Interpolation")
        self.root.geometry("800x600+200+100")
        self.root.resizable(FALSE, FALSE)
        
        self.x = []
        self.y = []
        self.points = 0
        self.f = False
        
        #createInputData
        self.inputData = LabelFrame(self.root, text="Input dada:", width=340, height=210, font="Colibri 11")
        self.labX = Label(self.inputData, text="X = ")
        self.labX.place(x=20,y=8)
        self.entX = Entry(self.inputData, width=8)
        self.entX.place(x=60,y=8)
        self.labY = Label(self.inputData, text="Y = ")
        self.labY.place(x=20,y=40)
        self.entY = Entry(self.inputData, width=8)
        self.entY.place(x=60,y=40)
        
        self.textData = scrolledtext.ScrolledText(self.inputData,width=22,height=10)
        self.textData.place(x=145, y=8)
        self.btnData = Button(self.inputData,text="Додати", width=8, command= self.addPoints)
        self.btnData.place(x=15,y=80)
        self.btnData = Button(self.inputData,text="Очистити", width=8, command=self.clearPoints)
        self.btnData.place(x=15,y=108)
        
        # createInputMethod
        self.inputMethod = LabelFrame(self.root, text="Input method:", width=340, height=160, font="Colibri 11")
        self.lab_xpoint = Label(self.inputMethod,text="X value for interpolation: ", font="Colibri 10")
        self.lab_xpoint.place(x=8,y=10)
        self.entX_point = Entry(self.inputMethod, width=8)
        self.entX_point.place(x=160,y=10)
        
        self.lab_res = Label(self.inputMethod,text='Result', font = 'Colibri 11', fg='blue')
        self.lab_res.place(x=200,y=60)
        
        self.method = IntVar()
        self.rbLinear = Radiobutton(self.inputMethod,text="Лінійна інтерполяція", variable=self.method, value=1, font="Colibri 10")
        self.rbLinear.place(x=20, y=40)
        self.rbCubic = Radiobutton(self.inputMethod,text="Кубічна інтерполяція", variable=self.method, value=2, font="Colibri 10")
        self.rbCubic.place(x=20, y=70)
        
        # buttons
        self.btnIntpol = Button(self.inputMethod,text="INTERPOLATE",state='disabled', command=self.work)
        self.btnIntpol.place(x=8, y=104)
        self.btn_Stat = Button(self.inputMethod, text="Статистика", state='disabled', command=self.stat)
        self.btn_Stat.place(x=188,y=104)
        
        
        # createFigure
        self.createFigure = LabelFrame(self.root, text='Побудова графіка:', width=360, height=400)
        self.fig = Figure(figsize=(4,3), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.createFigure)
        self.canvas.get_tk_widget().pack(fill=NONE)
        self.gr = self.fig.add_subplot(1,1,1)
        toolbar = NavigationToolbar2Tk(self.canvas, self.createFigure)
        toolbar.update()
        
        #createSplines
        self.createSplines = LabelFrame(self.root, text = 'Splines:', width=764, height=200, font="Colibri 11")
        self.textPolinoms = scrolledtext.ScrolledText(self.createSplines,width=78,height=10, state='disabled')
        self.textPolinoms.place(x=8, y=8)
        self.btn_Save = Button(self.createSplines, text="Зберегти", state='disabled', command=self.save_file, width=8, height=8)
        self.btn_Save.place(x=600,y=8)
        
        
    def show_widgets(self):
        self.inputData.place(x=10,y=10)
        self.inputMethod.place(x=10, y=220)
        self.createFigure.place(x=370,y=8)
        self.createSplines.place(x=10,y=380)
        
        
    def addPoints(self):
        try:
            x_i = float(self.entX.get())
            self.entX.delete(0,END)
            self.entX.focus_set()
            y_i = float(self.entY.get())
            self.entY.delete(0,END)
            if x_i in self.x:
                pos = self.x.index(x_i)
                answer = messagebox.askyesno(title ="Попередження", message="Значення X=" + str(x_i) +" вже додано.\nЗамінити!?")
                if answer:
                    self.x[pos] = x_i
                    self.y[pos] = y_i
            else:
                self.x.append(x_i)
                self.y.append(y_i)
            self.points = len(self.x)
            self.textData.delete(1.0,END)
            for i in range(self.points):
                self.lineXY = "x = " + str(self.x[i]) + "\ty= " + str(self.y[i]) + "\n"
                self.textData.insert(END, self.lineXY)
            if self.points>=2: self.btnIntpol['state'] = 'normal'
        except ValueError:
            messagebox.showerror(title="Помилка", message="Введіть коректні дані")
            self.entX.focus_set()
    
    # впорядковуємо на випадок якщо Х вводились не за зростанням        
    def sort_xy(self):
        dic = dict(zip(self.x, self.y))
        key = sorted(dic.keys())
        new_dic = dict()
        for i in key:
            new_dic[i] = dic[i]
        self.x = list(new_dic.keys())
        self.y = list(new_dic.values())
    
    def clearPoints(self):
        self.textData.delete(1.0, END)
        self.x.clear()
        self.y.clear()
        self.lab_res['text'] = 'Result'
        self.method.set(0)
        self.btn_Stat['state'] = 'disabled'
        self.btn_Save['state'] = 'disabled'
        self.btnIntpol['state'] = 'disabled'
        self.textPolinoms.configure(state='normal')
        self.textPolinoms.delete(1.0,END)
        self.textPolinoms.configure(state='disabled')
        print(self.x,self.y)
        self.gr.clear()
        self.fig.suptitle('')
        self.canvas.draw()
        
    def work_linear(self):
        try:
            self.btn_Stat['state'] = 'normal'
            self.btn_Save['state'] = 'normal'
            self.lin_interp = interpol.LinearInterpolation(self.x, self.y)
            self.x_point = float(self.entX_point.get())
            
            if self.x_point<min(self.x) or self.x_point>max(self.x):
                raise Exception("Х має бути в межах від "+str(min(self.x))+" до "+str(max(self.x)))
            
            self.entX_point.delete(0, END)
            self.y_result = self.lin_interp.interpolate(self.x_point)
            #print(self.x,self.y)
            self.lab_res.config(text=" x = {} is {}".format(self.x_point, round(self.y_result,2)))
            
            # будуємо графік
            self.createGrafic(self.lin_interp, 'Лінійна інтерполяція')
            
            # формуємо поліноми
            self.polinoms = self.lin_interp.print_polynomial()
            self.textPolinoms.configure(state='normal')
            self.textPolinoms.delete(1.0,END)
            self.textPolinoms.insert(END, self.polinoms)
            self.textPolinoms.configure(state='disabled')
            
        except ValueError:
            messagebox.showerror(title="Помилка", message="Некоректне значення X")
            self.entX_point.focus_set()
        except Exception as e:
            messagebox.showerror(title="Помилка", message="Некоректне значення X\n"+str(e))
            self.entX_point.focus_set()
   
   
    def work_cubicSpline(self):
        try:
            self.btn_Stat['state'] = 'normal'
            self.btn_Save['state'] = 'normal'
            self.spline = interpol.CubicSpline()
            self.spline.build_spline(self.x,self.y)
            self.x_point = float(self.entX_point.get())
            if self.x_point<min(self.x) or self.x_point>max(self.x):
                raise Exception("Х має бути в межах від "+str(min(self.x))+" до "+str(max(self.x)))
            self.entX_point.delete(0, END)
            self.y_result = self.spline.interpolate(self.x_point)
            self.lab_res.config(text=" x = {} is {}".format(self.x_point, round(self.y_result,2)))
            
            # будуємо графік
            self.createGrafic(self.spline, 'Кубічна інтерполяція')
            
            # формуємо поліном
            self.polinoms = self.spline.print_polynomial()
            self.textPolinoms.configure(state='normal')
            self.textPolinoms.delete(1.0,END)
            self.textPolinoms.insert(END, self.polinoms)
            self.textPolinoms.configure(state='disabled')
            
        except ValueError:    
            messagebox.showerror(title="Помилка", message="Введіть значення X")
            self.entX_point.focus_set()
        except Exception as e:
            messagebox.showerror(title="Помилка", message="Некоректне значення X\n"+str(e))
            self.entX_point.focus_set()
            
    def createGrafic(self, method, title):
        x_sp = np.arange(min(self.x),max(self.x)+0.1,0.1)
        y_sp = []
        for i in x_sp:
            yx = method.interpolate(i)
            y_sp.append(yx)
            
    # побудова графіка
        self.gr.clear()
        self.gr.plot(self.x_point, self.y_result,'o')
        self.gr.plot(self.x,self.y,'o',x_sp,y_sp,'-')
        self.gr.grid()
        self.fig.suptitle(title)
        self.canvas.draw()
    
    
    def work(self):
        self.sort_xy()
        if self.method.get() == 1:
            self.work_linear() 
        elif self.method.get() == 2:
            self.work_cubicSpline()
        else:
            messagebox.showerror(title="Помилка", message="Оберіть метод інтерполяції!")
            
    def stat(self):
        line_stat = ''
        if self.method.get() == 1:
            line_stat = 'Інтерполяція: лінійна\nІтерацій: {0:}\nОперацій: {1:}\nЧас: {2:.4f} ms'.format(self.lin_interp.iterations,self.lin_interp.operations,round(self.lin_interp.execution_time,4))
        elif self.method.get() == 2:
            line_stat = 'Інтерполяція: кубічна\nІтерацій: {0:}\nОперацій: {1:}\nЧас: {2:.4f} ms'.format(self.spline.iterations,self.spline.operations,round(self.spline.execution_time,4))
        messagebox.showinfo('Статистика', line_stat)
    
    def save_file(self):
        ask_save = asksaveasfilename()
        polinoms = self.textPolinoms.get(1.0, END)
        f = open(ask_save, "w")
        f.write(polinoms)
        f.close()
    
        
    def run(self):
        self.show_widgets()
        self.root.mainloop()
  

