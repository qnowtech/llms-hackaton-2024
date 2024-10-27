# Neo4j GDS

Para que funcione es importante realizar los pasos en el orden que están descritos a continuación, cargar la data, crear las realciones y nodos, crear una proyección del grafo y ejecutar los algoritmos mencionados.

Al final del docuemento hay un script de utilidad para borrar la proeycción de ser necesario. 

# Load Data 

```sql
-- 1. Cargar Agentes. Este bloque carga datos desde un archivo CSV que contiene información sobre agentes. Cada agente se crea como un nodo de tipo :Agent con propiedades específicas.

LOAD CSV WITH HEADERS FROM 'file:///agents.csv' AS row
CREATE (:Agent {
    AgentId: row.AgentId,     // Identificador único del agente
    Role: row.Role,           // Rol del agente dentro de la organización
    Backstory: row.Backstory, // Historia o antecedentes del agente
    Tools: row.Tools          // Herramientas o recursos que utiliza el agente
});

-- 2. Cargar Clientes. Este bloque carga datos desde un archivo CSV que contiene información sobre clientes. Cada cliente se crea como un nodo de tipo :Client con las propiedades correspondientes.

LOAD CSV WITH HEADERS FROM 'file:///clients.csv' AS row
CREATE (:Client {
    ClientId: row.ClientId,   // Identificador único del cliente
    Name: row.Name,           // Nombre del cliente
    Email: row.Email,         // Correo electrónico del cliente
    Phone: row.Phone,         // Número de teléfono del cliente
    CompanyId: row.CompanyId, // Identificador de la empresa asociada al cliente
    Status: row.Status        // Estado actual del cliente (activo, inactivo, etc.)
});

-- 3. Cargar Categorías de Problemas. Este bloque carga datos desde un archivo CSV que contiene categorías de problemas. Cada categoría se crea como un nodo de tipo :IssueCategory.

LOAD CSV WITH HEADERS FROM 'file:///issue_category.csv' AS row
CREATE (:IssueCategory {
    IssueId: row.IssueId,     // Identificador único de la categoría de problema
    Name_Issue: row.Name_Issue,// Nombre de la categoría de problema
    Relevance: row.Relevance,   // Relevancia de la categoría (por ejemplo, alta, media, baja)
    Description: row.Description // Descripción detallada de la categoría
});

-- 4. Cargar Productos. Este bloque carga datos desde un archivo CSV que contiene información sobre productos. Cada producto se crea como un nodo de tipo :Product.

LOAD CSV WITH HEADERS FROM 'file:///products.csv' AS row
CREATE (:Product {
    ProductId: row.ProductId,   // Identificador único del producto
    Name_Product: row.Name_Product, // Nombre del producto
    Category: row.Category,     // Categoría a la que pertenece el producto
    Description: row.Description, // Descripción del producto
    Price: row.Price,           // Precio del producto
    Status: row.Status          // Estado del producto (disponible, no disponible, etc.)
});

-- 5. Cargar Empresas. Este bloque carga datos desde un archivo CSV que contiene información sobre empresas. Cada empresa se crea como un nodo de tipo :Company.

LOAD CSV WITH HEADERS FROM 'file:///companies.csv' AS row
CREATE (:Company {
    CompanyId: row.CompanyId,   // Identificador único de la empresa
    Name_company: row.Name_company, // Nombre de la empresa
    Sector: row.Sector,         // Sector industrial de la empresa
    Location: row.Location       // Ubicación geográfica de la empresa
});

-- 6. Cargar Casos. Este bloque carga datos desde un archivo CSV que contiene información sobre casos. Cada caso se crea como un nodo de tipo :Case con relaciones a otros nodos (Clientes, Productos, Agentes).

LOAD CSV WITH HEADERS FROM 'file:///case.csv' AS row
CREATE (:Case {
    CaseId: row.CaseId,               // Identificador único del caso
    IssueId: row.IssueId,             // Identificador del problema asociado
    ClientId: row.ClientId,           // Identificador del cliente asociado al caso
    ProductId: row.ProductId,         // Identificador del producto relacionado con el caso
    AgentId: row.AgentId,             // Identificador del agente que maneja el caso
    Description_Case: row.Description_Case, // Descripción del caso
    Status: row.Status                 // Estado actual del caso (abierto, cerrado, etc.)
});
```

# Relations

```sql
-- 1. Crear relaciones entre Clientes y Casos
MATCH (c:Client), (ca:Case)
WHERE c.ClientId = ca.ClientId 
CREATE (c)-[:HAS_CASE]->(ca); 

-- 2. Crear relaciones entre Categorías de Problemas y Casos
MATCH (i:IssueCategory), (ca:Case)
WHERE i.IssueId = ca.IssueId 
CREATE (i)-[:RELATED_TO]->(ca); 

-- 3. Crear relaciones entre Productos y Casos

MATCH (p:Product), (ca:Case)
WHERE p.ProductId = ca.ProductId
CREATE (p)-[:RELATED_TO]->(ca); 

-- 4. Crear relaciones entre Agentes y Casos
MATCH (a:Agent), (ca:Case)
WHERE a.AgentId = ca.AgentId
CREATE (a)-[:HANDLES]->(ca);

```

# Projection

```sql
-- Crear proyección del grafo o especie de subgrafo. Este bloque utiliza el procedimiento de GDS para crear una proyección de grafo llamada 'myGraph'. La proyección incluye nodos y relaciones especificadas mediante consultas Cypher.

CALL gds.graph.project.cypher(
  'myGraph',
  'MATCH (n) 
   WHERE n:Agent OR n:Company OR n:IssueCategory OR n:Product OR n:Client OR n:Case 
   RETURN id(n) AS id, labels(n) AS labels', 
  'MATCH (a)-[r]->(b) 
   RETURN id(a) AS source, id(b) AS target, type(r) AS type'
)
YIELD graphName, nodeCount, relationshipCount; 

```

# Degree Centrality


```sql

-- Calcular la Centralidad de Grado de los 3 mejores Agentes para resolver un Issue. Este bloque utiliza el procedimiento de GDS para calcular la centralidad de grado de los nodos en la proyección de grafo 'myGraph'. La centralidad de grado mide el número de conexiones directas que tiene un nodo, indicando su nivel de influencia en la red.

CALL gds.degree.stream('myGraph') 
YIELD nodeId, score
WHERE gds.util.asNode(nodeId).AgentId IS NOT NULL 
RETURN gds.util.asNode(nodeId).AgentId AS AgentId, score 
ORDER BY score DESC
LIMIT 3;

```


# Community of Agents

```sql

-- Detección de Comunidades. Este bloque utiliza el algoritmo de Louvain para identificar comunidades dentro del grafo 'myGraph'. Las comunidades pueden ayudar a identificar grupos de Clientes que tienden a tener problemas similares o que utilizan los mismos productos. En este caso, nos enfocamos en los Agentes que resuelven casos.

CALL gds.louvain.stream('myGraph') 
YIELD nodeId, communityId 
RETURN communityId, collect(gds.util.asNode(nodeId).AgentId) AS Members
ORDER BY size(Members) DESC;

```

# Community of Clients

```sql
-- Detección de Comunidades de Clientes. Este bloque utiliza el algoritmo de propagación de etiquetas para identificar comunidades dentro del grafo 'myGraph'. El enfoque se centra en los Clientes, permitiendo agrupar a aquellos que están más interconectados en la red.

CALL gds.labelPropagation.stream('myGraph') 
YIELD nodeId, communityId 
RETURN communityId, collect(gds.util.asNode(nodeId).ClientId) AS Members
ORDER BY size(Members) DESC;

```
# Node Similarity

```sql
-- Cálculo de Similitud de Nodos. Este bloque utiliza el algoritmo de similitud de nodos para identificar Clientes que presentan tipos de problemas similares o Productos que están relacionados con las mismas categorías de problema. Esto puede ayudar a mejorar la atención al cliente y la recomendación de productos.

CALL gds.nodeSimilarity.stream('myGraph') 
YIELD node1, node2, similarity 
WHERE gds.util.asNode(node1).ClientId IS NOT NULL 
AND gds.util.asNode(node2).ClientId IS NOT NULL
RETURN gds.util.asNode(node1).ClientId AS Node1, gds.util.asNode(node2).ClientId AS Node2, similarity
ORDER BY similarity DESC 
LIMIT 10;

```

# Drop Queries

```sql

--Mostrar Proyecciones
CALL gds.graph.list()
YIELD graphName, nodeCount, relationshipCount

--Eliminate projections Stocks
CALL gds.graph.drop(
    'myGraph'
) YIELD graphName

--Borrar nodos y relaciones
MATCH (n) 
DETACH DELETE n;

```