import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import base64

LOGO_B64 = "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"

# --- Page Configuration ---
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Look ---
st.markdown("""
<style>
    /* Base App Theme */
    .stApp {
        background: linear-gradient(135deg, #020617 0%, #0F172A 100%);
    }
    
    /* Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@500;700;900&display=swap');
    h1, h2, h3, p, span, div {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Title Styling */
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    
    /* Group Headers */
    .group-header {
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #F8FAFC !important;
        padding-top: 2.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(56, 189, 248, 0.15);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 12px;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
    }
    
    /* Subheaders */
    h3 {
        font-family: 'Outfit', sans-serif;
        color: #CBD5E1 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 1.5rem !important;
    }
    
    /* Card Styling for Charts */
    .stPlotlyChart {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 15px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .stPlotlyChart:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.5), 0 0 15px rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    
    /* Hide Plotly Modebar and Disable Interaction UI */
    .modebar-container, .modebar-group, .modebar {
        display: none !important;
    }
    
    /* Sidebar / Hamburger Hiding */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Header UI */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 25px;
        background: rgba(15, 23, 42, 0.4);
        padding: 25px 35px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        margin: 0 auto 30px auto;
        max-width: 650px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
    .header-logo {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: #ffffff;
        padding: 5px;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.3), inset 0 0 10px rgba(0,0,0,0.1);
        border: 2px solid #38BDF8;
        object-fit: contain;
        flex-shrink: 0;
    }
    .header-text {
        display: flex;
        flex-direction: column;
        text-align: left;
    }
    .header-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.5rem;
        font-weight: 900;
        color: #F8FAFC;
        margin-bottom: 5px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        line-height: 1.1;
        letter-spacing: -0.5px;
    }
    .header-desc {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #94A3B8;
        line-height: 1.4;
    }
    
    /* Segmented Control Navigation */
    .stRadio [role=radiogroup] {
        display: flex;
        flex-direction: row;
        justify-content: center;
        background: rgba(15, 23, 42, 0.6);
        border-radius: 30px;
        padding: 6px;
        width: fit-content;
        margin: 0 auto;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.3);
    }
    .stRadio [role=radiogroup] label > div:first-child {
        display: none !important;
    }
    .stRadio [role=radiogroup] label {
        background: transparent !important;
        border: none !important;
        padding: 12px 35px !important;
        border-radius: 25px !important;
        margin: 0 !important;
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
    }
    .stRadio [role=radiogroup] label:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        transform: none !important;
    }
    .stRadio [role=radiogroup] label:has(input:checked) {
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%) !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4) !important;
        border: none !important;
    }
    .stRadio [role=radiogroup] label p {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
        margin: 0 !important;
    }
    .stRadio [role=radiogroup] label:has(input:checked) p {
        color: #ffffff !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Dataframes */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- Player Name Mapping ---
PLAYER_MAPPING = {
    "AD Russell": "Andre Russell", "SR Watson": "Shane Watson", "YK Pathan": "Yusuf Pathan",
    "S Dhawan": "Shikhar Dhawan", "AT Rayudu": "Ambati Rayudu", "R Ashwin": "Ravichandran Ashwin",
    "DW Steyn": "Dale Steyn", "DS Kulkarni": "Dhawal Kulkarni", "AM Rahane": "Ajinkya Rahane",
    "Mohammed Shami": "Mohammed Shami", "F du Plessis": "Faf du Plessis", "RV Uthappa": "Robin Uthappa",
    "Harbhajan Singh": "Harbhajan Singh", "SL Malinga": "Lasith Malinga", "HV Patel": "Harshal Patel",
    "IK Pathan": "Irfan Pathan", "RA Jadeja": "Ravindra Jadeja", "A Mishra": "Amit Mishra",
    "UT Yadav": "Umesh Yadav", "JJ Bumrah": "Jasprit Bumrah", "Rashid Khan": "Rashid Khan",
    "SA Yadav": "Suryakumar Yadav", "KA Pollard": "Kieron Pollard", "KD Karthik": "Dinesh Karthik",
    "YS Chahal": "Yuzvendra Chahal", "Sandeep Sharma": "Sandeep Sharma", "G Gambhir": "Gautam Gambhir",
    "Shubman Gill": "Shubman Gill", "SK Raina": "Suresh Raina", "MM Sharma": "Mohit Sharma",
    "B Kumar": "Bhuvneshwar Kumar", "P Kumar": "Praveen Kumar", "SV Samson": "Sanju Samson",
    "DJ Bravo": "Dwayne Bravo", "MK Pandey": "Manish Pandey", "AR Patel": "Axar Patel",
    "V Kohli": "Virat Kohli", "MS Dhoni": "Mahendra Singh Dhoni", "JC Buttler": "Jos Buttler",
    "PP Chawla": "Piyush Chawla", "CH Gayle": "Chris Gayle", "RG Sharma": "Rohit Sharma",
    "KL Rahul": "KL Rahul", "TA Boult": "Trent Boult", "DA Warner": "David Warner",
    "SP Narine": "Sunil Narine", "AB de Villiers": "AB de Villiers"
}

def map_player_names(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].replace(PLAYER_MAPPING)
    return df

TEAM_MAPPING = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiants": "Rising Pune Supergiant",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru"
}

VENUE_MAPPING = {
    "Wankhede Stadium, Mumbai": "Wankhede Stadium",
    "M Chinnaswamy Stadium, Bengaluru": "M Chinnaswamy Stadium",
    "MA Chidambaram Stadium, Chepauk, Chennai": "MA Chidambaram Stadium",
    "MA Chidambaram Stadium, Chepauk": "MA Chidambaram Stadium",
    "Eden Gardens, Kolkata": "Eden Gardens",
    "Feroz Shah Kotla": "Arun Jaitley Stadium",
    "Arun Jaitley Stadium, Delhi": "Arun Jaitley Stadium",
    "Rajiv Gandhi International Stadium, Uppal": "Rajiv Gandhi International Stadium",
    "Rajiv Gandhi International Stadium, Uppal, Hyderabad": "Rajiv Gandhi International Stadium",
    "Punjab Cricket Association Stadium, Mohali": "Punjab Cricket Association IS Bindra Stadium",
    "Punjab Cricket Association IS Bindra Stadium, Mohali": "Punjab Cricket Association IS Bindra Stadium",
    "Sardar Patel Stadium, Motera": "Narendra Modi Stadium",
    "Narendra Modi Stadium, Ahmedabad": "Narendra Modi Stadium",
    "Dr DY Patil Sports Academy, Mumbai": "Dr DY Patil Sports Academy",
    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow": "Ekana Cricket Stadium",
    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium": "Ekana Cricket Stadium",
    "Sawai Mansingh Stadium, Jaipur": "Sawai Mansingh Stadium",
    "Maharashtra Cricket Association Stadium, Pune": "Maharashtra Cricket Association Stadium",
    "Zayed Cricket Stadium, Abu Dhabi": "Sheikh Zayed Stadium"
}

def map_team_names(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].replace(TEAM_MAPPING)
    return df

def map_venue_names(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].replace(VENUE_MAPPING)
    return df

# --- Data Loading ---
@st.cache_data
def load_data():
    matches_path = os.path.join(os.path.dirname(__file__), 'archive', 'matches_updated_ipl_upto_2025.csv')
    deliveries_path = os.path.join(os.path.dirname(__file__), 'archive', 'deliveries_updated_ipl_upto_2025.csv')
    
    matches_df = pd.read_csv(matches_path)
    deliveries_df = pd.read_csv(deliveries_path)
    
    matches_df = map_player_names(matches_df, ['player_of_match'])
    deliveries_df = map_player_names(deliveries_df, ['batsman', 'bowler', 'non_striker', 'player_dismissed'])
    
    matches_df = map_team_names(matches_df, ['team1', 'team2', 'toss_winner', 'winner'])
    deliveries_df = map_team_names(deliveries_df, ['batting_team', 'bowling_team'])
    
    matches_df = map_venue_names(matches_df, ['venue'])
    
    return matches_df, deliveries_df

matches, deliveries = load_data()

# --- Global Chart Settings & Aesthetics ---
def apply_premium_layout(fig, height=350, show_x=False):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=height,
        margin=dict(l=0, r=60, t=35, b=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=show_x, title=""),
        yaxis=dict(showgrid=False, zeroline=False, title="", tickfont=dict(color='#E2E8F0', size=13)),
        hovermode='closest',
        dragmode=False,
        font=dict(family="Inter, sans-serif", color="#94A3B8")
    )
    fig.update_traces(width=0.55, cliponaxis=False)
    return fig

CHART_THEME = "plotly_dark"

# --- Top Navigation ---
header_html = f"""
<div class="app-header">
    <img src="data:image/png;base64,{{LOGO_B64}}" class="header-logo">
    <div class="header-text">
        <div class="header-title">IPL Analytics</div>
        <div class="header-desc">Explore Indian Premier League Data (2008 - 2025) with cutting-edge analytics.</div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

st.write("")
page = st.radio("Navigation", ["Data Explorer", "Deep Insights"], horizontal=True, label_visibility="collapsed")
st.divider()

def plot_mini_histogram(df, column, title, color="#38BDF8"):
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, 'count']
    if len(counts) > 10:
        counts = counts.head(10)
    
    fig = px.bar(counts, x=column, y='count', title=title, template=CHART_THEME, color='count', color_continuous_scale='Blues')
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=150, xaxis_title=None, yaxis_title=None, 
                      xaxis_showticklabels=False, yaxis_showticklabels=False, plot_bgcolor='rgba(0,0,0,0)', 
                      paper_bgcolor='rgba(0,0,0,0)', title_font_size=14, title_font_color="#E2E8F0",
                      coloraxis_showscale=False)
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return fig

# --- Page: Data Explorer ---
if page == "Data Explorer":
    st.title("Data Explorer")
    st.markdown("Browse and filter through the complete historical datasets with a high-level overview.")
    st.divider()
    
    dataset_choice = st.selectbox("Select Dataset to Explore", ["Matches Data", "Deliveries Data"])
    st.write("")
    
    if dataset_choice == "Matches Data":
        col1, col2 = st.columns(2)
        col1.metric("Total Matches", f"{matches.shape[0]:,}")
        col2.metric("Total Features", matches.shape[1])
        st.write("")
        cols = st.columns(4)
        with cols[0]: st.plotly_chart(plot_mini_histogram(matches, 'season', 'Matches per Season'), use_container_width=True)
        with cols[1]: st.plotly_chart(plot_mini_histogram(matches, 'toss_decision', 'Toss Decisions'), use_container_width=True)
        with cols[2]: st.plotly_chart(plot_mini_histogram(matches, 'winner', 'Top Winners'), use_container_width=True)
        with cols[3]: st.plotly_chart(plot_mini_histogram(matches, 'venue', 'Top Venues'), use_container_width=True)
        st.write("")
        st.dataframe(matches, height=500, use_container_width=True)
        
    elif dataset_choice == "Deliveries Data":
        col1, col2 = st.columns(2)
        col1.metric("Total Deliveries", f"{deliveries.shape[0]:,}")
        col2.metric("Total Features", deliveries.shape[1])
        st.write("")
        cols = st.columns(4)
        with cols[0]: st.plotly_chart(plot_mini_histogram(deliveries, 'batting_team', 'Batting Teams'), use_container_width=True)
        with cols[1]: st.plotly_chart(plot_mini_histogram(deliveries, 'bowling_team', 'Bowling Teams'), use_container_width=True)
        with cols[2]: st.plotly_chart(plot_mini_histogram(deliveries, 'batsman_runs', 'Runs Scored per Ball'), use_container_width=True)
        with cols[3]:
            st.plotly_chart(plot_mini_histogram(deliveries[deliveries['dismissal_kind'].notna()], 'dismissal_kind', 'Dismissal Types'), use_container_width=True)
        st.write("")
        st.dataframe(deliveries.head(10000), height=500, use_container_width=True)

# --- Page: Deep Insights ---
elif page == "Deep Insights":
    st.markdown('<div class="main-title">Deep IPL Insights</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 1.15rem; margin-bottom: 2rem;'>A structured, analytical deep dive into the numbers that define the Indian Premier League.</p>", unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # COMPUTATIONS
    # ---------------------------------------------------------
    deliveries['total_runs'] = deliveries['batsman_runs'] + deliveries['extras']
    
    # Batsmen
    top_run_scorers = deliveries.groupby('batsman')['batsman_runs'].sum().reset_index().sort_values(by='batsman_runs', ascending=False).head(10)
    sixes = deliveries[deliveries['batsman_runs'] == 6].groupby('batsman').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    fours = deliveries[deliveries['batsman_runs'] == 4].groupby('batsman').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    boundaries = deliveries[deliveries['batsman_runs'].isin([4, 6])].groupby('batsman').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    
    # Bowlers
    bowler_wickets_kinds = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
    wickets_df = deliveries[deliveries['dismissal_kind'].isin(bowler_wickets_kinds)]
    top_wicket_takers = wickets_df.groupby('bowler')['dismissal_kind'].count().reset_index().rename(columns={'dismissal_kind':'wickets'}).sort_values(by='wickets', ascending=False).head(10)
    dismissals_count = wickets_df['dismissal_kind'].value_counts().reset_index()
    dismissals_count.columns = ['Dismissal Kind', 'Count']
    
    deliveries['isWide'] = deliveries['isWide'].fillna(0)
    deliveries['isNoBall'] = deliveries['isNoBall'].fillna(0)
    deliveries['bowler_runs'] = deliveries['batsman_runs'] + deliveries['isWide'] + deliveries['isNoBall']
    deliveries['isLegal'] = (deliveries['isWide'] == 0) & (deliveries['isNoBall'] == 0)
    
    overs = deliveries.groupby(['matchId', 'inning', 'over', 'bowler']).agg(
        bowler_runs=('bowler_runs', 'sum'),
        legal_balls=('isLegal', 'sum')
    ).reset_index()
    
    maidens = overs[(overs['bowler_runs'] == 0) & (overs['legal_balls'] == 6)]
    top_maidens = maidens['bowler'].value_counts().reset_index().head(10)
    top_maidens.columns = ['Bowler', 'Maiden Overs']
    
    # Team
    team_wins = matches['winner'].value_counts().reset_index()
    team_wins.columns = ['Team', 'Wins']
    
    matches_df = matches.copy()
    matches_df['date'] = pd.to_datetime(matches_df['date'], errors='coerce')
    finals = matches_df.loc[matches_df.groupby('season')['date'].idxmax()]
    trophies = finals['winner'].value_counts().reset_index()
    trophies.columns = ['Team', 'Trophies']
    
    team_total_runs = deliveries.groupby('batting_team')['total_runs'].sum().reset_index().sort_values(by='total_runs', ascending=False)
    team_wickets_df = deliveries[~deliveries['dismissal_kind'].isin(['retired hurt', 'retired out']) & deliveries['dismissal_kind'].notna()]
    team_total_wickets = team_wickets_df.groupby('bowling_team')['dismissal_kind'].count().reset_index().rename(columns={'dismissal_kind':'wickets'}).sort_values(by='wickets', ascending=False)
    
    over_runs = deliveries.groupby(['matchId', 'inning', 'over', 'batting_team'])['total_runs'].sum().reset_index()
    over_runs['over'] = over_runs['over'] + 1
    highest_over = over_runs.sort_values(by='total_runs', ascending=False).head(10)
    
    valid_matches = matches.dropna(subset=['winner'])
    toss_impact = (valid_matches['toss_winner'] == valid_matches['winner']).value_counts().reset_index()
    toss_impact.columns = ['Won Match after Winning Toss', 'Count']
    toss_impact['Won Match after Winning Toss'] = toss_impact['Won Match after Winning Toss'].map({True: 'Yes', False: 'No'})
    
    runs_per_season = deliveries.merge(matches[['matchId', 'season']], on='matchId', how='left').groupby(['season', 'matchId'])['total_runs'].sum().reset_index()
    avg_runs_season = runs_per_season.groupby('season')['total_runs'].mean().reset_index()
    
    over_totals = deliveries.groupby(['matchId', 'inning', 'over'])['total_runs'].sum().reset_index()
    runs_by_over = over_totals.groupby('over')['total_runs'].mean().reset_index()
    runs_by_over.columns = ['over', 'Expected Runs per Over']
    runs_by_over['over'] = runs_by_over['over'] + 1
    
    # General Records
    pom_count = matches['player_of_match'].value_counts().reset_index().head(10)
    pom_count.columns = ['Player', 'Awards']
    venues_count = matches['venue'].value_counts().reset_index().head(10)
    venues_count.columns = ['Venue', 'Matches Hosted']

    # ---------------------------------------------------------
    # BATSMEN INSIGHTS
    # ---------------------------------------------------------
    st.markdown('<h2 class="group-header">Batsmen Insights</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Top 10 Run-Scorers")
        fig1 = px.bar(top_run_scorers, x='batsman_runs', y='batsman', orientation='h', text='batsman_runs', template=CHART_THEME, color='batsman_runs', color_continuous_scale='Sunsetdark')
        fig1.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig1.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig1), use_container_width=True)
    with col2:
        st.markdown("### Most Boundaries (4s & 6s)")
        fig15 = px.bar(boundaries, x='count', y='batsman', orientation='h', text='count', template=CHART_THEME, color='count', color_continuous_scale='Purp')
        fig15.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig15.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig15), use_container_width=True)
        
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Most 6s by a Player")
        fig13 = px.bar(sixes, x='count', y='batsman', orientation='h', text='count', template=CHART_THEME, color='count', color_continuous_scale='Magma')
        fig13.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig13.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig13), use_container_width=True)
    with col4:
        st.markdown("### Most 4s by a Player")
        fig14 = px.bar(fours, x='count', y='batsman', orientation='h', text='count', template=CHART_THEME, color='count', color_continuous_scale='Teal')
        fig14.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig14.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig14), use_container_width=True)

    # ---------------------------------------------------------
    # BOWLERS INSIGHTS
    # ---------------------------------------------------------
    st.markdown('<h2 class="group-header">Bowlers Insights</h2>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("### Top 10 Wicket-Takers")
        fig2 = px.bar(top_wicket_takers, x='wickets', y='bowler', orientation='h', text='wickets', template=CHART_THEME, color='wickets', color_continuous_scale='Blues')
        fig2.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig2.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig2), use_container_width=True)
    with col6:
        st.markdown("### Most Maiden Overs Bowled")
        fig17 = px.bar(top_maidens, x='Maiden Overs', y='Bowler', orientation='h', text='Maiden Overs', template=CHART_THEME, color='Maiden Overs', color_continuous_scale='Mint')
        fig17.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig17.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig17), use_container_width=True)

    st.markdown("### Common Dismissal Types")
    fig6 = px.pie(dismissals_count, values='Count', names='Dismissal Kind', hole=0.55, template=CHART_THEME, color_discrete_sequence=px.colors.sequential.Tealgrn)
    fig6.update_traces(textposition='outside', textinfo='percent+label', marker=dict(line=dict(color='#0F172A', width=3)), pull=[0.02]*len(dismissals_count))
    fig6.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False, margin=dict(t=20, b=20), height=400, font=dict(family="Inter, sans-serif", color="#F8FAFC", size=13))
    st.plotly_chart(fig6, use_container_width=True)

    # ---------------------------------------------------------
    # TEAM INSIGHTS
    # ---------------------------------------------------------
    st.markdown('<h2 class="group-header">Team Insights</h2>', unsafe_allow_html=True)
    col7, col8 = st.columns(2)
    with col7:
        st.markdown("### Most IPL Trophies Won")
        fig11 = px.bar(trophies, x='Trophies', y='Team', orientation='h', text='Trophies', template=CHART_THEME, color='Trophies', color_continuous_scale='Oryel')
        fig11.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig11.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig11), use_container_width=True)
    with col8:
        st.markdown("### Most Matches Won")
        fig3 = px.bar(team_wins.sort_values(by='Wins', ascending=True), x='Wins', y='Team', orientation='h', text='Wins', template=CHART_THEME, color='Wins', color_continuous_scale='Plasma')
        fig3.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig3.update_layout(coloraxis_showscale=False)
        st.plotly_chart(apply_premium_layout(fig3, height=450), use_container_width=True)
        
    col9, col10 = st.columns(2)
    with col9:
        st.markdown("### Total Runs Scored by Franchise")
        fig12 = px.bar(team_total_runs, x='total_runs', y='batting_team', orientation='h', text='total_runs', template=CHART_THEME, color='total_runs', color_continuous_scale='Sunsetdark')
        fig12.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig12.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig12, height=450), use_container_width=True)
    with col10:
        st.markdown("### Total Wickets Taken by Franchise")
        fig_tw = px.bar(team_total_wickets, x='wickets', y='bowling_team', orientation='h', text='wickets', template=CHART_THEME, color='wickets', color_continuous_scale='Teal')
        fig_tw.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig_tw.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig_tw, height=450), use_container_width=True)
        
    col11, col12 = st.columns(2)
    with col11:
        st.markdown("### Average Runs Per Match Across Seasons")
        fig5 = px.line(avg_runs_season, x='season', y='total_runs', markers=True, template=CHART_THEME)
        fig5.update_traces(line_color='#38BDF8', line_width=4, marker=dict(size=12, color='#818CF8', line=dict(width=3, color='#020617')))
        fig5.update_layout(xaxis_title="Season", yaxis_title="Average Runs per Match", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Inter, sans-serif", color="#94A3B8"), margin=dict(l=0, r=20, t=20, b=0))
        st.plotly_chart(fig5, use_container_width=True)
    with col12:
        st.markdown("### Toss Impact on Match Outcome")
        fig4 = px.pie(toss_impact, values='Count', names='Won Match after Winning Toss', hole=0.55, template=CHART_THEME, color_discrete_sequence=['#10B981', '#F43F5E'])
        fig4.update_traces(textposition='outside', textinfo='percent+label', marker=dict(line=dict(color='#0F172A', width=3)), pull=[0.02, 0.02])
        fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False, margin=dict(t=20, b=20), height=400, font=dict(family="Inter, sans-serif", color="#F8FAFC", size=13))
        st.plotly_chart(fig4, use_container_width=True)
        
    col13, col14 = st.columns(2)
    with col13:
        st.markdown("### Average Scoring Rate by Over (1 to 20)")
        fig8 = px.bar(runs_by_over, x='over', y='Expected Runs per Over', template=CHART_THEME, color='Expected Runs per Over', color_continuous_scale='Purp')
        fig8.update_traces(textposition='outside', texttemplate='%{y:.1f}', textfont=dict(color='#F8FAFC', size=11), marker_line_width=0)
        fig8.update_layout(coloraxis_showscale=False, xaxis_title="Over Number", yaxis_title="Avg Runs per Over", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=20, t=30, b=0), font=dict(family="Inter, sans-serif", color="#94A3B8"))
        fig8.update_xaxes(tickmode='linear', tick0=1, dtick=1, showgrid=False)
        fig8.update_yaxes(showgrid=False)
        st.plotly_chart(fig8, use_container_width=True)
    with col14:
        st.markdown("### Highest Run Score in a Single Over")
        fig16 = go.Figure(data=[go.Table(
            header=dict(values=['<b>Team</b>', '<b>Over No.</b>', '<b>Runs Scored</b>'], fill_color='rgba(30, 41, 59, 0.8)', align='left', font=dict(color='white', size=14, family='Outfit')),
            cells=dict(values=[highest_over.batting_team, highest_over.over, highest_over.total_runs], fill_color='rgba(15, 23, 42, 0.5)', align='left', font=dict(color='#E2E8F0', size=13, family='Inter'), height=35))
        ])
        fig16.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=380, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig16, use_container_width=True)

    # ---------------------------------------------------------
    # GENERAL RECORDS
    # ---------------------------------------------------------
    st.markdown('<h2 class="group-header">General Records</h2>', unsafe_allow_html=True)
    col15, col16 = st.columns(2)
    with col15:
        st.markdown("### Most 'Player of the Match' Awards")
        fig7 = px.bar(pom_count, x='Awards', y='Player', orientation='h', text='Awards', template=CHART_THEME, color='Awards', color_continuous_scale='Sunsetdark')
        fig7.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig7.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig7), use_container_width=True)
    with col16:
        st.markdown("### Venues Hosting Most Matches")
        fig10 = px.bar(venues_count, x='Matches Hosted', y='Venue', orientation='h', text='Matches Hosted', template=CHART_THEME, color='Matches Hosted', color_continuous_scale='Blues')
        fig10.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=13), marker_line_width=0)
        fig10.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_premium_layout(fig10), use_container_width=True)
