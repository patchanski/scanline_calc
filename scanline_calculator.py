from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox


class scanline(Frame):
    def __init__(self, master):
        #self.img_thumbsup=PhotoImage(file="./imgs/thumbsup.gif")
        Frame.__init__(self, master)
        self.master = master

        self.master.geometry("600x400")
        self.master.title("Scanline Calculator")

        self.input = StringVar()
        self.weight = StringVar()
        self.modvalue = StringVar()
        self.box_value = StringVar()
        self.box_value2 = StringVar()
        self.subtract_value = StringVar()

        self.top_frame = Frame(master)
        self.top_frame.pack(side="top", fill=X)
        #self.top_frame.config(bg="RED")
        self.bottom_frame = Frame(master)
        self.bottom_frame.pack(side="top", fill=X)
        #self.bottom_frame.config(bg="BLUE")

        row_val = 0

        Label(self.top_frame, text="Input string: ").grid(row=row_val, column = 0, sticky=W)
        Entry(self.top_frame, textvariable=self.input, width=50).grid(row=row_val, column=1, sticky=W, padx=5)
        row_val+=1

        Label(self.top_frame, text="Weight: ").grid(row=row_val, column = 0, sticky=W)
        Entry(self.top_frame, textvariable=self.weight, width=30).grid(row=row_val, column=1, sticky=W, padx=5)
        row_val+=1

        Label(self.top_frame, text="MOD value: ").grid(row=row_val, column = 0, sticky=W)
        Entry(self.top_frame, textvariable=self.modvalue, width=10).grid(row=row_val, column=1, sticky=W, padx=5)
        row_val+=1

        Label(self.top_frame, text="Alpha handler: ").grid(row=row_val, column = 0, sticky=W)
        self.comboBox = Combobox(self.top_frame, state="readonly", textvariable=self.box_value)
        self.comboBox['values'] = ('NONE', '1: All letters are 0', '2: A = 1, B = 2, C = 3 etc','3: A = 10, B = 11, C = 12 etc.')
        self.comboBox.current(0)
        #self.comboBox.bind("<<ComboboxSelected>>", self.updatealphahandler)
        self.comboBox.grid(row=row_val, column = 1, sticky=W, padx=5)
        row_val+=1

        Label(self.top_frame, text="Subtract: ").grid(row=row_val, column = 0, sticky=W)
        Entry(self.top_frame, textvariable=self.subtract_value, width=10).grid(row=row_val, column=1, sticky=W, padx=5)
        row_val+=1

        Label(self.top_frame, text="Minus handle: ").grid(row=row_val, column = 0, sticky=W)
        self.comboBox2 = Combobox(self.top_frame, state="readonly", textvariable=self.box_value2)
        self.comboBox2['values'] = ('1: Minus sign as is', '2: Minus sign assiged as 0')
        self.comboBox2.current(0)
        #self.comboBox2.bind("<<ComboboxSelected>>", self.updatealphahandler)
        self.comboBox2.grid(row=row_val, column = 1, sticky=W, padx=5)
        row_val+=1

        Button(self.top_frame, text="CALCULATE", command=self.CalculateCheckDigit).grid(row=row_val, column=0, rowspan=2)

    def IsInt(self, number):
        try:
            int(number)
            return True
        except:
            return False

    def CalculateCheckDigit(self):
        # check for missing values
        if self.input.get().strip() == "":
            messagebox.showinfo("Missing input", "PLEASE ENTER INPUT STRING")
        elif self.weight.get().strip() == "":
            messagebox.showinfo("Missing input", "PLEASE ENTER WEIGHT VALUE")
        elif self.modvalue.get().strip() == "":
            messagebox.showinfo("Missing input", "PLEASE ENTER MOD VALUE\nDEFAULT: 10")
        elif self.modvalue.get().strip() != "" and not self.IsInt(self.modvalue.get()):
            messagebox.showinfo("Missing input", "MOD VALUE SHOULD BE AN INTEGER\nDEFAULT: 10")

        else:
            # destroy all widgets in frame to avoid overlap
            for widget in self.bottom_frame.winfo_children():
                widget.destroy()

            alpha_sel = self.box_value.get().split(':')[0]
            sub_sel = self.box_value2.get().split(':')[0]
            in_str = self.input.get()

            weight_val = self.weight.get()
            weight_val = weight_val.split(',')


            Label(self.bottom_frame, text="Input String:", font = "Helvetica 10 bold").grid(row=0, column = 0, sticky=W)
            Label(self.bottom_frame, text="Conversion Char:", font = "Helvetica 10 bold").grid(row=1, column = 0, sticky=W)
            Label(self.bottom_frame, text="Weight Value:", font = "Helvetica 10 bold").grid(row=2, column = 0, sticky=W)
            Label(self.bottom_frame, text="Multiple Value:", font = "Helvetica 10 bold").grid(row=3, column = 0, sticky=W)
            Label(self.bottom_frame, text="Merge Value:", font = "Helvetica 10 bold").grid(row=4, column = 0, sticky=W)

            col = 1
            w = 0
            display_w = 3
            itotal = 0

            for char in in_str:
                # input char
                Label(self.bottom_frame, text=char, width = display_w).grid(row=0, column = col, sticky=W)
                # weight val
                Label(self.bottom_frame, text=weight_val[w], width = display_w).grid(row=2, column = col, sticky=W)

                # convert alpha and minus signs
                if not self.IsInt(char):
                    char = char.upper()
                    char_con = char
                    if char == "-":
                        if sub_sel == "2":
                            char = 0
                            char_con = 0
                    elif alpha_sel == "1":
                        char = 0
                        char_con = 0
                    elif alpha_sel == "2":
                        char = ord(char) - ord('A') + 1
                        char_con = char
                    elif alpha_sel == "3":
                        char = ord(char) - ord('A') + 10
                        char_con = char
                    else:
                        char = ''

                    if self.IsInt(char_con):
                        Label(self.bottom_frame, text=char_con, width = display_w).grid(row=1, column = col, sticky=W)

                # Multiply the digit by the current weight.
                if self.IsInt(char):
                    val = int(char) * int(weight_val[w])
                else:
                    val = 0
                Label(self.bottom_frame, text=str(val), width = display_w).grid(row=3, column = col, sticky=W)

                # if value is 2 digits, add together
                if val >= 10:
                    val =(val % 10) + int(val / 10)
                Label(self.bottom_frame, text=str(val), width = display_w).grid(row=4, column = col, sticky=W)
                itotal+=int(val)

                if w+1 >= len(weight_val):
                    w = 0
                else:
                    w+=1

                col+=1


            col_span_val = col - 2
            row_val = 5
            # display original summation value
            Label(self.bottom_frame, text="Sum of previous row:", font = "Helvetica 10 bold").grid(row=row_val, column = 0, sticky=W)
            Label(self.bottom_frame, text=str(itotal)).grid(row=row_val, column = 1, sticky=W)
            row_val+=1


            # Mod the total to get the check digit.
            iCheckDigit = 0
            iCheckDigit = itotal % int(self.modvalue.get())
            Label(self.bottom_frame, text="Initial CheckDigit:", font = "Helvetica 10 bold").grid(row=row_val, column = 0, sticky=W)
            Label(self.bottom_frame, text=str(iCheckDigit)).grid(row=row_val, column = 1, sticky=W)
            formula_disp = '(' + str(itotal) + ' % ' + self.modvalue.get() + ')'
            Label(self.bottom_frame, text=formula_disp).grid(row=row_val, column = 2, sticky=W, columnspan = col_span_val)
            row_val+=1


            # We may need to subtract the result from another value (usually 10).
            sub_val = self.subtract_value.get().strip()
            formula_disp = "No subtract value"
            if sub_val != '' and self.IsInt(sub_val):
                formula_disp = '(' + sub_val + ' - ' + str(iCheckDigit) + ')'
                iCheckDigit = int(sub_val) - iCheckDigit
            Label(self.bottom_frame, text="Subtracted Value:", font = "Helvetica 10 bold").grid(row=row_val, column = 0, sticky=W)
            Label(self.bottom_frame, text=str(iCheckDigit)).grid(row=row_val, column = 1, sticky=W)
            Label(self.bottom_frame, text=formula_disp).grid(row=row_val, column = 2, sticky=W, columnspan = col_span_val)
            row_val+=1


            if iCheckDigit == 10:
                iCheckDigit = 0

            Label(self.bottom_frame, text="Final CheckDigit:", font = "Helvetica 10 bold").grid(row=row_val, column = 0, sticky=W)
            Label(self.bottom_frame, text=str(iCheckDigit)).grid(row=row_val, column = 1, sticky=W)
            row_val+=1


root = Tk()
app = scanline(root)
app.mainloop()
