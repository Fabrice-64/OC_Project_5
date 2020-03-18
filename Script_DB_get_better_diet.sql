-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema get_better_diet
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema get_better_diet
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `get_better_diet` DEFAULT CHARACTER SET utf8 ;
USE `get_better_diet` ;

-- -----------------------------------------------------
-- Table `get_better_diet`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `get_better_diet`.`category` (
  `idcategory` INT(2) UNSIGNED NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idcategory`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `get_better_diet`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `get_better_diet`.`product` (
  `code` VARCHAR(13) NOT NULL,
  `category_id` INT(2) UNSIGNED NOT NULL,
  `brand` VARCHAR(200) NOT NULL,
  `stores` VARCHAR(160) NOT NULL,
  `name` TEXT NOT NULL,
  `nutrition_grade` VARCHAR(1) NOT NULL,
  `ingredients` TEXT NULL,
  PRIMARY KEY (`code`),
  INDEX `FK_category_id_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `FK_category_id`
    FOREIGN KEY (`category_id`)
    REFERENCES `get_better_diet`.`category` (`idcategory`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `get_better_diet`.`best_product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `get_better_diet`.`best_product` (
  `idbest_product` INT(6) NOT NULL,
  `product_id` VARCHAR(13) NOT NULL,
  `query_created` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`idbest_product`),
  INDEX `FK_code_product_idx` (`product_id` ASC) VISIBLE,
  CONSTRAINT `FK_code_product`
    FOREIGN KEY (`product_id`)
    REFERENCES `get_better_diet`.`product` (`code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
