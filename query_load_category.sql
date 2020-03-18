LOAD DATA INFILE 
        '/Users/fabricejaouen/DepotLocalGIT/OC_Project_5/Response_API.txt' 
        IGNORE INTO TABLE Product 
        FIELDS TERMINATED BY ';' ENCLOSED BY '"' 
        LINES STARTING BY ' ' TERMINATED BY '\n'
        (brand, name, category_id, code, nutrition_grade, stores, ingredients);
        
INSERT INTO category (name) VALUES ('Yaourts');

SELECT * FROM Product WHERE name = "Yaourt";

SELECT * FROM category;

SELECT COUNT(*) FROM Product;

DELETE FROM category WHERE name = 'Produits laitiers fermentés';

ALTER TABLE category ADD UNIQUE (idcategory,name);