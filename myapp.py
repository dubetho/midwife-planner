import streamlit as st
import pandas as pd
from icalendar import Calendar, Event
from datetime import datetime, timedelta





def load_excel(file):
    xls = pd.ExcelFile(file)
    sheet_name = xls.sheet_names[0]
    df = pd.read_excel(xls, sheet_name)
    return df


def get_shifts(df, name):
    # Adjust based on the structure of your Excel file
    row = df[df.iloc[:, 0].str.contains(name, case=False, na=False)]
    if row.empty:
        return None
    return row


def create_ical(name, shifts):
    cal = Calendar()
    for index, row in shifts.iterrows():
        for col in shifts.columns[1:]:
            shift = row[col]
            if pd.notnull(shift):
                date = datetime.strptime(col, '%d-%b-%Y')  # Adjust date format as per your excel
                start_time = datetime.combine(date, datetime.min.time())
                if shift == "Day":
                    end_time = start_time + timedelta(hours=8)  # Example shift duration
                elif shift == "Night":
                    end_time = start_time + timedelta(hours=12)  # Example shift duration

                event = Event()
                event.add('summary', f'Shift: {shift}')
                event.add('dtstart', start_time)
                event.add('dtend', end_time)
                event.add('dtstamp', datetime.now())
                cal.add_component(event)

    return cal


def save_ical(cal, name):
    filename = f"{name.replace(' ', '_')}_shifts.ics"
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())
    return filename


def main():
    st.title("Midwife Shift to iCal Converter")

    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
    if uploaded_file is not None:
        df = load_excel(uploaded_file)
        st.write(df.head())

        names = df.iloc[:, 0].dropna().unique()
        name = st.selectbox("Select a midwife's name", names)

        if name:
            shifts = get_shifts(df, name)
            if shifts is not None:
                st.write(f"Shifts for {name}:")
                st.write(shifts)

                cal = create_ical(name, shifts)
                filename = save_ical(cal, name)

                st.success(f"iCal file created: {filename}")
                with open(filename, 'rb') as f:
                    st.download_button('Download iCal', f, file_name=filename)
            else:
                st.error("Name not found in the Excel file.")


if __name__ == "__main__":
    main()
