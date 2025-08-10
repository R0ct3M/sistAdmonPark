import datetime
import re
import math

# Variables Globales
parkCarros = []
capacidadCarros = 3
capacidadMotos = 3

#valida formato de placa de carro, ejemplo MOX245
def validarPlacaCarro(placa):
    return re.match(r'^[A-Z]{3}\d{3}$', placa.upper())

#valida formato de placa de carro, ejemplo MOX24G
def validarPlacaMoto(placa):
    return re.match(r'^[A-Z]{3}\d{2}[A-Z]$', placa.upper())

#Verifica si hay espacio dispobible en el parqueadero.
def verificarEspacio(tipoVehiculo):
    tipoVehiculo = tipoVehiculo.lower()

    nroCarros = sum(1 for v in parkCarros if v["datosFijos"][1].lower() == "carro")
    nroMotos = sum(1 for v in parkCarros if v["datosFijos"][1].lower() == "moto")

    if tipoVehiculo == "carro" and nroCarros < capacidadCarros:
        return True
    if tipoVehiculo == "moto" and nroMotos < capacidadMotos:
        return True

    return False

#Verifica si el vehículo ya está estacionado.
def verificarVehiculoEstacionado(placa):
    for vehiculo in parkCarros:
        if vehiculo["datosFijos"][0].upper() == placa.upper():
            return True
    return False

#Calcula el tiempo total en horas: entrada - salida.
def calcularTiempo(horaEntrada, horaSalida):
    tiempoVehiculoParqueadero = horaSalida - horaEntrada
    # Se pasa a horas y se redondea.
    tiempoTotal = (tiempoVehiculoParqueadero.total_seconds() / 3600)
    # Se cobra por hora.
    if tiempoTotal <= 0.25:
        return 0
    else:
        return max(1, math.ceil(tiempoTotal))

    #return max(1, math.ceil(tiempoTotal))

#Calcula y muestra el valor a pagar por el estacionamiento.
def calcularTarifa(vehiculo, tiempo):
    tarifaCarroHora = 4000
    tarifaEstandarCarro = 20000
    tarifaMotoHora = 2000
    tarifaEstandarMoto = 10000

    placa, tipo = vehiculo["datosFijos"]
    tarifaTotal = 0

    if tiempo > 5:
        if tipo.lower() == "carro":
            tarifaTotal = tarifaEstandarCarro
        else:
            tarifaTotal = tarifaEstandarMoto
    elif tipo.lower() == "carro":
        tarifaTotal = tarifaCarroHora * tiempo
    else:
        tarifaTotal = tarifaMotoHora * tiempo

    print(f"Valor a pagar -> Tipo: {tipo.lower()} con placa {placa}: ${tarifaTotal:,.0f}.")

#Registra la entrada de un nuevo vehículo al parqueadero.
def registrarVehiculo():
    tipoVehiculo = input("Ingrese el tipo de vehículo (Carro o Moto): ").strip()

    if tipoVehiculo.lower() not in ("carro", "moto"):
        print("Error: Ingrese si es 'Carro' o 'Moto'.")
        return

    placa = input("Ingrese la placa: ").strip().upper()

    # Valida placas moto - carro
    if tipoVehiculo.lower() == "carro" and not validarPlacaCarro(placa):
        print("Error: Ingrese una placa correcta (ej. MOX245).")
        return

    if tipoVehiculo.lower() == "moto" and not validarPlacaMoto(placa):
        print("Error: Ingrese una placa correcta (ej. MOX24E).")
        return

    # Valida si el vehículo ya ingresó
    if verificarVehiculoEstacionado(placa):
        print(f"Error: El vehículo con placa {placa} ya está estacionado.")
        return

    # Validar disponibilidad de espacio
    if not verificarEspacio(tipoVehiculo):
        print("Error: Parqueadero lleno. No se puede ingresar.")
        return

    # Registro exitoso
    horaIngreso = datetime.datetime.now()
    vehiculo = {
        "horaEntrada": horaIngreso,
        "horaSalida": None,
        "datosFijos": (placa, tipoVehiculo) #Tupla
    }
    parkCarros.append(vehiculo) #Se agrega el vehículo a la lista
    print(
        f"✅ ¡Registro exitoso! Su {tipoVehiculo.lower()} con placa {placa}. Hora de ingreso: {horaIngreso.strftime('%I:%M %p')}.")

#Registra de salida y calculo de valor a pagar.
def registrarSalida():
    placa = input("Ingrese la placa: ").strip().upper()

    vehiculoEncontrado = None
    for v in parkCarros:
        if v["datosFijos"][0] == placa:
            vehiculoEncontrado = v
            break

    if not vehiculoEncontrado:
        print(f"Error: No se encontró un vehículo de la placa {placa}.")
        return

    horaSalida = datetime.datetime.now()
    vehiculoEncontrado["horaSalida"] = horaSalida

    horaEntrada = vehiculoEncontrado["horaEntrada"]
    tiempoTotal = calcularTiempo(horaEntrada, horaSalida)

    if tiempoTotal == 0:
        print("Tiempo de gracia. Puede salir")
    else:
        print(f"Salida: {placa} -> Hora: {horaSalida.strftime('%I:%M %p')}.")
        print(f"Tiempo total: {tiempoTotal} horas.")

    calcularTarifa(vehiculoEncontrado, tiempoTotal)

    parkCarros.remove(vehiculoEncontrado)

#Muestra una lista de todos los vehículos actualmente estacionados.
def verVehiculosEstacionados():
    if not parkCarros:
        print("No hay vehículos estacionados en este momento.")
    else:
        print("=== VEHÍCULOS ESTACIONADOS ===")
        for vehiculo in parkCarros:
            placa, tipo = vehiculo["datosFijos"]
            entrada = vehiculo["horaEntrada"].strftime('%d-%m-%Y %I:%M %p')
            print(f"Placa: {placa}, Tipo: {tipo}, Hora de entrada: {entrada}")


# --- Bucle principal ---
if __name__ == '__main__':
    opcion = ""
    while opcion != "4":
        print("\n" + "=" * 25)
        print("--- MENÚ PARQUEADERO ---")
        print("=" * 25)
        print("1. Ingreso")
        print("2. Salida")
        print("3. Ver vehículos estacionados")
        print("4. Salir del menú")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrarVehiculo()
        elif opcion == "2":
            registrarSalida()
        elif opcion == "3":
            verVehiculosEstacionados()
        elif opcion == "4":
            print("Vuelva Pronto...")
        else:
            print("Opción no válida. Intente de nuevo.")