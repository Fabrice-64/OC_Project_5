LOAD DATA INFILE 
        '/Users/fabricejaouen/DepotLocalGIT/OC_Project_5/Response_API.txt' 
        INTO TABLE Product 
        FIELDS TERMINATED BY ';' ENCLOSED BY '"' 
        LINES STARTING BY ' ' TERMINATED BY '\n'
        (brand, name, category_id, code, nutrition_grade, stores, ingredients)