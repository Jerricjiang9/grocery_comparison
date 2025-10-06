#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re
import streamlit as st


# In[2]:


aldi = pd.read_csv("aldi_all_products.csv")
aldi.head()


# In[3]:


#Clean Aldi price column
aldi['price'] = aldi['price'].str.replace("$", "")
aldi['price'] = aldi['price'].astype("float64")


# In[4]:


hyvee = pd.read_csv("hyvee_all_products.csv")
hyvee.head()


# In[5]:


def clean_price(raw_price):
    if not isinstance(raw_price, str):
        return None

    raw_price = raw_price.strip().lower()

    # Step 1: Convert cents to dollars
    cent_match = re.search(r'(\d+)\s*¢', raw_price)
    if cent_match:
        cents = int(cent_match.group(1))
        return round(cents / 100, 2)

    # Step 2: Convert $X.XX patterns
    dollar_match = re.search(r'\$?(\d+(?:\.\d{1,2})?)', raw_price)
    if dollar_match:
        return float(dollar_match.group(1))

    return None  # fallback if no price found


# In[6]:


hyvee['price'] = hyvee['price'].apply(clean_price)


# In[7]:


hyvee.head()


# In[ ]:





# In[ ]:





# In[8]:


def compare_grocery_prices(
    shopping_list,
    df1,
    df2,
    name_col='name',
    price_col='price',
    store_names=('Store 1', 'Store 2')
):
    total_1 = 0.0
    total_2 = 0.0
    missing_items = []
    comparison_table = []

    print(f"{'Item':<15} | {store_names[0]:<40} | {store_names[1]:<40}")
    print("-" * 110)

    for item in shopping_list:
        # Find matching rows sorted by price
        match_1 = df1[df1[name_col].str.contains(item, case=False, na=False)].sort_values(price_col)
        match_2 = df2[df2[name_col].str.contains(item, case=False, na=False)].sort_values(price_col)

        row_1 = match_1.iloc[0] if not match_1.empty else None
        row_2 = match_2.iloc[0] if not match_2.empty else None

        name_1 = row_1[name_col] if row_1 is not None else "N/A"
        price_1 = row_1[price_col] if row_1 is not None else None

        name_2 = row_2[name_col] if row_2 is not None else "N/A"
        price_2 = row_2[price_col] if row_2 is not None else None

        if price_1 is not None:
            total_1 += price_1
        else:
            missing_items.append((item, store_names[0]))

        if price_2 is not None:
            total_2 += price_2
        else:
            missing_items.append((item, store_names[1]))

        print(f"{item:<15} | {f'{name_1} (${price_1:.2f})' if price_1 else 'N/A':<40} | {f'{name_2} (${price_2:.2f})' if price_2 else 'N/A':<40}")

        comparison_table.append({
            'item': item,
            store_names[0] + '_item': name_1,
            store_names[0] + '_price': price_1,
            store_names[1] + '_item': name_2,
            store_names[1] + '_price': price_2,
        })

    print("\nTOTAL")
    print(f"{store_names[0]}: ${total_1:.2f}")
    print(f"{store_names[1]}: ${total_2:.2f}")

    if missing_items:
        print("\n⚠️ Missing Items:")
        for item, store in missing_items:
            print(f"- {item} not found in {store}")

    return {
        'total_1': round(total_1, 2),
        'total_2': round(total_2, 2),
        'store_1_name': store_names[0],
        'store_2_name': store_names[1],
        'item_breakdown': comparison_table,
        'missing': missing_items
    }


# In[9]:


shopping_list = ["milk", "eggs", "bread", "cheese", "banana"]


# In[10]:


compare_grocery_prices(shopping_list, hyvee, aldi, store_names=("Hy-Vee", "Aldi"))


# In[11]:


st.title("🛒 Grocery Price Comparison")

st.markdown("Enter your grocery list (one item per line):")
input_text = st.text_area("Shopping List", height=200)

if st.button("Compare Prices"):
    if input_text.strip():
        shopping_list = [line.strip() for line in input_text.splitlines() if line.strip()]
        result = compare_grocery_prices(shopping_list, hyvee, aldi)

        # Now extract values
        result_df = pd.DataFrame(result['item_breakdown'])
        total_hyvee = result['total_1']
        total_aldi = result['total_2']


        st.markdown("### 🧾 Price Breakdown")
        st.dataframe(result_df, use_container_width=True)

        st.markdown("### 💵 Total Costs")
        col1, col2 = st.columns(2)
        col1.metric("Hy-Vee Total", f"${total_hyvee:.2f}")
        col2.metric("Aldi Total", f"${total_aldi:.2f}")
    else:
        st.warning("Please enter at least one item.")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




