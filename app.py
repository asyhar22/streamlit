# --- MODULES ---
import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import date, timedelta  # Core Python Module
import plotly.graph_objects as go  # pip install plotly
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
# --------------------------------------

# --- SETTINGS ---
page_title = "Twitter Scrapper"
page_icon = "🤸‍♂️"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)
# --------------------------------------

# --- FORM ---
with st.form('Input Form'):

# --- INPUT ---
    keyword = st.text_input('Keyword','') #create text input
    start_date = st.date_input('Start date', (date.today()- timedelta(days=30))) #create calendar input
    end_date = st.date_input('End date', (date.today())) #create calendar input
    max_tweet = st.number_input('Max Tweet (0-100)', min_value=0, max_value=100) #create number input

# --- ENGINE ---
    scraper = sntwitter.TwitterSearchScraper(f'{keyword} since:{start_date} until:{end_date}').get_items()

# --- SUBMIT ---
    submitted = st.form_submit_button(label='Submit')
    if submitted:
        # st.write(f'{keyword} since:{start_date} until:{end_date}')
        tweet_list = []
        for i, tweet in enumerate(scraper):
            if i==max_tweet:
                break
            tweet_list.append([tweet.date, tweet.id, tweet.user.username, tweet.content])
        # st.write(tweet_list)
# --- OUTPUT ---
        df = pd.DataFrame(tweet_list, columns=['DateTime', 'TweetId', 'Username', 'Text'])
        st.dataframe(df.head())

# --- EXPORT OUTPUT ---
        export_xlsx = st.form_submit_button(label='Export to Excel')
        if export_xlsx:
            df.to_excel('export.xlsx', index=False)
# --------------------------------------

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Data", "Analysis & Visualization"],
    icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# --- INPUT & SAVE PERIODS ---
# if selected == "Data":
#     st.header(f"Data in {currency}")
#     with st.form("entry_form", clear_on_submit=True):
#         col1, col2 = st.columns(2)
#         col1.selectbox("Select Month:", months, key="month")
#         col2.selectbox("Select Year:", years, key="year")

#         "---"
#         with st.expander("Income"):
#             for income in incomes:
#                 st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income)
#         with st.expander("Expenses"):
#             for expense in expenses:
#                 st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)
#         with st.expander("Comment"):
#             comment = st.text_area("", placeholder="Enter a comment here ...")

#         "---"
#         submitted = st.form_submit_button("Save Data")
#         if submitted:
#             period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
#             incomes = {income: st.session_state[income] for income in incomes}
#             expenses = {expense: st.session_state[expense] for expense in expenses}
#             # db.insert_period(period, incomes, expenses, comment)
#             st.success("Data saved!")


# # --- PLOT PERIODS ---
# if selected == "Analysis & Visualization":
#     st.header("Analysis & Visualization")
#     with st.form("saved_periods"):
#         period = st.selectbox("Select Period:", get_all_periods())
#         submitted = st.form_submit_button("Plot Period")
#         if submitted:
#             # Get data from database
#             # period_data = db.get_period(period)
#             # comment = period_data.get("comment")
#             # expenses = period_data.get("expenses")
#             # incomes = period_data.get("incomes")

#             # Create metrics
#             total_income = sum(incomes.values())
#             total_expense = sum(expenses.values())
#             remaining_budget = total_income - total_expense
#             col1, col2, col3 = st.columns(3)
#             col1.metric("Total Income", f"{total_income} {currency}")
#             col2.metric("Total Expense", f"{total_expense} {currency}")
#             col3.metric("Remaining Budget", f"{remaining_budget} {currency}")
#             st.text(f"Comment: {comment}")

#             # Create sankey chart
#             label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
#             source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
#             target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
#             value = list(incomes.values()) + list(expenses.values())

#             # Data to dict, dict to sankey
#             link = dict(source=source, target=target, value=value)
#             node = dict(label=label, pad=20, thickness=30, color="#E694FF")
#             data = go.Sankey(link=link, node=node)

#             # Plot it!
#             fig = go.Figure(data)
#             fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
#             st.plotly_chart(fig, use_container_width=True)