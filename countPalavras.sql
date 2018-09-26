SELECT 	palavra, COUNT(palavra) 
FROM 	palavras 
WHERE 	tag IS NULL	
GROUP BY palavra
HAVING COUNT(palavra) >= 100
ORDER BY COUNT(palavra) DESC, palavra ASC;


SELECT 	tag, COUNT(palavra) 
FROM 	palavras 
WHERE 	tag IS NOT NULL	
GROUP BY tag
ORDER BY tag, COUNT(palavra) DESC;


SELECT 	tag, palavra 
FROM 	palavras 
WHERE 	tag = 'WRB'	
ORDER BY tag, palavra;