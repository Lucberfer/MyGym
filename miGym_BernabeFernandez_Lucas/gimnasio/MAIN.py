from GestionGym import GestionGym


def menu_usuario(gestion):
    while True:
        print("\n Menú Usuario")
        print("1. Reservar máquina.")
        print("2. Ver ocupación.")
        print("3. Ver ocupación por día.")
        print("4. --SALIR--")
        opcion = input("Seleccione una opción: ")

        opciones_usuario = {
            '1': lambda: gestion.reservar(
                input("Introduzca el DNI del socio: "),
                int(input("Introduzca el ID de la máquina: ")),
                input("Introduzca el día de la semana (Lunes a Viernes): "),
                int(input("Introduzca la hora de inicio (HHMM): "))
            ),
            '2': lambda: gestion.ver_ocupacion(),
            '3': lambda: gestion.ver_ocupacion_por_dia(input("Introduzca el día a consultar: ")),
            '4': lambda: print("Saliendo del menú de usuario.")
        }

        if opcion in opciones_usuario:
            opciones_usuario[opcion]()
            if opcion == '4':
                break
        else:
            print("Opción no válida. Introduzca un número correcto.")


def menu_admin(gestion):
    while True:
        print("\n Menú Admin")
        print("1. Agregar socio.")
        print("2. Agregar máquina.")
        print("3. Ver ocupación.")
        print("4. Ver ocupación por día.")
        print("5. Generar recibo.")
        print("6. Lista de morosos")
        print("7. --SALIR--")
        opcion = input("Seleccione una opción: ")

        opciones_admin = {
            '1': lambda: gestion.agregar_socio(
                input("Introduzca el DNI del socio: "),
                input("Introduzca el nombre del socio: "),
                input("Estado de pago (pagado/moroso): ")
            ),
            # Otros métodos...
            '6': gestion.lista_morosos,  # Asegúrate de que esto esté correcto
            '7': lambda: print("Saliendo del menú de admin.")
        }

        if opcion in opciones_admin:
            opciones_admin[opcion]()  # Llama a la función correspondiente
            if opcion == '7':  # Si se selecciona salir, se termina el bucle
                break
        else:
            print("Opción no válida. Introduzca un número correcto")

def MAIN():
    gestion = GestionGym()
    while True:
        print("\n Menú Principal")
        print("Seleccione categoría:")
        print("1. Usuario")
        print("2. Administrador")
        print("3. --SALIR--")
        opcion = input("Ingrese el número correspondiente: ")

        if opcion == '1':
            menu_usuario(gestion)
        elif opcion == '2':
            menu_admin(gestion)
        elif opcion == '3':
            print("Salimos mi gente.")
            break
        else:
            print("Opción no válida. Introduzca '1' para Usuario o '2' para Administrador.")

if __name__ == "__main__":
    MAIN()
