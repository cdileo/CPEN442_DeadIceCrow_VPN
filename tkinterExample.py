from tkinter import *

class Application(Frame):
	
	def __init__(self, master = None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
		

	def createWidgets(self):
		self.mode = IntVar(self)
		self.mode.set(0)

		self.host = StringVar(self)
		self.port = StringVar(self)
		self.key = StringVar(self)
		self.data = StringVar(self)
		self.op_mode = IntVar(self)

		self.toggleClient = Radiobutton(self, text="client", variable=self.mode, value=0, command=self.get_mode)
		self.toggleClient.pack(side="top")
		self.toggleServer = Radiobutton(self, text="server", variable=self.mode, value=1, command=self.get_mode)
		self.toggleServer.pack(side="top")

		self.hostLabel = Label(self, text="Host")
		self.hostLabel.pack()
		self.hostEntry = Entry(self)
		self.hostEntry.pack()
		self.enterHost = Button(self, text="Enter host", command=self.get_host)
		self.enterHost.pack()

		self.portLabel = Label(self, text="Port")
		self.portLabel.pack()
		self.portEntry = Entry(self)
		self.portEntry.pack()
		self.enterPort = Button(self, text="Enter port", command=self.get_port)
		self.enterPort.pack()

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
		self.enterdataToSend = Button(self, text="Enter Data to be Sent", command=self.get_data)
		self.enterdataToSend.pack()

		self.dataReceivedLabel = Label(self, text="Data Received")
		self.dataReceivedLabel.pack()
		self.dataReceived = Message(self)
		self.dataReceived.pack()

	def get_mode(self):
		self.op_mode.set(self.mode.get())

	def get_host(self):
		self.host.set(self.hostEntry.get())

	def get_port(self):
		self.port.set(self.portEntry.get())

	def send_shared_key(self):
		key = self.keyField.get()
		return key

	def get_data(self):
		data = self.dataToSend.get("1.0", 'end-1c')
		print("DATA "+data)
		return data