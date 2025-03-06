from enum import StrEnum, auto
import pandas as pd
import requests


class ProjectionSystem(StrEnum):
    ZIPS = auto()
    STEAMER = auto()
    ATC = auto()
    FANGRAPHSDC = auto()


class BernackiLeague(StrEnum):
    ONE_OH_EIGHT = auto()
    EAST_HARTFORD = auto()


BERNACKI_LEAGUES = [m for m in BernackiLeague.__members__]

BASE_URL = 'https://www.fangraphs.com/api/fantasy/auction-calculator/data?'
URL_PART_2 = '&players=&proj='
POSITION_TYPES = ['pit', 'hit']

SETTINGS_108_PART_1 = 'teams=12&lg=MLB&dollars=500&mb=1&mp=20&msp=5&mrp=5&type='
SETTINGS_EH_PART_1 = 'teams=12&lg=MLB&dollars=251&mb=1&mp=20&msp=5&mrp=5&type='

PROJECTION_SYSTEMS = sorted([m for m in ProjectionSystem.__members__])
SETTINGS_108_PART_2 = '&split=&points=p%7C0%2C.25%2C0%2C1%2C2%2C3%2C4%2C2%2C-1%2C1%2C1%2C1%2C-1%2C1%2C0%2C0%7C.5%2C7%2C-5%2C8%2C1%2C-1%2C0%2C-.25%2C0%2C-.5%2C0&rep=0&drp=0&pp=C%2CSS%2C2B%2C3B%2COF%2C1B&pos=1%2C1%2C1%2C1%2C3%2C1%2C0%2C0%2C0%2C1%2C0%2C0%2C7%2C6%2C0&sort=&view=0'
SETTINGS_EH_PART_2 = '&split=&points=c%7C0%2C1%2C2%2C3%2C4%7C0%2C1%2C2%2C3%2C4&rep=0&drp=0&pp=C%2CSS%2C2B%2C3B%2COF%2C1B&pos=1%2C1%2C1%2C1%2C4%2C1%2C0%2C0%2C1%2C1%2C5%2C3%2C0%2C6%2C0&sort=&view=0'

GROUPERS = ['playerid', 'PlayerName', 'Team', 'POS', 'ADP']
COLS_TO_AVG = {
    ('Hitters', 'Points'): ['PA', 'rPTS', 'PTS', 'aPOS', 'FPTS', 'Dollars'],
    ('Hitters', 'Roto'): ['PA', 'mAVG', 'mRBI', 'mR', 'mSB', 'mHR', 'PTS', 'aPOS', 'Dollars'],
    ('Pitchers', 'Points'): ['IP', 'rPTS', 'PTS', 'aPOS', 'Dollars'],
    ('Pitchers', 'Roto'): ['mW', 'mSV', 'mERA', 'mWHIP', 'mSO', 'PTS', 'aPOS', 'Dollars']
}


def _get_from_fg(url: str) -> list[dict]:
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError(f"Can't reach {url}")
    return response.json()['data']


def get_all_data() -> dict[tuple[str, str]: pd.DataFrame]:
    """Gets data from Fangraphs APIs and return a dictionary of (ex): {('Hitters', 'Points'): pd.DataFrame, ...}"""
    dataframes: dict[tuple[str, str]: list[pd.DataFrame]] = {('Hitters', 'Points'): [], ('Hitters', 'Roto'): [],
                                                             ('Pitchers', 'Points'): [], ('Pitchers', 'Roto'): []}

    # This could use a re-write
    for position_type in POSITION_TYPES:
        for proj_system in PROJECTION_SYSTEMS:
            for idx, url in enumerate((BASE_URL + SETTINGS_108_PART_1 + position_type + URL_PART_2 + proj_system.lower() + SETTINGS_108_PART_2,
                                       BASE_URL + SETTINGS_EH_PART_1 + position_type + URL_PART_2 + proj_system.lower() + SETTINGS_EH_PART_2)):
                data: list[dict] = _get_from_fg(url)
                df = pd.DataFrame(data)  # Convert list of dicts to DataFrame
                df["Hitter/Pitcher"] = position_type
                df["Projection System"] = proj_system  # Add column to track data source
                df["League Format"] = 'Points' if idx == 0 else 'Roto'
                if idx == 0 and position_type == 'hit':
                    dataframes[('Hitters', 'Points')].append(df)
                elif idx == 0 and position_type == 'pit':
                    dataframes[('Pitchers', 'Points')].append(df)
                elif idx == 1 and position_type == 'hit':
                    dataframes[('Hitters', 'Roto')].append(df)
                elif idx == 1 and position_type == 'pit':
                    dataframes[('Pitchers', 'Roto')].append(df)
                else:
                    raise ValueError('Something went wrong')

    # for each combo of hit/pitch/roto/points, concatenate all projection systems into a single dataframe
    for k, v in dataframes.items():
        dataframes[k] = pd.concat(v, ignore_index=True)

    return dataframes


if __name__ == '__main__':
    my_data_frames = get_all_data()
    for val in my_data_frames.values():
        print(len(val))
