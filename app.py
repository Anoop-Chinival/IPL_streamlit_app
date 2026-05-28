import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Look ---
st.markdown("""
<style>
    .stApp {
        background-color: #0F172A;
    }
    h1, h2, h3, p, span, div {
        font-family: 'Inter', sans-serif;
    }
    h1 {
        color: #F8FAFC;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    h2, h3 {
        color: #E2E8F0;
        font-weight: 600;
    }
    .st-bb {
        background-color: transparent;
    }
    [data-testid="stMetricValue"] {
        color: #F59E0B;
        font-size: 2rem;
        font-weight: bold;
    }
    div[role="radiogroup"] label p {
        font-size: 1.25rem !important;
        padding-top: 5px;
        padding-bottom: 5px;
    }
    .row_heading.level0 {display:none}
    .blank {display:none}
    .group-header {
        color: #38BDF8 !important;
        padding-top: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #1E293B;
        margin-bottom: 1.5rem;
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

# --- Global Chart Settings ---
CHART_THEME = "plotly_dark"
PRIMARY_COLOR = "#F59E0B"
SECONDARY_COLOR = "#38BDF8"
DISCRETE_COLORS = ["#F59E0B", "#38BDF8", "#10B981", "#8B5CF6", "#EC4899", "#F43F5E", "#EAB308", "#14B8A6"]

# --- Sidebar Navigation ---
with st.sidebar:
    st.image("IPL_Logo.png", use_container_width=True)
    st.title("IPL Analytics")
    st.markdown("Explore Indian Premier League Data (2008 - 2025).")
    st.divider()
    page = st.radio("Navigation", ["📊 Data Explorer", "💡 Deep Insights"])

# --- Helper Functions ---
def plot_mini_histogram(df, column, title, color=SECONDARY_COLOR):
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, 'count']
    if len(counts) > 10:
        counts = counts.head(10)
    
    fig = px.bar(counts, x=column, y='count', title=title, template=CHART_THEME, color_discrete_sequence=[color])
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=150, xaxis_title=None, yaxis_title=None, 
                      xaxis_showticklabels=False, yaxis_showticklabels=False, plot_bgcolor='rgba(0,0,0,0)', 
                      paper_bgcolor='rgba(0,0,0,0)', title_font_size=13, title_font_color="#94A3B8")
    return fig

# --- Page: Data Explorer ---
if page == "📊 Data Explorer":
    st.title("📊 Data Explorer")
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
elif page == "💡 Deep Insights":
    st.title("💡 Deep IPL Insights (2008-2025)")
    st.markdown("A structured, analytical deep dive into the numbers that define the Indian Premier League.")
    
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
    
    team_total_runs = deliveries.groupby('batting_team')['total_runs'].sum().reset_index().sort_values(by='total_runs', ascending=False).head(10)
    team_wickets_df = deliveries[~deliveries['dismissal_kind'].isin(['retired hurt', 'retired out']) & deliveries['dismissal_kind'].notna()]
    team_total_wickets = team_wickets_df.groupby('bowling_team')['dismissal_kind'].count().reset_index().rename(columns={'dismissal_kind':'wickets'}).sort_values(by='wickets', ascending=False).head(10)
    
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
    # 🏏 BATSMEN INSIGHTS
    # ---------------------------------------------------------
    st.markdown('<h2 class="group-header">🏏 Batsmen Insights</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Top 10 Run-Scorers")
        fig1 = px.bar(top_run_scorers, x='batsman_runs', y='batsman', orientation='h', text='batsman_runs', template=CHART_THEME)
        fig1.update_traces(marker_color=PRIMARY_COLOR, textposition='inside')
        fig1.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Total Runs", yaxis_title="")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.markdown("### Most Boundaries (4s & 6s)")
        fig15 = px.bar(boundaries, x='count', y='batsman', orientation='h', text='count', template=CHART_THEME)
        fig15.update_traces(marker_color='#8B5CF6', textposition='inside')
        fig15.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Total Boundaries", yaxis_title="")
        st.plotly_chart(fig15, use_container_width=True)
        
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Most 6s by a Player")
        fig13 = px.bar(sixes, x='count', y='batsman', orientation='h', text='count', template=CHART_THEME)
        fig13.update_traces(marker_color='#F43F5E', textposition='inside')
        fig13.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Total Sixes", yaxis_title="")
        st.plotly_chart(fig13, use_container_width=True)
    with col4:
        st.markdown("### Most 4s by a Player")
        fig14 = px.bar(fours, x='count', y='batsman', orientation='h', text='count', template=CHART_THEME)
        fig14.update_traces(marker_color='#10B981', textposition='inside')
        fig14.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Total Fours", yaxis_title="")
        st.plotly_chart(fig14, use_container_width=True)

    # ---------------------------------------------------------
    # 🎯 BOWLERS INSIGHTS
    # ---------------------------------------------------------
    st.markdown('<h2 class="group-header">🎯 Bowlers Insights</h2>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("### Top 10 Wicket-Takers")
        fig2 = px.bar(top_wicket_takers, x='wickets', y='bowler', orientation='h', text='wickets', template=CHART_THEME)
        fig2.update_traces(marker_color=SECONDARY_COLOR, textposition='inside')
        fig2.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Total Wickets", yaxis_title="")
        st.plotly_chart(fig2, use_container_width=True)
    with col6:
        st.markdown("### Most Maiden Overs Bowled")
        fig17 = px.bar(top_maidens, x='Maiden Overs', y='Bowler', orientation='h', text='Maiden Overs', template=CHART_THEME)
        fig17.update_traces(marker_color='#F59E0B', textposition='inside')
        fig17.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Total Maidens", yaxis_title="")
        st.plotly_chart(fig17, use_container_width=True)

    st.markdown("### Common Dismissal Types")
    fig6 = px.pie(dismissals_count, values='Count', names='Dismissal Kind', hole=0.4, template=CHART_THEME, color_discrete_sequence=DISCRETE_COLORS)
    fig6.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#0F172A', width=2)))
    fig6.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False, margin=dict(t=20, b=20), height=350)
    st.plotly_chart(fig6, use_container_width=True)

    # ---------------------------------------------------------
    # 🏟️ TEAM INSIGHTS
    # ---------------------------------------------------------
    st.markdown('<h2 class="group-header">🏟️ Team Insights</h2>', unsafe_allow_html=True)
    col7, col8 = st.columns(2)
    with col7:
        st.markdown("### Most IPL Trophies Won")
        fig11 = px.bar(trophies, x='Trophies', y='Team', orientation='h', text='Trophies', template=CHART_THEME)
        fig11.update_traces(marker_color=SECONDARY_COLOR, textposition='inside')
        fig11.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Trophies", yaxis_title="")
        st.plotly_chart(fig11, use_container_width=True)
    with col8:
        st.markdown("### Most Matches Won")
        fig3 = px.bar(team_wins.head(10).sort_values(by='Wins', ascending=True), x='Wins', y='Team', orientation='h', text='Wins', template=CHART_THEME)
        fig3.update_traces(marker_color=PRIMARY_COLOR, textposition='inside')
        fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Total Matches Won", yaxis_title="")
        st.plotly_chart(fig3, use_container_width=True)
        
    col9, col10 = st.columns(2)
    with col9:
        st.markdown("### Total Runs Scored by Franchise")
        fig12 = px.bar(team_total_runs, x='total_runs', y='batting_team', orientation='h', text='total_runs', template=CHART_THEME)
        fig12.update_traces(marker_color=PRIMARY_COLOR, textposition='inside')
        fig12.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Total Runs", yaxis_title="")
        st.plotly_chart(fig12, use_container_width=True)
    with col10:
        st.markdown("### Total Wickets Taken by Franchise")
        fig_tw = px.bar(team_total_wickets, x='wickets', y='bowling_team', orientation='h', text='wickets', template=CHART_THEME)
        fig_tw.update_traces(marker_color=SECONDARY_COLOR, textposition='inside')
        fig_tw.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Total Wickets", yaxis_title="")
        st.plotly_chart(fig_tw, use_container_width=True)
        
    col11, col12 = st.columns(2)
    with col11:
        st.markdown("### Average Runs Per Match Across Seasons")
        fig5 = px.line(avg_runs_season, x='season', y='total_runs', markers=True, template=CHART_THEME)
        fig5.update_traces(line_color=PRIMARY_COLOR, line_width=4, marker=dict(size=10, color=SECONDARY_COLOR, line=dict(width=2, color='#0F172A')))
        fig5.update_layout(xaxis_title="Season", yaxis_title="Average Runs per Match", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig5, use_container_width=True)
    with col12:
        st.markdown("### Toss Impact on Match Outcome")
        fig4 = px.pie(toss_impact, values='Count', names='Won Match after Winning Toss', hole=0.5, template=CHART_THEME, color_discrete_sequence=['#10B981', '#F43F5E'])
        fig4.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#0F172A', width=2)))
        fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False, margin=dict(t=20, b=20))
        st.plotly_chart(fig4, use_container_width=True)
        
    col13, col14 = st.columns(2)
    with col13:
        st.markdown("### Average Scoring Rate by Over (1 to 20)")
        fig8 = px.bar(runs_by_over, x='over', y='Expected Runs per Over', template=CHART_THEME)
        fig8.update_traces(marker_color=SECONDARY_COLOR, textposition='outside', texttemplate='%{y:.1f}')
        fig8.update_layout(xaxis_title="Over Number", yaxis_title="Avg Runs per Over", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        fig8.update_xaxes(tickmode='linear', tick0=1, dtick=1)
        st.plotly_chart(fig8, use_container_width=True)
    with col14:
        st.markdown("### Highest Run Score in a Single Over")
        fig16 = go.Figure(data=[go.Table(
            header=dict(values=['<b>Team</b>', '<b>Over No.</b>', '<b>Runs Scored</b>'], fill_color='#1E293B', align='left', font=dict(color='white', size=14)),
            cells=dict(values=[highest_over.batting_team, highest_over.over, highest_over.total_runs], fill_color='#0F172A', align='left', font=dict(color='#E2E8F0', size=13), height=30))
        ])
        fig16.update_layout(margin=dict(l=0, r=0, t=20, b=0), height=350, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig16, use_container_width=True)

    # ---------------------------------------------------------
    # ⭐ GENERAL RECORDS
    # ---------------------------------------------------------
    st.markdown('<h2 class="group-header">⭐ General Records</h2>', unsafe_allow_html=True)
    col15, col16 = st.columns(2)
    with col15:
        st.markdown("### Most 'Player of the Match' Awards")
        fig7 = px.bar(pom_count, x='Awards', y='Player', orientation='h', text='Awards', template=CHART_THEME)
        fig7.update_traces(marker_color=PRIMARY_COLOR, textposition='inside')
        fig7.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Awards", yaxis_title="")
        st.plotly_chart(fig7, use_container_width=True)
    with col16:
        st.markdown("### Venues Hosting Most Matches")
        fig10 = px.bar(venues_count, x='Matches Hosted', y='Venue', orientation='h', text='Matches Hosted', template=CHART_THEME)
        fig10.update_traces(marker_color=SECONDARY_COLOR, textposition='inside')
        fig10.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Matches", yaxis_title="")
        st.plotly_chart(fig10, use_container_width=True)
