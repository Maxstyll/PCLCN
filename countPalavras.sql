SELECT 	palavra, COUNT(palavra) 
FROM 	palavras 
WHERE 	tag IS NULL	
GROUP BY palavra
HAVING COUNT(palavra) >= 50
ORDER BY COUNT(palavra) DESC, palavra ASC;


SELECT 	tag, COUNT(palavra) 
FROM 	palavras 
WHERE 	tag IS NOT NULL	
GROUP BY tag
ORDER BY tag, COUNT(palavra) DESC;


SELECT 	tag, palavra, COUNT(palavra) as qtde 
FROM 	palavras
WHERE 	tag IS NULL
GROUP BY tag, palavra
HAVING COUNT(palavra) = 1
ORDER BY palavra;