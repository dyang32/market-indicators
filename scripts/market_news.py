"""FinViz market news — run via hermes-venv Python."""
import sys

from finvizfinance.news import News

fnews = News()
all_news = fnews.get_news()

for _, row in all_news['news'].iterrows():
    print(f"{row['Date']}\t{row['Source']}\t{row['Title'].strip()}\t{row['Link'].strip()}")
