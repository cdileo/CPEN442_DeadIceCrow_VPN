from tkinter import *
import vpn

class Application(Frame):
	
	def __init__(self, master = None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
		

	def createWidgets(self):
		self.mode = IntVar(self)
		self.mode.set(1)

		self.toggleClient = Radiobutton(self, text="client", variable=self.mode, value=1, command=self.get_mode)
		self.toggleClient.pack(side="top")
		self.toggleServer = Radiobutton(self, text="server", variable=self.mode, value=2, command=self.get_mode)
		self.toggleServer.pack(side="top")

		self.sharedKey = Label(self, text="Shared Secret Value")
		self.sharedKey.pack()
		self.keyField = Entry(self)
		self.keyField.pack()
		self.enterKey = Button(self, text="Enter Secret Value", command=self.send_shared_key)
		self.enterKey.pack()
		
		self.dataToSendLabel = Label(self, text="Data to be Sent")
		self.dataToSendLabel.pack()
		self.dataToSend = Text(self)
		self.dataToSend.pack()
		self.enterdataToSend = Button(self, text="Enter Data to be Sent", command=self.send_data)
		self.enterdataToSend.pack()

		self.dataReceivedLabel = Label(self, text="Data Received")
		self.dataReceivedLabel.pack()
		self.dataReceived = Message(self)
		self.dataReceived.pack()

		self.QUIT = Button(self, text = "QUIT", fg="red", command = root.destroy)
		self.QUIT.pack()

# python vpn.py -s 128.189.217.70 -p 9009
	def get_mode(self):
		mode = self.mode.get()
		if mode == 1:
			print("CLIENT")
			mode = '-s'
		else:
			mode = '-m'
			print("SERVER")

		vpn.main([mode, '128.189.217.70', '-p', 9009])

	def send_shared_key(self):
		key = self.keyField.get()
		print("CODE "+key)

	def send_data(self):
		data = self.dataToSend.get("1.0", 'end-1c')
		print("DATA "+data)

root = Tk()
app = Application(master = root)
app.mainloop()