CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `view_pacientes` AS
    SELECT
		`p`.`maxVisitas` AS `maxVisitas`,
        `p`.`edadMin` AS `edadMin`,
        `p`.`edadMax` AS `edadMax`,
        `p`.`horarioInicio` AS `horarioInicio`,
        `p`.`horarioFin` AS `horarioFin`,
        `dp`.`nombrePersona` AS `nombrePersona`,
        `dp`.`apellidoPaterno` AS `apellidoPaterno`,
        `dp`.`apellidoMaterno` AS `apellidoMaterno`,
        `dp`.`fechaNacimiento` AS `fechaNacimiento`,
        `dp`.`telefono` AS `telefono`,
        `ep`.`estado` AS `estado`,
        COALESCE(`h`.`nombreHabitacion`, '') AS `nombreHabitacion`
    FROM
        ((((`paciente` `p`
        JOIN `datospersonales` `dp` ON (`p`.`idDatosPersonales` = `dp`.`idDatosPersonales`))
        JOIN `estadopaciente` `ep` ON (`p`.`idEstadoPaciente` = `ep`.`idEstadoPaciente`))
        LEFT JOIN `estancia` `e` ON (`p`.`idPaciente` = `e`.`idPaciente`))
        LEFT JOIN `habitacion` `h` ON (`e`.`idHabitacion` = `h`.`idHabitacion`))
	ORDER BY `p`.`idPaciente`