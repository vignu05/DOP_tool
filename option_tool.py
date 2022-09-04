import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

## Variables used
# long_calls = number of long call options (buy) 
# short_calls= number of short call options (sell) 
# long_puts = number of long put options (buy) 
# short_puts = number of short put options (sell) 
# underlying_price = input current price of underlying stock 
# net_stock = net number of stocks in portfolio

##arrays for premiums
#lcp = premiums for each long call
#scp = premiums for each short call
#lpp = premiums for each long put
#spp = premiums for each short put

##arrays for strike price
#lcs = strike price for each long call
#scs = strike price for each short call
#lps = strike price for each long put
#sps = strike price for each short put

#array for quantities
#lcq = number of each long call options (buy) 
#scq = number of each short call options (sell) 
#lpq = np.ones(long_puts)
#spq = np.ones(short_puts)


#Intitialize layout configurations
st.set_page_config(
     page_title='Option Payoff Calculator',
     layout="wide",
     initial_sidebar_state="expanded",
)



##########################
# Main body of calculator
##########################
#Heading and authors
st.write("""
    # Option Payoff Calculator
    ### Created by : Savithri Rao, Sahana Seetharaman and Sumana Bag
    
    This Payoff Calculator can be used for calculating the Net Payoff for spreads and combinations of options with the same underlying asset and same maturity. The underlying asset taken for these instruments is an equity stock, and can be included in the portfolio as well.
    """)


''' # ''' #line spacing
st.header('Set up the number of options for the portfolio')
layout = st.columns(2) #split into two columns

with layout[0]: # First column inputs number of long calls and short calls for the portfolio
    long_calls = st.slider("Long Calls",0,5, value = 1) # number of long call options (buy)
    short_calls = st.slider("Short Calls",0,5)# number of short call options (sell)
 
with layout[-1]: 
    long_puts = st.slider("Long Puts",0,5) # number of long put options (buy)
    short_puts = st.slider("Short Puts",0,5) # number of short put options (sell)



with layout[0]:
    ''' ## ''' #line spacing
    st.header('Set up the underlying asset for the portfolio') #input current price of underlying stockr
    underlying_price = st.number_input('Stock Price',key = 'Underlying asset price', step =1e-2, value = 150.00) 
    net_stock = st.number_input('Net Quantity of Stock in the portfolio',key = 'Stock quantity', step =1e-2) 



#array for premiums
lcp = np.ones(long_calls)
scp = np.ones(short_calls)
lpp = np.ones(long_puts)
spp = np.ones(short_puts)
#array for strike price
lcs = np.ones(long_calls)
scs = np.ones(short_calls)
lps = np.ones(long_puts)
sps = np.ones(short_puts)
#array for quantities
lcq = np.ones(long_calls)
scq = np.ones(short_calls)
lpq = np.ones(long_puts)
spq = np.ones(short_puts)

''' # ''' #line spacing
if long_calls+short_calls+long_puts+short_puts > 0:
    st.header('Set up the individual options in the portfolio')
    
col1, col2, col3, col4, col5, col6 = st.columns(6)
if long_calls >0:
    col2.subheader('Long Calls')
else:
    col2.subheader('No Long Calls')
if long_puts >0:
    col5.subheader('Long Puts')
else:
    col5.subheader('No Long Puts')
    
lcol1, lcol2, lcol3, lcol4, lcol5, lcol6 = st.columns(6)


for i in range (long_calls):
    with lcol1:
        lcq[i] = st.number_input('Quantity',key =('lcq'+str(i)), step =1e-2)
    with lcol2:
        lcp[i] = st.number_input('Price of option',key =('lcp'+str(i)), step =1e-2)
    with lcol3:
        lcs[i] = st.number_input('Strike Price',key =('lcs'+str(i)), step =1e-2)
        

for i in range (long_puts):
    with lcol4:
        lpq[i] = st.number_input('Quantity',key =('lpq'+str(i)), step =1e-2)
    with lcol5:
        lpp[i] = st.number_input('Price of option',key =('lpp'+str(i)), step =1e-2)
    with lcol6:
        lps[i] = st.number_input('Strike Price',key =('lps'+str(i)), step =1e-2)    

####
col1, col2, col3, col4, col5, col6 = st.columns(6)
if short_calls >0:
    col2.subheader('Short Calls')
else:
    col2.subheader('No Short Calls')
if short_puts >0:
    col5.subheader('Short Puts')
else:
    col5.subheader('No Short Puts')
    
scol1, scol2, scol3, scol4, scol5, scol6 = st.columns(6)

for i in range (short_calls):
    with scol1:
        scq[i] = st.number_input('Quantity',key =('scq'+str(i)), step =1e-2)
    with scol2:
        scp[i] = st.number_input('Price of option',key =('scp'+str(i)), step =1e-2)
    with scol3:
        scs[i] = st.number_input('Strike Price',key =('scs'+str(i)), step =1e-2)    
        

for i in range (short_puts):
    with scol4:
        spp[i] = st.number_input('Quantity',key =('spq'+str(i)), step =1e-2)
    with scol5:
        spp[i] = st.number_input('Price of option',key =('spp'+str(i)), step =1e-2)
    with scol6:
        sps[i] = st.number_input('Strike Price',key =('sps'+str(i)), step =1e-2)

    

''' # ''' #line spacing
# Calculating the cost of entering into the portfolio
st.header('Cost of Portfolio')
portfolio_cost = (underlying_price * net_stock) + np.sum(np.multiply(lcq,lcp)) + np.sum(np.multiply(lpq,lpp)) - np.sum(np.multiply(scq,scp)) - np.sum(np.multiply(spq,spp))

if portfolio_cost == 0:
    st.metric(label="Total Cost of entering into the portfolio", value = ('$'+str(0)))
if portfolio_cost > 0:
    st.metric(label="Total Cost of entering into the portfolio", value = ('$'+str(abs(portfolio_cost))), delta='Outflow',delta_color= "inverse")
if portfolio_cost < 0:
    st.metric(label="Total Cost of entering into the portfolio", value = ('$'+str(abs(portfolio_cost))), delta='Inflow')

#st.button("Re-run")




def plot_option_payoff(k, q):
   # x-axis
   S_t = np.arange(start = 0, stop = 2*k, step = 0.1)
    
   # defining y variables
   y_1 = np.empty(len(S_t))
   y_2 = np.empty(len(S_t))
   y_3 = np.empty(len(S_t))
   y_4 = np.empty(len(S_t))
   

   # y-axis is sum of payoffs
   # long call
   for i in range (len(S_t)):
       y_1[i] = np.sum(np.maximum(lcq*(S_t[i] - lcs), 0))
   # short call
       y_2[i] = np.sum(np.minimum(scq*(scs - S_t[i]), 0))
   # long put
       y_3[i] = np.sum(np.maximum(lpq*(lps - S_t[i]), 0))
   # short put
       y_4[i] = np.sum(np.minimum(spq*(S_t[i] - sps), 0))
   # buying a buying/selling stocks
   s = (q)*(S_t - k)

   # total
   y = y_1 + y_2 + y_3 + y_4+s-portfolio_cost
    
   # converting to df
   plot_data = pd.DataFrame({'Stock Price': S_t, 'Net Payoff': y})
   return plot_data
   
dataset = plot_option_payoff(underlying_price, net_stock)               
#Line Chart

st.header('Payoff from Portfolio')

chart = (
        alt.Chart(
            data=dataset
        )
        .mark_line()
        .encode(
            x=alt.X("Stock Price", title="Stock Price"),
            y=alt.Y("Net Payoff", title="Net Payoff"),
            tooltip = ['Stock Price', 'Net Payoff']
        )
)

st.altair_chart(chart, use_container_width=True)

