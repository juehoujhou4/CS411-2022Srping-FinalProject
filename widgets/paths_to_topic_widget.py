# This widget is used to visualize relationship of a faculty member with the given topic (keyword)
import dash
from dash import html
import dash_cytoscape as cyto


def build_content(neo4jdb, faculty_name: str, keyword: str, player: int ) -> html.Div:
    paths = neo4jdb.get_shortest_paths(faculty_name, keyword)

    # Build graph, nodes and relations
    nodes_map = {}
    edges_map = {}
    for path in paths:
        start_node_id = path[0].start_node.id
        end_node_de = path[0].end_node.id
        for node in path[0].nodes:
            node_id = node.id
            if node_id not in nodes_map:
                node_label = node['name'] if 'name' in node else ""
                nodes_map[node_id] = {
                    'id': node_id,
                    'data': {
                        'id': node_id,
                        'label': node_label,
                        'tooltip': node['title'] if 'title' in node else node_label,
                    },
                    'style': {
                        'background-color': 'orange',
                        'shape': 'circle',
                    }
                }
                # Set color based on node type
                node_type = list(node.labels)[0]
                if node_type == 'FACULTY':
                    nodes_map[node_id]['style']['background-color'] = 'red'
                elif node_type == 'KEYWORD':
                    nodes_map[node_id]['style']['background-color'] = 'green'
                elif node_type == 'INSTITUTE':
                    nodes_map[node_id]['style']['background-color'] = 'blue'
                # Set shape and size for start and end nodes
                if node_id == start_node_id  or node_id == end_node_de:
                    nodes_map[node_id]['style']['shape'] = 'star'
                    nodes_map[node_id]['style']['width'] = '50px'
                    nodes_map[node_id]['style']['height'] = '50px'


        for rel in path[0].relationships:
            if rel.id not in edges_map:
                edges_map[rel.id] = {
                    'data': {
                        'id': rel.id,
                        'source': rel.start_node.id,
                        'target': rel.end_node.id,
                    },
                    'style': {
                        'line-color': 'grey',
                    }
                }
                #Set color based on relationship type
                if rel.type == 'PUBLISH':
                    edges_map[rel.id]['style']['line-color'] = 'lightblue'
                elif rel.type == 'LABEL_BY':
                    edges_map[rel.id]['style']['line-color'] = 'lightgreen'
                elif rel.type == 'INTERESTED_IN':
                    edges_map[rel.id]['style']['line-color'] = 'lightgrey'
                elif rel.type == 'AFFILIATED_WITH':
                    edges_map[rel.id]['style']['line-color'] = 'lightyellow'

    content = html.Div([
        html.H4("Shortest paths to discussion topic"),
        html.Div("Hover over a node", id='tooltip-text' + str(player), style={'font-size': '12px'}),
        cyto.Cytoscape(
            id='path_to_topic' + str(player),
            layout={'name': 'breadthfirst'},
            style={
                'width': '100%',
                'height': '400px',
                'display': 'left',
                'border': '1px solid black',
                'margin': 'auto',
                'text-valign': 'center',
                'background-color': '#f7f7f7',
                'line-color': '#9dbaea',
                'target-arrow-color': '#9dbaea',
                'source-arrow-color': '#9dbaea',
                'font-size': '14px',
                'font-family': 'Arial',
                'text-outline-width': '0px'
            },
            elements={
                "nodes": list(nodes_map.values()),
                "edges": list(edges_map.values())
            }
        ),

    ], style={'width': '100%', 'height': '100%', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center'})

    return content