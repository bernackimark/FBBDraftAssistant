import pandas as pd
import streamlit as st

from fg_data import url_108_zips, url_108_atc, url_108_steamer, url_108_fangraphsdc, get_data_as_df, ProjectionSystem

st.set_page_config(layout="wide")

POSITIONS = ('C', '1B', '2B', '3B', 'SS', 'OF', 'DH')

proj_urls = {
    'ZIPS': url_108_zips,
    'ATC': url_108_atc,
    'STEAMER': url_108_steamer,
    'FANGRAPHSDC': url_108_fangraphsdc
}

pos_endpoint_map = {
    'Hitters': 'hit',
    'Pitchers': 'pit',
    'C': 'C',
    '1B': '1B',
    '2B': '2B',
    '3B': '3B',
    'SS': 'SS',
    'OF': 'OF',
    'UT': 'UT'
}

sel_proj_systems: list[str] = st.multiselect('Projection Systems:', sorted([m for m in ProjectionSystem.__members__]))
sel_pos: str = st.segmented_control('HOP', pos_endpoint_map.keys(),
                                                  label_visibility='hidden', default='Hitters')

if sel_proj_systems:
    df_raw: pd.DataFrame = get_data_as_df([proj_urls[ps] for ps in sel_proj_systems])
    df_raw = df_raw[['playerid', 'PlayerName', 'Team', 'POS', 'ADP', 'PA', 'rPTS', 'PTS', 'aPOS', 'FPTS', 'Dollars']]
    st.write(f"Player Projections: {len(df_raw)}. Unique Players: {df_raw['playerid'].nunique()}")
    groupers = ['playerid', 'PlayerName', 'Team', 'POS', 'ADP']
    values_for_averaging = ['PA', 'rPTS', 'PTS', 'aPOS', 'FPTS', 'Dollars']
    df = df_raw.groupby(groupers)[values_for_averaging].mean().round(0).reset_index()
    df.sort_values(by='Dollars', ascending=False, inplace=True)
    df.round(0)
    st.subheader('C')
    st.dataframe(df, hide_index=True, use_container_width=True)


# pull the data once for all projection systems -- pitchers and hitters
# pitchers will have different columns than hitters
# based on the selected projection system & position, filter what dataframes are used in pd.concat()
# filter position based on 'POS' column
# handle UT as only DH


