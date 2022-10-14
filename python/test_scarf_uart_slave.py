from scarf_uart_slave import scarf_uart_slave
import random

bram = scarf_uart_slave(slave_id=0x01, num_addr_bytes=2)
print(bram.read_id())
bram.write_list(addr=0x0000, write_byte_list=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
bram.write_list(addr=0x0010, write_byte_list=[16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31])
print(bram.read_list(addr=0x0000, num_bytes=32))
print(bram.read_list(addr=0x0016, num_bytes=1))

num_values = 4096
random_list = []
for i in range(0,num_values):
	random_list.append(random.randint(0,255))

read_list = []
bram.write_list(addr=0x0000, write_byte_list=random_list)
read_list = bram.read_list(addr=0x0000, num_bytes=num_values)

for i in range(0,num_values):
	if (read_list[i] != random_list[i]):
		print("Misscompare at index {:d}, expected value 0x{:02x}, read value 0x{:02x}".format(i,random_list[i],read_list[i]))
