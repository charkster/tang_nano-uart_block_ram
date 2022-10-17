# tang_nano-uart_block_ram
UART interface to a block ram in the Tang Nano FPGA. **No pin connections needed, just use the USB UART.**
Tang Nano supports up to 4k bytes of block ram (I used it all for this example). I use my own **SCARF** protocol where the first transmitted byte is the RNW bit as the MSBit, and the lower 7 bits are the slave ID (127 possible slaves in the FPGA). The next two bytes are the address (MSByte first). If a read is being done the last byte specifies the number of bytes to be read. If a write is being done the write data immediately follows the address.

**Dependancies:**

pip3 install pyftdi

pip3 install pyserial==3.4

Timing Diagram:
![picture](https://github.com/charkster/tang_nano-uart_block_ram/blob/main/images/uart_header1.png)

This example project shows how to implement a block ram, and interface to it using the **USB serial port**. This structure could be used to store data to transmit using a different protocol implemented in the FPGA (like SPMI or USB-PD). If a flip-flop based register map is used instead of the block ram, actions can be triggered by writing to specific bits.

I program my Tang Nano using https://github.com/trabucayre/openFPGALoader

**openFPGALoader -b tangnano uart_blockram_1k.fs**

<!-- ![picture](https://tangnano.sipeed.com/assets/tang_nano_pinout_v1.0.0_w5676_h4000_large.png) --!>
![picture](https://github.com/charkster/tang_nano-uart_block_ram/blob/main/images/tang_nano_pinout_v1.0.0_w5676_h4000_large.png)
