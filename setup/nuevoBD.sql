-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema dist2025
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dist2025` DEFAULT CHARACTER SET utf8mb3 ;
USE `dist2025` ;

-- -----------------------------------------------------
-- Table `dist2025`.`rol`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`rol` (
  `idrol` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idrol`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dist2025`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`usuario` (
  `idusuario` INT NOT NULL AUTO_INCREMENT,
  `nombreUsuario` VARCHAR(45) NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `rol` INT NOT NULL,
  `clave` VARCHAR(100) NULL DEFAULT NULL,
  `telefono` VARCHAR(45) NULL DEFAULT NULL,
  `activo` TINYINT NULL DEFAULT NULL,
  PRIMARY KEY (`idusuario`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `nombreUsuario_UNIQUE` (`nombreUsuario` ASC) VISIBLE,
  INDEX `fk_usuario_rol1_idx` (`rol` ASC) VISIBLE,
  CONSTRAINT `fk_usuario_rol1`
    FOREIGN KEY (`rol`)
    REFERENCES `dist2025`.`rol` (`idrol`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dist2025`.`donaciones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`donaciones` (
  `iddonaciones` INT NOT NULL AUTO_INCREMENT,
  `categoria` VARCHAR(45) NOT NULL,
  `descripcion` VARCHAR(45) NOT NULL,
  `cantidad` INT NOT NULL,
  `eliminado` TINYINT NULL DEFAULT NULL,
  `fecha_alta` DATETIME NULL DEFAULT NULL,
  `fecha_mod` DATETIME NULL DEFAULT NULL,
  `usuario_alta` INT NOT NULL,
  `usuario_mod` INT NOT NULL,
  PRIMARY KEY (`iddonaciones`),
  INDEX `fk_donaciones_usuario1_idx` (`usuario_alta` ASC) VISIBLE,
  INDEX `fk_donaciones_usuario2_idx` (`usuario_mod` ASC) VISIBLE,
  CONSTRAINT `fk_donaciones_usuario1`
    FOREIGN KEY (`usuario_alta`)
    REFERENCES `dist2025`.`usuario` (`idusuario`),
  CONSTRAINT `fk_donaciones_usuario2`
    FOREIGN KEY (`usuario_mod`)
    REFERENCES `dist2025`.`usuario` (`idusuario`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dist2025`.`eventos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`eventos` (
  `ideventos` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `descripcion` VARCHAR(45) NOT NULL,
  `fechaHora` DATETIME NOT NULL,
  PRIMARY KEY (`ideventos`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dist2025`.`donaciones_has_eventos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`donaciones_has_eventos` (
  `donaciones_iddonaciones` INT NOT NULL,
  `eventos_ideventos` INT NOT NULL,
  `cantidad_donada` INT NOT NULL DEFAULT '0',
  PRIMARY KEY (`donaciones_iddonaciones`, `eventos_ideventos`),
  INDEX `fk_donaciones_has_eventos_eventos1_idx` (`eventos_ideventos` ASC) VISIBLE,
  INDEX `fk_donaciones_has_eventos_donaciones1_idx` (`donaciones_iddonaciones` ASC) VISIBLE,
  CONSTRAINT `fk_donaciones_has_eventos_donaciones1`
    FOREIGN KEY (`donaciones_iddonaciones`)
    REFERENCES `dist2025`.`donaciones` (`iddonaciones`),
  CONSTRAINT `fk_donaciones_has_eventos_eventos1`
    FOREIGN KEY (`eventos_ideventos`)
    REFERENCES `dist2025`.`eventos` (`ideventos`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dist2025`.`organizacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`organizacion` (
  `idOrganizacion` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`idOrganizacion`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dist2025`.`eventoExterno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`eventoExterno` (
  `idEventoExt` INT NOT NULL AUTO_INCREMENT,
  `idOrganizacion` INT NOT NULL,
  `ideventos` INT NOT NULL,
  `estado` VARCHAR(20) NOT NULL DEFAULT 'ACTIVO',
  PRIMARY KEY (`idEventoExt`),
  INDEX `IdOrganizacion` (`idOrganizacion` ASC) VISIBLE,
  INDEX `fk_eventoExterno_eventos1_idx` (`ideventos` ASC) VISIBLE,
  CONSTRAINT `evento_ibfk_1`
    FOREIGN KEY (`idOrganizacion`)
    REFERENCES `dist2025`.`organizacion` (`idOrganizacion`),
  CONSTRAINT `fk_eventoExterno_eventos1`
    FOREIGN KEY (`ideventos`)
    REFERENCES `dist2025`.`eventos` (`ideventos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dist2025`.`inventario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`inventario` (
  `idInventario` INT NOT NULL AUTO_INCREMENT,
  `idOrganizacion` INT NOT NULL,
  `categoria` VARCHAR(50) NULL DEFAULT NULL,
  `descripcion` VARCHAR(100) NULL DEFAULT NULL,
  `cantidad` INT NULL DEFAULT NULL,
  `unidad` VARCHAR(45) NULL,
  PRIMARY KEY (`idInventario`),
  UNIQUE INDEX `IdOrganizacion` (`idOrganizacion` ASC, `categoria` ASC, `descripcion` ASC) VISIBLE,
  CONSTRAINT `inventario_ibfk_1`
    FOREIGN KEY (`idOrganizacion`)
    REFERENCES `dist2025`.`organizacion` (`idOrganizacion`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dist2025`.`itemdonacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`itemdonacion` (
  `idItem` INT NOT NULL AUTO_INCREMENT,
  `idOrganizacion` INT NOT NULL,
  `categoria` VARCHAR(45) NULL,
  `descripcion` VARCHAR(45) NULL,
  `cantidad` INT NULL,
  `unidad` VARCHAR(45) NULL,
  PRIMARY KEY (`idItem`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dist2025`.`oferta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`oferta` (
  `idOferta` INT NOT NULL AUTO_INCREMENT,
  `idOrganizacionDonante` INT NOT NULL,
  PRIMARY KEY (`idOferta`),
  INDEX `IdOrganizacionDonante` (`idOrganizacionDonante` ASC) VISIBLE,
  CONSTRAINT `oferta_ibfk_1`
    FOREIGN KEY (`idOrganizacionDonante`)
    REFERENCES `dist2025`.`organizacion` (`idOrganizacion`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dist2025`.`participacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`participacion` (
  `usuario_idusuario` INT NOT NULL,
  `eventos_ideventos` INT NOT NULL,
  PRIMARY KEY (`usuario_idusuario`, `eventos_ideventos`),
  INDEX `fk_usuario_has_eventos_eventos1_idx` (`eventos_ideventos` ASC) VISIBLE,
  INDEX `fk_usuario_has_eventos_usuario1_idx` (`usuario_idusuario` ASC) VISIBLE,
  CONSTRAINT `fk_usuario_has_eventos_eventos1`
    FOREIGN KEY (`eventos_ideventos`)
    REFERENCES `dist2025`.`eventos` (`ideventos`),
  CONSTRAINT `fk_usuario_has_eventos_usuario1`
    FOREIGN KEY (`usuario_idusuario`)
    REFERENCES `dist2025`.`usuario` (`idusuario`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dist2025`.`solicitud`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`solicitud` (
  `idSolicitud` INT NOT NULL AUTO_INCREMENT,
  `idOrganizacionSolicitante` INT NOT NULL,
  `estado` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`idSolicitud`),
  INDEX `IdOrganizacionSolicitante` (`idOrganizacionSolicitante` ASC) VISIBLE,
  CONSTRAINT `solicitud_ibfk_1`
    FOREIGN KEY (`idOrganizacionSolicitante`)
    REFERENCES `dist2025`.`organizacion` (`idOrganizacion`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dist2025`.`voluntario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`voluntario` (
  `idVoluntario` INT NOT NULL AUTO_INCREMENT,
  `idOrganizacion` INT NOT NULL,
  `idusuario` INT NOT NULL,
  PRIMARY KEY (`idVoluntario`),
  INDEX `IdOrganizacion` (`idOrganizacion` ASC) VISIBLE,
  INDEX `fk_voluntario_usuario1_idx` (`idusuario` ASC) VISIBLE,
  CONSTRAINT `voluntario_ibfk_1`
    FOREIGN KEY (`idOrganizacion`)
    REFERENCES `dist2025`.`organizacion` (`idOrganizacion`),
  CONSTRAINT `fk_voluntario_usuario1`
    FOREIGN KEY (`idusuario`)
    REFERENCES `dist2025`.`usuario` (`idusuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `dist2025`.`adhesionevento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`adhesionevento` (
  `voluntario_IdVoluntario` INT NOT NULL,
  `eventoExterno_IdEventoExt` INT NOT NULL,
  PRIMARY KEY (`voluntario_IdVoluntario`, `eventoExterno_IdEventoExt`),
  INDEX `fk_voluntario_has_eventoExterno_eventoExterno1_idx` (`eventoExterno_IdEventoExt` ASC) VISIBLE,
  INDEX `fk_voluntario_has_eventoExterno_voluntario1_idx` (`voluntario_IdVoluntario` ASC) VISIBLE,
  CONSTRAINT `fk_voluntario_has_eventoExterno_voluntario1`
    FOREIGN KEY (`voluntario_IdVoluntario`)
    REFERENCES `dist2025`.`voluntario` (`idVoluntario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_voluntario_has_eventoExterno_eventoExterno1`
    FOREIGN KEY (`eventoExterno_IdEventoExt`)
    REFERENCES `dist2025`.`eventoExterno` (`idEventoExt`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
