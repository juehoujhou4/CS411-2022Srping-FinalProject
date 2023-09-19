from neo4j import GraphDatabase

# Neo4j Adapter
#
# This adapter uses the Neo4j graph database to store the
# results of the analysis.


class Neo4jAdapter:
    def __init__(self, uri, database, user, password):
        self.driver = GraphDatabase.driver(uri, database=database, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query):
        with self.driver.session() as session:
            return session.run(query)

    def get_shortest_paths(self, source, target):
        query = f"MATCH (s:FACULTY {{name: \"{source}\"}}), (t:KEYWORD {{name: \"{target}\"}}), sp = allShortestPaths((s) - [*] - (t)) RETURN sp LIMIT 50"
        with self.driver.session() as session:
            results = session.run(query)
            records = list(results)
            return records

    def get_publications_score (self, faculty: str, keyword: str) -> list:
        query = f"MATCH (:FACULTY {{name: \"{faculty}\"}})-[:PUBLISH]-(p:PUBLICATION)-[l:LABEL_BY]-(k:KEYWORD {{name: \"{keyword}\"}}) RETURN p.numCitations * l.score"
        with self.driver.session() as session:
            results = session.run(query)
            records = list(results)
            return [r[0] for r in  records]

    def run_transaction(self, query):
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                result = tx.run(query)
                return result
