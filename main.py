import pandas as pd
import openai
from collections import defaultdict
from agents.topic_extraction_agent import extract_topics
from agents.topic_dedup_agent import load_memory, save_memory, deduplicate_topic

# ---------- CONFIG ----------
OPENAI_API_KEY = "PUT_YOUR_API_KEY_HERE"
DATA_PATH = "data/reviews.csv"
MEMORY_PATH = "data/topic_memory.json"
OUTPUT_PATH = "output/trend_report.csv"

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# ---------- LOAD DATA ----------
df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])

# ---------- LOAD MEMORY ----------
topic_memory = load_memory(MEMORY_PATH)

# ---------- PROCESS ----------
daily_topic_counts = defaultdict(lambda: defaultdict(int))

for _, row in df.iterrows():
    date = row["date"].strftime("%Y-%m-%d")
    review = row["review"]

    extracted_topics = extract_topics(review, openai_client)

    for topic in extracted_topics:
        canonical = deduplicate_topic(topic, topic_memory, openai_client)
        daily_topic_counts[canonical][date] += 1

# ---------- SAVE MEMORY ----------
save_memory(topic_memory, MEMORY_PATH)

# ---------- BUILD TREND TABLE ----------
all_dates = sorted(df["date"].dt.strftime("%Y-%m-%d").unique())
topics = daily_topic_counts.keys()

trend_df = pd.DataFrame(index=topics, columns=all_dates).fillna(0)

for topic, date_counts in daily_topic_counts.items():
    for date, count in date_counts.items():
        trend_df.loc[topic, date] = count

trend_df.to_csv(OUTPUT_PATH)

print("✅ Trend report generated:", OUTPUT_PATH)
