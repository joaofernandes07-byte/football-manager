import io
import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from dash import dash_table
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# -------------------------------------------------------------
# EMBEDDED DATASET (GARANTE QUE FUNCIONA NO RENDER SEM ERROS DE FICHEIRO)
# -------------------------------------------------------------
CSV_DATA = """year,decade,award_era,awarded,player,country,modern_country,confederation,club,club_league,position,age_at_win,season_goals,season_assists,winner_points,runner_up,runner_up_country,third_place,third_place_country,key_achievement,general_position,goal_contributions
1956,1950s,European Players Only,True,Stanley Matthews,England,England,UEFA,Blackpool,England (First Division),Forward / Winger,41,3,12,47,Alfredo Di Stéfano,Spain,Raymond Kopa,France,FA Cup Finalist,Forward,15
1957,1950s,European Players Only,True,Alfredo Di Stéfano,Spain,Spain,UEFA,Real Madrid,Spain (La Liga),Forward,31,43,10,72,Billy Wright,England,Duncan Edwards / Raymond Kopa,England / France,European Cup & La Liga,Forward,53
1958,1950s,European Players Only,True,Raymond Kopa,France,France,UEFA,Real Madrid,Spain (La Liga),Attacking Midfielder / Forward,27,11,15,71,Helmut Rahn,West Germany,Just Fontaine,France,European Cup & 3rd Place World Cup,Midfielder,26
1959,1950s,European Players Only,True,Alfredo Di Stéfano,Spain,Spain,UEFA,Real Madrid,Spain (La Liga),Forward,33,34,11,80,Raymond Kopa,France,John Charles,Wales,European Cup,Forward,45
1960,1960s,European Players Only,True,Luis Suárez,Spain,Spain,UEFA,Barcelona,Spain (La Liga),Midfielder,25,14,18,54,Ferenc Puskás,Hungary,Uwe Seeler,West Germany,La Liga & Inter-Cities Fairs Cup,Midfielder,32
1961,1960s,European Players Only,True,Omar Sívori,Italy,Italy,UEFA,Juventus,Italy (Serie A),Forward,26,28,12,46,Luis Suárez,Spain,Johnny Haynes,England,Serie A,Forward,40
1962,1960s,European Players Only,True,Josef Masopust,Czechoslovakia,Czech Republic,UEFA,Dukla Prague,Czechoslovakia (1. Liga),Midfielder,31,12,14,65,Eusébio,Portugal,Karl-Heinz Schnellinger,West Germany,World Cup Finalist & Czechoslovak First League,Midfielder,26
1963,1960s,European Players Only,True,Lev Yashin,Soviet Union,Soviet Union,UEFA,Dynamo Moscow,USSR (Top League),Goalkeeper,34,0,0,73,Gianni Rivera,Italy,Jimmy Greaves,England,Soviet Top League,Goalkeeper,0
1964,1960s,European Players Only,True,Denis Law,Scotland,Scotland,UEFA,Manchester United,England (First Division),Forward,24,46,9,61,Luis Suárez,Spain,Amancio,Spain,46 Goals in Season,Forward,55
1965,1960s,European Players Only,True,Eusébio,Portugal,Portugal,UEFA,Benfica,Portugal (Primeira Divisão),Forward,23,48,11,67,Giacinto Facchetti,Italy,Luis Suárez,Spain,Primeira Divisão & European Cup Finalist,Forward,59
1966,1960s,European Players Only,True,Bobby Charlton,England,England,UEFA,Manchester United,England (First Division),Attacking Midfielder,29,18,15,81,Eusébio,Portugal,Franz Beckenbauer,West Germany,1966 FIFA World Cup Winner,Midfielder,33
1967,1960s,European Players Only,True,Flórián Albert,Hungary,Hungary,UEFA,Ferencváros,Hungary (NB I),Forward,26,28,10,68,Bobby Charlton,England,Jimmy Johnstone,Scotland,Hungarian League,Forward,38
1968,1960s,European Players Only,True,George Best,Northern Ireland,Northern Ireland,UEFA,Manchester United,England (First Division),Winger / Forward,22,32,14,61,Bobby Charlton,England,Dragan Džajić,Yugoslavia,European Cup,Forward,46
1969,1960s,European Players Only,True,Gianni Rivera,Italy,Italy,UEFA,AC Milan,Italy (Serie A),Attacking Midfielder,26,11,19,83,Luigi Riva,Italy,Gerd Müller,West Germany,European Cup & Intercontinental Cup,Midfielder,30
1970,1970s,European Players Only,True,Gerd Müller,West Germany,Germany,UEFA,Bayern Munich,Germany (Bundesliga),Forward,25,42,6,77,Bobby Moore,England,Luigi Riva,Italy,1970 World Cup Golden Boot (10 goals),Forward,48
1971,1970s,European Players Only,True,Johan Cruyff,Netherlands,Netherlands,UEFA,Ajax,Netherlands (Eredivisie),Forward / Midfielder,24,27,21,116,Sandro Mazzola,Italy,George Best,Northern Ireland,European Cup,Forward,48
1972,1970s,European Players Only,True,Franz Beckenbauer,West Germany,Germany,UEFA,Bayern Munich,Germany (Bundesliga),Defender / Sweeper,27,6,11,81,Gerd Müller / Günter Netzer,West Germany,None,None,Euro 1972 & Bundesliga,Defender,17
1973,1970s,European Players Only,True,Johan Cruyff,Netherlands,Netherlands,UEFA,Ajax / Barcelona,Spain (La Liga),Forward / Midfielder,26,24,22,96,Dino Zoff,Italy,Gerd Müller,West Germany,European Cup & La Liga,Forward,46
1974,1970s,European Players Only,True,Johan Cruyff,Netherlands,Netherlands,UEFA,Barcelona,Spain (La Liga),Forward / Midfielder,27,19,20,116,Franz Beckenbauer,West Germany,Kazimierz Deyna,Poland,La Liga & World Cup Finalist,Forward,39
1975,1970s,European Players Only,True,Oleg Blokhin,Soviet Union,Soviet Union,UEFA,Dynamo Kyiv,USSR (Top League),Forward,23,25,9,122,Franz Beckenbauer,West Germany,Johan Cruyff,Netherlands,European Cup Winners' Cup & UEFA Super Cup,Forward,34
1976,1970s,European Players Only,True,Franz Beckenbauer,West Germany,Germany,UEFA,Bayern Munich,Germany (Bundesliga),Defender / Sweeper,31,5,10,91,Rob Rensenbrink,Netherlands,Ivo Viktor,Czechoslovakia,European Cup & Intercontinental Cup,Defender,15
1977,1970s,European Players Only,True,Allan Simonsen,Denmark,Denmark,UEFA,Borussia Mönchengladbach,Germany (Bundesliga),Forward,25,18,12,74,Kevin Keegan,England,Michel Platini,France,Bundesliga & European Cup Finalist,Forward,30
1978,1970s,European Players Only,True,Kevin Keegan,England,England,UEFA,Hamburger SV,Germany (Bundesliga),Forward,27,17,13,87,Hans Krankl,Austria,Rob Rensenbrink,Netherlands,Bundesliga,Forward,30
1979,1970s,European Players Only,True,Kevin Keegan,England,England,UEFA,Hamburger SV,Germany (Bundesliga),Forward,28,17,14,118,Karl-Heinz Rummenigge,West Germany,Ruud Krol,Netherlands,Bundesliga,Forward,31
1980,1980s,European Players Only,True,Karl-Heinz Rummenigge,West Germany,Germany,UEFA,Bayern Munich,Germany (Bundesliga),Forward,25,29,11,122,Bernd Schuster,West Germany,Michel Platini,France,Euro 1980 & Bundesliga,Forward,40
1981,1980s,European Players Only,True,Karl-Heinz Rummenigge,West Germany,Germany,UEFA,Bayern Munich,Germany (Bundesliga),Forward,26,29,10,106,Paul Breitner,West Germany,Bernd Schuster,West Germany,Bundesliga,Forward,39
1982,1980s,European Players Only,True,Paolo Rossi,Italy,Italy,UEFA,Juventus,Italy (Serie A),Forward,26,13,4,115,Alain Giresse,France,Zbigniew Boniek,Poland,1982 FIFA World Cup Winner & Golden Boot,Forward,17
1983,1980s,European Players Only,True,Michel Platini,France,France,UEFA,Juventus,Italy (Serie A),Attacking Midfielder,28,28,14,110,Kenny Dalglish,Scotland,Allan Simonsen,Denmark,Coppa Italia & Serie A Top Scorer,Midfielder,42
1984,1980s,European Players Only,True,Michel Platini,France,France,UEFA,Juventus,Italy (Serie A),Attacking Midfielder,29,25,16,128,Jean Tigana,France,Preben Elkjær,Denmark,Euro 1984 (9 goals) & Serie A,Midfielder,41
1985,1980s,European Players Only,True,Michel Platini,France,France,UEFA,Juventus,Italy (Serie A),Attacking Midfielder,30,29,15,127,Preben Elkjær,Denmark,Bernd Schuster,West Germany,European Cup & Intercontinental Cup,Midfielder,44
1986,1980s,European Players Only,True,Igor Belanov,Soviet Union,Soviet Union,UEFA,Dynamo Kyiv,USSR (Top League),Forward,26,20,8,84,Gary Lineker,England,Emilio Butragueño,Spain,European Cup Winners' Cup & Soviet Top League,Forward,28
1987,1980s,European Players Only,True,Ruud Gullit,Netherlands,Netherlands,UEFA,PSV / AC Milan,Italy (Serie A),Midfielder / Forward,25,24,15,106,Paulo Futre,Portugal,Emilio Butragueño,Spain,Eredivisie (PSV),Midfielder,39
1988,1980s,European Players Only,True,Marco van Basten,Netherlands,Netherlands,UEFA,AC Milan,Italy (Serie A),Forward,24,19,6,129,Ruud Gullit,Netherlands,Frank Rijkaard,Netherlands,Euro 1988 & Serie A,Forward,25
1989,1980s,European Players Only,True,Marco van Basten,Netherlands,Netherlands,UEFA,AC Milan,Italy (Serie A),Forward,25,32,8,119,Franco Baresi,Italy,Frank Rijkaard,Netherlands,European Cup & Intercontinental Cup,Forward,40
1990,1990s,European Players Only,True,Lothar Matthäus,West Germany,Germany,UEFA,Inter Milan,Italy (Serie A),Midfielder,29,13,12,137,Salvatore Schillaci,Italy,Andreas Brehme,West Germany,1990 FIFA World Cup Winner,Midfielder,25
1991,1990s,European Players Only,True,Jean-Pierre Papin,France,France,UEFA,Marseille,France (Ligue 1),Forward,28,36,7,141,Dejan Savićević / Darko Pančev / Lothar Matthäus,Yugoslavia / Germany,None,None,Ligue 1 & European Cup Finalist,Forward,43
1992,1990s,European Players Only,True,Marco van Basten,Netherlands,Netherlands,UEFA,AC Milan,Italy (Serie A),Forward,28,29,9,98,Hristo Stoichkov,Bulgaria,Dennis Bergkamp,Netherlands,Serie A (Unbeaten),Forward,38
1993,1990s,European Players Only,True,Roberto Baggio,Italy,Italy,UEFA,Juventus,Italy (Serie A),Attacking Midfielder / Forward,26,30,14,142,Dennis Bergkamp,Netherlands,Eric Cantona,France,UEFA Cup,Midfielder,44
1994,1990s,European Players Only,True,Hristo Stoichkov,Bulgaria,Bulgaria,UEFA,Barcelona,Spain (La Liga),Forward,28,24,11,210,Roberto Baggio,Italy,Paolo Maldini,Italy,La Liga & 1994 World Cup Golden Boot,Forward,35
1995,1990s,European Club Players,True,George Weah,Liberia,Liberia,CAF,Paris Saint-Germain / AC Milan,Italy (Serie A),Forward,29,18,9,144,Jürgen Klinsmann,Germany,Jari Litmanen,Finland,Coupe de France & Champions League Top Scorer,Forward,27
1996,1990s,European Club Players,True,Matthias Sammer,Germany,Germany,UEFA,Borussia Dortmund,Germany (Bundesliga),Defender / Sweeper,29,5,6,144,Ronaldo,Brazil,Alan Shearer,England,Euro 1996 & Bundesliga,Defender,11
1997,1990s,European Club Players,True,Ronaldo,Brazil,Brazil,CONMEBOL,Barcelona / Inter Milan,Italy (Serie A),Forward,21,47,12,222,Predrag Mijatović,Yugoslavia,Zinédine Zidane,France,UEFA Cup Winners' Cup & Copa América 1997,Forward,59
1998,1990s,European Club Players,True,Zinédine Zidane,France,France,UEFA,Juventus,Italy (Serie A),Attacking Midfielder,26,11,16,244,Davor Šuker,Croatia,Ronaldo,Brazil,1998 FIFA World Cup Winner & Serie A,Midfielder,27
1999,1990s,European Club Players,True,Rivaldo,Brazil,Brazil,CONMEBOL,Barcelona,Spain (La Liga),Attacking Midfielder / Forward,27,29,15,219,David Beckham,England,Andriy Shevchenko,Ukraine,La Liga & Copa América 1999,Midfielder,44
2000,2000s,European Club Players,True,Luís Figo,Portugal,Portugal,UEFA,Barcelona / Real Madrid,Spain (La Liga),Winger / Midfielder,28,14,22,197,Zinédine Zidane,France,Andriy Shevchenko,Ukraine,Euro 2000 Semi-Finalist,Forward,36
2001,2000s,European Club Players,True,Michael Owen,England,England,UEFA,Liverpool,England (Premier League),Forward,22,24,7,176,Raúl,Spain,Oliver Kahn,Germany,UEFA Cup, FA Cup & League Cup,Forward,31
2002,2000s,European Club Players,True,Ronaldo,Brazil,Brazil,CONMEBOL,Inter Milan / Real Madrid,Spain (La Liga),Forward,26,15,3,169,Roberto Carlos,Brazil,Oliver Kahn,Germany,2002 FIFA World Cup Winner (8 goals),Forward,18
2003,2000s,European Club Players,True,Pavel Nedvěd,Czech Republic,Czech Republic,UEFA,Juventus,Italy (Serie A),Midfielder,31,14,17,190,Thierry Henry,France,Paolo Maldini,Italy,Serie A & Champions League Finalist,Midfielder,31
2004,2000s,European Club Players,True,Andriy Shevchenko,Ukraine,Ukraine,UEFA,AC Milan,Italy (Serie A),Forward,28,29,5,175,Deco,Portugal,Ronaldinho,Brazil,Serie A & Capocannoniere,Forward,34
2005,2000s,European Club Players,True,Ronaldinho,Brazil,Brazil,CONMEBOL,Barcelona,Spain (La Liga),Attacking Midfielder / Winger,25,13,16,225,Frank Lampard,England,Steven Gerrard,England,La Liga & FIFA Confederations Cup,Midfielder,29
2006,2000s,European Club Players,True,Fabio Cannavaro,Italy,Italy,UEFA,Juventus / Real Madrid,Spain (La Liga),Center-Back,33,4,1,173,Gianluigi Buffon,Italy,Thierry Henry,France,2006 FIFA World Cup Winner,Defender,5
2007,2000s,Global Era,True,Kaká,Brazil,Brazil,CONMEBOL,AC Milan,Italy (Serie A),Attacking Midfielder,25,18,11,444,Cristiano Ronaldo,Portugal,Lionel Messi,Argentina,Champions League & FIFA Club World Cup,Midfielder,29
2008,2000s,Global Era,True,Cristiano Ronaldo,Portugal,Portugal,UEFA,Manchester United,England (Premier League),Winger / Forward,23,42,8,446,Lionel Messi,Argentina,Fernando Torres,Spain,Champions League, Premier League & European Golden Shoe,Forward,50
2009,2000s,Global Era,True,Lionel Messi,Argentina,Argentina,CONMEBOL,Barcelona,Spain (La Liga),Forward / Winger,22,38,18,473,Cristiano Ronaldo,Portugal,Xavi,Spain,Continental Treble (Champions League, La Liga, Copa del Rey),Forward,56
2010,2010s,FIFA Ballon d'Or,True,Lionel Messi,Argentina,Argentina,CONMEBOL,Barcelona,Spain (La Liga),Forward,23,47,11,2265,Andrés Iniesta,Spain,Xavi,Spain,La Liga & European Golden Shoe,Forward,58
2011,2010s,FIFA Ballon d'Or,True,Lionel Messi,Argentina,Argentina,CONMEBOL,Barcelona,Spain (La Liga),Forward,24,53,24,4788,Cristiano Ronaldo,Portugal,Xavi,Spain,Champions League & La Liga,Forward,77
2012,2010s,FIFA Ballon d'Or,True,Lionel Messi,Argentina,Argentina,CONMEBOL,Barcelona,Spain (La Liga),Forward,25,73,29,4160,Cristiano Ronaldo,Portugal,Andrés Iniesta,Spain,Record 91 Calendar Year Goals & Golden Shoe,Forward,102
2013,2010s,FIFA Ballon d'Or,True,Cristiano Ronaldo,Portugal,Portugal,UEFA,Real Madrid,Spain (La Liga),Winger / Forward,28,55,13,1365,Lionel Messi,Argentina,Franck Ribéry,France,69 Calendar Year Goals & World Cup Play-off,Forward,68
2014,2010s,FIFA Ballon d'Or,True,Cristiano Ronaldo,Portugal,Portugal,UEFA,Real Madrid,Spain (La Liga),Winger / Forward,29,51,17,3766,Lionel Messi,Argentina,Manuel Neuer,Germany,Champions League (La Décima) & Golden Shoe,Forward,68
2015,2010s,FIFA Ballon d'Or,True,Lionel Messi,Argentina,Argentina,CONMEBOL,Barcelona,Spain (La Liga),Forward / Winger,28,58,27,4133,Cristiano Ronaldo,Portugal,Neymar,Brazil,Continental Treble (Champions League, La Liga, Copa del Rey),Forward,85
2016,2010s,France Football Return,True,Cristiano Ronaldo,Portugal,Portugal,UEFA,Real Madrid,Spain (La Liga),Forward / Winger,31,51,15,745,Lionel Messi,Argentina,Antoine Griezmann,France,Champions League & Euro 2016,Forward,66
2017,2010s,France Football Return,True,Cristiano Ronaldo,Portugal,Portugal,UEFA,Real Madrid,Spain (La Liga),Forward,32,42,12,946,Lionel Messi,Argentina,Neymar,Brazil,Champions League & La Liga,Forward,54
2018,2010s,France Football Return,True,Luka Modrić,Croatia,Croatia,UEFA,Real Madrid,Spain (La Liga),Midfielder,33,2,8,753,Cristiano Ronaldo,Portugal,Antoine Griezmann,France,Champions League & World Cup Finalist (Golden Ball),Midfielder,10
2019,2010s,France Football Return,True,Lionel Messi,Argentina,Argentina,CONMEBOL,Barcelona,Spain (La Liga),Forward,32,51,22,686,Virgil van Dijk,Netherlands,Cristiano Ronaldo,Portugal,La Liga & European Golden Shoe,Forward,73
2020,2020s,Cancelled (COVID-19),False,,,,,,,,,,,,,,,,Cancelled due to COVID-19 pandemic,,
2021,2020s,France Football Return,True,Lionel Messi,Argentina,Argentina,CONMEBOL,Barcelona / Paris Saint-Germain,France (Ligue 1),Forward,34,38,14,613,Robert Lewandowski,Poland,Jorginho,Italy,Copa América 2021,Forward,52
2022,2020s,Season-Based Format,True,Karim Benzema,France,France,UEFA,Real Madrid,Spain (La Liga),Forward,34,44,15,549,Sadio Mané,Senegal,Kevin De Bruyne,Belgium,Champions League & La Liga,Forward,59
2023,2020s,Season-Based Format,True,Lionel Messi,Argentina,Argentina,CONMEBOL,Paris Saint-Germain / Inter Miami,USA (MLS),Forward,36,21,20,462,Erling Haaland,Norway,Kylian Mbappé,France,2022 FIFA World Cup Winner (Golden Ball),Forward,41
2024,2020s,Season-Based Format (UEFA),True,Rodri,Spain,Spain,UEFA,Manchester City,England (Premier League),Midfielder,28,9,14,1170,Vinícius Júnior,Brazil,Jude Bellingham,England,Euro 2024 & Premier League,Midfielder,23
"""

# -------------------------------------------------------------
# LOAD DATA & CLASSIFY COLLECTIVE TROPHIES
# -------------------------------------------------------------
csv_candidates = ["ballon_dor_complete.csv", "ballon_dor_complete-v2.csv"]
df = None
for fname in csv_candidates:
    if os.path.exists(fname):
        df = pd.read_csv(fname)
        break

if df is None:
    df = pd.read_csv(io.StringIO(CSV_DATA))

df.columns = df.columns.str.strip()
df["year"] = df["year"].astype(int)

def classify_trophy(ach):
    if pd.isna(ach):
        return "Domestic / Individual Only"
    ach_low = ach.lower()
    if "world cup winner" in ach_low:
        return "World Cup Winner"
    if "euro " in ach_low or "copa américa" in ach_low:
        return "Continental National (Euro/Copa)"
    if "champions league" in ach_low or "european cup" in ach_low:
        if "european cup finalist" not in ach_low and "champions league finalist" not in ach_low and "top scorer" not in ach_low:
            return "Champions League / European Cup"
    return "Domestic / Individual Only"

df_valid = df[df["awarded"] == True].copy()
df_valid["trophy_tier"] = df_valid["key_achievement"].apply(classify_trophy)

countries = sorted(df_valid["modern_country"].dropna().unique())
positions = sorted(df_valid["general_position"].dropna().unique())
trophies = [
    "Champions League / European Cup",
    "World Cup Winner",
    "Continental National (Euro/Copa)",
    "Domestic / Individual Only"
]
max_goals = int(df_valid["season_goals"].max())

# -------------------------------------------------------------
# CREATE DASH APP (COMPATIBLE WITH gunicorn app:app ON RENDER)
# -------------------------------------------------------------
dash_app = dash.Dash(__name__, suppress_callback_exceptions=True)
app = dash_app.server

# -------------------------------------------------------------
# LAYOUT
# -------------------------------------------------------------
dash_app.layout = html.Div([
    html.H1("Ballon d'Or Historical Dashboard (1956–2024)", style={"textAlign": "center"}),
    html.P(
        "Exploring Individual Performance (Goals & Assists) vs. Collective Trophies",
        style={"textAlign": "center", "color": "#555", "marginTop": "-10px"}
    ),

    dcc.Tabs(id="mainTabs", value="overviewTab", children=[
        dcc.Tab(label="Overview", value="overviewTab"),
        dcc.Tab(label="Graphics (Nested Tabs)", value="graphicsTab"),
        dcc.Tab(label="Data Table", value="tableTab"),
        dcc.Tab(label="Summary Statistics", value="summaryTab"),
    ]),

    html.Hr(),

    # ------------------- ROW 1: CATEGORICAL FILTERS -------------------
    html.Div([
        html.Div([
            html.Label("Select Country:"),
            dcc.Dropdown(
                id="countryFilter",
                options=[{"label": "All", "value": "All"}] + [{"label": c, "value": c} for c in countries],
                value=["All"],
                multi=True,
                style={"width": "95%"}
            )
        ], style={"width": "32%", "display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            html.Label("Select Position:"),
            dcc.Dropdown(
                id="positionFilter",
                options=[{"label": "All", "value": "All"}] + [{"label": p, "value": p} for p in positions],
                value=["All"],
                multi=True,
                style={"width": "95%"}
            )
        ], style={"width": "32%", "display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            html.Label("Select Major Collective Trophy:"),
            dcc.Dropdown(
                id="trophyFilter",
                options=[{"label": "All", "value": "All"}] + [{"label": t, "value": t} for t in trophies],
                value=["All"],
                multi=True,
                style={"width": "95%"}
            )
        ], style={"width": "34%", "display": "inline-block", "verticalAlign": "top"}),
    ], style={"padding": "10px 15px"}),

    # ------------------- ROW 2: NUMERIC SLIDERS -------------------
    html.Div([
        html.Div([
            html.Label("Select Year Range:"),
            dcc.RangeSlider(
                id="yearFilter",
                min=int(df_valid["year"].min()),
                max=int(df_valid["year"].max()),
                value=[int(df_valid["year"].min()), int(df_valid["year"].max())],
                marks={y: str(y) for y in range(int(df_valid["year"].min()), int(df_valid["year"].max()) + 1, 8)},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={"width": "54%", "display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            html.Label("Minimum Season Goals (Individual Output):"),
            dcc.Slider(
                id="minGoalsFilter",
                min=0,
                max=max_goals,
                step=5,
                value=0,
                marks={g: str(g) for g in range(0, max_goals + 1, 10)},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={"width": "42%", "display": "inline-block", "paddingLeft": "3%", "verticalAlign": "top"}),
    ], style={"padding": "10px 15px 20px 15px"}),

    html.Hr(),

    html.Div(id="tabContent"),
    dcc.Store(id="filteredData")
], style={"fontFamily": "Arial, sans-serif", "padding": "10px"})

# -------------------------------------------------------------
# CALLBACK -> FILTER DATA
# -------------------------------------------------------------
@dash_app.callback(
    Output("filteredData", "data"),
    [Input("countryFilter", "value"),
     Input("positionFilter", "value"),
     Input("trophyFilter", "value"),
     Input("yearFilter", "value"),
     Input("minGoalsFilter", "value")]
)
def filter_data(country_sel, pos_sel, trophy_sel, year_range, min_goals):
    low, high = year_range
    dff = df_valid.copy()

    if country_sel and "All" not in country_sel:
        dff = dff[dff["modern_country"].isin(country_sel)]

    if pos_sel and "All" not in pos_sel:
        dff = dff[dff["general_position"].isin(pos_sel)]

    if trophy_sel and "All" not in trophy_sel:
        dff = dff[dff["trophy_tier"].isin(trophy_sel)]

    dff = dff[(dff["year"] >= low) & (dff["year"] <= high)]
    dff = dff[dff["season_goals"] >= (min_goals or 0)]

    return dff.to_dict("records")

# -------------------------------------------------------------
# CALLBACK -> MAIN TABS
# -------------------------------------------------------------
@dash_app.callback(
    Output("tabContent", "children"),
    [Input("mainTabs", "value"),
     Input("filteredData", "data")]
)
def render_tabs(tab, data):
    if not data:
        return html.Div("No Ballon d'Or winners match the selected filters.", style={"padding": "20px", "fontWeight": "bold"})

    dff = pd.DataFrame(data)

    # KPI CARDS (DYNAMICALLY UPDATED WITH FILTERS)
    total_awards = len(dff)
    avg_goals = round(dff["season_goals"].mean(), 1)
    avg_ga = round(dff["goal_contributions"].mean(), 1)
    no_major_intl_pct = round((dff["trophy_tier"] == "Domestic / Individual Only").mean() * 100, 1)

    kpi_bar = html.Div([
        html.Div([
            html.H4(f"{total_awards}", style={"margin": "0", "fontSize": "26px", "color": "#1f77b4"}),
            html.Span("Filtered Awards", style={"fontSize": "12px", "color": "#555"})
        ], style={"width": "22%", "display": "inline-block", "textAlign": "center", "padding": "10px", "border": "1px solid #ddd", "borderRadius": "6px", "marginRight": "2%"}),

        html.Div([
            html.H4(f"{avg_goals}", style={"margin": "0", "fontSize": "26px", "color": "#2ca02c"}),
            html.Span("Avg. Season Goals", style={"fontSize": "12px", "color": "#555"})
        ], style={"width": "22%", "display": "inline-block", "textAlign": "center", "padding": "10px", "border": "1px solid #ddd", "borderRadius": "6px", "marginRight": "2%"}),

        html.Div([
            html.H4(f"{avg_ga}", style={"margin": "0", "fontSize": "26px", "color": "#ff7f0e"}),
            html.Span("Avg. Goal Contributions (G+A)", style={"fontSize": "12px", "color": "#555"})
        ], style={"width": "22%", "display": "inline-block", "textAlign": "center", "padding": "10px", "border": "1px solid #ddd", "borderRadius": "6px", "marginRight": "2%"}),

        html.Div([
            html.H4(f"{no_major_intl_pct}%", style={"margin": "0", "fontSize": "26px", "color": "#d62728"}),
            html.Span("Won Without UCL / World Cup / Euro", style={"fontSize": "12px", "color": "#555"})
        ], style={"width": "24%", "display": "inline-block", "textAlign": "center", "padding": "10px", "border": "1px solid #ddd", "borderRadius": "6px"}),
    ], style={"padding": "0 15px 15px 15px"})

    if tab == "overviewTab":
        dff_sorted = dff.sort_values("year").copy()
        dff_sorted["cumulative_awards"] = dff_sorted.groupby("modern_country").cumcount() + 1

        fig = go.Figure()
        for country in sorted(dff_sorted["modern_country"].unique()):
            df_c = dff_sorted[dff_sorted["modern_country"] == country]
            fig.add_trace(go.Scatter(
                x=df_c["year"],
                y=df_c["cumulative_awards"],
                mode="lines+markers",
                name=country,
                text=df_c["player"] + " | " + df_c["season_goals"].astype(int).astype(str) + "G, " + df_c["season_assists"].astype(int).astype(str) + "A | " + df_c["trophy_tier"],
                hovertemplate="<b>%{fullData.name}</b><br>Year: %{x}<br>Cumulative Awards: %{y}<br>Details: %{text}<extra></extra>"
            ))

        fig.update_layout(
            title="Cumulative Ballon d'Or Wins by Country",
            xaxis_title="Year",
            yaxis_title="Cumulative Awards"
        )

        return html.Div([
            kpi_bar,
            dcc.Graph(figure=fig)
        ])

    if tab == "graphicsTab":
        return html.Div([
            kpi_bar,
            dcc.Tabs(id="nestedTabs", value="indivVsColl", children=[
                dcc.Tab(label="Individual vs. Collective (Key Insight)", value="indivVsColl"),
                dcc.Tab(label="Wins by Trophy Type", value="trophyPie"),
                dcc.Tab(label="Wins by Country", value="barCountry"),
                dcc.Tab(label="Wins by Club", value="barClub"),
                dcc.Tab(label="Goals & Assists Trend", value="goalsLine"),
                dcc.Tab(label="Age vs. Year (Scatter)", value="ageScatter"),
                dcc.Tab(label="Cumulative Trendline", value="trend")
            ]),
            html.Div(id="nestedContent", style={"paddingTop": "20px"})
        ])

    if tab == "tableTab":
        cols_display = [
            "year", "player", "modern_country", "club", "general_position",
            "season_goals", "season_assists", "goal_contributions",
            "trophy_tier", "key_achievement", "runner_up"
        ]
        return html.Div([
            kpi_bar,
            html.H3("Filtered Ballon d'Or Data Table"),
            dash_table.DataTable(
                columns=[{"name": col.replace("_", " ").title(), "id": col} for col in cols_display],
                data=dff[cols_display].to_dict("records"),
                page_size=15,
                sort_action="native",
                filter_action="native",
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "center", "padding": "6px", "fontSize": "13px"}
            )
        ])

    if tab == "summaryTab":
        trophy_summary = (
            dff.groupby("trophy_tier")
            .agg(
                Total_Winners=("year", "count"),
                Share_Pct=("year", lambda x: round(len(x) / len(dff) * 100, 1)),
                Avg_Goals=("season_goals", "mean"),
                Avg_Assists=("season_assists", "mean"),
                Avg_Goal_Contrib=("goal_contributions", "mean")
            )
            .round(1)
            .sort_values(by="Total_Winners", ascending=False)
        )

        country_summary = (
            dff.groupby("modern_country")
            .agg(
                Total_Awards=("year", "count"),
                Unique_Winners=("player", "nunique"),
                Avg_Age=("age_at_win", "mean"),
                Avg_Goals=("season_goals", "mean"),
                Avg_Assists=("season_assists", "mean"),
                First_Win=("year", "min"),
                Last_Win=("year", "max")
            )
            .round(1)
            .sort_values(by="Total_Awards", ascending=False)
        )
        return html.Div([
            kpi_bar,
            html.H3("1. Individual Output by Collective Trophy Tier"),
            html.Pre(trophy_summary.to_string(), style={"fontSize": "14px", "backgroundColor": "#f9f9f9", "padding": "10px"}),
            html.H3("2. Summary Statistics by Country"),
            html.Pre(country_summary.to_string(), style={"fontSize": "14px", "backgroundColor": "#f9f9f9", "padding": "10px"})
        ])

# -------------------------------------------------------------
# CALLBACK -> NESTED GRAPH TABS
# -------------------------------------------------------------
@dash_app.callback(
    Output("nestedContent", "children"),
    [Input("nestedTabs", "value"),
     Input("filteredData", "data")]
)
def nested_graphs(nested_tab, data):
    if not data:
        return html.Div("Waiting for data...")

    dff = pd.DataFrame(data)
    dff_sorted = dff.sort_values("year").copy()
    dff_sorted["cumulative_awards"] = dff_sorted.groupby("modern_country").cumcount() + 1

    if nested_tab == "indivVsColl":
        fig = go.Figure()
        for tier in trophies:
            df_t = dff[dff["trophy_tier"] == tier]
            if not df_t.empty:
                fig.add_trace(go.Scatter(
                    x=df_t["year"],
                    y=df_t["goal_contributions"],
                    mode="markers",
                    marker=dict(size=12, line=dict(width=1, color="DarkSlateGrey")),
                    name=tier,
                    text=df_t["player"] + " (" + df_t["season_goals"].astype(int).astype(str) + "G + " + df_t["season_assists"].astype(int).astype(str) + "A) - " + df_t["key_achievement"],
                    hovertemplate="<b>%{text}</b><br>Year: %{x}<br>Total G+A: %{y}<extra></extra>"
                ))

        fig.update_layout(
            title="Individual Output (Goals + Assists) Colored by Major Collective Trophy Won",
            xaxis_title="Year",
            yaxis_title="Season Goal Contributions (Goals + Assists)",
            legend_title="Major Collective Trophy"
        )
        return dcc.Graph(figure=fig)

    if nested_tab == "trophyPie":
        t_counts = dff["trophy_tier"].value_counts().reset_index()
        t_counts.columns = ["Trophy_Tier", "Count"]
        fig = go.Figure(data=[go.Pie(
            labels=t_counts["Trophy_Tier"],
            values=t_counts["Count"],
            hole=0.4,
            textinfo="label+percent+value"
        )])
        fig.update_layout(title="Share of Ballon d'Or Wins by Major Collective Trophy")
        return dcc.Graph(figure=fig)

    if nested_tab == "barCountry":
        sums = dff.groupby("modern_country").size().reset_index(name="total_awards")
        sums = sums.sort_values("total_awards", ascending=False)
        fig = go.Figure(go.Bar(
            x=sums["modern_country"],
            y=sums["total_awards"],
            text=sums["total_awards"],
            textposition="auto"
        ))
        fig.update_layout(
            title="Total Ballon d'Or Awards by Country",
            xaxis_title="Country",
            yaxis_title="Number of Awards"
        )
        return dcc.Graph(figure=fig)

    if nested_tab == "barClub":
        club_sums = dff.groupby("club").size().reset_index(name="total_awards")
        club_sums = club_sums.sort_values("total_awards", ascending=False)
        fig = go.Figure(go.Bar(
            x=club_sums["club"],
            y=club_sums["total_awards"],
            text=club_sums["total_awards"],
            textposition="auto"
        ))
        fig.update_layout(
            title="Total Ballon d'Or Awards by Club",
            xaxis_title="Club",
            yaxis_title="Number of Awards"
        )
        return dcc.Graph(figure=fig)

    if nested_tab == "goalsLine":
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dff_sorted["year"],
            y=dff_sorted["season_goals"],
            mode="lines+markers",
            name="Season Goals",
            text=dff_sorted["player"],
            hovertemplate="<b>%{text}</b> (%{x})<br>Goals: %{y}<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=dff_sorted["year"],
            y=dff_sorted["season_assists"],
            mode="lines+markers",
            name="Season Assists",
            text=dff_sorted["player"],
            hovertemplate="<b>%{text}</b> (%{x})<br>Assists: %{y}<extra></extra>"
        ))
        fig.update_layout(
            title="Winner Season Goals & Assists Over Time",
            xaxis_title="Year",
            yaxis_title="Count"
        )
        return dcc.Graph(figure=fig)

    if nested_tab == "ageScatter":
        fig = go.Figure()
        for pos in sorted(dff["general_position"].dropna().unique()):
            df_p = dff[dff["general_position"] == pos]
            fig.add_trace(go.Scatter(
                x=df_p["year"],
                y=df_p["age_at_win"],
                mode="markers",
                marker=dict(size=10),
                name=pos,
                text=df_p["player"] + " (" + df_p["modern_country"] + ")",
                hovertemplate="<b>%{text}</b><br>Year: %{x}<br>Age: %{y}<extra></extra>"
            ))
        fig.update_layout(
            title="Winner Age at Victory by Position",
            xaxis_title="Year",
            yaxis_title="Age at Win"
        )
        return dcc.Graph(figure=fig)

    if nested_tab == "trend":
        fig = go.Figure()
        for country in sorted(dff_sorted["modern_country"].unique()):
            df_c = dff_sorted[dff_sorted["modern_country"] == country]
            fig.add_trace(go.Scatter(
                x=df_c["year"],
                y=df_c["cumulative_awards"],
                mode="markers",
                name=country
            ))
            if len(df_c) > 1:
                m, b = np.polyfit(df_c["year"], df_c["cumulative_awards"], 1)
                fig.add_trace(go.Scatter(
                    x=df_c["year"],
                    y=m * df_c["year"] + b,
                    mode="lines",
                    name=f"{country} trend"
                ))
        fig.update_layout(
            title="Cumulative Wins Linear Trend by Country",
            xaxis_title="Year",
            yaxis_title="Cumulative Awards"
        )
        return dcc.Graph(figure=fig)

# -------------------------------------------------------------
# RUN APP
# -------------------------------------------------------------
if __name__ == "__main__":
    dash_app.run(debug=True)