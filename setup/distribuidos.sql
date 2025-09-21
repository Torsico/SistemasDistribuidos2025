-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `dist2025`;
CREATE SCHEMA IF NOT EXISTS `dist2025` DEFAULT CHARACTER SET utf8 ;
USE `dist2025` ;

-- -----------------------------------------------------
-- Table `dist2025`.`rol`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`rol` (
  `idrol` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idrol`))
ENGINE = InnoDB;


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
  `clave` VARCHAR(100) NULL,
  `telefono` VARCHAR(45) NULL,
  `activo` TINYINT NULL,
  PRIMARY KEY (`idusuario`),
  INDEX `fk_usuario_rol1_idx` (`rol` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `nombreUsuario_UNIQUE` (`nombreUsuario` ASC) VISIBLE,
  CONSTRAINT `fk_usuario_rol1`
    FOREIGN KEY (`rol`)
    REFERENCES `dist2025`.`rol` (`idrol`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dist2025`.`donaciones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`donaciones` (
  `iddonaciones` INT NOT NULL AUTO_INCREMENT,
  `categoria` VARCHAR(45) NOT NULL,
  `descripcion` VARCHAR(45) NOT NULL,
  `cantidad` INT NOT NULL,
  `eliminado` TINYINT NULL,
  `fecha_alta` DATETIME NULL,
  `fecha_mod` DATETIME NULL,
  `usuario_alta` INT NOT NULL,
  `usuario_mod` INT NOT NULL,
  PRIMARY KEY (`iddonaciones`),
  INDEX `fk_donaciones_usuario1_idx` (`usuario_alta` ASC) VISIBLE,
  INDEX `fk_donaciones_usuario2_idx` (`usuario_mod` ASC) VISIBLE,
  CONSTRAINT `fk_donaciones_usuario1`
    FOREIGN KEY (`usuario_alta`)
    REFERENCES `dist2025`.`usuario` (`idusuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_donaciones_usuario2`
    FOREIGN KEY (`usuario_mod`)
    REFERENCES `dist2025`.`usuario` (`idusuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dist2025`.`eventos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`eventos` (
  `ideventos` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `descripcion` VARCHAR(45) NOT NULL,
  `fechaHora` DATETIME NOT NULL,
  PRIMARY KEY (`ideventos`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dist2025`.`donaciones_has_eventos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`donaciones_has_eventos` (
  `donaciones_iddonaciones` INT NOT NULL,
  `eventos_ideventos` INT NOT NULL,
  PRIMARY KEY (`donaciones_iddonaciones`, `eventos_ideventos`),
  INDEX `fk_donaciones_has_eventos_eventos1_idx` (`eventos_ideventos` ASC) VISIBLE,
  INDEX `fk_donaciones_has_eventos_donaciones1_idx` (`donaciones_iddonaciones` ASC) VISIBLE,
  CONSTRAINT `fk_donaciones_has_eventos_donaciones1`
    FOREIGN KEY (`donaciones_iddonaciones`)
    REFERENCES `dist2025`.`donaciones` (`iddonaciones`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_donaciones_has_eventos_eventos1`
    FOREIGN KEY (`eventos_ideventos`)
    REFERENCES `dist2025`.`eventos` (`ideventos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `dist2025`.`participacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dist2025`.`participacion` (
  `usuario_idusuario` INT NOT NULL,
  `eventos_ideventos` INT NOT NULL,
  PRIMARY KEY (`usuario_idusuario`, `eventos_ideventos`),
  INDEX `fk_usuario_has_eventos_eventos1_idx` (`eventos_ideventos` ASC) VISIBLE,
  INDEX `fk_usuario_has_eventos_usuario1_idx` (`usuario_idusuario` ASC) VISIBLE,
  CONSTRAINT `fk_usuario_has_eventos_usuario1`
    FOREIGN KEY (`usuario_idusuario`)
    REFERENCES `dist2025`.`usuario` (`idusuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuario_has_eventos_eventos1`
    FOREIGN KEY (`eventos_ideventos`)
    REFERENCES `dist2025`.`eventos` (`ideventos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
