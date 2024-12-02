DROP TRIGGER IF EXISTS on_insert_estancia;
DROP TRIGGER IF EXISTS on_delete_estancia;
DROP TRIGGER IF EXISTS on_update_estancia;

DROP TRIGGER IF EXISTS on_delete_medico;
DROP TRIGGER IF EXISTS on_delete_enfermero;
DROP TRIGGER IF EXISTS on_delete_visitante;

-- PACIENTE (Actualizar disponibilidad de habitaciones cada q metamos a un wn ahi)
DELIMITER //
CREATE TRIGGER on_insert_estancia
BEFORE INSERT ON estancia
FOR EACH ROW
BEGIN
	UPDATE habitacion
    SET disponible = 'NO'
    WHERE idHabitacion = NEW.idHabitacion;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER on_delete_estancia
BEFORE DELETE ON estancia
FOR EACH ROW
BEGIN
	UPDATE habitacion
    SET disponible = 'SI'
    WHERE idHabitacion = OLD.idHabitacion;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER on_update_estancia
BEFORE UPDATE ON estancia
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
