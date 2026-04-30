import tkinter as tk
from tkinter import font
import math

def equation(a,b,c): 
    d=(b**2)-(4*a*c)
    if d<0:
        return("math error")
    elif a==0:
        return("math error")
    elif d==0:
        root=-b/(2*a)
        return(f"X = {root}")
    else:
        root1=(-b+ math.sqrt(d))/(2*a)
        root2=(-b- math.sqrt(d))/(2*a)
        return(f"X1 = {root1} , X2 = {root2}")

class AdvancedCalculator:

    
    def __init__(self, root):
        self.root = root
        self.shift_on=False
        self.root.title("Advanced Calculator")

        
        WINDOW_BG = "#1e1e1e"
        DISPLAY_BG = "#252525"
        STANDARD_BUTTON_BG = "#3c3c3c"
        FUNCTION_BUTTON_BG = "#5c5c5c"
        EQUALS_BG = "#4CAF50"  # Green
        CLEAR_BG = "#E91E63"   # Red/Pink
        TEXT_COLOR = "white"
       

        
        self.root.configure(bg=WINDOW_BG)

        window_width = 500
        window_height = 700
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)

        self.custom_font = font.Font(size=18)

        
        self.entry_display = tk.Entry(root, font=("Arial", 24), bd=10, insertwidth=2, width=28, borderwidth=4, justify="right",
                                     bg=DISPLAY_BG, fg=TEXT_COLOR) # Added bg and fg
        self.entry_display.grid(row=0, column=0, columnspan=5, padx=5, pady=5)
        self.current_input = ""
        self.result = 0
        self.trig_unit = "rad" 

        
        self.buttons = [
            ('⌫',1,0), ('C',1,1), ('shift',1,2), ('√',1,3), ('Eq',1,4),
            ('7',2,0), ('8',2,1), ('9',2,2), ('/',2,3), ('(',2,4),
            ('4',3,0), ('5',3,1), ('6',3,2), ('x',3,3), (")",3,4), 
            ('1',4,0), ('2',4,1), ('3',4,2), ('-',4,3), ('𝑒',4,4),
            ('0',5,0), ('.',5,1), ('=',5,2), ('+',5,3), ('^',5,4),
            ('sin',6,0), ('cos',6,1), ('tan',6,2), ('log',6,3), ('ln',6,4), 
            ('Rad/Deg',7,0), ('10^x',7,1), ('x^2',7,2), ("BIN→DEC",7,3), ('!',7,4),
        ]
        self.button_widgets={}

        for (text, row, col) in self.buttons:
            cmd = self.get_command(text)
            
            
            if text == '=':
                bg_color = EQUALS_BG
            elif text == '⌫' or text == 'C':
                bg_color = CLEAR_BG
            elif text in ['sin', 'cos', 'tan', 'log', 'ln', 'Rad/Deg', '10^x', 'x^2', 'BIN→DEC', '!', '√', '𝝅', '𝑒', 'Eq', '^', '/', 'x', '-', '+', '(', ')']:
                bg_color = FUNCTION_BUTTON_BG
            else:
                bg_color = STANDARD_BUTTON_BG
            
            button = tk.Button(self.root, text=text, font=self.custom_font, command=cmd, 
                               padx=20, pady=20, 
                               bg=bg_color, 
                               fg=TEXT_COLOR, 
                               activebackground=TEXT_COLOR, 
                               activeforeground=bg_color)
            button.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
            self.button_widgets[text]=button
        
        for i in range(8):
            self.root.grid_rowconfigure(i, weight=1)

        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)

    def get_command(self, text):
        if text == '⌫':
            return self.backspace
        elif text == 'C':
            return self.clear
        elif text == '=':
            return self.equal
        elif text == "shift":
            return self.toggle_shift
        else:
            return lambda t=text: self.button_click(t)
    def convert_BIN_DEC(self):
        try:
            value=self.current_input.strip()
            if not value:
                return
            if self.shift_on:
                DEC=int(float(value))
                self.current_input=bin(DEC)[2:]
                self.toggle_shift()  
            else:
                if value.endswith(".0"):
                    value=value[:-2]
                if not all((c in "01" for c in value)):
                    self.current_input="error"
                    return
                self.current_input=str(int(value,2))
        except Exception:
            self.current_input="error"
        self.update_entry()
        
    def button_click(self, char):

        if char in ['sin','cos','tan','log','ln','√','!','x^2']:
            self.handle_functions(char)
        elif char == 'BIN→DEC': 
            self.convert_BIN_DEC()
        elif char == '𝑒':
            self.current_input += str(math.e)
        elif char == 'Eq':
            print("aX**2+bX+c")
            self.equation_from_input()
        elif char == 'Rad/Deg':
            self.toggle_trig_unit()
        elif char == '.':
            if not self.has_decimal():
                self.current_input += '.'
        elif char == 'x':
            self.current_input += '*'    
        elif char == ")":
            if self.shift_on:
                self.current_input+=","
                self.toggle_shift()
            else:
                self.current_input+=")"
        elif char == "10^x":
            if self.shift_on:
                self.current_input+= str(math.pi)
                self.toggle_shift()
            else:
                self.handle_functions("10^x")
        else:
            self.current_input += str(char)

        self.update_entry()

    def has_decimal(self):
        operators = ['+', '-', '*', '/', '^', '(', ')', '**']
        last_op = -1
        
        for op in operators:
            idx = self.current_input.rfind(op)
            if idx > last_op:
                last_op = idx
        
        current_number = self.current_input[last_op + 1:]
        return '.' in current_number

    def handle_functions(self, func):
        try:

            if not self.current_input:
                return


            expression = self.current_input.replace('^', '**')
            value = float(eval(expression))
            
            result = 0

            Exact_Trig={
                "sin":{
                    0:"0", 30:"0.5", 45:f"{math.sqrt(2)/2:.10g}",
                    60:f"{math.sqrt(3)/2:.10g}", 90:"1", 180:"0", math.pi:"0"
                },
                "cos":{
                    0:"1", 30:f"{math.sqrt(3)/2:.10g}", 45:f"{math.sqrt(2)/2:.10g}",
                    60:"0.5", 90:"0", 180:"-1", math.pi:"-1"
                },
                "tan":{
                    0:"0", 30:f"{math.sqrt(3)/3:.10g}", 45:"1",
                    60:f"{math.sqrt(3):.10g}", 90:"MATH ERROR", 180:"0", math.pi:"0"
                }
            }

            if func in ['sin','cos','tan']:
                if abs(value-math.pi)<1e-9:
                    if self.trig_unit == "deg":
                        value=180

                if self.trig_unit == "deg":
                    int_value = int(value)
                    if value == int(value) and int_value in Exact_Trig[func]:
                        self.current_input = Exact_Trig[func][int_value]
                        self.update_entry()
                        return             
                    value = math.radians(value)
                result = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan}[func](value)
                
            elif func == 'log':
                result = math.log10(value)        
            elif func == 'ln':
                result = math.log(value)         
            elif func == '√':
                result = math.sqrt(value)           
            elif func == '!':
                result = math.factorial(int(value))
            elif func == '10^x':
                result = 10 ** value            
            elif func == 'x^2': 
                result = value ** 2
            
            self.current_input = f"{result:.10g}"
        except Exception:
            self.current_input = "Error"
        
        self.update_entry()

    def clear(self):
        self.current_input = ""
        self.update_entry()

    def backspace(self):
        self.current_input = self.current_input[:-1]
        self.update_entry()

    
    def equal(self):
        try:
            expression = self.current_input.replace('^', '**') 
            self.result = str(eval(expression))
            self.current_input = self.result
        except Exception:
            self.current_input = "Error"
        self.update_entry()

    
    def toggle_trig_unit(self):

        if self.trig_unit == "rad":
            self.trig_unit = "deg"
            self.root.title("Advanced Calculator (DEGREE)")
        else:
            self.trig_unit = "rad"
            self.root.title("Advanced Calculator (RADIAN)")
    
    def update_entry(self):
        self.entry_display.delete(0, tk.END)
        self.entry_display.insert(0, self.current_input)

    def toggle_shift(self):
        self.shift_on = not self.shift_on
        if self.shift_on:
            self.button_widgets[")"].config(text=",")
            self.button_widgets["10^x"].config(text="π")
            self.button_widgets["BIN→DEC"].config(text="DEC→BIN")
            self.button_widgets["shift"].config(bg="#2196F3") #Cyan
        else:
            self.button_widgets[")"].config(text=")")
            self.button_widgets["10^x"].config(text="10^x")
            self.button_widgets["BIN→DEC"].config(text="BIN→DEC")
            self.button_widgets["shift"].config(bg="#5c5c5c") #Grey

    def equation_from_input(self):
        inputs=self.current_input.split(",")
        if len(inputs)!=3:
            self.current_input="use: a,b,c"
            self.update_entry()
            return
        
        a,b,c=map(float,inputs)
        Result= equation(a,b,c)
        self.current_input=str(Result)
        self.update_entry()
if __name__ == "__main__":
    root = tk.Tk() 
    calculator = AdvancedCalculator(root)
    root.mainloop()