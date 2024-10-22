import mysql.connector
from Reserva import reserva
from Maquina import maquina
from Socio import socio

class GestionGym:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="Lucas",
                password="",
                database="GymYNam"
            )
            self.cursor = self.conn.cursor()
            print("Conexión exitosa.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.conn = None
            self.cursor = None

    def agregar_socio(self, dni, nombre, estado_pago):
        if self.cursor is None:
            print("No se puede agregar socio porque la conexión es inválida.")
            return

        sql = "INSERT INTO Clientes (dni, nombre, estado_pago) VALUES (%s, %s, %s)"
        values = (dni, nombre, estado_pago)
        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            print("Socio agregado con éxito.")
        except mysql.connector.Error as err:
            print(f"Error al agregar socio: {err}")

    def agregar_maquina(self, nombre):
        sql = "INSERT INTO Maquinas (nombre) VALUES (%s)"
        self.cursor.execute(sql, (nombre,))
        self.conn.commit()
        print(f"Máquina '{nombre}' agregada a la base de datos.")

    def reservar(self, dni_cliente, id_maquina, dia_semana, hora_inicio, hora_fin):

        # Calcula la hora de fin sumando 30 minutos (en HHMM)
        hora_fin = int(hora_inicio) + 30

        if hora_fin % 100 >= 60:  # Si los minutos son 60 o más
            hora_fin += 40  # Sumar 40 para corregir a la siguiente hora y ajustar los minutos

        # Verifica si la máquina está disponible
        if not self.buscarMaquina(id_maquina).disponible(hora_inicio):
            print("Máquina no disponible.")
            return

        # Crear la nueva reserva
        nueva_reserva = reserva(dni_cliente, id_maquina, dia_semana, hora_inicio, hora_fin)
        self.buscarMaquina(id_maquina).reservar(nueva_reserva)
        print(
            f"Reserva confirmada para el socio {dni_cliente} en la máquina {id_maquina} el {dia_semana} desde {hora_inicio} hasta {hora_fin}.")

    def calculate_hora_fin(self, hora_inicio):
        from datetime import datetime, timedelta
        hora_inicio_dt = datetime.strptime(hora_inicio, '%H:%M:%S')
        hora_fin_dt = hora_inicio_dt + timedelta(minutes=30)
        return hora_fin_dt.strftime('%H:%M:%S')

    def ver_ocupacion(self):
        query = """
        SELECT c.nombre AS socio, m.nombre AS maquina, r.dia_semana, r.hora_inicio, r.hora_fin
        FROM Reservas r
        JOIN Clientes c ON r.dni_cliente = c.dni_cliente  
        JOIN Maquinas m ON r.id_maquina = m.id_maquina
        ORDER BY r.dia_semana, r.hora_inicio;
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        for row in results:
            print(f"Socio: {row[0]}, Máquina: {row[1]}, Día: {row[2]}, Desde: {row[3]} Hasta: {row[4]}")

    def ver_ocupacion_por_dia(self, dia):
        query = """
        SELECT c.nombre AS socio, m.nombre AS maquina, r.hora_inicio, r.hora_fin
        FROM Reservas r
        JOIN Clientes c ON r.dni_cliente = c.dni_cliente  
        JOIN Maquinas m ON r.id_maquina = m.id_maquina
        WHERE r.dia_semana = %s
        ORDER BY r.hora_inicio;
        """
        self.cursor.execute(query, (dia,))
        results = self.cursor.fetchall()
        if not results:
            print(f"No hay reservas para el día {dia}.")
            return
        for row in results:
            print(f"Socio: {row[0]}, Máquina: {row[1]}, Desde: {row[2]} Hasta: {row[3]}")

    def generar_recibo(self, dni):
        query = "SELECT nombre FROM Clientes WHERE dni_cliente = %s AND estado_pago = 'moroso';"
        self.cursor.execute(query, (dni,))
        result = self.cursor.fetchone()
        if result:
            print(f"Recibo generado para el socio: {result[0]}.")
        else:
            print("No hay recibos pendientes para este socio.")

    def lista_morosos(self):
        query = "SELECT nombre FROM Clientes WHERE estado_pago = 'moroso';"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        print("Socios morosos:")
        for row in results:
            print(row[0])

    def socio_existe(self, dni):
        query = "SELECT COUNT(*) FROM Clientes WHERE dni_cliente = %s;"
        self.cursor.execute(query, (dni,))
        return self.cursor.fetchone()[0] > 0

    def maquina_existe(self, id_maquina):
        query = "SELECT COUNT(*) FROM Maquinas WHERE id_maquina = %s;"
        self.cursor.execute(query, (id_maquina,))
        return self.cursor.fetchone()[0] > 0

    def maquina_disponible(self, id_maquina, dia_semana, hora_inicio, hora_fin):
        query = """
        SELECT COUNT(*) FROM Reservas
        WHERE id_maquina = %s AND dia_semana = %s
        AND (hora_inicio < %s AND hora_fin > %s);
        """
        self.cursor.execute(query, (id_maquina, dia_semana, hora_fin, hora_inicio))
        return self.cursor.fetchone()[0] == 0

    def cerrar_conexion(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
