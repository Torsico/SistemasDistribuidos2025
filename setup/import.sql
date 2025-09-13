use dist2025;

-- Roles
INSERT INTO rol (nombre) VALUES
	("Presidente"),
	("Vocal"),
	("Coordinador"),
	("Voluntario");

-- Usuario
INSERT INTO usuario (nombreUsuario, nombre, apellido, email, rol, clave, telefono, activo)
VALUES ('jdoe', 'John', 'Doe', 'jdoe@mail.com', 1, '1234', '1111-1111', 1),
       ('mlopez', 'Maria', 'Lopez', 'mlopez@mail.com', 2, 'abcd', '2222-2222', 1);

-- Donaciones
INSERT INTO donaciones (categoria, descripcion, cantidad, eliminado, hora_alta, hora_mod, usuario_alta, usuario_mod)
VALUES ('Ropa', 'Camperas de abrigo', 10, 0, '2025-09-01 10:00:00', '2025-09-01 11:00:00', 1, 2),
       ('Alimentos', 'Paquetes de arroz', 25, 0, '2025-09-05 09:30:00', '2025-09-05 09:45:00', 2, 2);

-- Eventos
INSERT INTO eventos (nombre, descripcion, fechaHora)
VALUES ('Colecta Escolar', 'Recolección de útiles escolares', '2025-10-01'),
       ('Campaña de Invierno', 'Entrega de ropa de abrigo', '2025-07-15');

-- Relación donaciones-eventos
INSERT INTO donaciones_has_eventos (donaciones_iddonaciones, eventos_ideventos)
VALUES (1, 1),
       (2, 2);