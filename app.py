# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import time

import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from game.game import Game
from widgets import paths_to_topic_widget, \
    basic_statistics_widget, \
    select_university_widget, \
    faculty_members_list_widget, \
    display_faculty_info_widget, \
    display_publication_widget, \
    score_widget, \
    select_debate_topic_widget

from adapters.mysql_adapter import MySQLDatabase
from adapters.mongo_adapter import MongoDatabase
from adapters.neo4j_adater import Neo4jAdapter
from widgets.debate_results_modal import getModal

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/style.css'], suppress_callback_exceptions=True, title="Academic World",
           update_title="Loading...", prevent_initial_callbacks='initial_duplicate')

PlayRound = {
    'university0': None,  # University 1
    'university0_photo': None,  # University 1 photo
    'university1': None,  # University 2
    'university1_photo': None,  # University 2 photo
    'player0': None,  # Player 1
    'player1': None,  # Player 2
    'topic': None,  # Topic
    'score0': 0,  # Score 1
    'score1': 0,  # Score 2
}


mysql = MySQLDatabase("localhost", "root", "Bearloveguinguin872439!", "academicworld")
mysql.connect()

neo4jDB = Neo4jAdapter("bolt://localhost:7687", "academicworld", "neo4j", "fushilaola")

# Prompt the user for MySQL credentials
# mysql_user = input("Enter MySQL username: ")
# mysql_password = input("Enter MySQL password: ")

# Connect to MySQL database using user input credentials
# mysql = MySQLDatabase("localhost", mysql_user, mysql_password, "academicworld")
# mysql.connect()

# Prompt the user for Neo4j credentials
# neo4j_user = input("Enter Neo4j username: ")
# neo4j_password = input("Enter Neo4j password: ")

# Connect to Neo4j database using user input credentials
# neo4jDB = Neo4jAdapter("bolt://localhost:7687", "academicworld", neo4j_user, neo4j_password)

# Connect to MongoDB
mongo = MongoDatabase("localhost", 27017)
mongo.connect("academicworld")

widgetContainerStyle = {'width': 'calc(33.33% - 10px)', 'marginBottom': '20px', 'padding': '10px',
                        'boxSizing': 'border-box', 'border': '1px solid #ccc'}

app.layout = html.Div(children=[

    # Header widget
    html.Div([
        html.Div(style={'width': '10%', 'opacity': '0'}),
        html.Div(["Faculty debates"], style={'width': '80%', 'textAlign': 'center', 'fontSize': '30px', "flex": "1"}),
        html.Div(basic_statistics_widget.build_content(mysql),
                 style={'width': '10%', 'float': 'right', 'fontSize': '12px'})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'width': '100%',
              'marginBottom': '20px', 'padding': '10px', 'boxSizing': 'border-box', 'border': '1px solid #ccc',
              'backgroundColor': 'lightgreen'}),

    # Select university widgets
    html.Div([
        html.Div(select_university_widget.build_content(mysql, 0), style={'width': '45%', 'display': 'inline-block',
                                                                          'float': 'left'}),
        html.Div(score_widget.build_content(0, 0), id='score_board', style={'width': '10%', 'display': 'inline-block',
                                                                            'float': 'left'}),
        html.Div(select_university_widget.build_content(mysql, 1), style={'width': '45%', 'display': 'inline-block',
                                                                          'float': 'right'}),
    ], style={'textAlign': 'center', 'marginTop': '20px'}),

    # start debate button
    html.Div([
        html.Button('Start debate', id='start_debate_button', disabled=True, n_clicks=0,
                    style={'width': '95%', 'height': '70px', 'fontSize': '20px', 'backgroundColor': 'orange',
                           'cursor': 'pointer'})
    ], style={'textAlign': 'center', 'marginTop': '20px'}),

    # Select Debate topic widget
    html.Div([
        html.Div(select_debate_topic_widget.build_content(mysql),
                 style={'width': '100%', 'display': 'inline-block', 'float': 'left'}),
    ], style={'textAlign': 'center', 'marginTop': '20px'}),

    # Display Faculty members
    html.Div([
        html.Div(faculty_members_list_widget.build_content(mysql, "", 0), id='list_faculty_members0', style={'width': '50%', 'display': 'inline-block'}),
        html.Div(faculty_members_list_widget.build_content(mysql, "", 1), id='list_faculty_members1', style={'width': '50%', 'display': 'inline-block'}),
    ], style={}),

    # Display Faculty info
    html.Div([
        html.Div(display_faculty_info_widget.build_content(mongo, "", 0), id='display_faculty_info0',
                 className="faculty-info-container", style={'width': '50%', 'display': 'inline-block', 'height': '200px'}),
        html.Div(display_faculty_info_widget.build_content(mongo, "", 1), id='display_faculty_info1',
                 className="faculty-info-container", style={'width': '50%', 'display': 'inline-block', 'height': '200px'}),
    ], style={'border': '2px solid blue', 'padding': '20px'}),

    # Display Publication info
    html.Div([
        html.Div(display_publication_widget.build_content(mysql, "", ""), id='display_publication0',
                 className="publication-container",
                 style={'width': '50%', 'display': 'inline-block', 'float': 'left'}),
        html.Div(display_publication_widget.build_content(mysql, "", ""), id='display_publication1',
                 className="publication-container",
                 style={'width': '50%', 'display': 'inline-block', 'float': 'right'}),
    ], style={'textAlign': 'center', 'marginTop': '20px', 'height': '470px', 'border': '2px solid green',
              'padding': '10px'}),

    # Paths to topic widget
    html.Div([
        html.Div(paths_to_topic_widget.build_content(neo4jDB, "", "", 0), id='paths_to_topic0',
                 className="network-container",
                 style={'width': '48%', 'display': 'inline-block', 'float': 'left', 'border': '1px solid #ccc'}),
        html.Div(paths_to_topic_widget.build_content(neo4jDB, "", "", 1), id='paths_to_topic1',
                 className="network-container",
                 style={'width': '48%', 'display': 'inline-block', 'float': 'right', 'border': '1px solid #ccc'}),
    ], style={'marginTop': '20px', 'height': '470px', 'border': '2px solid orange', 'padding': '10px'}),

    getModal(mysql),
    dcc.Loading(id="loading", children=[], type="default", fullscreen=True)
])


####################
# Callbacks
# Don't like the idea to have callbacks here and not in the widget files, but it should have access to
# `app` which is available only in main file. If I'll import `app` in widgets files, it will be circular
# dependency because this file imports widgets.
####################
@app.callback(
    dash.dependencies.Output('tooltip-text0', 'children'),
    [dash.dependencies.Input('path_to_topic0', 'mouseoverNodeData')])
def display_hover_data0(data):
    return data['tooltip'] if data and 'tooltip' in data else data['label'] if data else "Hover over a node to see more info"

@app.callback(
    dash.dependencies.Output('tooltip-text1', 'children'),
    [dash.dependencies.Input('path_to_topic1', 'mouseoverNodeData')])
def display_hover_data1(data):
    return data['tooltip'] if data and 'tooltip' in data else data['label'] if data else "Hover over a node to see more info"

# Start Debate button click handler
@app.callback(
    [dash.dependencies.Output('loading', 'children'),
     dash.dependencies.Output('modal', 'is_open'),
     dash.dependencies.Output('univer_winner', 'children'),
     dash.dependencies.Output('univer_winner_logo', 'src'),
     dash.dependencies.Output('player_winner', 'children'),
     dash.dependencies.Output('faculty_interest_explanation', 'children'),
     dash.dependencies.Output('faculty_publications_explanation', 'children'),
     dash.dependencies.Output('faculty_relation_explanation', 'children'),
     dash.dependencies.Output('score_board', 'children', allow_duplicate=True)],
    [dash.dependencies.Input('start_debate_button', 'n_clicks')],
    [dash.dependencies.State('modal', 'is_open')])
def start_debate(n_clicks, is_open):
    if n_clicks:
        game = Game(mysql, neo4jDB, PlayRound['university0'], PlayRound['university1'])
        game.start_debate(PlayRound['player0'], PlayRound['player1'], PlayRound['topic'])
        time.sleep(1.5)
        univer, player = game.get_winner()
        if univer == PlayRound['university0']:
            PlayRound['score0'] += 1
        elif univer == PlayRound['university1']:
            PlayRound['score1'] += 1
        mysql.update_score(PlayRound['university0'], PlayRound['score0'], PlayRound['university1'], PlayRound['score1'],
                           PlayRound['topic'])

        return [], not is_open, \
            univer, \
            PlayRound['university0_photo'] if univer == PlayRound['university0'] else PlayRound['university1_photo'] if univer == PlayRound['university1'] else "", \
            player, \
            game.explanation['interest'], \
            game.explanation['publications'], \
            game.explanation['shortest_path'], \
            score_widget.build_content(PlayRound['score0'], PlayRound['score1'])
    else:
        return [], is_open, "", "", "", "", "", "", score_widget.build_content(PlayRound['score0'], PlayRound['score1'])


# Close modal window
@app.callback(
    [dash.dependencies.Output('modal', 'is_open', allow_duplicate=True),
     dash.dependencies.Output('list_faculty_members0', 'children', allow_duplicate=True),
     dash.dependencies.Output('list_faculty_members1', 'children', allow_duplicate=True)],
    [dash.dependencies.Input("close_modal", "n_clicks")],
    [dash.dependencies.State('modal', 'is_open')])
def close_modal(n_clicks, is_open):
    if not n_clicks:
        return dash.no_update, dash.no_update, dash.no_update
    return not is_open, \
        faculty_members_list_widget.build_content(mysql, PlayRound['university0'], 0), \
        faculty_members_list_widget.build_content(mysql, PlayRound['university1'], 1)


# Select university dropdown handler
@app.callback(
    [dash.dependencies.Output('score_board', 'children'),
     dash.dependencies.Output('start_debate_button', 'disabled')],
    [dash.dependencies.Input('select_university_dropdown0', 'value'),
     dash.dependencies.Input('select_university_dropdown1', 'value'),
     dash.dependencies.Input('select_debate_topic_dropdown', 'value')])
def update_score_board(uni_name_0, uni_name_1, topic):
    PlayRound['university0'] = uni_name_0
    PlayRound['university1'] = uni_name_1
    PlayRound['topic'] = topic
    min_uni, max_uni = sorted([uni_name_0, uni_name_1])
    result = mysql.execute_query(
        f"select score1, score2 from scores where university1 = '{min_uni}' and university2 = '{max_uni}' and topic = '{topic}'")
    if len(result) == 0:
        PlayRound['score0'] = 0
        PlayRound['score1'] = 0
        mysql.set_initial_score(min_uni, max_uni, topic)
        return score_widget.build_content(0, 0), False
    if uni_name_0 < uni_name_1:
        PlayRound['score0'] = result[0][0]
        PlayRound['score1'] = result[0][1]
        return score_widget.build_content(result[0][0], result[0][1]), False
    else:
        PlayRound['score0'] = result[0][1]
        PlayRound['score1'] = result[0][0]
        return score_widget.build_content(result[0][1], result[0][0]), False


@app.callback(
    [dash.dependencies.Output('list_faculty_members0', 'children'),
     dash.dependencies.Output('university_image0', 'src')],
    [dash.dependencies.Input('select_university_dropdown0', 'value')])
def university_0_selection(value):
    if value is None:
        return [], ""
    stripped_value = value.replace('\'', '\\\'')
    result = mysql.execute_query(f"SELECT photo_url FROM university WHERE name = '{stripped_value}'")
    PlayRound['university0_photo'] = result[0][0] if len(result) > 0 else ""
    return faculty_members_list_widget.build_content(mysql, value, 0), \
        result[0][0] if len(result) > 0 else ""


@app.callback(
    [dash.dependencies.Output('list_faculty_members1', 'children'),
     dash.dependencies.Output('university_image1', 'src')],
    [dash.dependencies.Input('select_university_dropdown1', 'value')])
def university_1_selection(value):
    if value is None:
        return [], ""
    stripped_value = value.replace('\'', '\\\'')
    result = mysql.execute_query(f"SELECT photo_url FROM university WHERE name = '{stripped_value}'")
    PlayRound['university1_photo'] = result[0][0] if len(result) > 0 else ""
    return faculty_members_list_widget.build_content(mysql, value, 1), \
        result[0][0] if len(result) > 0 else ""


@app.callback(
    [dash.dependencies.Output('display_faculty_info0', 'children'),
     dash.dependencies.Output('display_publication0', 'children'),
     dash.dependencies.Output('paths_to_topic0', 'children')],
    [dash.dependencies.Input('university_members_table_0', 'selected_cells'),
     dash.dependencies.Input('select_debate_topic_dropdown', 'value')],
    [dash.dependencies.State('university_members_table_0', 'data')])
def display_faculty_info0(active_cell, topic, data):
    try:
        if len(active_cell) > 0 and len(data) > 0:
            name = data[active_cell[0]['row']]['Name']
            PlayRound['player0'] = name
            return display_faculty_info_widget.build_content(mongo, name, 0), \
                display_publication_widget.build_content(mysql, name, topic), \
                paths_to_topic_widget.build_content(neo4jDB, name, topic, 0)
        else:
            return display_faculty_info_widget.build_content(mongo, "", 0), \
                display_publication_widget.build_content(mysql, "", ""), \
                paths_to_topic_widget.build_content(neo4jDB, "", topic, 0)
    except Exception as e:
        print(e)
        pass


@app.callback(
    [dash.dependencies.Output('display_faculty_info1', 'children'),
     dash.dependencies.Output('display_publication1', 'children'),
     dash.dependencies.Output('paths_to_topic1', 'children')],
    [dash.dependencies.Input('university_members_table_1', 'selected_cells'),
     dash.dependencies.Input('select_debate_topic_dropdown', 'value')],
    [dash.dependencies.State('university_members_table_1', 'data')])
def display_faculty_info1(active_cell, topic, data):
    if len(active_cell) > 0 and len(data) > 0:
        name = data[active_cell[0]['row']]['Name']
        PlayRound['player1'] = name
        return display_faculty_info_widget.build_content(mongo, name, 1), \
            display_publication_widget.build_content(mysql, name, topic), \
            paths_to_topic_widget.build_content(neo4jDB, name, topic, 1)
    else:
        return display_faculty_info_widget.build_content(mongo, "", 1), \
            display_publication_widget.build_content(mysql, "", ""), \
            paths_to_topic_widget.build_content(neo4jDB, "", topic, 1)


if __name__ == '__main__':
    app.run_server(debug=True)
