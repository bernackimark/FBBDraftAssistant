from dataclasses import dataclass
from enum import StrEnum, auto
import pandas as pd
import requests
from typing import Any

# EH league settings
url_eh='https://www.fangraphs.com/api/fantasy/auction-calculator/data?teams=12&lg=MLB&dollars=251&mb=1&mp=20&msp=5&mrp=5&type=C&players=&proj=zips&split=&points=c%7C0%2C1%2C2%2C3%2C4%7C0%2C1%2C2%2C3%2C4&rep=0&drp=0&pp=C%2CSS%2C2B%2C3B%2COF%2C1B&pos=1%2C1%2C1%2C1%2C4%2C1%2C0%2C0%2C1%2C1%2C5%2C3%2C0%2C6%2C0&sort=&view=0'

# 108 league settings
url_108='https://www.fangraphs.com/api/fantasy/auction-calculator/data?teams=12&lg=MLB&dollars=500&mb=1&mp=20&msp=5&mrp=5&type=C&players=&proj=zips&split=&points=p%7C0%2C.25%2C0%2C1%2C2%2C3%2C4%2C2%2C-1%2C1%2C1%2C1%2C-1%2C1%2C0%2C0%7C.5%2C7%2C-5%2C8%2C1%2C-1%2C0%2C-.25%2C0%2C-.5%2C0&rep=0&drp=0&pp=C%2CSS%2C2B%2C3B%2COF%2C1B&pos=1%2C1%2C1%2C1%2C3%2C1%2C0%2C0%2C0%2C1%2C0%2C0%2C7%2C6%2C0&sort=&view=0'
url_108_zips='https://www.fangraphs.com/api/fantasy/auction-calculator/data?teams=12&lg=MLB&dollars=500&mb=1&mp=20&msp=5&mrp=5&type=C&players=&proj=zips&split=&points=p%7C0%2C.25%2C0%2C1%2C2%2C3%2C4%2C2%2C-1%2C1%2C1%2C1%2C-1%2C1%2C0%2C0%7C.5%2C7%2C-5%2C8%2C1%2C-1%2C0%2C-.25%2C0%2C-.5%2C0&rep=0&drp=0&pp=C%2CSS%2C2B%2C3B%2COF%2C1B&pos=1%2C1%2C1%2C1%2C3%2C1%2C0%2C0%2C0%2C1%2C0%2C0%2C7%2C6%2C0&sort=&view=0'
url_108_steamer='https://www.fangraphs.com/api/fantasy/auction-calculator/data?teams=12&lg=MLB&dollars=500&mb=1&mp=20&msp=5&mrp=5&type=C&players=&proj=steamer&split=&points=p%7C0%2C.25%2C0%2C1%2C2%2C3%2C4%2C2%2C-1%2C1%2C1%2C1%2C-1%2C1%2C0%2C0%7C.5%2C7%2C-5%2C8%2C1%2C-1%2C0%2C-.25%2C0%2C-.5%2C0&rep=0&drp=0&pp=C%2CSS%2C2B%2C3B%2COF%2C1B&pos=1%2C1%2C1%2C1%2C3%2C1%2C0%2C0%2C0%2C1%2C0%2C0%2C7%2C6%2C0&sort=&view=0'
url_108_atc='https://www.fangraphs.com/api/fantasy/auction-calculator/data?teams=12&lg=MLB&dollars=500&mb=1&mp=20&msp=5&mrp=5&type=C&players=&proj=atc&split=&points=p%7C0%2C.25%2C0%2C1%2C2%2C3%2C4%2C2%2C-1%2C1%2C1%2C1%2C-1%2C1%2C0%2C0%7C.5%2C7%2C-5%2C8%2C1%2C-1%2C0%2C-.25%2C0%2C-.5%2C0&rep=0&drp=0&pp=C%2CSS%2C2B%2C3B%2COF%2C1B&pos=1%2C1%2C1%2C1%2C3%2C1%2C0%2C0%2C0%2C1%2C0%2C0%2C7%2C6%2C0&sort=&view=0'
url_108_fangraphsdc='https://www.fangraphs.com/api/fantasy/auction-calculator/data?teams=12&lg=MLB&dollars=500&mb=1&mp=20&msp=5&mrp=5&type=C&players=&proj=fangraphsdc&split=&points=p%7C0%2C.25%2C0%2C1%2C2%2C3%2C4%2C2%2C-1%2C1%2C1%2C1%2C-1%2C1%2C0%2C0%7C.5%2C7%2C-5%2C8%2C1%2C-1%2C0%2C-.25%2C0%2C-.5%2C0&rep=0&drp=0&pp=C%2CSS%2C2B%2C3B%2COF%2C1B&pos=1%2C1%2C1%2C1%2C3%2C1%2C0%2C0%2C0%2C1%2C0%2C0%2C7%2C6%2C0&sort=&view=0'




class ProjectionSystem(StrEnum):
    ZIPS = auto()
    STEAMER = auto()
    ATC = auto()
    FANGRAPHSDC = auto()


@dataclass
class PlayerRotoHitterURLParameters:
    teams: int
    team_budget: int  # key is dollars
    min_bid: int  # key is mb
    starts_to_qualify_at_pp: int  # key is mp
    starts_to_qualify_at_sp: int  # key is sp
    starts_to_qualify_at_rp: int  # key is rp
    position: str  # key is type ... bat, pit, C, 1B, 2B, SS, 3B, OF, DH, MI, CI, IF, SP, RP
    players: Any  # this might be for keepers?
    projection_system: ProjectionSystem  # key is proj ... zips, steamer, atc
    split: int  # key is split ... this is for bat split % & pitch split %, leaving this blank
    points: Any  # key is points ... points=c%7C0%2C1%2C2%2C3%2C4%7C0%2C1%2C2%2C3%2C4
    rep: Any  # key is rep ... default is 0
    deflate_rp: int  # key is drp ... default is 0
    position_players: Any  # key is pp, looks like a list of C%2CSS%2C2B%2C3B%2COF%2C1B
    position_counts: Any  # key is pos, 1%2C1%2C1%2C1%2C4%2C1%2C0%2C0%2C1%2C1%2C5%2C3%2C0%2C6%2C0
    sort: Any  # key is sort, default is blank
    view: int  # key is view, default is 0


@dataclass
class RotoHitter:
    Name: str
    playerid: str
    Team: str
    PlayerName: str
    firstLastName: str
    UPURL: str
    xMLBAMID: int
    POS: str
    ADP: float
    PA: float
    mAVG: float
    mRBI: float
    mR: float
    mSB: float
    mHR: float
    PTS: float
    aPOS: float
    FPTS: float
    Dollars: float
    Adjusted: float
    Cost: Any
    cPOS: int


@dataclass
class PointsHitter:
    Name: str
    playerid: str
    Team: str
    PlayerName: str
    firstLastName: str
    UPURL: str
    xMLBAMID: int
    POS: str
    ADP: float
    PA: float
    rPTS: float
    PTS: float
    aPOS: float
    FPTS: float
    Dollars: float
    Adjusted: float
    Cost: Any
    cPOS: int


@dataclass
class RotoPitcher:
    Name: str
    playerid: str
    Team: str
    PlayerName: str
    firstLastName: str
    UPURL: str
    xMLBAMID: int
    POS: str
    ADP: float
    IP: float
    mW: float
    mSV: float
    mERA: float
    mWHIP: float
    mSO: float
    PTS: float
    aPOS: float
    FPTS: float
    Dollars: float
    Adjusted: float
    Cost: Any  # default is null/None
    cPOS: int


@dataclass
class PointsPitcher:
    Name: str
    playerid: str
    Team: str
    PlayerName: str
    firstLastName: str
    UPURL: str
    xMLBAMID: int
    POS: str
    ADP: float
    IP: float
    rPTS: float
    PTS: float
    aPOS: float
    FPTS: float
    Dollars: float
    Adjusted: float
    Cost: Any  # default is null/None
    cPOS: int


# resp = requests.get(url_eh).json()
# data: list[dict] = resp['data']
# ui_table_headers: list[str] = resp['dataColumns']
#
# for p in data:
#     print(RotoHitter(**p))
#     break
#
# print()
#
# resp = requests.get(url_108).json()
# data: list[dict] = resp['data']
# ui_table_headers: list[str] = resp['dataColumns']
#
# for p in data:
#     print(PointsHitter(**p))
#     break


def get_data_as_df(end_points: list[str]) -> pd.DataFrame:
    data_frames = []
    for url in end_points:
        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError(f"Can't reach {url}")
        data = response.json()['data']
        df = pd.DataFrame(data)  # Convert list of dicts to DataFrame
        df["source"] = url  # Add column to track data source
        data_frames.append(df)

    return pd.concat(data_frames, ignore_index=True)


if __name__ == '__main__':
    get_data_as_df([url_eh, url_108])
