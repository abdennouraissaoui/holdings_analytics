import streamlit as st
import pandas as pd

st.write("""
# FLUIDEFI
### *Wallet performance analysis*
""")

df_formatting = {
	"Avg buy price": "${:,.2f}",
	"Price": "${:,.2f}",
	"Market Value": "${:,.2f}",
	"Book Value": "${:,.2f}",
	"Realized P&L": "${:,.2f}",
	"Unrealized P&L": "${:,.2f}",
	"P&L (%)": "{:.2%}"
}

def to_dollar_format(value):
	return "${:,.2f}".format(value)

wallet_address = st.text_input("Enter address:", "0x2139bf99eA01a129aE11c9Cf046e2e189bA6eE0a")

if wallet_address != '':
	ts_positions = pd.read_csv(f"{wallet_address}/ts_positions.csv", index_col=0, parse_dates=True).resample("D").last()
	ts_positions['Overall'] = ts_positions.sum(axis=1)
	gas = pd.read_csv(f"{wallet_address}/gas.csv")
	positions_summary = pd.read_csv(f"{wallet_address}/positions_summary.csv", index_col=0)
	
	positions_summary = positions_summary[[
		"open_quantity",
		"current_price",
		"average_price",
		"market_value",
		"book_value",
		"closed_quantity",
		"realized_profits",
		"unrealized_profits", 
		"pct_profits"]]
	open_positions = positions_summary[positions_summary['open_quantity']>0]
	closed_positions = positions_summary[positions_summary['open_quantity']==0]
	
	# closed_positions.drop(['open_quantity', 'market_value', ''])
	realized_profits = positions_summary['realized_profits'].sum()
	unrealized_profits = positions_summary['unrealized_profits'].sum()
	total_gas_spent = gas['gas_burned_fiat'].sum()

	st.write("""
		---
	## P&L Summary
	""")

	st.write(f"""
	**Gas cost**:       {to_dollar_format(total_gas_spent)}\n
	**Realized P&L**:   {to_dollar_format(realized_profits)}\n
	**Unrealized P&L**: {to_dollar_format(unrealized_profits)}\n
	**Total P&L**: 	  {to_dollar_format(realized_profits+unrealized_profits)}\n
	""")
	st.write("""
		---
	## Historical Market Value
	""")
	selected_columns = st.multiselect(label = "Select position", 
									options = list(ts_positions.columns), 
									default=['Overall'])
	st.line_chart(ts_positions[selected_columns])
	st.write("""## Positions:""")
	st.write("""#### Open positions:""")
	
	cols = [
			'Qty',
			'Price',
			'Avg buy price',
			'Market Value',
			"Book Value",
			"Closed Qty",
			'Realized P&L',
			'Unrealized P&L',
			'P&L (%)']
	open_positions.columns = cols
	closed_positions.columns = cols
	st.write(open_positions.style.format(df_formatting))

	st.write("""#### Closed positions:""")
	st.write(closed_positions)


	# st.write("""
	# ## Total value
	# """)
	# st.line_chart(ts_positions.sum(axis=1))
