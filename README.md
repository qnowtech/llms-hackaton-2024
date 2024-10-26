# llms-hackaton-2024
llms-hackaton-2024


# Knowledge Graph Recommender System

## Overview
The **Knowledge Graph Recommender System** is a Python class designed to facilitate interaction with a Neo4j graph database. It provides methods for creating nodes, calculating centrality measures, and analyzing similarities and communities among nodes. Thi is particularly useful for applications that require graph-based data modeling and analysis.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Features
- Establish a connection to a Neo4j database.
- Calculate degree centrality for nodes.
- Assess similarity between nodes.
- Detect communities among clients and agents using graph algorithms.

## Installation
To use the Knowledge Graph Recommender System, ensure you have Python installed (version 3.6 or higher) and then install the required libraries and Neo4j version `5.24.0` also for local development its important to consider install de [APOC](https://neo4j.com/labs/apoc/) procedures and [GDS](https://neo4j.com/docs/graph-data-science/current/algorithms/) module for the Knowledge Graph


### Prerequisites
- Neo4j database instance (local or remote).
- Python 3.6 or higher.
- Install the Neo4j driver:

```bash
pip install neo4j
```