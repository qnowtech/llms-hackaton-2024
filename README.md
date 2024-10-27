# llms-hackaton-2024

In this repo you will be able to simulate with a Crew of AI agents of a customer support agency, with the goal to solve custumers issues, in this case we are using this Crew of agents working in a Sequential flow:
    1 -  user: simulated user from GuruWalk app
    2 - customer_support_agent: specialized customer support agent
    3 - kg_engineer: Agent for execute Graph Machine Learning algorithms and create Cypher queries for obtain the best Agent for the issue, find find communities with similar cases.  
    4 - ml_engineer: Agent for instance new agents or Crew to be able to solve the issues based in the output of kg_engineer

We want to demostrate that if you use Knowledge Graphs with Multiagentic solutions be powered to get results baesed on rules transformed in knowledge.

![Flow](./assets/flow.png)

### Goal

Perform the current process of the 'Router Agent', based in Knowledge and KG Machine learning algorithms, to allow auto feedback and delegations with more accuracy.

![current process](./assets/current.png)


## Knowledge Graph Recommender System

![Grafo](./assets/graph.png)

### Overview
The **Knowledge Graph Recommender System** is a Python class designed to facilitate interaction with a Neo4j graph database. It provides methods for creating nodes, calculating centrality measures, and analyzing similarities and communities among nodes. Thi is particularly useful for applications that require graph-based data modeling and analysis.

#### Schema

![Schema](./assets/schema.png)

### Requirements
- install Neo4j Desktop or self host Server that alows [GDS](https://neo4j.com/docs/graph-data-science/current/algorithms/)
- Establish a connection to a Neo4j database.
- Calculate degree centrality for nodes.
- Assess similarity between nodes.
- Detect communities among clients and agents using graph algorithms.
- Import data from Cypher Queries in folder scripts

### Installation
To use the Knowledge Graph Recommender System, ensure you have Python installed (version 3.6 or higher) and then install the required libraries and Neo4j version `5.24.0` also for local development its important to consider install [GDS](https://neo4j.com/docs/graph-data-science/current/algorithms/) module for the Knowledge Graph Data Science


### Prerequisites
- Neo4j database instance (local or remote).
- Python 3.10 or higher.
- Install the Neo4j driver:

```bash
pip install -r requirements.txt
```

### Custumer Support Crewai Simulation
Run the Crew simulation from Notebook in folder 'crew' or from Streamlit App

## Results
 
#### Degree Centrality

![Centrality](./assets/DegreeCentrality.png)

#### Detail of the best Agents recommendation

![Detail Centrality](./assets/DetailDegree.png)

### Used Tools

##### Mistral & Athropic as LLM Model

![Mistral](./assets/mistral-ai.svg)

![Athropic](./assets/claude.jpg)

##### Google colab for notebooks

![Colab](./assets/colab.png)

##### CodeGPT for code generation

![CodeGpt](./assets/codegpt.png)


### Team

**Alejandro Giraldo**

[![Alejandro Giraldo](https://media.licdn.com/dms/image/v2/C5603AQF_VCpp6yXD-w/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1614615633542?e=1735776000&v=beta&t=PUF6Fz3__WqlFeZmq8IA31nf5OANqxO5r3RC8zrEXa8)](https://www.linkedin.com/in/alejandrosin/)


**Daniel Ruiz**

[![Daniel Ruiz](https://media.licdn.com/dms/image/v2/D4D03AQHFSsAbCY8FDQ/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1686782759750?e=1735776000&v=beta&t=kyAaiCNHXMN9Tqfplgm8jyMLwbqxjZ2J83_iIl1amvE)](https://www.linkedin.com/in/luisdanielruiz-in/)