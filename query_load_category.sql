
INSERT INTO product (brand, name, category_id, code, nutrition_grade, stores, ingredients)
VALUES ('Yoplait', 'Panier Quartiers Fraise Des Bois', (SELECT idcategory FROM category WHERE name ='Produits laitiers'), '3329770050648', 'b', '', "lait ecreme a base de poudre de lait -\ncreme - sucre 8,8% - fraise 8,7% - fraise des bois 2,1% - jus de carotte - Amidon transformé en maïs - Arômes naturels - epaississant (caraghénanes) - correcteur d'acidité (citrate de sodium - acide citrique).")
;
        
INSERT INTO category (name) VALUES ('Snacks');

SELECT * FROM Product;

SELECT * FROM category ORDER BY idcategory ASC;

SELECT COUNT(*) FROM Product;

DELETE FROM category WHERE name = 'Produits laitiers fermentés';

ALTER TABLE category ADD UNIQUE (idcategory,name);

ALTER TABLE product DROP foreign key FK_category_id;
ALTER TABLE best_product DROP foreign key FK_product_id;
TRUNCATE TABLE product;
TRUNCATE TABLE category;

SELECT DISTINCT
    category.idcategory, category.name
FROM
    category
        RIGHT JOIN
    product ON category.idcategory = product.category_id;

SELECT LEFT(product.name,45), product.nutrition_grade, product.brand FROM product WHERE category.name = "Aliments et boissons à base de végétaux" AND product.name LIKE "%%" and product.nutrition_grade LIKE "%%" AND product.brand LIKE "%%" ORDER BY product.nutrition_grade ASC, product.name DESC LIMIT 5;