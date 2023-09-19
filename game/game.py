from adapters.mysql_adapter import MySQLDatabase
from adapters.neo4j_adater import Neo4jAdapter


class Game:
    def __init__(self, mysql: MySQLDatabase, neo4j: Neo4jAdapter, university_1: str, university_2: str):
        self.player2 = None
        self.player1 = None
        self.id = "-".join(sorted([university_1, university_2]))
        self.mysql = mysql
        self.neo4j = neo4j
        self.university_1 = university_1
        self.university_2 = university_2
        self.player_1_score = 0
        self.player_2_score = 0
        self.explanation = {}


    def start_debate(self, player1: str, player2: str, topic: str):
        self.player1 = player1
        self.player2 = player2

        # Calculate interest score based on faculty's interest
        self.player_1_score = (50 * self.get_player_interest_score(player1, topic))
        self.player_2_score = (50 * self.get_player_interest_score(player2, topic))
        self.explanation["interest"] = f"{player1} got {self.player_1_score} points, {player2} got {self.player_2_score} points for their interest in {topic}"

        # Calculate score based on faculty's publications on the topic
        player1_pub_score = self.get_player_publication_score(player1, topic)
        player2_pub_score = self.get_player_publication_score(player2, topic)
        self.explanation["publications"] = f"{player1} got {100 * player1_pub_score} points, {player2} got {100 * player2_pub_score} points for their publications on topic {topic}"
        self.player_1_score += (player1_pub_score * 100)
        self.player_2_score += (player2_pub_score * 100)

        # Calculate score based on shortest path between faculty and keyword
        player1_shortest_path_score = self.get_shortest_path_score(player1, topic)
        player2_shortest_path_score = self.get_shortest_path_score(player2, topic)
        self.explanation["shortest_path"] = f"{player1} got {player1_shortest_path_score} points, {player2} got {player2_shortest_path_score} points for relation to the {topic}"
        self.player_1_score += player1_shortest_path_score
        self.player_2_score += player2_shortest_path_score

    def get_player_interest_score(self, player: str, topic: str):
        # Get faculty interest
        result = self.mysql.execute_query(f"select fk.score from faculty as f, faculty_keyword as fk, keyword as k where f.id = fk.faculty_id and f.name = '{player}' and fk.keyword_id = k.id and k.name = '{topic}'")
        if len(result) == 0:
            return 0
        return result[0][0]

    def get_player_publication_score (self, player: str, topic: str):
        # Get faculty interest
        results = self.neo4j.get_publications_score(player, topic)
        return sum(results)


    def get_shortest_path_score(self, player: str, topic: str):
        # Get faculty interest
        results = self.neo4j.get_shortest_paths(player, topic)
        return len(results) * 1/len(results[0][0].relationships) if len(results) > 0 else 0

    def get_winner(self):
        if self.player_1_score > self.player_2_score:
            return self.university_1, self.player1
        elif self.player_1_score < self.player_2_score:
            return self.university_2, self.player2
        else:
            return "Draw", "Draw"

