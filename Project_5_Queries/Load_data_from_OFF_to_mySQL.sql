 LOAD DATA INFILE '/Users/fabricejaouen/DepotLocalGIT/OC_Project_5/Response_API.txt'
 INTO TABLE Products FIELDS TERMINATED BY ';' ENCLOSED BY '"' 
 LINES STARTING BY ' ' 
 (brands, name, category, code, nutrition_grade, stores, ingredients, url);