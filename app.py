# example/st_app_gsheets_using_service_account.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
# Fetch existing vendors data
saledf= conn.read(worksheet="sale", usecols=[0,1,2,3])
saledf = saledf.dropna(how="all")
productdf= conn.read(worksheet="product", usecols=[0,1,2])
productdf = productdf.dropna(how="all")
empdf= conn.read(worksheet="employee", usecols=[0,1,2])
empdf = empdf.dropna(how="all")


# for row in df.itertuples():
#     st.write(f"{row.name} has a :{row.pet}:")
# st.header("Sales")
# st.dataframe(saledf.head(2))
# st.header("Product")
# st.dataframe(productdf.head(2))
# st.header("Employee")
# st.dataframe(empdf.head(2))

#unique_pdt = list(productdf.ProductName.unique())  #unique_emp= list(empdf.EmpName.unique())
unique_pdtid = list(productdf.ProductId.unique())
unique_empid = list(empdf.EmpId.unique())

#st.write(unique_emp)

# Using object notation
emp_box = st.sidebar.selectbox("Employee",unique_empid)
pdt_box = st.sidebar.selectbox("Products",unique_pdtid)

#st.write(unique_empid)
st.header("Daily Sales")
with st.form(key="Myform"):
    date = st.date_input(label="Date")
    empd= st.selectbox("EmpId", unique_empid, index=None)
    prdtd= st.selectbox("ProductId", unique_pdtid, index=None)
    unitsold= st.text_input(label="UnitSold")

    submit_button=st.form_submit_button(label="Submit Details")

    if submit_button:
        if not unitsold :
                st.warning("Ensure all mandatory fields are filled.")
                st.stop()
        #st.write("Daily Sales Submitted Successfully")
        else:
                sale_data = pd.DataFrame(
                    [
                        {
                            "Date": date.strftime("%Y-%m-%d"),
                            "EmpId": empd,
                            "ProductId": prdtd,
                            "UnitSold": unitsold
                           
                        }
                    ]
                )
                updated_df = pd.concat([saledf, sale_data], ignore_index=True)
                conn.update(worksheet="sale", data=updated_df)
                st.success("Daily Sales successfully submitted!")