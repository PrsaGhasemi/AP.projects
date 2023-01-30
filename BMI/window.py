from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class Window:
    def __init__(self, title, width, height):
        self.master = Tk()
        self.master.title(title)
        self.master.geometry(f'{width}x{height}')
        self.master.resizable(False, False)
        self.master = ttk.Frame(self.master, padding=5)
        self.master.grid()

        self.weightUnit = StringVar(self.master)
        self.heightUnit = StringVar(self.master)
        self.weight = StringVar(self.master)
        self.height = StringVar(self.master)

        heightLabel = Label(self.master, text="Height:")
        weightLabel = Label(self.master, text="Weight:")

        heightLabel.grid(row=0, column=0, sticky=W, pady=10)
        weightLabel.grid(row=1, column=0, sticky=W, pady=10)

        heightInput = Entry(self.master, textvariable=self.height)
        weightInput = Entry(self.master, textvariable=self.weight)

        heightInput.grid(row=0, column=1, pady=2)
        weightInput.grid(row=1, column=1, pady=2)

        weightOptions = OptionMenu(self.master, self.weightUnit, "Pond", "Kilogram", "Gram")
        heightOptions = OptionMenu(self.master, self.heightUnit, "Meter", "Centimeter", "Inch")

        heightOptions.grid(row=0, column=2, pady=10)
        weightOptions.grid(row=1, column=2, pady=10)

        self.weightUnit.set("Kilogram")
        self.heightUnit.set("Centimeter")

        button = Button(self.master, text="Calculate", fg="blue", command=self.calculate)
        button.grid(row=2, column=2, pady=5)

    def run(self):
        self.master.mainloop()

    def calculate(self):
        if self.weight.get().replace(".", "").isnumeric() and self.height.get().replace(".", "").isnumeric():
            weight = float(self.weight.get())
            height = float(self.height.get())

            if self.weightUnit.get() == "Pond":
                weight = weight * 0.453592
            elif self.weightUnit.get() == "Gram":
                weight = weight * 0.001

            if self.heightUnit.get() == "Centimeter":
                height = height * 0.01
            elif self.heightUnit.get() == "Inch":
                height = height * 0.0254
            bmi = weight / (height * height)
            messagebox.showinfo("BMI", "BMI is : " + bmi.__str__())
            self.height.set("")
            self.weight.set("")
        else:
            messagebox.showerror("Error", "Please enter a valid number")
