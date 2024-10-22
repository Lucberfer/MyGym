
class reserva:
    def __init__(self, dni_cliente, id_maquina, dia_semana, hora_inicio, hora_fin):
        # Inicializa la reserva con socio, hora de inicio y día
        self.dni_cliente = dni_cliente
        self.id_maquina = id_maquina
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio  # HHMM
        self.hora_fin = hora_fin  # HHMM

    def __str__(self):
        # Retorna una representación en cadena de la reserva
        return f"Reserva: Cliente DNI {self.dni_cliente}, Máquina {self.id_maquina}, Día: {self.dia_semana}, De: {self.hora_inicio} a {self.hora_fin}"
