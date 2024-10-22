-- Creación de la base de datos
DROP DATABASE IF EXISTS gymynam;
CREATE DATABASE GymYNam;
USE GymYNam;

-- Tabla Clientes
CREATE TABLE Clientes (
    dni VARCHAR(9) PRIMARY KEY,  
    nombre VARCHAR(50) NOT NULL,
    estado_pago ENUM('pagado', 'moroso') DEFAULT 'moroso'
);

-- Tabla Maquinas
CREATE TABLE Maquinas (
    id_maquina INT AUTO_INCREMENT PRIMARY KEY, 
    nombre VARCHAR(50) NOT NULL
);

-- Tabla Reservas
CREATE TABLE Reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    dni_cliente VARCHAR(9) NOT NULL,  -- Referencia a dni de Clientes
    id_maquina INT NOT NULL,          -- Referencia a id_maquina de Maquinas
    dia_semana ENUM('lunes', 'martes', 'miércoles', 'jueves', 'viernes') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    
    -- Relacion con la tabla Clientes (referencia la columna dni_cliente)
    FOREIGN KEY (dni_cliente) REFERENCES Clientes(dni),
    -- Relacion con la tabla Maquinas (referencia la columna id_maquina)
    FOREIGN KEY (id_maquina) REFERENCES Maquinas(id_maquina),
	-- Restriccion para asegurarse de que la hora_fin sea siempre 30 minutos despues de la hora_inicio
    CONSTRAINT CHK_HoraFin CHECK (hora_fin = ADDTIME(hora_inicio, '00:30:00'))
);

-- Inserción de datos en la tabla Clientes
INSERT INTO Clientes (dni, nombre, estado_pago)
VALUES 
('12345678A', 'Juan', 'pagado'),
('87654321B', 'Ana', 'moroso'),
('98765432C', 'Carlos', 'pagado');

-- Inserción de datos en la tabla Maquinas 
INSERT INTO Maquinas (nombre)
VALUES
('El paritorio'),
('Mancuernas'),
('Press de Banca');

-- Insercion de datos en la tabla Reservas
INSERT INTO Reservas (dni_cliente, id_maquina, dia_semana, hora_inicio, hora_fin)
VALUES
('12345678A', 1, 'lunes', '0900', '0930'),
('87654321B', 2, 'martes', '1000', '1030'),
('98765432C', 1, 'miércoles', '1100', '1130');

-- Consultas útiles:
-- Obtener el listado de maquinas ocupadas por dia y cliente
SELECT * FROM Clientes;
SELECT c.nombre, m.nombre AS maquina, r.dia_semana, r.hora_inicio, r.hora_fin
FROM Reservas r
JOIN Clientes c ON r.dni_cliente = c.dni  
JOIN Maquinas m ON r.id_maquina = m.id_maquina
ORDER BY r.dia_semana, r.hora_inicio;

-- Obtener el listado de clientes morosos
SELECT nombre
FROM Clientes
WHERE estado_pago = 'moroso';