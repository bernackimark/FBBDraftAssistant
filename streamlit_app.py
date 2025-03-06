import pandas as pd
import streamlit as st

from fg_data import get_all_data, BernackiLeague, COLS_TO_AVG, GROUPERS, POSITION_TYPES, PROJECTION_SYSTEMS

st.set_page_config(layout="wide")


@st.cache_data
def get_data() -> dict[tuple[str, str]: pd.DataFrame]:
    # return pd.DataFrame(hitter_data), pd.DataFrame(pitcher_data)
    return get_all_data()

def get_correct_df_and_value_cols() -> tuple[pd.DataFrame, list[str]]:
    hit_or_pitch = 'Pitchers' if sel_position in ('Pitchers', 'SP', 'RP') else 'Hitters'
    lg_format = 'Points' if sel_league == BernackiLeague.ONE_OH_EIGHT.name else 'Roto'
    return data[(hit_or_pitch, lg_format)], COLS_TO_AVG[(hit_or_pitch, lg_format)]

def show_table(my_df: pd.DataFrame, my_value_cols: list[str]) -> None:
    # filter based on user-selected: projection system, league (points/roto), and position (hit/pit or actual position)
    filtered_df = my_df[my_df['Projection System'].isin(sel_proj_system)]
    if sel_position == 'Hitters':
        filtered_df = filtered_df[filtered_df['Hitter/Pitcher'] == 'hit']
    elif sel_position == 'Pitchers':
        filtered_df = filtered_df[filtered_df['Hitter/Pitcher'] == 'pit']
    elif sel_position == 'UT':
        filtered_df = filtered_df[filtered_df['POS'] == 'DH']
    else:
        filtered_df = filtered_df[df_raw['POS'].str.contains(sel_position, na=False, case=False)]

    # for columns, use the common groupers (name, team, etc.) & those specific to each dataframe (runs, wins, etc.)
    filtered_df = filtered_df[GROUPERS + my_value_cols]

    # group the data, round values to zero, sort by Dollars desc
    df = filtered_df.groupby(GROUPERS)[my_value_cols].mean().round(0).reset_index().sort_values(by='Dollars', ascending=False)

    st.dataframe(df, hide_index=True, use_container_width=True)


data = get_data()

POSITIONS = ('Hitters', 'Pitchers', 'C', '1B', '2B', '3B', 'SS', 'OF', 'UT', 'SP', 'RP')

# UI
st.subheader('Bernacki FBB Draft Value Assistant')
sel_league = st.segmented_control('League', [_ for _ in BernackiLeague.__members__], label_visibility='hidden')
sel_proj_system = st.multiselect('Projection System(s)', PROJECTION_SYSTEMS)
sel_position = st.segmented_control('Position', POSITIONS, label_visibility='hidden')

if not sel_proj_system or not sel_league or not sel_position:
    st.error("Please select at least one projection system, a position, and a league")
else:
    # get the correct dataframe (there are four: Hitter-Roto, Hitter-Points, Pitcher-Roto, Pitcher-Points)
    df_raw, value_cols = get_correct_df_and_value_cols()
    show_table(df_raw, value_cols)
