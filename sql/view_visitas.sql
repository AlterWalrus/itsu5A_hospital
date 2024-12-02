CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `view_visitas` AS
    SELECT 
        `v`.`entrada` AS `entrada`,
        `v`.`salida` AS `salida`,
        CASE
            WHEN `med`.`idMedico` IS NOT NULL THEN 'medico'
            WHEN `enf`.`idEnfermero` IS NOT NULL THEN 'enfermero'
            WHEN `vis`.`idVisitante` IS NOT NULL THEN 'visitante'
            ELSE 'unknown'
        END AS `tipo`,
        COALESCE(`med_rfid`.`codigoRFID`,
                `enf_rfid`.`codigoRFID`,
                `vis_rfid`.`codigoRFID`) AS `visitaRFID`,
        COALESCE(`med_data`.`nombrePersona`,
                `enf_data`.`nombrePersona`,
                `vis_data`.`nombrePersona`) AS `visitaNombre`,
        COALESCE(`med_data`.`apellidoPaterno`,
                `enf_data`.`apellidoPaterno`,
                `vis_data`.`apellidoPaterno`) AS `visitaApellido`,
        `habi`.`nombreHabitacion` AS `pacienteHabitacion`,
        `pac_data`.`nombrePersona` AS `pacienteNombre`,
        `pac_data`.`apellidoPaterno` AS `pacienteApellido`
    FROM
        ((((((((((((`visita` `v`
        JOIN `paciente` `p` ON (`v`.`idPaciente` = `p`.`idPaciente`))
        JOIN `datospersonales` `pac_data` ON (`p`.`idDatosPersonales` = `pac_data`.`idDatosPersonales`))
        JOIN `habitacion` `habi` ON (`v`.`idHabitacion` = `habi`.`idHabitacion`))
        LEFT JOIN `medico` `med` ON (`v`.`idCodigoRFID` = `med`.`idCodigoRFID`))
        LEFT JOIN `datospersonales` `med_data` ON (`med`.`idDatosPersonales` = `med_data`.`idDatosPersonales`))
        LEFT JOIN `codigorfid` `med_rfid` ON (`med`.`idCodigoRFID` = `med_rfid`.`idCodigoRFID`))
        LEFT JOIN `enfermero` `enf` ON (`v`.`idCodigoRFID` = `enf`.`idCodigoRFID`))
        LEFT JOIN `datospersonales` `enf_data` ON (`enf`.`idDatosPersonales` = `enf_data`.`idDatosPersonales`))
        LEFT JOIN `codigorfid` `enf_rfid` ON (`enf`.`idCodigoRFID` = `enf_rfid`.`idCodigoRFID`))
        LEFT JOIN `visitante` `vis` ON (`v`.`idCodigoRFID` = `vis`.`idCodigoRFID`))
        LEFT JOIN `datospersonales` `vis_data` ON (`vis`.`idDatosPersonales` = `vis_data`.`idDatosPersonales`))
        LEFT JOIN `codigorfid` `vis_rfid` ON (`vis`.`idCodigoRFID` = `vis_rfid`.`idCodigoRFID`))
    WHERE
        `med`.`idMedico` IS NOT NULL
            OR `vis`.`idVisitante` IS NOT NULL
            OR `enf`.`idEnfermero` IS NOT NULL
	ORDER BY `v`.`idVisita`