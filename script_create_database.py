"""
    This file contains the script needed for the creation of the Database.

"""
import config
DB_CREATION = """CREATE DATABASE IF NOT EXISTS {} CHARACTER SET = 'utf8' """

DB_USE = """USE {}"""

DB_TABLES = {}
DB_TABLES['category'] = (
"CREATE TABLE `category` ("
  "`idcategory` int(2) unsigned NOT NULL AUTO_INCREMENT,"
 "`name` varchar(45) NOT NULL,"
  "PRIMARY KEY (`idcategory`),"
  "UNIQUE KEY `idcategory` (`idcategory`,`name`)"
") ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8")

DB_TABLES['product'] = (
"CREATE TABLE `product` ("
  "`code` varchar(13) NOT NULL,"
  "`category_id` int(2) unsigned NOT NULL,"
  "`brand` varchar(200) NOT NULL,"
  "`stores` varchar(160) NOT NULL,"
  "`name` text NOT NULL,"
  "`nutrition_grade` varchar(1) NOT NULL,"
  "`ingredients` text,"
  "PRIMARY KEY (`code`),"
  "KEY `FK_category_id_idx` (`category_id`),"
  "CONSTRAINT `FK_category_id` FOREIGN KEY (`category_id`) REFERENCES `category` (`idcategory`)"
") ENGINE=InnoDB DEFAULT CHARSET=utf8")

DB_TABLES['best_product'] = (
  "CREATE TABLE `best_product` ("
  "`idbest_product` int(6) NOT NULL AUTO_INCREMENT,"
  "`product_id` varchar(13) NOT NULL,"
  "`query_created` datetime DEFAULT NULL,"
  "`reference_product` varchar(13) NOT NULL,"
  "PRIMARY KEY (`idbest_product`),"
  "UNIQUE KEY `product_id_UNIQUE` (`product_id`),"
  "KEY `FK_code_product_idx` (`product_id`),"
  "CONSTRAINT `FK_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`code`)"
  "ON DELETE CASCADE ON UPDATE CASCADE"
  ") ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8")


