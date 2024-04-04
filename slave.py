import machine
import time
import uctypes
import ustruct

I2C_SLAVE_ADDRESS = 0x17
I2C_BAUDRATE = 100000

I2C_SLAVE_SDA_PIN = machine.Pin(0)
I2C_SLAVE_SCL_PIN = machine.Pin(1)

context = uctypes.struct(
    {
        "mem": uctypes.ARRAY(uctypes.UINT8 | 0, 256),
        "mem_address": uctypes.UINT8 | 256,
        "mem_address_written": uctypes.BOOL,
    },
    ptr=uctypes.addressof(uctypes.bytearray_at(0x20000000, 256)),
)

def i2c_slave_handler(i2c, event):
    global context
    if event == machine.I2C.RECEIVED:
        if not context.mem_address_written:
            context.mem_address = i2c.readfrom(1)[0]
            context.mem_address_written = True
        else:
            context.mem[context.mem_address] = i2c.readfrom(1)[0]
            context.mem_address += 1
    elif event == machine.I2C.REQUEST:
        i2c.writeto(bytes([context.mem[context.mem_address]]))
        context.mem_address += 1
    elif event == machine.I2C.FINISHED:
        context.mem_address_written = False

def setup_slave():
    i2c_slave = machine.I2C(0, sda=I2C_SLAVE_SDA_PIN, scl=I2C_SLAVE_SCL_PIN, freq=I2C_BAUDRATE)
    i2c_slave.set_as_slave(I2C_SLAVE_ADDRESS, handler=i2c_slave_handler)

def run_master():
    I2C_MASTER_SDA_PIN = machine.Pin(6)
    I2C_MASTER_SCL_PIN = machine.Pin(7)

    i2c_master = machine.I2C(1, sda=I2C_MASTER_SDA_PIN, scl=I2C_MASTER_SCL_PIN, freq=I2C_BAUDRATE)

    for mem_address in range(0, 256, 32):
        msg = "Hello, I2C slave! - 0x{:02X}".format(mem_address)
        msg_len = len(msg)

        buf = bytearray(32)
        buf[0] = mem_address
        buf[1:msg_len + 1] = msg.encode()
        print("Write at 0x{:02X}: '{}'".format(mem_address, msg))
        count = i2c_master.writeto(I2C_SLAVE_ADDRESS, buf, False)
        if count < 0:
            print("Couldn't write to slave, please check your wiring!")
            return

        i2c_master.writeto(I2C_SLAVE_ADDRESS, bytes([mem_address]), True)
        split = 5
        buf = i2c_master.readfrom(I2C_SLAVE_ADDRESS, split, True)
        print("Read  at 0x{:02X}: '{}'".format(mem_address, buf.decode()))
        buf = i2c_master.readfrom(I2C_SLAVE_ADDRESS, msg_len - split, False)
        print("Read  at 0x{:02X}: '{}'".format(mem_address + split, buf.decode()))

        print("")
        time.sleep(2)

print("\nI2C slave example")
setup_slave()
run_master()
