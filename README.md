● Title: Faculty Debates

● Purpose: 
○ This application is designed to simulate an academic debate game between two universities. The game randomly selects faculty members from each university to compete against each other on a given topic. The purpose of the game is to provide both entertainment and an opportunity for users to explore the academic strengths of different universities, particularly in relation to research topics. 
○ The application is suitable for anyone who is interested in academic debates, regardless of their academic background. It is also a useful tool for students, scholars, and researchers who want to explore the strengths and expertise of university faculty in a fun and engaging way. 
○ The primary objective of this application is to create a unique game that is both entertaining and educational. By simulating academic debates, the game encourages users to learn more about different research topics and the strengths of various universities.

● Demo: https://mediaspace.illinois.edu/media/t/1_frnspqwa

● Installation: To use this application, you must first import the Academic World dataset into MySQL, MongoDB, and Neo4j. Once imported, you will need to input your local database credentials for each of these platforms. After this, you will need to create a score table in MySQL within Academic World dataset using the following code in your terminal.

CREATE TABLE scores (
   university1 VARCHAR(255),
   university2 VARCHAR(255),
   topic VARCHAR(255),
   score1 INT,
   score2 INT
);

CREATE INDEX idx_topic_name ON scores(topic);
CREATE INDEX idx_university_name ON university(name);
CREATE INDEX idx_keyword_name ON keyword(name);
ALTER TABLE scores ADD FOREIGN KEY (university1) REFERENCES university(name);
ALTER TABLE scores ADD FOREIGN KEY (university2) REFERENCES university(name);
ALTER TABLE scores ADD FOREIGN KEY (topic) REFERENCES keyword(name);

● Usage: 
1. To start the game, the player selects their university team from the drop-down box, which contains all available universities in the dataset. Player 1 and player 2 can select their desired universities separately.
2. Once the university team is selected, the player can choose a topic for the debate by typing in keywords related to the topic in the "Select a topic for discussion" box. The box displays related keywords as the player types.
3. A full list of faculty members from the selected university will be presented. The player can select one faculty member (per round debate) by clicking on their name.
4. The player then clicks on the "Debate" button to start the debate.
5. The game consists of 10 rounds, and each round awards a point to the winning team.
6. During the debate, each faculty member makes arguments based on their area of expertise and interests. The winner of the debate is declared based on the Final Debate Score, which is calculated based on the sum of the faculty member's keyword/discussion topic scores, as well as the score of each publication that matches the topic of discussion and networking score.

Display/Viz: 
I. Once two faculties from different universities are selected, their basic information will be displayed below, including their name, title, affiliation, email, research interests, phone number, and Google Scholar page. If any information is not available, it will show "not available".
II. The publications of the selected faculties will be displayed in a time-course format. The number of publications over time is shown in a blue bar plot. If any of the selected faculty members have publications that align with the selected topic, those publications will be shown in red.
III. The shortest paths from the given faculty to the selected topic will be connected via the faculty’s interests, faculty’s colleagues, publication etc.  

● Design: What is the design of the application? Overall architecture and components.
       The design of the application includes a two-layered architecture with several components working together to provide an interactive user experience. 
       The database layer includes three different databases: MySQL, MongoDB, and neo4j. The application also includes a Google Scholar API, which enables the retrieval of additional information on faculty members. 
       The client layer was built on Dash framework to implement the user interface. It is designed to be modular, with each component having a specific role and working together to provide a seamless user experience. The user interface provides a simple and intuitive way for users to select their university team, choose a topic, and select faculty members for debate. The application's backend then retrieves information from the databases and Google Scholar to provide relevant information on faculty members and their publications. Finally, the application calculates the debate score based on the selected topic and the faculty members' expertise, publications, and networking score. 


● Implementation: How did you implement it? What frameworks and libraries or any tools have you used to realize the dashboard and functionalities?
       To implement the application, we used the Dash framework to create a web-based dashboard with interactive data visualization components. We also used several libraries such as Pandas, Plotly, Dash Bootstrap Components, and Scholarly to manipulate and visualize data, build UI components, and retrieve information from external sources.
       The dashboard was structured as a single-page application with multiple tabs, and it contained various interactive components such as dropdowns, checkboxes, and sliders that allowed users to filter and explore the data. We also implemented some functionality to display the selected data in real-time, allowing users to view changes as they occurred.
       Additionally, we used a MySQL database to store and manage game-related data, and a MongoDB database to cache scholarly data. we also implemented a queue-based approach with threads to manage database queries and data retrieval asynchronously, which improved the performance and responsiveness of the application.
       Finally, we implemented a modal component using Dash Bootstrap Components to display the results of a debate game. The modal contained several HTML components that displayed the winners of the debate and an explanation of the results.

● Database Techniques: What database techniques have you implemented? How?
1. Indexing: create index on the ‘topic’ column of the ‘score’ table, the ‘name’ column of the ‘university’ table, and the ‘name’ column of the ‘keyword’ table. 
2. Constraint: add foreign key for university name and keyword name
3. Trigger: The process involves checking if a faculty member's Google Scholar data exists in the MongoDB database. If it's found, the Google Scholar page URL is used and displayed in the faculty information widget. If not, Scholarly is used to access the Google Scholar server and search for matching faculty information by matching the full name and university email postfix. If the Google Scholar page is found, it's added to the MongoDB database. Otherwise, the field is filled up as "not available."
4. REST API for accessing databases: Scholarly library use REST API for accessing Google Scholar databases. 


● Extra-Credit Capabilities: 
1. Multi-database querying: The full list of faculties displayed from selected universities is query result from MySQL, Then, when an individual faculty member is selected, their information is queried from the MongoDB database. 

2. Data expansion: Faculty members' Google Scholar information is searched for and added to the MongoDB database.

3. External data sourcing: Google Scholar services are queried to bring in more data on faculty members' information, and their Google Scholar page is hyperlinked to display. 

● Contributions: How each member has contributed, in terms of 1) tasks done and 2) time spent?
Jue Hou: ‘mongo_adapter’, ‘display_faculty_info_widget’, ‘display_publication_widget’, ‘style.css’, all style/font related amendments, draft readme, video. 30hrs. 
Boris Tsekinovsky: ‘mysql_adapter’, ‘basic_statistics_widget’, ‘debate_results_modal’, ‘faculty_members_list_widget’, ‘paths_to_topic_widget’, ‘select_debate_topic_widget’ and ‘select_university_widget’, revise readme. 30 hrs. 

