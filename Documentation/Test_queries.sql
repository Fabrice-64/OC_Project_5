SELECT * FROM product WHERE product.name = "Madeleines" LIMIT 10;

SELECT * , category.name FROM product, category  ORDER by product.name ASC LIMIT 100;

SELECT * FROM category;

SELECT * FROM best_product;

REPLACE INTO best_product VALUES (NULL, '10082584', '2020-03-27 10:34:00');

SELECT product.name, product.category_id, product.brand, category.name FROM product JOIN category ON product.category_id = category.idcategory WHERE product.brand LIKE '%Crownfield%' AND product.name LIKE 'Choco%';

DELETE FROM best_product WHERE query_created = '2020-03-26 17:34:34';

SELECT LEFT(product.name, 40), product.brand, product.code, product.nutrition_grade, best_product.query_created, best_product.reference_product FROM product RIGHT JOIN best_product ON best_product.reference_product =product.code ORDER BY best_product.query_created ASC;

REPLACE INTO product (brand, name, category_id, code, nutrition_grade, stores, ingredients) VALUES ("Seeberger", "Bananenchips", (SELECT idcategory FROM category WHERE name = "Snacks"), '10082584', "e", " ", "Sojakerne geröstet
Graines de soja grillées");

INSERT INTO best_product VALUES (NULL, '3178530410112', '2020-03-27 15:15:30', '1126542');

UPDATE best_product SET best_product.query_created  = '2020-03-27 18:10:30' WHERE product_id = '20562175'

SELECT LEFT(product.name, 40), product.brand, product.code, product.nutrition_grade, best_product.query_created, best_product.reference_product FROM product JOIN best_product ON best_product.product_id =product.code ORDER BY best_product.query_created ASC;

SELECT LEFT(product.name, 40), product.brand, product.code, product.nutrition_grade,  product.stores, (SELECT product.name FROM product WHERE best_product.reference_product = product.code),(SELECT product.brand FROM product WHERE best_product.reference_product = product.code), (SELECT product.nutrition_grade FROM product WHERE best_product.reference_product = product.code)  FROM product JOIN  best_product ON best_product.product_id = product.code;

 SELECT LEFT(product.name,40), product.brand, product.nutrition_grade, product.code, product.category_id, category.name FROM product JOIN category on product.category_id = category.idcategory WHERE category.name = 'Boissons'
        AND product.name LIKE "%Cola%" ORDER BY product.nutrition_grade ASC LIMIT 30;       
   
REPLACE INTO best_product VALUES (NULL, '20562175', '2020-03-27 15:15:30', '3057640238703');

SELECT DISTINCT  category.idcategory, category.name
        FROM category RIGHT JOIN product
        ON category.idcategory = product.category_id ;
        
SELECT COUNT(*), category.name FROM product JOIN category ON product.category_id = category.idcategory GROUP BY product.category_id HAVING COUNT(*) >200;

SELECT COUNT(*) FROM product;
