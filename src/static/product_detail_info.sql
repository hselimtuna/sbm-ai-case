SELECT
    p.id AS product_id,
    p.name AS product_name,
    p.barcode,
    b.name AS brand_name,
    c.name AS category_name,
    p.description,
    jsonb_object_agg(ca.name, pa.value) AS product_attributes,
    jsonb_object_agg(ca.name, ca.type) AS category_attributes,
    pi.quantity,
    pi.list_price,
    pi.sale_price,
    pi.currency
FROM products p
LEFT JOIN brands b ON p.brand_id = b.id
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN product_attributes pa ON p.id = pa.product_id
LEFT JOIN category_attributes ca ON pa.attribute_id = ca.id
LEFT JOIN product_inventory pi ON p.id = pi.product_id
WHERE p.name like '%%{product_name}%%'
GROUP BY p.id, p.name, p.barcode, b.name, c.name, p.description, pi.quantity, pi.list_price, pi.sale_price, pi.currency

