DROP TRIGGER IF EXISTS on_insert_paciente;
DROP TRIGGER IF EXISTS on_delete_paciente;
DROP TRIGGER IF EXISTS on_update_paciente;

DROP TRIGGER IF EXISTS on_delete_medico;
DROP TRIGGER IF EXISTS on_delete_enfermero;
DROP TRIGGER IF EXISTS on_delete_visitante;

-- PACIENTE
DELIMITER //
CREATE TRIGGER on_insert_paciente
BEFORE INSERT ON paciente
FOR EACH ROW
BEGIN
	UPDATE habitacion
    SET disponible = 'NO'
    WHERE idHabitacion = NEW.idHabitacion;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER on_delete_paciente
BEFORE DELETE ON paciente
FOR EACH ROW
BEGIN
	UPDATE habitacion
    SET disponible = 'SI'
    WHERE idHabitacion = OLD.idHabitacion;
    
    DELETE FROM datospersonales
    WHERE iddatospersonales = OLD.iddatospersonales;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER on_update_paciente
BEFORE UPDATE ON paciente
FOR EACH ROW
BEGIN
	IF OLD.idHabitacion <> NEW.idHabitacion THEN
		UPDATE habitacion
		SET disponible = 'SI'
		WHERE idHabitacion = OLD.idHabitacion;
    END IF;
    
    UPDATE habitacion
    SET disponible = 'NO'
    WHERE idHabitacion = NEW.idHabitacion;
END //
DELIMITER ;

-- LOS DEMAS XD
DELIMITER //
CREATE TRIGGER on_delete_medico
BEFORE DELETE ON medico
FOR EACH ROW
BEGIN
    DELETE FROM datospersonales
    WHERE iddatospersonales = OLD.iddatospersonales;
    DELETE FROM codigorfid
    WHERE idCodigoRFID = OLD.idCodigoRFID;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER on_delete_enfermero
BEFORE DELETE ON enfermero
FOR EACH ROW
BEGIN
    DELETE FROM datospersonales
    WHERE iddatospersonales = OLD.iddatospersonales;
    DELETE FROM codigorfid
    WHERE idCodigoRFID = OLD.idCodigoRFID;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER on_delete_visitante
BEFORE DELETE ON visitante
FOR EACH ROW
BEGIN
    DELETE FROM datospersonales
    WHERE iddatospersonales = OLD.iddatospersonales;
    DELETE FROM codigorfid
    WHERE idCodigoRFID = OLD.idCodigoRFID;
END //
DELIMITER ;
