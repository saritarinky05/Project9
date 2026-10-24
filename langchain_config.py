import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from newsapi import NewsApiClient

load_dotenv(dotenv_path="Keys.env")

openai_api_key = os.getenv("OPENAI_API_KEY")
newsapi_key = os.getenv("NEWSAPI_KEY")

prompt = ChatPromptTemplate.from_template("Summarize these articles about {query}: {summaries}")
llm = ChatOpenAI(model="gpt-4o")
#llm = ChatOpenAI(api_key=openai_api_key, temperature=0.7)

newsapi = NewsApiClient(api_key=newsapi_key)

template = """
You are an AI assistant helping an equity research analyst. Given the following query
and the provided news article summaries, provide a concise and insightful overall summary.

Query: {query}

Summaries: {summaries}

Overall Summary:
"""

prompt = PromptTemplate(template=template, input_variables=["query", "summaries"])

chain = prompt | llm


def get_news_articles(query):
    response = newsapi.get_everything(
        q=query,
        language="en",
        sort_by="relevancy",
        page_size=10
    )
    return response.get("articles", [])


def summarize_articles(articles):
    descriptions = [
        article["description"]
        for article in articles
        if article.get("description")
    ]
    return " ".join(descriptions) if descriptions else "No article descriptions available."


def get_summary(query):
    articles = get_news_articles(query)
    if not articles:
        return None, "No articles found for this query."
    summaries = summarize_articles(articles)
    return articles, summaries
