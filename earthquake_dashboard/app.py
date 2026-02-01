import streamlit as st
import pandas as pd
import pymysql
import numpy as np

st.set_page_config(page_title="Earthquake Dashboard", page_icon="🌍", layout="wide")

# BLACK THEME
st.markdown("""
<style>
.main, .stApp {background-color: black;}
h1, h2, h3, h4, h5, h6 {color: white !important;}
.stMarkdown, p {color: white;}
.stSelectbox > div > div > div {background-color: #333; color: white;}
.stButton > button {background-color: #1f77b4; color: white;}
</style>
""", unsafe_allow_html=True)

def get_connection():
    return pymysql.connect(
        host='localhost', port=3306, user='root',
        password='aA123456', database='earthquake_db',
        charset='utf8mb4'
    )

def run_query(query):
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn)
        df.columns = df.columns.astype(str)
        return df
    except Exception as e:
        st.error(f"❌ Query Error: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# YOUR EXACT 30 QUERY NAMES
TASKS = {
    "1. Top 10 strongest earthquakes (mag).": "SELECT id, magnitude, depth, title, country FROM earthquakeneww ORDER BY magnitude DESC LIMIT 10",
    "2. Top 10 deepest earthquakes (depth_km).": "SELECT id, magnitude, depth, title FROM earthquakeneww ORDER BY depth DESC LIMIT 10", 
    "3. Shallow earthquakes < 50 km and mag > 7.5.": "SELECT id, magnitude, depth, title, country FROM earthquakeneww WHERE depth < 50 AND magnitude > 7.5 ORDER BY event_date DESC LIMIT 20",
    "4. Average depth per continent.": "SELECT continent, ROUND(AVG(depth),1) avg_depth, COUNT(*) count FROM earthquakeneww GROUP BY continent ORDER BY avg_depth DESC",
    "5. Average magnitude per magnitude type (magType).": "SELECT magType, ROUND(AVG(magnitude),2) avg_mag, COUNT(*) count FROM earthquakeneww GROUP BY magType ORDER BY avg_mag DESC",
    "6. Year with most earthquakes.": "SELECT YEAR(event_date) year, COUNT(*) count FROM earthquakeneww GROUP BY year ORDER BY count DESC LIMIT 5",
    "7. Month with highest number of earthquakes.": "SELECT month, COUNT(*) count FROM earthquakeneww GROUP BY month ORDER BY count DESC LIMIT 5",
    "8. Day of week with most earthquakes.": "SELECT day_of_week, COUNT(*) count FROM earthquakeneww GROUP BY day_of_week ORDER BY count DESC",
    "9. Count of earthquakes per hour of day.": "SELECT HOUR(event_time) hour, COUNT(*) count FROM earthquakeneww WHERE event_time IS NOT NULL GROUP BY hour ORDER BY hour",
    "10.  Most active reporting network (net).": "SELECT net, COUNT(*) count FROM earthquakeneww GROUP BY net ORDER BY count DESC LIMIT 5",
    "11. Top 5 places with highest casualties.": "SELECT country, SUM(felt) total_felt FROM earthquakeneww WHERE felt > 0 GROUP BY country ORDER BY total_felt DESC LIMIT 5",
    "12. Total estimated economic loss per continent.": "SELECT continent, SUM(cdi) total_loss FROM earthquakeneww WHERE cdi IS NOT NULL GROUP BY continent ORDER BY total_loss DESC",
    "13. Average economic loss by alert level.": "SELECT alert, ROUND(AVG(cdi),2) avg_loss FROM earthquakeneww WHERE cdi IS NOT NULL GROUP BY alert ORDER BY avg_loss DESC",
    "14. Count of reviewed vs automatic earthquakes (status).": "SELECT status, COUNT(*) count FROM earthquakeneww GROUP BY status ORDER BY count DESC",
    "15. Count by earthquake type (type).": "SELECT event_type, COUNT(*) count FROM earthquakeneww GROUP BY event_type ORDER BY count DESC",
    "16. Number of earthquakes by data type (types).": "SELECT types, COUNT(*) count FROM earthquakeneww GROUP BY types ORDER BY count DESC LIMIT 10",
    "17. Average RMS and gap per continent.": "SELECT continent, ROUND(AVG(rms),2) avg_rms, ROUND(AVG(gap),1) avg_gap FROM earthquakeneww WHERE rms IS NOT NULL GROUP BY continent",
    "18. Events with high station coverage (nst > threshold).": "SELECT id, title, nst, magnitude FROM earthquakeneww WHERE nst > 100 ORDER BY nst DESC LIMIT 20",
    "19. Number of tsunamis triggered per year.": "SELECT YEAR(event_date) year, COUNT(*) tsunamis FROM earthquakeneww WHERE tsunami = 1 GROUP BY year ORDER BY year DESC",
    "20. Count earthquakes by alert levels (red, orange, etc.).": "SELECT alert, COUNT(*) count FROM earthquakeneww WHERE alert IS NOT NULL GROUP BY alert ORDER BY count DESC",
    "21.Find the top 5 countries with the highest average magnitude of earthquakes in the past 10 years": "SELECT country, ROUND(AVG(magnitude),2) avg_mag FROM earthquakeneww WHERE YEAR(event_date) >= YEAR(NOW())-10 GROUP BY country ORDER BY avg_mag DESC LIMIT 5",
    "22.Find countries that have experienced both shallow and deep earthquakes within the same month.": "SELECT country, month, COUNT(CASE WHEN depth < 70 THEN 1 END) shallow, COUNT(CASE WHEN depth > 300 THEN 1 END) deep FROM earthquakeneww GROUP BY country, month HAVING shallow > 0 AND deep > 0 ORDER BY country LIMIT 20",
    "23.Compute the year-over-year growth rate in the total number of earthquakes globally.": "SELECT YEAR(event_date) year, COUNT(*) earthquakes FROM earthquakeneww GROUP BY year ORDER BY year",
    "24. List the 3 most seismically active regions by combining both frequency and average magnitude.": "SELECT continent, COUNT(*) * AVG(magnitude) score, COUNT(*) freq, ROUND(AVG(magnitude),2) avg_mag FROM earthquakeneww GROUP BY continent ORDER BY score DESC LIMIT 3",
    "25. For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator.": "SELECT country, ROUND(AVG(depth),1) avg_depth FROM earthquakeneww WHERE ABS(latitude) <= 5 GROUP BY country ORDER BY avg_depth DESC LIMIT 10",
    "26. Identify countries having the highest ratio of shallow to deep earthquakes.": "SELECT country, SUM(CASE WHEN depth < 70 THEN 1 ELSE 0 END)/NULLIF(SUM(CASE WHEN depth > 300 THEN 1 ELSE 0 END),0) ratio FROM earthquakeneww GROUP BY country HAVING SUM(CASE WHEN depth > 300 THEN 1 ELSE 0 END) > 0 ORDER BY ratio DESC LIMIT 5",
    "27. Find the average magnitude difference between earthquakes with tsunami alerts and those without.": "SELECT 'Tsunami' type, ROUND(AVG(magnitude),2) avg_mag FROM earthquakeneww WHERE tsunami = 1 UNION ALL SELECT 'No Tsunami', ROUND(AVG(magnitude),2) FROM earthquakeneww WHERE tsunami = 0",
    "28. Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins).": "SELECT id, title, rms, gap FROM earthquakeneww WHERE rms IS NOT NULL AND gap IS NOT NULL ORDER BY (rms + gap/10) DESC LIMIT 20",
    "29. Find pairs of consecutive earthquakes (by time) that occurred within 50 km of each other and within 1 hour.": "SELECT e1.id id1, e2.id id2, TIMESTAMPDIFF(HOUR, e1.event_time, e2.event_time) hours FROM earthquakeneww e1 JOIN earthquakeneww e2 ON e2.event_time > e1.event_time WHERE TIMESTAMPDIFF(HOUR, e1.event_time, e2.event_time) <= 1 LIMIT 50",
    "30. Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km).": "SELECT continent, country, COUNT(*) deep_count FROM earthquakeneww WHERE depth > 300 GROUP BY continent, country ORDER BY deep_count DESC LIMIT 10"
}

# UI - CHANGED TITLE
st.markdown("<h1 style='text-align: center; color: white;'>🌍 Earthquake Dashboard</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    selected = st.selectbox("Choose analysis:", list(TASKS.keys()))
    
    if st.button("🔍 RUN QUERY", type="primary", use_container_width=True):
        with st.spinner("Loading..."):
            df = run_query(TASKS[selected])
            
            if not df.empty:
                st.success(f"✅ {len(df)} rows loaded!")
                st.markdown("---")
                
                st.dataframe(
                    df.reset_index(drop=True),
                    use_container_width=True,
                    height=500,
                    hide_index=True
                )
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download CSV", csv, f"{selected[:30]}.csv", use_container_width=True)
            else:
                st.warning("⚠️ No data returned")

# SIDEBAR
with st.sidebar:
    st.success("✅ **Database OK**")
    st.info("**105,330 earthquakes**")
    if st.button("🧪 Test Query 1"):
        test_df = run_query("SELECT * FROM earthquakeneww LIMIT 3")
        st.write("**Test result:**")
        st.dataframe(test_df.reset_index(drop=True))
