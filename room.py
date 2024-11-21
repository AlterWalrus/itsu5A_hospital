class Room():
	def __init__(self):
		self.visitors = []
		self.max_visitors = 0
		self.min_age = 0
		self.max_age = 0
		self.min_time = 0
		self.max_time = 0
		self.fname = ""
		self.lname = ""
		self.occupied = False
	
	def get_visitor_number(self):
		return len(self.visitors)

	def enter_visitor(self, rfid):
		self.visitors.append(rfid)
	
	def exit_visitor(self, rfid):
		self.visitors.remove(rfid)

	def put_patient(self, patient_data):
		self.occupied = True
		self.max_visitors = patient_data[0]
		self.min_age = patient_data[1]
		self.max_age = patient_data[2]
		self.min_time = patient_data[3]
		self.max_time = patient_data[4]
		self.fname = patient_data[5]
		self.lname = patient_data[6]