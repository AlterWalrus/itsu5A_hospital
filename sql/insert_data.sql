insert into admin(nombreAdmin, contrasenia) values('Israel Arroyo', '987');
insert into admin(nombreAdmin, contrasenia) values('Omar Paz', '654');
insert into admin(nombreAdmin, contrasenia) values('Rubén Zamudio', '321');

insert into habitacion(nombreHabitacion) values('A1');
insert into habitacion(nombreHabitacion) values('A2');
insert into habitacion(nombreHabitacion) values('B3');
insert into habitacion(nombreHabitacion) values('B4');
insert into habitacion(nombreHabitacion) values('C5');

insert into codigorfid(codigorfid) values('D3210225');
insert into codigorfid(codigorfid) values('335A1FF8');

insert into datospersonales(nombrepersona, apellidopaterno, apellidomaterno, fechanacimiento, telefono)
values('Pepito', 'Ramirez', 'Tomate', '2000-12-12', '4521231234');
insert into datospersonales(nombrepersona, apellidopaterno, apellidomaterno, fechanacimiento, telefono)
values('Adolfo', 'Giterio', 'Moreno', '1988-08-08', '4520000000');
insert into datospersonales(nombrepersona, apellidopaterno, apellidomaterno, fechanacimiento, telefono)
values('Lola', 'La', 'Trailera', '1996-06-09', '4520101010');
insert into datospersonales(nombrepersona, apellidopaterno, apellidomaterno, fechanacimiento, telefono)
values('Claudette', 'Morel', 'na', '1998-08-12', '4522201220');

insert into paciente(maxvisitas, iddatospersonales, idhabitacion)
values(1, 1, 1);
insert into paciente(maxvisitas, iddatospersonales, idhabitacion)
values(2, 2, 2);

insert into visitante(iddatospersonales, idcodigorfid) values(3, 1);

insert into medico(cedula, iddatospersonales, idcodigorfid) values('10029292', 4, 2);

insert into visita(entrada, salida, idpaciente, idcodigorfid)
values('2024-11-14 10:10:00', '2024-11-14 10:15:00', 1, 1);