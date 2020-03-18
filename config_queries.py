query_categories = "SELECT * FROM category"

query_count_rows = "SELECT COUNT(*) FROM product"

query_upload_new_category = "INSERT INTO category (name) VALUES ('{}')"

query_upload_new_category_products = "INSERT IGNORE INTO TABLE product (brand, name, \
        category_id, code, nutrition_grade, stores, ingredients) \
        VALUES ('{0}',)"