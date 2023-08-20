import streamlit as st
import pandas as pd
import datetime
import pytz
# import matplotlib.pyplot as plt
import altair as alt
from deta import Deta

prayer_labels = ["Subuh", "Zuhur", "Asar", "Maghrib", "Isyak"]

# Get the Singapore timezone object
sg_timezone = pytz.timezone('Asia/Singapore')

st.title('Solat Time Tracker')
df = pd.read_csv('data.csv')

deta = Deta(st.secrets["DETA_KEY"])
db = deta.Base("ToDoApp")

col1, col2, col3, col4, col5 = st.columns(5)

columns = [col1, col2, col3, col4, col5]

for idx, prayer_label in enumerate(prayer_labels):
    with columns[idx]:
        if st.button(prayer_labels[idx]):
            # Get the current time
            current_time = datetime.datetime.now(sg_timezone).strftime('%H:%M')
            current_day = datetime.datetime.now(sg_timezone).strftime('%Y-%m-%d %H:%M')

            new_data = {"Date": current_day, "Prayer": prayer_label, "Time": current_time}
            df2 = pd.DataFrame(new_data, index=[0])
            df = pd.concat([df, df2])
            df.to_csv("data.csv", index=False)
            
            db.put({"Date": current_day, "Prayer": prayer_label, "Time": current_time})

            # Display success message
            st.success(f"{prayer_label} time logged successfully!")    

# Filter data for a specific prayer (you can customize this)
selected_prayer = st.selectbox("Select Prayer", df["Prayer"].unique())
filtered_data = df[df["Prayer"] == selected_prayer]

st.write(filtered_data)

db_content = db.fetch().items
st.write(db_content)

fig = alt.Chart(filtered_data).mark_line().encode(
    x=alt.X('yearmonthdate(Date):O').title('Date'),
    # y=alt.Y('hoursminutes(Date):T', scale=alt.Scale(domain=['2012-01-01T00:00:00', '2012-01-02T00:00:00'])).title('Time'),
    y=alt.Y('Time')
).properties(
    width=800,
    height=400,
    title='Prayer time'
)

st.altair_chart(fig, use_container_width=True)

# # Plot the line chart
# st.write(f"Line Chart for {selected_prayer} Prayer Time")
# st.line_chart(filtered_data.set_index("Date")["Time"])

# st.write(f"Matplotlib figure")
# fig, ax = plt.subplots()
# ax.plot(filtered_data['Date'], filtered_data['Time'])
# ax.set_xlabel('Date')
# ax.set_ylabel('Time')
# ax.set_yticks(range(25))
# ax.set_yticklabels([f'{t:02.0f}:00' for t in range(25)])
# st.pyplot(fig)

st.header("Existing dataset")
st.write(df)