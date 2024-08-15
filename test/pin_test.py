import wiringpi
import time
from wiringpi import GPIO




class GpiosManager():
    def __init__(self):
        super().__init__()
        wiringpi.wiringPiSetup()
        #pines de salidas
        self.cerradura1 = 6
        self.electroiman = 5
        self.actuador_up = 21
        self.actuador_down = 20
        self.semaforo = 27
        self.pin_libre1 = 17
        self.pin_libre2 = 24
        self.pin_libre3 = 23
        # pines de entradas
        self.fin_carrera = 16
        self.sensor = 26
        # declaracion de salidas
        wiringpi.pinMode(self.cerradura1, GPIO.OUTPUT)
        wiringpi.pinMode(self.electroiman, GPIO.OUTPUT)
        wiringpi.pinMode(self.actuador_up, GPIO.OUTPUT)
        wiringpi.pinMode(self.actuador_down, GPIO.OUTPUT)
        wiringpi.pinMode(self.semaforo, GPIO.OUTPUT)
        wiringpi.pinMode(self.pin_libre1, GPIO.OUTPUT)
        wiringpi.pinMode(self.pin_libre2, GPIO.OUTPUT)
        wiringpi.pinMode(self.pin_libre3, GPIO.OUTPUT)
        # declaracion de entradas
        wiringpi.pinMode(self.sensor, wiringpi.GPIO.INPUT)
        wiringpi.pinMode(self.fin_carrera, wiringpi.GPIO.INPUT)

        wiringpi.pullUpDnControl(self.sensor, wiringpi.GPIO.PUD_UP)
        wiringpi.pullUpDnControl(self.fin_carrera, wiringpi.GPIO.PUD_UP)

    def turnstileOpen(self):
            wiringpi.digitalWrite(self.cerradura1, GPIO.LOW)
            wiringpi.digitalWrite(self.semaforo, GPIO.HIGH)
            return "puerta general abierta"
    
    def turnstileBlock(self):
        wiringpi.digitalWrite(self.cerradura1, GPIO.HIGH)
        wiringpi.digitalWrite(self.semaforo, GPIO.HIGH)
        return "puerta general bloqueada" 

    def testCerradura1(self):
        wiringpi.digitalWrite(self.cerradura1, GPIO.LOW)
        time.sleep(2)
        wiringpi.digitalWrite(self.cerradura1, GPIO.HIGH)
        time.sleep(2)
        return 'Cerradura 1 testeada con exito'
    
    def testLuzLed(self):
        wiringpi.digitalWrite(self.semaforo, GPIO.LOW)
        time.sleep(2)
        wiringpi.digitalWrite(self.semaforo, GPIO.HIGH)
        time.sleep(2)
        return 'Luz Led testeada con exito'
    
    def testCerradura2(self):
        wiringpi.digitalWrite(self.pin_libre1, GPIO.LOW)
        time.sleep(2)
        wiringpi.digitalWrite(self.pin_libre1, GPIO.HIGH)
        time.sleep(2)
        return 'Cerradura 2 testeada con exito'

    def specialDoorOpen(self):
        wiringpi.digitalWrite(self.actuador_down, GPIO.HIGH)
        wiringpi.digitalWrite(self.actuador_up, GPIO.LOW)
        wiringpi.digitalWrite(self.semaforo, GPIO.LOW) 
        return "Puerta especial Abierta"
    
    def specialDoorClose(self):
        wiringpi.digitalWrite(self.actuador_up, GPIO.HIGH)
        wiringpi.digitalWrite(self.actuador_down, GPIO.LOW)
        wiringpi.digitalWrite(self.semaforo, GPIO.HIGH) 
        return "Puerta Especial Cerrada"
    
    def specialDoorOff(self):
        wiringpi.digitalWrite(self.actuador_up, GPIO.HIGH)
        wiringpi.digitalWrite(self.actuador_down, GPIO.HIGH)
        return "sistema silla de ruedas"
    
    def ReadSensor(self):
        return bool(wiringpi.digitalRead(self.sensor))
    
    def ReadFinCarrera(self):
        return bool(wiringpi.digitalRead(self.fin_carrera))
    def electroImanOn(self):
        wiringpi.digitalWrite(self.electroiman,GPIO.LOW)
        return 'electro iman activado'
    
    def electroImanOff(self):
        wiringpi.digitalWrite(self.electroiman,GPIO.HIGH)
        return 'electro iman desactivado'