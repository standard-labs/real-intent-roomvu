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

    st.info("Upload one or more Real Intent CSVs. The app will combine and convert them to Roomvu's import format: **name, email, phone**.")

    uploaded_files = st.file_uploader("Choose CSV file(s)", type="csv", accept_multiple_files=True)

    if uploaded_files:
        frames: list[pd.DataFrame] = []
        for f in uploaded_files:
            df = pd.read_csv(f)
            missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
            if missing:
                st.error(f"**{f.name}** is missing required columns: {', '.join(missing)}")
                return
            frames.append(df)

        combined = pd.concat(frames, ignore_index=True)
        st.caption(f"{len(uploaded_files)} file(s) uploaded — {len(combined)} total rows")

        out = pd.DataFrame()
        out["name"] = (combined["first_name"].fillna("") + " " + combined["last_name"].fillna("")).str.strip()
        out["email"] = combined["email_1"].fillna("")
        out["phone"] = combined["phone_1"].apply(format_phone)

        st.write("Converted DataFrame:")
        st.dataframe(out)

        csv = out.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download converted CSV",
            data=csv,
            file_name="roomvu_import.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()