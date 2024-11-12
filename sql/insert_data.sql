insert into admin(nombreAdmin, contrasenia) values('Israel Arroyo', '987');
insert into admin(nombreAdmin, contrasenia) values('Omar Paz', '654');
insert into admin(nombreAdmin, contrasenia) values('Rubén Zamudio', '321');

insert into habitacion(nombreHabitacion) values('A1');

insert into codigorfid(codigorfid) values('D3210225');

insert into datospersonales(nombrepersona, apellidopaterno, apellidomaterno, fechanacimiento, telefono)
values('Pepito', 'Ramirez', 'Tomate', '2000-12-12', '4521231234');
insert into datospersonales(nombrepersona, apellidopaterno, apellidomaterno, fechanacimiento, telefono)
values('Lola', 'La', 'Trailera', '1996-06-09', '4520101010');

insert into horario(horarioinicio, horariofin) values('12:00', '5:00');

insert into paciente(maxvisitas, iddatospersonales, idhabitacion, idhorario)
values(1, 1, 1, 1);

insert into visitante(iddatospersonales, idcodigorfid) values(2, 1);