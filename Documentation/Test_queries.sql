SELECT * FROM product WHERE product.name = "Madeleines" LIMIT 10;

SELECT * FROM category;

SELECT * FROM best_product;

REPLACE INTO best_product VALUES (NULL, '10082584', '2020-03-27 10:34:00');

SELECT product.name FROM product WHERE product.code = '3596710308996';

DELETE FROM best_product WHERE query_created = '2020-03-26 17:34:34';

SELECT product.brand, product.code, best_product.query_created FROM product JOIN best_product ON best_product.product_id =product.code ORDER BY best_product.query_created ASC;

REPLACE INTO product (brand, name, category_id, code, nutrition_grade, stores, ingredients) VALUES ("Seeberger", "Bananenchips", (SELECT idcategory FROM category WHERE name = "Snacks"), '10082584', "e", " ", "Sojakerne geröstet
Graines de soja grillées");

INSERT INTO best_product VALUES (NULL, '3178530410112', '2020-03-27 15:15:30', '1126542');

SELECT product.brand, product.code, best_product.query_created FROM product JOIN best_product ON best_product.reference_product = product.code WHERE best_product.reference_product = "1126542";