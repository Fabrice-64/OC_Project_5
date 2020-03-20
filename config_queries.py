query_categories = """SELECT * FROM category ORDER BY idcategory ASC"""

query_count_rows = """SELECT COUNT(*) FROM product"""

query_upload_new_category = """INSERT INTO category (name) VALUES ("{}")"""

query_upload_new_category_products = """REPLACE INTO product (brand, name, category_id, code, nutrition_grade, stores, ingredients) \
        VALUES (%s, %s, (SELECT idcategory FROM category WHERE name = %s), %s, %s, %s, %s)"""
