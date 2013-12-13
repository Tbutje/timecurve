import Tkinter, tkMessageBox, csv
from generate_csv import Generate_csv
import sys
from datetime import datetime

class Gui(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # needed for settings
        self.mydict = {}
        try:
            with open("conf.cfg", 'rb+') as input_file:
                reader = csv.reader(input_file)
                try:
                    for row in reader:
                        self.mydict[row[0]] = row[1]
                except csv.Error as error:
                    sys.exit('file %s, line %d: %s' % (input_file, reader.line_num, error))
        except IOError:
            print "conf.cfg bestaat niet dus wordt gemaakt"

        # needed for grid init
        self.grid()
        self.bind("<Return>", self.apply)


        button_a = Tkinter.Button(self,text="Apply",
                                command=self.apply)

        button_q = Tkinter.Button(self,text="Quit",
                                command=self.quit)


        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")

        self.labelVariable.set("Time curve program")

        # LABELS & BUTTONS
        Tkinter.Label(self, text="input file:").grid(row=0, sticky= "we")
        Tkinter.Label(self, text="output file:").grid(row=1)
        Tkinter.Label(self, text="").grid(row=2)

        Tkinter.Label(self, text="year").grid(row=3)
        Tkinter.Label(self, text="month:").grid(row=4)
        Tkinter.Label(self, text="day:").grid(row=5)
        Tkinter.Label(self, text="hour :").grid(row=6)
        Tkinter.Label(self, text="minute :").grid(row=7)
        Tkinter.Label(self, text="second :").grid(row=8)
        label.grid(column=0,row=9,columnspan=2,sticky='WE')
        button_a.grid(column=0,row=10,sticky= "WE")
        button_q.grid(column=1,row=10, sticky= "WE")

        # INPUT
        self.input = Tkinter.Entry(self)
        self.output = Tkinter.Entry(self)

        self.year = Tkinter.Entry(self)
        self.month = Tkinter.Entry(self)
        self.day = Tkinter.Entry(self)
        self.hour = Tkinter.Entry(self)
        self.minute = Tkinter.Entry(self)
        self.second = Tkinter.Entry(self)


        self.input.grid(row=0, column=1)
        self.input.insert(0, self.mydict.get("input", "input.csv"))
        self.output.grid(row=1, column=1)
        self.output.insert(0, self.mydict.get("output", "output.csv"))

        self.year.grid(row=3, column=1)
        self.year.insert(0, self.mydict.get("year", "2000"))
        self.month.grid(row=4, column=1)
        self.month.insert(0,self.mydict.get("month", "1"))
        self.day.grid(row=5, column=1)
        self.day.insert(0,self.mydict.get("day", "1"))
        self.hour.grid(row=6, column=1)
        self.hour.insert(0,self.mydict.get("hour", "1"))
        self.minute.grid(row=7, column=1)
        self.minute.insert(0,self.mydict.get("minute", "1"))
        self.second.grid(row=8, column=1)
        self.second.insert(0,self.mydict.get("second", "1"))



        # stuf to make it resizable, or not
        self.grid_columnconfigure(0,weight=1)
        # Horizondat x vertical resize
        self.resizable(False,False)
        return self.input.focus()



    def apply(self, *args):

        try:
            input = self.input.get()
            open(input, 'rb')
            output = self.output.get()
            year = int(self.year.get())
            month = int(self.month.get())
            day = int(self.day.get())
            hour = int(self.hour.get())
            minute = int(self.minute.get())
            second = int(self.second.get())

            # do the read and write stuff
            data = Generate_csv(input, year, month, day, hour, minute, second)
            data.create()
            data.write(output)
            # store values in config

            self.labelVariable.set("Time curve generated at " +
                                    datetime.now().strftime("%X"))
        # wrong values
        except ValueError:
            tkMessageBox.showwarning(
                "Bad input",
                "Illegal values, please try again"
            )
            self.labelVariable.set( "Time curve NOT generated" )
        # input file can't be found
        except IOError:
            tkMessageBox.showwarning(
                "input file problem",
                "cant find input file, please try again"
            )


    def quit(self):
        self.destroy()

    def save_settings(self):
        with open("conf.cfg", 'wb') as file:
            writer = csv.writer(file)
            writer.writerows([("input", input), ("output", output), ("year", year),
            ("month", month), ("day", day), ("hour", hour), ("minute", minute),
            ("second", second)])


if __name__ == "__main__":
    app = Gui(None)
    app.title('time profile to time_curve')
    app.mainloop()