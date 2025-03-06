"""Presently not being used in the project"""

# TODO: the order of position_count doesn't seem to line up w the query parm order
from urllib import parse

import streamlit as st

def convert_league_stat_points_to_query_param(hitter_values: list[int | float], pitcher_values: list[int | float]):
    """Accepts list of ints/floats (which must be ordered exactly) into the URL query parameter for the key 'points'"""
    values = hitter_values + pitcher_values
    # Split values into two equal parts
    mid = len(values) // 2
    part1 = values[:mid]
    part2 = values[mid:]

    # Convert values to comma-separated strings
    part1_str = ','.join(map(str, part1))
    part2_str = ','.join(map(str, part2))

    # Combine with the required format
    points_param = f"p%7C{parse.quote(part1_str)}%7C{parse.quote(part2_str)}"

    return f"points={points_param}"

points_categories_bat = ['PA', 'AB', 'H', '1B', '2B', '3B', 'HR', 'SB', 'CS', 'R', 'RBI', 'BB', 'SO', 'HBP', 'SF', 'SH']
points_categories_pit = ['IP', 'W', 'L', 'SV', 'K', 'ER', 'RA', 'HA', 'HRA', 'BBI', 'HLD']
positions_count = ['C', '1B', '2B', 'SS', '3B', 'OF', 'MI', 'CI', 'IF', 'UT', 'SP', 'RP', 'P', 'Bench', 'Min IP']

forced_parameters = {
    'dollars': 500,
    'league': 'MLB',
    'mb': 1,  # minimum bid
    'players': None,  # this would be for specific players either included or excluded (not sure)
    'split': None,  # this is for bat split % & pitch split %, not exactly certain what this means
    'rep': 0,  # unknown key, default is 0
    'pp': 'C%2CSS%2C2B%2C3B%2COF%2C1B',  # position priority  (i've never used this)
    'sort': None,  # default is blank
    'view': 0,  # default is 0, don't know what this does
}
with st.expander('League Settings', expanded=False):
    points_col, positions_col, other_col = st.columns([1, 1, 1])
    with points_col:
        points_container = st.container(border=True)
        points_container.write('Points')
        points_col_hit, points_col_pit = points_container.columns([1, 1])
    with positions_col:
        positions_container = st.container(border=True)
        positions_container.write('Starting Positions')
    with other_col:
        other_container = st.container(border=True)
        other_container.write('Other Settings')

sel_parameters = {
    'teams': other_container.number_input('Teams', 1, 20, 12),
    'mp': other_container.number_input('Min Eligibility: Positional Starts', 1, 100, 20),
    'msp': other_container.number_input('Min Eligibility: Starts (SP)', 1, 100, 5),
    'mrp': other_container.number_input('Min Eligibility Relief Appearances', 1, 100, 5),
    'type': st.segmented_control('HOP', pos_endpoint_map.keys(), label_visibility='hidden', default='Hitters'),
    'proj': st.multiselect('Projection Systems:', sorted([m for m in ProjectionSystem.__members__])),
    'points_hit': [points_col_hit.number_input(label, value=0.0, step=0.05) for label in points_categories_bat],
    'points_pit': [points_col_pit.number_input(label, value=0.0, step=0.05) for label in points_categories_pit],
    'drp': other_container.number_input('Artificially Deflate Relief Pitchers', 0, 100, 0),
    'pos': '%2'.join([str(positions_container.number_input(label, step=1)) for label in positions_count]),
}
# TODO: points_hit & points_pit aren't actually query parameters, it's just 'points' ... it's chopped up for aesthetics
#  need to use convert_league_stats_points_to_query_param

st.session_state['params'] = sel_parameters | forced_parameters