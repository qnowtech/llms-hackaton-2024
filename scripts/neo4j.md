# Neo4j GDS


Para que funcione es importante realizar los pasos en el orden que están descritos a continuación, cargar la data, crear las realciones y nodos, crear una proyección del grafo y ejecutar los algoritmos mencionados.

Al final del docuemento hay un script de utilidad para borrar la proeycción de ser necesario. 



# Load Data 

```sql
// 1. Cargar Agentes
// Este bloque carga datos desde un archivo CSV que contiene información sobre agentes.
// Cada agente se crea como un nodo de tipo :Agent con propiedades específicas.

LOAD CSV WITH HEADERS FROM 'file:///agents.csv' AS row
CREATE (:Agent {
    AgentId: row.AgentId,     // Identificador único del agente
    Role: row.Role,           // Rol del agente dentro de la organización
    Backstory: row.Backstory, // Historia o antecedentes del agente
    Tools: row.Tools          // Herramientas o recursos que utiliza el agente
});

// 2. Cargar Clientes
// Este bloque carga datos desde un archivo CSV que contiene información sobre clientes.
// Cada cliente se crea como un nodo de tipo :Client con las propiedades correspondientes.
LOAD CSV WITH HEADERS FROM 'file:///clients.csv' AS row
CREATE (:Client {
    ClientId: row.ClientId,   // Identificador único del cliente
    Name: row.Name,           // Nombre del cliente
    Email: row.Email,         // Correo electrónico del cliente
    Phone: row.Phone,         // Número de teléfono del cliente
    CompanyId: row.CompanyId, // Identificador de la empresa asociada al cliente
    Status: row.Status        // Estado actual del cliente (activo, inactivo, etc.)
});

// 3. Cargar Categorías de Problemas
// Este bloque carga datos desde un archivo CSV que contiene categorías de problemas.
// Cada categoría se crea como un nodo de tipo :IssueCategory.
LOAD CSV WITH HEADERS FROM 'file:///issue_category.csv' AS row
CREATE (:IssueCategory {
    IssueId: row.IssueId,     // Identificador único de la categoría de problema
    Name_Issue: row.Name_Issue,// Nombre de la categoría de problema
    Relevance: row.Relevance,   // Relevancia de la categoría (por ejemplo, alta, media, baja)
    Description: row.Description // Descripción detallada de la categoría
});

// 4. Cargar Productos
// Este bloque carga datos desde un archivo CSV que contiene información sobre productos.
// Cada producto se crea como un nodo de tipo :Product.
LOAD CSV WITH HEADERS FROM 'file:///products.csv' AS row
CREATE (:Product {
    ProductId: row.ProductId,   // Identificador único del producto
    Name_Product: row.Name_Product, // Nombre del producto
    Category: row.Category,     // Categoría a la que pertenece el producto
    Description: row.Description, // Descripción del producto
    Price: row.Price,           // Precio del producto
    Status: row.Status          // Estado del producto (disponible, no disponible, etc.)
});

// 5. Cargar Empresas
// Este bloque carga datos desde un archivo CSV que contiene información sobre empresas.
// Cada empresa se crea como un nodo de tipo :Company.
LOAD CSV WITH HEADERS FROM 'file:///companies.csv' AS row
CREATE (:Company {
    CompanyId: row.CompanyId,   // Identificador único de la empresa
    Name_company: row.Name_company, // Nombre de la empresa
    Sector: row.Sector,         // Sector industrial de la empresa
    Location: row.Location       // Ubicación geográfica de la empresa
});

// 6. Cargar Casos
// Este bloque carga datos desde un archivo CSV que contiene información sobre casos.
// Cada caso se crea como un nodo de tipo :Case con relaciones a otros nodos (Clientes, Productos, Agentes).
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
// 1. Crear relaciones entre Clientes y Casos
// Este bloque establece una relación entre los nodos :Client y :Case.
// Se crea una relación :HAS_CASE que conecta cada cliente con sus respectivos casos.
MATCH (c:Client), (ca:Case)
WHERE c.ClientId = ca.ClientId // Condición para encontrar el cliente correspondiente al caso
CREATE (c)-[:HAS_CASE]->(ca); // Se crea la relación entre el cliente y el caso

// 2. Crear relaciones entre Categorías de Problemas y Casos
// Este bloque establece una relación entre los nodos :IssueCategory y :Case.
// Se crea una relación :RELATED_TO que conecta cada categoría de problema con los casos asociados.
MATCH (i:IssueCategory), (ca:Case)
WHERE i.IssueId = ca.IssueId // Condición para encontrar la categoría de problema correspondiente al caso
CREATE (i)-[:RELATED_TO]->(ca); // Se crea la relación entre la categoría de problema y el caso

// 3. Crear relaciones entre Productos y Casos
// Este bloque establece una relación entre los nodos :Product y :Case.
// Se crea una relación :RELATED_TO que conecta cada producto con los casos donde se utiliza.
MATCH (p:Product), (ca:Case)
WHERE p.ProductId = ca.ProductId // Condición para encontrar el producto correspondiente al caso
CREATE (p)-[:RELATED_TO]->(ca); // Se crea la relación entre el producto y el caso

```

# Projection

```sql
// 3. Crear proyección del grafo
// Este bloque utiliza el procedimiento de GDS para crear una proyección de grafo llamada 'myGraph'.
// La proyección incluye nodos y relaciones especificadas mediante consultas Cypher.

CALL gds.graph.project.cypher(
  'myGraph', // Nombre de la proyección del grafo
  // Consulta para seleccionar los nodos a incluir en la proyección
  'MATCH (n) 
   WHERE n:Agent OR n:Company OR n:IssueCategory OR n:Product OR n:Client OR n:Case 
   RETURN id(n) AS id, labels(n) AS labels', 
  // Consulta para seleccionar las relaciones a incluir en la proyección
  'MATCH (a)-[r]->(b) 
   RETURN id(a) AS source, id(b) AS target, type(r) AS type'
)
YIELD graphName, nodeCount, relationshipCount; // Se devuelven el nombre del grafo, el conteo de nodos y el conteo de relaciones

```

# Degree Centrality


```sql

// 4. Calcular la Centralidad de Grado de los Agentes
// Este bloque utiliza el procedimiento de GDS para calcular la centralidad de grado de los nodos en la proyección de grafo 'myGraph'.
// La centralidad de grado mide el número de conexiones directas que tiene un nodo, indicando su nivel de influencia en la red.

CALL gds.degree.stream('myGraph') // Se llama al procedimiento para calcular la centralidad de grado
YIELD nodeId, score // Se devuelven el ID del nodo y su puntuación de centralidad de grado
WHERE gds.util.asNode(nodeId).AgentId IS NOT NULL // Filtramos para mantener solo nodos que son agentes
RETURN gds.util.asNode(nodeId).AgentId AS AgentId, score // Se devuelven el ID del agente y su puntuación
ORDER BY score DESC; // Se ordenan los resultados por puntuación de centralidad de grado en orden descendente

```


# Community of Agents

```sql

// 5. Detección de Comunidades
// Este bloque utiliza el algoritmo de Louvain para identificar comunidades dentro del grafo 'myGraph'.
// Las comunidades pueden ayudar a identificar grupos de Clientes que tienden a tener problemas similares
// o que utilizan los mismos productos. En este caso, nos enfocamos en los Agentes que resuelven casos.

CALL gds.louvain.stream('myGraph') // Se llama al procedimiento de detección de comunidades usando el algoritmo de Louvain
YIELD nodeId, communityId // Se devuelven el ID del nodo y el ID de la comunidad a la que pertenece
RETURN communityId, collect(gds.util.asNode(nodeId).AgentId) AS Members // Se devuelven el ID de la comunidad y los miembros de cada comunidad (Agentes)
ORDER BY size(Members) DESC; // Se ordenan los resultados por el tamaño de los miembros de cada comunidad en orden descendente

```

# Community of Clients

```sql
// 6. Detección de Comunidades de Clientes
// Este bloque utiliza el algoritmo de propagación de etiquetas para identificar comunidades dentro del grafo 'myGraph'.
// El enfoque se centra en los Clientes, permitiendo agrupar a aquellos que están más interconectados en la red.

CALL gds.labelPropagation.stream('myGraph') // Se llama al procedimiento de detección de comunidades utilizando el algoritmo de propagación de etiquetas
YIELD nodeId, communityId // Se devuelven el ID del nodo y el ID de la comunidad a la que pertenece
RETURN communityId, collect(gds.util.asNode(nodeId).ClientId) AS Members // Se devuelven el ID de la comunidad y los miembros de cada comunidad (Clientes)
ORDER BY size(Members) DESC; // Se ordenan los resultados por el tamaño de los miembros de cada comunidad en orden descendente

```

# Node Similarity

```sql
// 7. Cálculo de Similitud de Nodos
// Este bloque utiliza el algoritmo de similitud de nodos para identificar Clientes que presentan tipos de problemas similares
// o Productos que están relacionados con las mismas categorías de problema. Esto puede ayudar a mejorar la atención al cliente 
// y la recomendación de productos.

CALL gds.nodeSimilarity.stream('myGraph') // Se llama al procedimiento de similitud de nodos en la proyección de grafo 'myGraph'
YIELD node1, node2, similarity // Se devuelven los IDs de los nodos y su puntuación de similitud
WHERE gds.util.asNode(node1).ClientId IS NOT NULL // Filtramos para mantener solo nodos que son Clientes
AND gds.util.asNode(node2).ClientId IS NOT NULL // Aseguramos que ambos nodos en la comparación sean Clientes
RETURN gds.util.asNode(node1).ClientId AS Node1, gds.util.asNode(node2).ClientId AS Node2, similarity // Se devuelven los IDs de los Clientes y su puntuación de similitud
ORDER BY similarity DESC // Se ordenan los resultados por la puntuación de similitud en orden descendente
LIMIT 10; // Se limita la salida a los 10 pares de Clientes más similares

```

# Drop Graph

```sql

//Mostrar Proyecciones
CALL gds.graph.list()
YIELD graphName, nodeCount, relationshipCount

//Eliminate projections Stocks
// ToDO: Pass as $param for graph name
CALL gds.graph.drop(
    'NameOfProjection To delete'
) YIELD graphName

```