-- List Glam rock bands ranked by longevity
SELECT band_name,
    IFNULL(2022 - formed, 0) - IFNULL(2022 - split, 0) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', style) > 0
ORDER BY lifespan DESC,
    band_name;