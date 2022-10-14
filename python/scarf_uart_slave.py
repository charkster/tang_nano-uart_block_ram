from __future__  import print_function
from pyftdi.ftdi import Ftdi
import pyftdi.serialext

class scarf_uart_slave:
	
	# Constructor
	def __init__(self, slave_id=0x00, num_addr_bytes=2, ftdi_baudrate=1000000, debug=False):
		self.slave_id         = slave_id
		self.num_addr_bytes   = num_addr_bytes
		self.ftdi_baudrate    = ftdi_baudrate
		self.ftdi_port        = pyftdi.serialext.serial_for_url('ftdi://ftdi:2232:39526AC8FA/2', baudrate=self.ftdi_baudrate, bytesize=8, parity='N', stopbits=1, timeout=0.01)
		# use Ftdi.show_devices() to get URL
		self.read_buffer_max  = 31  - self.num_addr_bytes
		self.write_buffer_max = 60 - self.num_addr_bytes
		self.debug            = debug
		self.ftdi_port.write([0x00]) # get the party started
		
	def read_list(self, addr=0x00, num_bytes=1):
		if (self.debug == True):
			print("Called read")
		if (num_bytes == 0):
			print("Error: num_bytes must be larger than zero")
			return []
		else:
			byte0 = (self.slave_id + 0x80) & 0xFF
			remaining_bytes = num_bytes
			read_list = []
			address = addr - self.read_buffer_max # we will add this later
			while (remaining_bytes > 0):
				if (remaining_bytes >= self.read_buffer_max):
					step_size = self.read_buffer_max
					remaining_bytes = remaining_bytes - self.read_buffer_max
				else:
					step_size = remaining_bytes
					remaining_bytes = 0
				address = address + self.read_buffer_max # this keeps increasing in the loop
				addr_byte_list = []
				for addr_byte_num in range(self.num_addr_bytes):
					addr_byte_list.insert(0, address >> (8*addr_byte_num) & 0xFF )
				self.ftdi_port.write(bytearray([byte0] + addr_byte_list + [step_size]))
				tmp_read_list = list(self.ftdi_port.read(step_size+self.num_addr_bytes+1))
				if (self.num_addr_bytes > 1):
					del tmp_read_list[:2] # first two bytes are echoed slave_id
				read_list.extend(tmp_read_list)
			if (self.debug == True):
				address = addr
				for read_byte in read_list:
					print("Address 0x{:02x} Read data 0x{:02x}".format(address,read_byte))
					address += 1
			return read_list
	
	def write_list(self, addr=0x00, write_byte_list=[]):
		byte0 = self.slave_id & 0xFF
		remaining_bytes = len(write_byte_list)
		address = addr - self.write_buffer_max # expecting to add self.write_buffer_max
		while (remaining_bytes > 0):
			if (remaining_bytes >= self.write_buffer_max):
				step_size = self.write_buffer_max
				remaining_bytes = remaining_bytes - self.write_buffer_max
			else:
				step_size = remaining_bytes
				remaining_bytes = 0
			address = address + self.write_buffer_max
			addr_byte_list = []
			for addr_byte_num in range(self.num_addr_bytes):
				addr_byte_list.insert(0, address >> (8*addr_byte_num) & 0xFF )
			self.ftdi_port.write(bytearray([byte0] + addr_byte_list + write_byte_list[address-addr:address+step_size]))
		if (self.debug == True):
			print("Called write_bytes")
			address = addr
			for write_byte in write_byte_list:
				print("Wrote address 0x{:02x} data 0x{:02x}".format(address,write_byte))
				address += 1
		return 1
		
	def read_id(self):
		byte0 = (self.slave_id + 0x80) & 0xFF
		self.ftdi_port.write(bytearray([byte0] + self.num_addr_bytes * [0x00]))
		slave_id = list(self.ftdi_port.read(1))
		if (self.debug == True):
			print("Slave ID is 0x{:02x}".format(slave_id[0]))
		return slave_id[0] - 0x80
		
