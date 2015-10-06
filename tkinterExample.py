import tkinter as tk

class Application(tk.Frame):
	def __init__(self, master = None):
		tk.Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		self.hi_there = tk.Button(self)
		self.hi_there["text"] = "Hello World\n(click me)"
		self.hi_there["command"] = self.say_hi
		self.hi_there.pack(side="top")

		self.QUIT = tk.Button(self, text = "QUIT", fg="red", command = root.destroy)
		self.QUIT.pack(side = "bottom")
		self.messageField = tk.Text(self)
		self.messageField.pack(side = "bottom")
		self.keyField = tk.Entry(self)
		self.keyField.pack(side = "bottom")

	def say_hi(self):
		print("hi there, everyone!")
		print("The current entered key is {}", self.keyField.get())
		print("The current text entered is {}", self.messageField.get("1.0",'end-1c'))

root = tk.Tk()
app = Application(master = root)
app.mainloop()