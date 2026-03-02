import streamlit as st
import pandas as pd
import re


REQUIRED_COLUMNS = ["first_name", "last_name", "email_1", "phone_1"]


def format_phone(phone) -> str:
    """Normalize phone to +1XXXXXXXXXX format."""
    if pd.isna(phone) or str(phone).strip() == "":
        return ""
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    return f"+{digits}" if digits else ""


def main():
    st.title("Real Intent to Roomvu Converter")

    st.info("Upload a Real Intent CSV. The app will convert it to Roomvu's import format: **name, email, phone**.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]

        if not missing:
            out = pd.DataFrame()
            out["name"] = (df["first_name"].fillna("") + " " + df["last_name"].fillna("")).str.strip()
            out["email"] = df["email_1"].fillna("")
            out["phone"] = df["phone_1"].apply(format_phone)

            st.write("Converted DataFrame:")
            st.dataframe(out)

            csv = out.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download converted CSV",
                data=csv,
                file_name="roomvu_import.csv",
                mime="text/csv",
            )
        else:
            st.error(f"Missing required columns: {', '.join(missing)}")


if __name__ == "__main__":
    main()