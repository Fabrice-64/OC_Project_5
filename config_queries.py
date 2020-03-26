query_categories = """SELECT * FROM category ORDER BY idcategory ASC"""

query_count_rows = """SELECT COUNT(*) FROM product"""

query_upload_new_category = """INSERT INTO category (name) VALUES ("{}")"""

query_upload_new_category_products = """REPLACE INTO product (brand, name, category_id, code, nutrition_grade, stores, ingredients) \
        VALUES (%s, %s, (SELECT idcategory FROM category WHERE name = %s), %s, %s, %s, %s)"""

query_searched_item = """SELECT LEFT(product.name,40), product.brand, product.nutrition_grade, product.code FROM category, product WHERE category.name = \"{}\" AND product.name LIKE \"{}\" AND product.brand LIKE \"{}\" AND product.code LIKE \"{}\" ORDER BY product.nutrition_grade ASC LIMIT 10"""

query_best_product = """SELECT LEFT(product.name,40), product.brand, product.nutrition_grade, product.code, product.stores FROM category, product WHERE category.name = \"{}\" AND product.name LIKE \"{}\" AND product.nutrition_grade <= \"{}\" ORDER BY product.nutrition_grade ASC LIMIT 5"""


query_retrieve_available_categories = """SELECT DISTINCT category.idcategory, category.name FROM category RIGHT JOIN product ON category.idcategory = product.category_id"""

query_record_best_product = """REPLACE INTO best_product VALUES (NULL, {product_code}, {date_time})"""

query_retrieve_best_product = """SELECT product.name, product.brand, product.stores, product.nutrition_grade, product.code FROM product JOIN best_product ON best_product.product_id = product.code ORDER BY best_product.query_created ASC LIMIT 5"""