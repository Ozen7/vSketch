from tkinter import *
import math
class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    SCREEN_W=800
    SCREEN_H=800


    def __init__(self):    
        self.master = Tk()    

        self.line_button = Button(self.master, text='Line',command=self.set_tool_line)
        self.line_button.grid(row=1,column=0)

        self.circle_button = Button(self.master, text='Circle',command= self.set_tool_circle)
        self.circle_button.grid(row=1,column=1)

        self.point_button = Button(self.master, text='Point',command = self.set_tool_point)
        self.point_button.grid(row=1,column=2)

        self.point_button = Button(self.master, text='Freehand',command = self.set_tool_freehand)
        self.point_button.grid(row=1,column=3)

        self.point_button = Button(self.master, text ='Text', command = self.set_tool_text)
        self.point_button.grid(row=1,column=4)

        self.draw_zone = Canvas(self.master,height=400,width=400,bg='white')
        
        self.draw_zone.grid(row=5,columnspan=5)
        

        self.menubar = Menu(self.master)
        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menu1.add_separator()
        self.menu1.add_command(label="Quit", command=self.master.destroy)
        self.menubar.add_cascade(label="Settings", menu=self.menu1)
        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="Undo", command=self.undo )

        self.menu2.add_command(label="Redo", command=self.alert)
        self.menubar.add_cascade(label="Editor", menu=self.menu2)

        self.master.config(menu=self.menubar)
        self.master.title('UI')

        self.setup()
        self.master.mainloop()    

    def setup(self):
        self.line_start_x = None
        self.line_start_y = None

        self.circle_start_x = None
        self.circle_start_y = None

        self.text_start_x = None
        self.text_start_y = None

        self.tool_option = 'line'

        self.Line_objects = []
        self.Point_objects = []
        self.stack = []    
        self.px = 0
        self.py = 0
        self.draw_zone.focus_set()
        self.recentText = None


        self.draw_zone.bind('<Button-1>', self.draw_start)
        self.draw_zone.bind('<B1-Motion>',self.draw_motion)
        self.draw_zone.bind('<ButtonRelease-1>',self.draw_end)
        self.draw_zone.bind("<Key>", self.change_text)

        self.mode = ''
        
    
    def keyFun(self, event):
        print("h")
        print(event)


    def line_start(self,event):
        self.line_start_x=event.x
        self.line_start_y=event.y
    def line_motion(self,event):
        self.draw_zone.delete('temp_line_objects')
        self.draw_zone.create_line(self.line_start_x,self.line_start_y,event.x,event.y,fill=self.DEFAULT_COLOR,smooth=1,tags='temp_line_objects')
    def line_end(self,event):
        self.draw_zone.delete('temp_line_objects')
        x=self.draw_zone.create_line(self.line_start_x,self.line_start_y,event.x,event.y,fill=self.DEFAULT_COLOR,smooth=1)
        self.Line_objects.append(x)
        self.stack.append(x)


    def circle_start(self,event):
        self.circle_start_x = event.x
        self.circle_start_y = event.y
    def circle_motion(self,event):
        self.draw_zone.delete('temp_circle_objects')   #sym de circle_end par rapport a circle_start
        #self.draw_zone.create_oval(event.x,event.y,(2*self.circle_start_x-event.x),(2*self.circle_start_y-event.y),tags='temp_circle_objects')
        self.draw_zone.create_oval((self.circle_start_x),(self.circle_start_y),event.x,event.y,fill=None,tags='temp_circle_objects')
    def circle_end(self,event):
        self.draw_zone.delete('temp_circle_objects') 
        #x=self.draw_zone.create_oval(event.x,event.y,(2*self.circle_start_x-event.x),(2*self.circle_start_y-event.y))
        x=self.draw_zone.create_oval((self.circle_start_x),(self.circle_start_y),event.x,event.y,fill=None)
        self.stack.append(x)


    def point_start(self,event):
        x = self.draw_zone.create_line(event.x,event.y,event.x+1,event.y+1)
        self.Point_objects.append(x)

#create line from this place to previous place

    def freehand_start(self, event):
        self.px = event.x
        self.py = event.y
        self.stack.append("start")
    def freehand_motion(self, event):
        x = self.draw_zone.create_line(self.px, self.py, event.x, event.y, fill=self.DEFAULT_COLOR,smooth=1)
        self.px = event.x
        self.py = event.y
        self.stack.append(x)
    def freehand_end(self, event):
        self.stack.append("end")


    def text_start(self, event):
        self.text_start_x = event.x
        self.text_start_y = event.y
    def text_motion(self, event):
        self.draw_zone.delete('temp_text_objects')
        self.draw_zone.create_text(self.text_start_x, self.text_start_y, text = "hello", font = ("Purisa", math.floor(0.8*(event.y-self.text_start_y))), tags = 'temp_text_objects', anchor = NW)
    def text_end(self, event):
        self.draw_zone.delete('temp_text_objects')
        self.d = self.draw_zone.create_text(self.text_start_x, self.text_start_y, text = "hello", font = ("Purisa", math.floor(0.8*(event.y-self.text_start_y))), anchor = NW)
        self.mode = 'edit'
    def change_text(self, event):
        print(self.d)
        self.d.config(text="hello")
        # self.draw_zone.delete(self.d)

        
        
    

    def set_tool_line(self):
        self.tool_option = 'line'
    def set_tool_circle(self):
        self.tool_option = 'circle'
    def set_tool_point(self):
        self.tool_option = 'point'
    def set_tool_freehand(self):
        self.tool_option = 'freehand'
    def set_tool_text(self):
        self.tool_option = 'text'

    def draw_start(self,event):
        print("hello")
        if self.tool_option=='line':
            self.line_start(event)
        elif self.tool_option == 'circle':
            self.circle_start(event)
        elif self.tool_option=='point':
            self.point_start(event)
        elif self.tool_option == "freehand":
            self.freehand_start(event)
        elif self.tool_option == 'text':
            self.text_start(event)

    def draw_motion(self,event):
        if self.tool_option=='line':
            self.line_motion(event)
        if self.tool_option == 'freehand':
            self.freehand_motion(event)
        elif self.tool_option == 'circle':
            self.circle_motion(event)
        elif self.tool_option == 'text':
            self.text_motion(event)
    def draw_end(self,event):
        if self.tool_option=='line':
            self.line_end(event)
        if self.tool_option=='freehand':
            self.freehand_end(event)
        elif self.tool_option == 'circle':
            self.circle_end(event)
        elif self.tool_option == 'text':
            self.text_end(event)

    def undo(self):
        
        x = self.stack.pop()
        if x == "end":
            while x != "start":
                x = self.stack.pop()
                self.draw_zone.delete(x)
        else:
            self.draw_zone.delete(x)        

    def alert(self):
        print('yo')

if __name__ == '__main__':
    ge = Paint()
