from machine import Pin,SPI,PWM,Timer
import framebuf
import time
from utime import sleep, localtime, mktime


BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

P1 = 10
P2 = 20
P3 = 30
P4 = 40
P5 = 50
P6 = 60


class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 135

        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)

        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""
        self.rst(1)
        self.rst(0)
        self.rst(1)

        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A)
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35)

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F)

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)

        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)

        self.write_cmd(0x2C)

        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
    
    def separator(self, show):
        if show:
            self.fill_rect(115, 50, P1, P1, LCD.red)
            self.fill_rect(115, 70, P1, P1, LCD.red)
        else:
            # self.fill_rect(115, 50, P1, P1, LCD.white)
            # self.fill_rect(115, 70, P1, P1, LCD.white)
            self.rect(115, 50, P1, P1, LCD.red)
            self.rect(115, 70, P1, P1, LCD.red)
    
    def number0(self, pos=0):
        x = 5 + pos
        y = 28
        self.fill_rect(x+P1, y, P3, P1, LCD.blue)
        self.fill_rect(x, y+P1, P1, P5, LCD.blue)
        self.fill_rect(x+P1, y+P6, P3, P1, LCD.blue)
        self.fill_rect(x+P4, y+P1, P1, P5, LCD.blue)
    
    def number1(self, pos=0):
        x = 5 + pos
        y = 28
        self.fill_rect(x, y+P1, P2, P1, LCD.blue)
        self.fill_rect(x+P2, y, P1, P6, LCD.blue)
        self.fill_rect(x, y+P6, P5, P1, LCD.blue)
    
    def number2(self, pos=0):
        x = 5 + pos
        y = 28
        self.fill_rect(x, y+P1, P1, P1, LCD.blue)
        self.fill_rect(x+P1, y, P3, P1, LCD.blue)
        self.fill_rect(x+P4, y+P1, P1, P1, LCD.blue)
        self.fill_rect(x+P3, y+P2, P1, P1, LCD.blue)
        self.fill_rect(x+P2, y+P3, P1, P1, LCD.blue)
        self.fill_rect(x+P1, y+P4, P1, P1, LCD.blue)
        self.fill_rect(x, y+P5, P1, P1, LCD.blue)
        self.fill_rect(x, y+P6, P5, P1, LCD.blue)
    
    def number3(self, pos=0):
        x = 5 + pos
        y = 28
        self.fill_rect(x, y+P1, P1, P1, LCD.blue)
        self.fill_rect(x+P1, y, P3, P1, LCD.blue)
        self.fill_rect(x+P4, y+P1, P1, P2, LCD.blue)
        self.fill_rect(x+P2, y+P3, P2, P1, LCD.blue)
        self.fill_rect(x+P4, y+P4, P1, P2, LCD.blue)
        self.fill_rect(x, y+P5, P1, P1, LCD.blue)
        self.fill_rect(x+P1, y+P6, P3, P1, LCD.blue)
    
    def number4(self, pos=0):
        x = 5 + pos
        y = 28
        self.fill_rect(x, y, P1, P4, LCD.blue)
        self.fill_rect(x, y+P4, P5, P1, LCD.blue)
        self.fill_rect(x+P2, y+P3, P1, P4, LCD.blue)
    
    def number5(self, pos=0):
        x = 5 + pos
        y = 28
        self.fill_rect(x, y, P5, P1, LCD.blue)
        self.fill_rect(x, y+P1, P1, P2, LCD.blue)
        self.fill_rect(x, y+P3, P4, P1, LCD.blue)
        self.fill_rect(x+P4, y+P4, P1, P2, LCD.blue)
        self.fill_rect(x, y+P6, P4, P1, LCD.blue)
    
    def number6(self, pos=0):
        x = 5 + pos
        y = 28
        self.fill_rect(x+P1, y, P3, P1, LCD.blue)
        self.fill_rect(x+P4, y+P1, P1, P1, LCD.blue)
        self.fill_rect(x, y+P1, P1, P5, LCD.blue)
        self.fill_rect(x+P1, y+P3, P3, P1, LCD.blue)
        self.fill_rect(x+P4, y+P4, P1, P2, LCD.blue)
        self.fill_rect(x+P1, y+P6, P3, P1, LCD.blue)
    
    def number7(self, pos=0):
        x = 5 + pos
        y = 28
        self.fill_rect(x, y, P5, P1, LCD.blue)
        self.fill_rect(x+P4, y+P1, P1, P1, LCD.blue)
        self.fill_rect(x+P3, y+P2, P1, P1, LCD.blue)
        self.fill_rect(x+P2, y+P3, P1, P4, LCD.blue)
    
    def number8(self, pos=0):
        x = 5 + pos
        y = 28
        self.fill_rect(x+P1, y, P3, P1, LCD.blue)
        self.fill_rect(x+P1, y+P3, P3, P1, LCD.blue)
        self.fill_rect(x+P1, y+P6, P3, P1, LCD.blue)
        self.fill_rect(x, y+P1, P1, P2, LCD.blue)
        self.fill_rect(x+P4, y+P1, P1, P2, LCD.blue)
        self.fill_rect(x, y+P4, P1, P2, LCD.blue)
        self.fill_rect(x+P4, y+P4, P1, P2, LCD.blue)
    
    def number9(self, pos=0):
        x = 5 + pos
        y = 28
        self.fill_rect(x+P1, y, P3, P1, LCD.blue)
        self.fill_rect(x+P1, y+P3, P3, P1, LCD.blue)
        self.fill_rect(x+P1, y+P6, P3, P1, LCD.blue)
        self.fill_rect(x, y+P1, P1, P2, LCD.blue)
        self.fill_rect(x+P4, y+P1, P1, P5, LCD.blue)
        self.fill_rect(x, y+P5, P1, P1, LCD.blue)


class Count:
    def __init__(self):
        self.globaltime = localtime(0)
        self.timer = Timer(-1)
        self.led = Pin(25, Pin.OUT)
        self.h = 0
        self.m = 0
        self.s = 0

    def start(self):
        self.timer.init(
            mode=Timer.PERIODIC,
            period=1000,
            callback=self.update
        )

    def update(self, t):
        self.led.toggle()
        self.globaltime = localtime(
            mktime(self.globaltime) + 1
        )
        self.displayTime()

    def reset(self):
        self.count = 0
        self.globaltime = localtime(0)
        self.led.value(0)
        self.timer.deinit()
        self.timer = Timer(-1)

    def displayTime(self):
        self.s = self.globaltime[5]
        self.m = self.globaltime[4]
        self.h = self.globaltime[3]


if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch14()
    LCD.fill(LCD.white)

    LCD.show()
    LCD.text("Pico - Last Cat Service...",15,15,LCD.red)
    LCD.text("STOP",45,115,LCD.red)
    LCD.text("RESET",155,115,LCD.blue)

    LCD.show()
    keyB = Pin(17,Pin.IN,Pin.PULL_UP)

    key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)# CTRL

    count = Count()
    count.start()

    while(1):
        if(keyB.value() == 0):
            LCD.fill_rect(208,103,20,20,LCD.red)
            print("Reset")
            count.reset()
            count.start()
        else :
            LCD.fill_rect(208,103,20,20,LCD.white)
            LCD.rect(208,103,20,20,LCD.red)

        if(key3.value() == 0):# CTRL
            LCD.fill_rect(12,103,20,20,LCD.red)
            print("STOP")
            count.timer.deinit()
            Pin(25, Pin.OUT).value(0)
            break
        else :
            LCD.fill_rect(12,103,20,20,LCD.white)
            LCD.rect(12,102,20,20,LCD.red)

        LCD.fill_rect(5, 28, 230, 70, LCD.white)
        # H1
        h1 = int(count.h / 10)
        if h1 == 0:
            LCD.number0()
        if h1 == 1:
            LCD.number1()
        if h1 == 2:
            LCD.number2()
        # H2
        h2 = count.h % 10
        if h2 == 0:
            LCD.number0(55)
        if h2 == 1:
            LCD.number1(55)
        if h2 == 2:
            LCD.number2(55)
        if h2 == 3:
            LCD.number3(55)
        if h2 == 4:
            LCD.number4(55)
        if h2 == 5:
            LCD.number5(55)
        if h2 == 6:
            LCD.number6(55)
        if h2 == 7:
            LCD.number7(55)
        if h2 == 8:
            LCD.number8(55)
        if h2 == 9:
            LCD.number9(55)
        # M1
        m1 = int(count.m / 10)
        if m1 == 0:
            LCD.number0(125)
        if m1 == 1:
            LCD.number1(125)
        if m1 == 2:
            LCD.number2(125)
        if m1 == 3:
            LCD.number3(125)
        if m1 == 4:
            LCD.number4(125)
        if m1 == 5:
            LCD.number5(125)
        # M2
        m2 = count.m % 10
        if m2 == 0:
            LCD.number0(180)
        if m2 == 1:
            LCD.number1(180)
        if m2 == 2:
            LCD.number2(180)
        if m2 == 3:
            LCD.number3(180)
        if m2 == 4:
            LCD.number4(180)
        if m2 == 5:
            LCD.number5(180)
        if m2 == 6:
            LCD.number6(180)
        if m2 == 7:
            LCD.number7(180)
        if m2 == 8:
            LCD.number8(180)
        if m2 == 9:
            LCD.number9(180)

        LCD.separator((count.s % 2))
        LCD.fill_rect(110, 115, 20, 10, LCD.white)
        LCD.text(f'{count.s}', 110, 115,LCD.red)

        LCD.show()
    time.sleep(1)
    LCD.fill(0x0000)
    LCD.show()
