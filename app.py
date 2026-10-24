import streamlit as st
from langchain_config import chain, get_summary

st.set_page_config(
    page_title="Equity Research News Tool",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Equity Research News Tool")
st.write("Enter a query to fetch and summarize the latest relevant news articles.")

query = st.text_input("Query", placeholder="e.g. Apple earnings Q3 2024")

if st.button("Get News Summary", type="primary"):
    if query.strip():
        with st.spinner("Fetching articles and generating summary..."):
            # Step 1: fetch articles and concatenate descriptions
            articles, summaries = get_summary(query)

            if articles is None:
                # get_summary returns None when NewsAPI finds no results
                st.warning(summaries)
            else:
                # Step 2: pass query + raw summaries through the LLM chain
                response = chain.invoke({"query": query, "summaries": summaries})

                st.subheader("Summary")
                st.write(response)

                # Step 3: show individual source articles in expandable cards
                st.subheader(f"Source Articles ({len(articles)})")
                for i, article in enumerate(articles, 1):
                    with st.expander(f"{i}. {article.get('title', 'No title')}"):
                        st.write(f"**Source:** {article.get('source', {}).get('name', 'Unknown')}")
                        st.write(f"**Published:** {article.get('publishedAt', 'N/A')[:10]}")
                        st.write(article.get("description", "No description available."))
                        if article.get("url"):
                            st.markdown(f"[Read full article]({article['url']})")
    else:
        st.warning("Please enter a query.")
