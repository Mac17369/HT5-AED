#Kevin Macario 17369
#Rodrigo Urrutia
#Clase Principal

#import SistemaOperativo
#import Procesos
import simpy
import math
import random 

#-----VARIABLES---

#PROCESOS
#Cantidad maxima de instrucciones por proceso. 
instrucciones = 10
#cantidad de procesos que se crearan
procesos_totales = 25
# unidad de tiempo que abarca un proceso
procesos_tiempo = 1
#Contador de tiempo total que se tardan los procesos
tiempo_acumulado = 0.0
#contador que calcula el promedio de tiempo de ejecucion
promedio = 0.0 

#RAM
#espacio de memoria RAM
RAM_memoria = 100


#CPU
# instrucciones máximas que ejecuta la CPU
instruccionesMAX = 3
#Tiempo al azar de espera mientras espera al CPU
tiempoEspera= 10

#semilla inicial para los numeros al azar
RANDOM_SEED = 127

cola = []

#-----METODOS-----

def New(env, num_proceso, unidades, ram, io, mem, instrucciones):
    init = int(env.now)
    print('Proceso %s - creado                                 TIEMPO %s' %(num_proceso,init))
    print('Proceso %s - tiene %s instrucciones' %(num_proceso,instrucciones))
    global tiempo_acumulado, procesos_tiempo, instruccionesMAX

    with ram.get(instrucciones) as req:
        yield req
        initready = int(env.now)
        print('Proceso %s - entra a READY                          TIEMPO %s' %(num_proceso,initready))

        while(instrucciones >0):
            with unidades.request() as req2:
                yield req2
                initprocesos = int(env.now)
                print('Proceso %s - 3 instrucciones ejecutadas             TIEMPO %s' %(num_proceso,initprocesos))
                instrucciones -= 3
                if(instrucciones<=0):
                    print('Proceso %s - tiene 0 instrucciones pendientes' %(num_proceso))
                    print('Proceso %s - TERMINATED' %(num_proceso))
                else:
                    print('Proceso %s - tiene %s instrucciones pendientes' %(num_proceso,instrucciones))
                ram.put(3)

                if(random.randint(1,2)==1):
                # Si el Random es 2, el proceso sigue dentro del CPU
                    with io.request() as req3:
                        yield req3
                        initIO = int(env.now)
                        print('Proceso %s - sale de CPU y entra a WAITING          TIEMPO %s' % (num_proceso,initIO))
                        tiempoesperaIO = random.randint(1,tiempoEspera)
                        yield env.timeout(tiempoesperaIO)
                        salidaIO = int(env.now)
                        procesos_tiempo = salidaIO - init
                        cola.append(salidaIO)
                        print('Proceso %s - sale de WAITING y entra a READY        TIEMPO %s' % (num_proceso,salidaIO))

        yield env.timeout(procesos_tiempo)
        exitprocesos = int(env.now)
        tiempo_acumulado = tiempo_acumulado + exitprocesos - init



def Ready(env, cantidad, capacidad, unidades,io,ram):
    global instrucciones
    for i in range(cantidad):
        memoria = random.randint(1,instruccionesMAX)
        instruc = random.randint(1,instrucciones)
        nuevo_proceso = New(env,str(i+1),unidades,ram,io,memoria,instruc)
        env.process(nuevo_proceso)
        temptime = random.expovariate(1.0/capacidad)
        yield env.timeout(temptime)
        
#-----SIMULACION-----

env = simpy.Environment()
random.seed(RANDOM_SEED)
procesador = simpy.Resource(env, capacity=1) # Se emplea solo 1 procesador
ram_TOTAL = simpy.Container(env, capacity=RAM_memoria,init= RAM_memoria)
io = simpy.Resource(env, capacity=1) # Solo un input/output a la vez

env.process(Ready(env,procesos_totales,instruccionesMAX,procesador,io,ram_TOTAL))

env.run()
promedio = tiempo_acumulado/procesos_totales
print('Promedio de tiempo de ejecución %s' % (promedio))

