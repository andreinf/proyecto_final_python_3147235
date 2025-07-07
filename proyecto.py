

import json

# ---------- Clase Direccion ----------
class Direccion:
    def __init__(self, calle, ciudad, codigo_postal):
        self.calle = calle
        self.ciudad = ciudad
        self.codigo_postal = codigo_postal

    def __str__(self):
        return f"{self.calle}, {self.ciudad}, CP: {self.codigo_postal}"


# ---------- Clase Cliente ----------
class Cliente:
    def __init__(self, nombre, direccion):
        self.__nombre = nombre
        self.__direccion = direccion

    def get_nombre(self):
        return self.__nombre

    def get_direccion(self):
        return self.__direccion

    def __str__(self):
        return f"{self.__nombre} - Dirección: {self.__direccion}"


# ---------- Clase base Paquete ----------
class Paquete:
    def __init__(self, peso, descripcion):
        self._peso = peso
        self.descripcion = descripcion
        self.estado = "Pendiente"

    def set_estado(self, nuevo_estado):
        if nuevo_estado in ["Pendiente", "En tránsito", "Entregado"]:
            self.estado = nuevo_estado
        else:
            raise ValueError("Estado inválido")

    def calcular_precio(self):
        raise NotImplementedError("Debe ser implementado en la subclase")

    def __str__(self):
        return f"{self.descripcion} ({self.estado}) - {self._peso}kg"


# ---------- Subclases ----------
class PaqueteEstandar(Paquete):
    def calcular_precio(self):
        return 5 * self._peso


class PaqueteExpress(Paquete):
    def calcular_precio(self):
        return 8 * self._peso + 10


# ---------- Clase Envio ----------
class Envio:
    def __init__(self, cliente, paquete):
        self.cliente = cliente
        self.paquete = paquete

    def calcular_precio(self):
        return self.paquete.calcular_precio()

    def __str__(self):
        return f"Envío a {self.cliente.get_nombre()} - {self.paquete} - Precio: ${self.calcular_precio()}"


# ---------- Clase SistemaEnvios ----------
class SistemaEnvios:
    def __init__(self):
        self.clientes = []
        self.envios = []

    def registrar_cliente(self, nombre, calle, ciudad, codigo_postal):
        direccion = Direccion(calle, ciudad, codigo_postal)
        cliente = Cliente(nombre, direccion)
        self.clientes.append(cliente)

    def obtener_cliente(self, nombre):
        for c in self.clientes:
            if c.get_nombre() == nombre:
                return c
        return None

    def registrar_envio(self, nombre_cliente, paquete):
        cliente = self.obtener_cliente(nombre_cliente)
        if cliente:
            envio = Envio(cliente, paquete)
            self.envios.append(envio)
        else:
            print(" Cliente no encontrado.")

    def mostrar_envios(self):
        if not self.envios:
            print(" No hay envíos registrados.")
        for e in self.envios:
            print(e)

    def guardar_json(self, ruta="envios.json"):
        data = [{
            "cliente": e.cliente.get_nombre(),
            "direccion": str(e.cliente.get_direccion()),
            "descripcion": e.paquete.descripcion,
            "estado": e.paquete.estado,
            "precio": e.calcular_precio()
        } for e in self.envios]
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f" Información guardada en '{ruta}'")

    def resumen_por_tipo(self):
        total_estandar = sum(e.calcular_precio() for e in self.envios if isinstance(e.paquete, PaqueteEstandar))
        total_express = sum(e.calcular_precio() for e in self.envios if isinstance(e.paquete, PaqueteExpress))
        print(f" Total ventas estándar: ${total_estandar}")
        print(f" Total ventas express: ${total_express}")


# ---------- Menú interactivo ----------
def menu():
    sistema = SistemaEnvios()

    while True:
        print("\n MENÚ DEL SISTEMA DE ENVÍOS")
        print("1. Registrar cliente")
        print("2. Crear paquete estándar")
        print("3. Crear paquete express")
        print("4. Ver envíos")
        print("5. Guardar en archivo")
        print("6. Ver resumen por tipo")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre del cliente: ")
            calle = input("Calle: ")
            ciudad = input("Ciudad: ")
            cp = input("Código Postal: ")
            sistema.registrar_cliente(nombre, calle, ciudad, cp)

        elif opcion == "2":
            nombre = input("Nombre del cliente: ")
            peso = float(input("Peso del paquete (kg): "))
            desc = input("Descripción del paquete: ")
            paquete = PaqueteEstandar(peso, desc)
            sistema.registrar_envio(nombre, paquete)

        elif opcion == "3":
            nombre = input("Nombre del cliente: ")
            peso = float(input("Peso del paquete (kg): "))
            desc = input("Descripción del paquete: ")
            paquete = PaqueteExpress(peso, desc)
            sistema.registrar_envio(nombre, paquete)

        elif opcion == "4":
            sistema.mostrar_envios()

        elif opcion == "5":
            sistema.guardar_json()

        elif opcion == "6":
            sistema.resumen_por_tipo()

        elif opcion == "0":
            print("👋 Saliendo del sistema.")
            break

        else:
            print("⚠️ Opción inválida. Intente nuevamente.")


# 🔃 Ejecutar el menú
if __name__ == "__main__":
    menu()
