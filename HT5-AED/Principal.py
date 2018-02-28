#Kevin Macario 17369
#Rodrigo Urrutia
#Clase Principal

#import SistemaOperativo
#import Procesos
import random
import simpy

#-----METODOS-----

def New(self, env, ram):
    self.env = env
    self.proceso = env.process(self.run())
    print("Se comenzo un nuevo proceso")
    procesoIn = env.now
    print("El proceso llego a la RAM")
    tamanioProceso = random.randint(1,10)
    with ram.request() as turno:
        yield turno
        yield env.timeout(tamanioProceso)
        print ("El proceso sale de la ram")
    
    return

def Ready():
    return

def Running():
    return

#-----SIMULACION-----

env = simpy.Enviroment()
ram = simpy.Resource(env, capacity = 100)
