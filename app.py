import streamlit as st
import pandas as pd
import datetime

prayer_labels = ["Subuh", "Zuhur", "Asar", "Maghrib", "Isyak"]

st.title('Solat Time Tracker')
df = pd.read_csv('data.csv')

col1, col2, col3, col4, col5 = st.columns(5)

columns = [col1, col2, col3, col4, col5]

for idx, prayer_label in enumerate(prayer_labels):
    with columns[idx]:
        if st.button(prayer_labels[idx]):
            # Get the current time
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            current_day = datetime.datetime.now().strftime('%d-%m-%Y')

            new_data = {"Date": current_day, "Prayer": prayer_label, "Time": current_time}
            # df = df.append(new_data, ignore_index=True)
            df2 = pd.DataFrame(new_data, index=[0])
            df = pd.concat([df, df2])
            df.to_csv("data.csv", index=False)

            # Display success message
            st.success(f"{prayer_label} time logged successfully!")

# Filter data for a specific prayer (you can customize this)
selected_prayer = st.selectbox("Select Prayer", df["Prayer"].unique())
filtered_data = df[df["Prayer"] == selected_prayer]

# Convert time strings to datetime objects
# filtered_data["Time"] = pd.to_datetime(filtered_data["Time"], format='%H:%M:%S')

# Create a range of time for the y-axis
# y_range = pd.date_range("00:00:00", "23:59:59", freq="15T").time

# Plot the line chart
st.write(f"Line Chart for {selected_prayer} Prayer Time")
st.line_chart(filtered_data.set_index("Date")["Time"])


st.header("Existing dataset")
st.write(df)