SELECT * FROM category;

SELECT * FROM product;

REPLACE INTO best_product VALUES (NULL, '0072417152924', '2020-03-26 17:34:34');

DELETE FROM best_product WHERE query_created = '2020-03-26 17:34:34';

SELECT product.brand, product.code, best_product.query_created FROM product JOIN best_product ON best_product.product_id =product.code ORDER BY best_product.query_created ASC;