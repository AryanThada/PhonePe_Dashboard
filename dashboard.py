import streamlit as st 
from streamlit_option_menu import option_menu
import db
import plotly.express as px
import requests
import json
import pandas as pd



def Transaction_amount_count_Y(df , yr,type):
    tacy  = df[df["year"] ==yr]
    tacy.reset_index(drop = True , inplace =True )

    tacyg = tacy.groupby("state")[["count" , "amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1 , col2 = st.columns(2)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    states_name = []
    data1 =json.loads(response.content)
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()
    
    # print(tacyg.head())
    with col1:
        fig_amount = px.bar(tacyg , x = "state" ,y = "amount" , title = f"{yr}{type} Amount",
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,height = 650,width  = 600)
        # fig_amount.show()
        st.plotly_chart(fig_amount)

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="state" , featureidkey= "properties.ST_NM" , 
                                color = "amount" , color_continuous_scale= "tempo" ,
                                range_color= (tacyg["amount"].min() , tacyg["amount"].max()),
                                 hover_name= "state" , title = f"{yr} {type} amount" ,fitbounds = "locations" ,height = 650 , width = 600)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)
    
    with col2:
        fig_count = px.bar(tacyg , x = "state" ,y = "count" , title = f"{yr}{type} Count",
                            color_discrete_sequence= px.colors.sequential.Bluered_r , height = 650,width  = 600)
        # fig_count.show()
        st.plotly_chart(fig_count)

        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="state" , featureidkey= "properties.ST_NM" , 
                                    color = "count" , color_continuous_scale= "tempo" ,
                                    range_color= (tacyg["count"].min() , tacyg["count"].max()),
                                    hover_name= "state" , title = f"{yr} {type} count" ,fitbounds = "locations" ,height = 650 , width = 600)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
    # print("print fig 2")
    return tacy



def Transaction_amount_count_Y_Q(df , yr , quarter , type):
    tacy  = df[df["quarter"] ==quarter]
    tacy.reset_index(drop = True , inplace =True )

    tacyg = tacy.groupby("state")[["count" , "amount"]].sum()
    tacyg.reset_index(inplace = True)

    # print(tacyg.head())

    col1 , col2 = st.columns(2)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    states_name = []
    data1 =json.loads(response.content)
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()

    with col1:

        fig_amount = px.bar(tacyg , x = "state" ,y = "amount" , title = f"{yr}-{quarter} Quarter {type} Amount",
                            color_discrete_sequence= px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)

        
        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="state" , featureidkey= "properties.ST_NM" , 
                                    color = "amount" , color_continuous_scale= "tempo" ,
                                    range_color= (tacyg["amount"].min() , tacyg["amount"].max()),
                                    hover_name= "state" , title = f"{quarter}{type} amount" ,fitbounds = "locations" ,height = 650 , width = 600)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_count = px.bar(tacyg , x = "state" ,y = "count" , title = f"{yr}-{quarter}  Quarter {type} Count",
                            color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    


        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="state" , featureidkey= "properties.ST_NM" , 
                                    color = "count" , color_continuous_scale= "tempo" ,
                                    range_color= (tacyg["count"].min() , tacyg["count"].max()),
                                    hover_name= "state" , title = f"{quarter}{type} count" ,fitbounds = "locations" ,height = 650 , width = 600)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
    # print("print fig 2")
    return tacy


def Agg_Tran_Transaction_type(df , stat):
    tacy   = df[df["state"] == stat]
    tacy.reset_index(drop = True , inplace = True)
    colors  = px.colors.qualitative.Pastel 
    tacyg = tacy.groupby("name")[["count" , "amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2 = st.columns(2)

    with col1:
        fig_pie_1  = px.pie(data_frame= tacyg , names = "name" , values = "amount" ,
                            width = 600 , title = f"{stat} Transaction Amount" , hole = 0.5 ,color_discrete_sequence=colors)

        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2  = px.pie(data_frame= tacyg , names = "name" , values = "count" ,
                            width = 600 , title = f"{stat} Transaction Count" , hole = 0.5 ,color_discrete_sequence=colors)

        st.plotly_chart(fig_pie_2)
        
    return tacy

    
def Agg_user_plot_1(df , yr):
    aguy = df[df["year"] == yr]
    aguy.reset_index(drop = True , inplace = True)

    aguyg = pd.DataFrame(aguy.groupby("brand")[["user_count" , "user_percentage"]].sum())
    aguyg.reset_index(inplace = True)
    # aguyg

    fig_bar_1  = px.bar(aguyg , x = "brand" , y = "user_count" , title = f"{yr} Brand and User count",
                        width = 600 , color_discrete_sequence= px.colors.sequential.haline , hover_name="brand")

    
    st.plotly_chart(fig_bar_1)
    return aguy

def Agg_user_plot_2(df , yr , quat):
    aguy = df[df["quarter"] == quat]
    aguy.reset_index(drop = True , inplace = True)

    aguyg = pd.DataFrame(aguy.groupby("brand")[["user_count" , "user_percentage"]].sum())
    aguyg.reset_index(inplace = True)
    # aguyg

    fig_bar_1  = px.bar(aguyg , x = "brand" , y = "user_count" , title = f"{yr}-{quat} Quarter Brand and User count",
                        width = 600 , color_discrete_sequence= px.colors.sequential.haline)

    st.plotly_chart(fig_bar_1)
    return aguy

def Agg_user_plot_3(df , yr , stat):
    aguy = df[df["state"] == stat]
    aguy.reset_index(drop = True , inplace = True)

    aguyg = pd.DataFrame(aguy.groupby("brand")[["user_count" , "user_percentage"]].sum())
    aguyg.reset_index(inplace = True)
    # aguyg
    colors  = px.colors.qualitative.Pastel 
    # fig_bar_1  = px.bar(aguyg , x = "brand" , y = "user_count" , hover_data="user_percentage",title = f"{yr} {stat} Brand and User count",
    #                     width = 600 , color_discrete_sequence= px.colors.sequential.haline)
    
    fig_pie_2  = px.pie(aguyg , names = "brand" , values = "user_percentage" , hover_data= "user_count" ,
                        width = 600 , title = f"{yr} {stat} User Percentage" , hole = 0.5 ,color_discrete_sequence=colors)

    st.plotly_chart(fig_pie_2)

    # fig_bar_1.show()
    return aguy

def Agg_user_plot_4(df , yr ,quarter ,stat):
    aguy = df[df["state"] == stat]
    aguy.reset_index(drop = True , inplace = True)

    aguyg = pd.DataFrame(aguy.groupby("brand")[["user_count" , "user_percentage"]].sum())
    aguyg.reset_index(inplace = True)
    # aguyg
    colors  = px.colors.qualitative.Pastel 
    # fig_bar_1  = px.bar(aguyg , x = "brand" , y = "user_count" , hover_data="user_percentage",title = f"{yr} {stat} Brand and User count",
    #                     width = 600 , color_discrete_sequence= px.colors.sequential.haline)
    
    fig_pie_2  = px.pie(aguyg , names = "brand" , values = "user_percentage" , hover_data= "user_count" ,
                        width = 600 , title = f"{yr}-{quarter} {stat} User Percentage" , hole = 0.5 ,color_discrete_sequence=colors)

    st.plotly_chart(fig_pie_2)

    # fig_bar_1.show()
    return aguy


def Map_Transaction_amount_count_Y(df , yr , type):
    tacy  = df[df["year"] ==yr]
    tacy.reset_index(drop = True , inplace =True )

    tacyg = tacy.groupby("state")[["count" , "amount"]].sum()
    tacyg.reset_index(inplace = True)

    print(tacyg.head())

    # fig_amount = px.bar(tacyg , x = "state" ,y = "amount" , title = f"{yr}{type} Amount",
    #                     color_discrete_sequence= px.colors.sequential.Aggrnyl)
    # fig_amount.show()

    # fig_count = px.bar(tacyg , x = "state" ,y = "count" , title = "{yr}{type} Count",
    #                     color_discrete_sequence= px.colors.sequential.Bluered_r)
    # fig_count.show()
    return tacy

def Map_Tran_Transaction_type_state(df , yr , type , stat):
    tacy   = df[df["state"] == stat]
    tacy.reset_index(drop = True , inplace = True)
    colors  = px.colors.qualitative.Pastel 
    tacyg = tacy.groupby("district")[["count" , "amount"]].sum()
    tacyg.reset_index(inplace = True)

    
    fig_amount = px.bar(tacyg , x = "amount" ,y = "district" , orientation="h",title = f"{yr} {type} Amount",
                        color_discrete_sequence= px.colors.sequential.Aggrnyl,height = 600 , width = 650)
    st.plotly_chart(fig_amount)

    fig_count = px.bar(tacyg , x = "count" ,y = "district" , orientation="h", title = f"{yr} {type} Count",
                        color_discrete_sequence= px.colors.sequential.Bluered_r,height = 600 , width = 650)
    st.plotly_chart(fig_count)

    return tacy


def Top_Tran_Transaction_type_state(df, yr, type, stat):
    # Filter data
    tacy = df[(df["state"] == stat) & (df["year"] == yr)].copy()
    tacy.reset_index(drop=True, inplace=True)

    # Ensure pincode is string with leading zeros
    tacy["pincode"] = tacy["pincode"].astype(str).str.zfill(6)

    # Group by pincode
    tacyg = tacy.groupby("pincode")[["count", "amount"]].sum().reset_index()

    # Sort and select top 10 by amount and count
    top_amount = tacyg.sort_values(by="amount", ascending=False).head(10)
    top_count = tacyg.sort_values(by="count", ascending=False).head(10)

    # Plotting
    col1, col2 = st.columns(2)

    with col1:
        fig_amount = px.bar(
            top_amount,
            x="amount",
            y="pincode",
            orientation="h",
            title=f"{yr} {stat} Top 10 Pincodes by {type} Amount",
            color_discrete_sequence=px.colors.sequential.Aggrnyl,
            height=600, width=650
        )
        fig_amount.update_yaxes(type="category")
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(
            top_count,
            x="count",
            y="pincode",
            orientation="h",
            title=f"{yr} {stat} Top 10 Pincodes by {type} Count",
            color_discrete_sequence=px.colors.sequential.Bluered_r,
            height=600, width=650
        )
        fig_count.update_yaxes(type="category")
        st.plotly_chart(fig_count)

    return tacy


def Map_Tran_Transaction_type_quarter(df , qu):
    tacy   = df[df["quarter"] == qu]
    tacy.reset_index(drop = True , inplace = True)
    colors  = px.colors.qualitative.Pastel 
    tacyg = tacy.groupby("state")[["count" , "amount"]].sum()
    tacyg.reset_index(inplace = True)

    return tacy


def Map_Tran_Transaction_type_state_quarter(df , yr , type , stat ,quat):
    tacy   = df[df["state"] == stat]
    tacy.reset_index(drop = True , inplace = True)
    colors  = px.colors.qualitative.Pastel 
    tacyg = tacy.groupby("district")[["count" , "amount"]].sum()
    tacyg.reset_index(inplace = True)

    
    fig_amount = px.bar(tacyg , x = "amount" ,y = "district" , orientation="h",title = f"{yr}-{quat} {stat} {type} Amount",
                        color_discrete_sequence= px.colors.sequential.Aggrnyl,height = 600 , width = 650)
    st.plotly_chart(fig_amount)

    fig_count = px.bar(tacyg , x = "count" ,y = "district" , orientation="h", title = f"{yr}-{quat} {stat} {type} Count",
                        color_discrete_sequence= px.colors.sequential.Bluered_r,height = 600 , width = 650)
    st.plotly_chart(fig_count)


    return tacy



def Top_Tran_Transaction_type_state_quarter(df, yr, type, stat, quat):
    # Filter by state, year, and quarter
    tacy = df[(df["state"] == stat) & (df["year"] == yr) & (df["quarter"] == quat)].copy()
    tacy.reset_index(drop=True, inplace=True)

    # Ensure pincode is string with leading zeros
    tacy["pincode"] = tacy["pincode"].astype(str).str.zfill(6)

    # Group by pincode and calculate total amount & count
    tacyg = tacy.groupby("pincode")[["count", "amount"]].sum().reset_index()

    # Get top 10 by amount and count
    top_amount = tacyg.sort_values(by="amount", ascending=False).head(10)
    top_count = tacyg.sort_values(by="count", ascending=False).head(10)

    # Plotting
    col1, col2 = st.columns(2)

    with col1:
        fig_amount = px.bar(
            top_amount,
            x="amount",
            y="pincode",
            orientation="h",
            title=f"{yr} Q{quat} {stat} Top 10 Pincodes by {type} Amount",
            color_discrete_sequence=px.colors.sequential.Aggrnyl,
            height=600, width=650
        )
        fig_amount.update_yaxes(type="category")
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(
            top_count,
            x="count",
            y="pincode",
            orientation="h",
            title=f"{yr} Q{quat} {stat} Top 10 Pincodes by {type} Count",
            color_discrete_sequence=px.colors.sequential.Bluered_r,
            height=600, width=650
        )
        fig_count.update_yaxes(type="category")
        st.plotly_chart(fig_count)

    return tacy



def map_user_plot_1(df, yr):
    muy = df[df["year"] == yr]
    muy.reset_index(drop = True , inplace = True)
    # muy
    muyg = muy.groupby("state")[["registered_users" , "app_opens"]].sum()
    muyg.reset_index(inplace = True)
    # muyg


    fig_bar_1  = px.bar(muyg , x = "state" , y = "registered_users" , title = f"{yr} Registered Users",
                            height=800 , width = 800 ,color_discrete_sequence=px.colors.qualitative.Set2)

    st.plotly_chart(fig_bar_1)
    fig_bar_2  = px.bar(muyg , x = "state" , y = "app_opens" , title = f"{yr} App Opens",
                            height=800 , width = 800 ,color_discrete_sequence=px.colors.qualitative.Set3_r)

    st.plotly_chart(fig_bar_2)
    return muy

def map_user_plot_2(df, yr ,quat):
    muy = df[df["quarter"] == quat]
    muy.reset_index(drop = True , inplace = True)
    # muy
    muyg = muy.groupby("state")[["registered_users" , "app_opens"]].sum()
    muyg.reset_index(inplace = True)
    # muyg


    fig_bar_1  = px.bar(muyg , x = "state" , y = "registered_users" , title = f"{yr}-{quat} Registered Users",
                            height=800 , width = 800 ,color_discrete_sequence=px.colors.qualitative.Set2)

    st.plotly_chart(fig_bar_1)
    fig_bar_2  = px.bar(muyg , x = "state" , y = "app_opens" , title = f"{yr}-{quat} App Opens",
                            height=800 , width = 800 ,color_discrete_sequence=px.colors.qualitative.Set3_r)

    st.plotly_chart(fig_bar_2)
    return muy

def map_user_plot_3(df, yr ,quat ,stat):
    muy = df[df["state"] == stat]
    muy.reset_index(drop = True , inplace = True)
    # muy
    muyg = muy.groupby("district")[["registered_users" , "app_opens"]].sum()
    muyg.reset_index(inplace = True)
    # muyg


    fig_bar_1  = px.bar(muyg , x = "registered_users" , y = "district" ,orientation="h", title = f"{yr}-{quat} {stat} Registered Users",
                            height=800 , width = 800 ,color_discrete_sequence=px.colors.qualitative.Set2)

    st.plotly_chart(fig_bar_1)
    fig_bar_2  = px.bar(muyg , x = "app_opens" , y = "district" ,orientation= "h", title = f"{yr}-{quat} {stat} App Opens",
                            height=800 , width = 800 ,color_discrete_sequence=px.colors.qualitative.Set3_r)

    st.plotly_chart(fig_bar_2)
    return muy
def map_user_plot_4(df, yr ,stat):
    muy = df[df["state"] == stat]
    muy.reset_index(drop = True , inplace = True)
    # muy
    muyg = muy.groupby("district")[["registered_users" , "app_opens"]].sum()
    muyg.reset_index(inplace = True)
    # muyg


    fig_bar_1  = px.bar(muyg , x = "registered_users" , y = "district" ,orientation="h", title = f"{yr} {stat} Registered Users",
                            height=800 , width = 800 ,color_discrete_sequence=px.colors.qualitative.Set2)

    st.plotly_chart(fig_bar_1)
    fig_bar_2  = px.bar(muyg , x = "app_opens" , y = "district" ,orientation= "h", title = f"{yr} {stat} App Opens",
                            height=800 , width = 800 ,color_discrete_sequence=px.colors.qualitative.Set3_r)

    st.plotly_chart(fig_bar_2)
    return muy


def Top_User_Registered_by_State_district(df, yr, stat):
    # Filter by state and year
    tacy = df[(df["year"] == yr) & (df["state"] == stat)].copy()
    tacy.reset_index(drop=True, inplace=True)

    tacy["district"] = tacy["district"].astype(str).str.title()

    # Group and get top 10
    tacyg = tacy.groupby("district")[["registered_users"]].sum().reset_index()
    top_users = tacyg.sort_values(by="registered_users", ascending=False).head(10)

    # Plot
    fig = px.bar(
        top_users,
        x="registered_users",
        y="district",
        orientation="h",
        title=f"{yr} {stat} Top 10 Districts by Registered Users",
        color_discrete_sequence=px.colors.sequential.Teal,
        height=600, width=650
    )
    fig.update_yaxes(type="category")
    st.plotly_chart(fig)

    return tacy


def Top_User_Registered_by_State_pincode(df, yr, stat):
    # Filter by state and year
    tacy = df[(df["year"] == yr) & (df["state"] == stat)].copy()
    tacy.reset_index(drop=True, inplace=True)

    tacy["pincode"] = tacy["pincode"].astype(str).str.zfill(6)

    # Group and get top 10
    tacyg = tacy.groupby("pincode")[["registered_users"]].sum().reset_index()
    top_users = tacyg.sort_values(by="registered_users", ascending=False).head(10)

    # Plot
    fig = px.bar(
        top_users,
        x="registered_users",
        y="pincode",
        orientation="h",
        title=f"{yr} {stat} Top 10 Pincodes by Registered Users",
        color_discrete_sequence=px.colors.sequential.Teal,
        height=600, width=650
    )
    fig.update_yaxes(type="category")
    st.plotly_chart(fig)

    return tacy



def transaction_trend_growth(df):
    st.header("Transaction Growth Trend Analysis")
    
    trend_df = df.groupby(["year", "state"])[["count", "amount"]].sum().reset_index()

    top_states = trend_df.groupby("state")["amount"].sum().sort_values(ascending=False).head(5).index.tolist()
    filtered = trend_df[trend_df["state"].isin(top_states)]

    fig1 = px.line(filtered, x="year", y="amount", color="state", title="Top 5 States by Transaction Amount Over Time")
    fig2 = px.line(filtered, x="year", y="count", color="state", title="Top 5 States by Transaction Count Over Time")
    
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

def user_engagement_trend(df):
    st.header("User Engagement Trend Analysis")
    
    trend_df = df.groupby(["year", "state"])[["registered_users", "app_opens"]].sum().reset_index()

    top_states = trend_df.groupby("state")["registered_users"].sum().sort_values(ascending=False).head(5).index.tolist()
    filtered = trend_df[trend_df["state"].isin(top_states)]

    fig1 = px.line(filtered, x="year", y="registered_users", color="state", title="Top 5 States by Registered Users Over Time")
    fig2 = px.line(filtered, x="year", y="app_opens", color="state", title="Top 5 States by App Opens Over Time")

    st.plotly_chart(fig1)
    st.plotly_chart(fig2)


def quarterly_transaction_trend(df):
    st.header("Quarterly Transaction Trend (Across All Years)")

    df['year_quarter'] = df['year'].astype(str) + "-Q" + df['quarter'].astype(str)

    trend_df = df.groupby(["year_quarter", "state"])[["count", "amount"]].sum().reset_index()
    trend_df.sort_values("year_quarter", inplace=True)

    top_states = trend_df.groupby("state")["amount"].sum().sort_values(ascending=False).head(5).index.tolist()
    filtered = trend_df[trend_df["state"].isin(top_states)]

    fig1 = px.line(
        filtered,
        x="year_quarter",
        y="amount",
        color="state",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=px.colors.qualitative.Set1,
        title="Top 5 States - Transaction Amount by Quarter"
    )
    fig2 = px.line(
        filtered,
        x="year_quarter",
        y="count",
        color="state",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Top 5 States - Transaction Count by Quarter"
    )

    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

def quarterly_user_engagement_trend(df):
    st.header("Quarterly User Engagement Trend (Across All Years)")

    df['year_quarter'] = df['year'].astype(str) + "-Q" + df['quarter'].astype(str)

    trend_df = df.groupby(["year_quarter", "state"])[["registered_users", "app_opens"]].sum().reset_index()
    trend_df.sort_values("year_quarter", inplace=True)

    top_states = trend_df.groupby("state")["registered_users"].sum().sort_values(ascending=False).head(5).index.tolist()
    filtered = trend_df[trend_df["state"].isin(top_states)]

    fig1 = px.line(
        filtered,
        x="year_quarter",
        y="registered_users",
        color="state",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=px.colors.qualitative.Dark24,
        title="Top 5 States - Registered Users by Quarter"
    )
    fig2 = px.line(
        filtered,
        x="year_quarter",
        y="app_opens",
        color="state",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=px.colors.qualitative.Prism,
        title="Top 5 States - App Opens by Quarter"
    )

    st.plotly_chart(fig1)
    st.plotly_chart(fig2)


def quarterly_transaction_trend_by_state(df_district, df_pincode):
    st.header("Quarterly Transaction Trends by Districts & Pincodes")

    selected_state = st.selectbox("Select a State", sorted(df_district["state"].unique()))
    
    for df in [df_district, df_pincode]:
        df["year_quarter"] = df["year"].astype(str) + "-Q" + df["quarter"].astype(str)

    dist_filtered = df_district[df_district["state"] == selected_state]
    pin_filtered = df_pincode[df_pincode["state"] == selected_state]

    top_districts = dist_filtered.groupby("district")["amount"].sum().sort_values(ascending=False).head(5).index.tolist()
    df_d_top = dist_filtered[dist_filtered["district"].isin(top_districts)].sort_values("year_quarter")

    top_districts_count = dist_filtered.groupby("district")["count"].sum().sort_values(ascending=False).head(5).index.tolist()
    df_d_top_count = dist_filtered[dist_filtered["district"].isin(top_districts_count)].sort_values("year_quarter")

    top_pincodes = pin_filtered.groupby("pincode")["amount"].sum().sort_values(ascending=False).head(5).index.tolist()
    df_p_top = pin_filtered[pin_filtered["pincode"].isin(top_pincodes)].sort_values("year_quarter")

    top_pincodes_count = pin_filtered.groupby("pincode")["count"].sum().sort_values(ascending=False).head(5).index.tolist()
    df_p_top_count = pin_filtered[pin_filtered["pincode"].isin(top_pincodes_count)].sort_values("year_quarter")

    st.subheader(f"Top 5 Districts in {selected_state} (by Amount)")
    fig1 = px.line(df_d_top, x="year_quarter", y="amount", color="district", markers=True,
                   title="Transaction Amount by District (Quarterly)",
                   color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig1)

    st.subheader(f"Top 5 Pincodes in {selected_state} (by Amount)")
    fig2 = px.line(df_p_top, x="year_quarter", y="amount", color="pincode", markers=True,
                   title="Transaction Amount by Pincode (Quarterly)",
                   color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig2)

    st.subheader(f"Top 5 Districts in {selected_state} (by Count)")
    fig3 = px.line(df_d_top_count, x="year_quarter", y="count", color="district", markers=True,
                   title="Transaction Count by District (Quarterly)",
                   color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig3)

    st.subheader(f"Top 5 Pincodes in {selected_state} (by Count)")
    fig4 = px.line(df_p_top_count, x="year_quarter", y="count", color="pincode", markers=True,
                   title="Transaction Count by Pincode (Quarterly)",
                   color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig4)






















st.set_page_config(layout="wide")




col1, col2 = st.columns([1, 8])

with col1:
    st.image("phonepe_logo2.png", width=100)

with col2:
    st.markdown(
        """
        <div style='display: flex; align-items: center; height: 90%; background-color: #111;
                    padding: 10px 15px; border-radius: 0px;'>
            <h1 style='color: white; margin: 0;'>PhonePe Data Visualization and Exploration</h1>
        </div>
        """,
        unsafe_allow_html=True
    )


with st.sidebar:
    # st.write("Aryan")

    select = option_menu("Main Menu" , ["Home" , "Interactive Explorer" , "Trend Insights"])


# if select =="Home":
#     pass
if select == "Home":

    # st.title("Welcome to PhonePe Data Analytics Dashboard")
    st.markdown("""
    This interactive dashboard provides powerful insights into PhonePe's digital payment ecosystem.  
    Dive into transaction patterns, user engagement, and insurance trends across India.
    """)

    # Project Overview
    st.subheader("Project Overview")
    st.markdown("""
    This project analyzes PhonePe's digital transaction ecosystem using data from 2018 to 2023.  
    Key features include:
    - **Pan-India coverage** of states, districts, and pincodes
    - **User, transaction, and insurance analysis**
    - **Quarterly and yearly trend comparisons**
    - **Top-performing locations and device usage**
    """)

    # Business Case Studies
    st.subheader("Business Case Studies")
    st.markdown("""
    This dashboard is designed to answer real-world business questions including:
    1. **Decoding Transaction Dynamics** Identify growing/stagnant regions and categories
    2. **User Engagement & Device Analysis** Explore user activity across devices and regions
    3. **Insurance Growth Analysis** Discover untapped potential in the insurance segment
    4. **Market Expansion Opportunities** Locate regions with high growth potential
    5. **District & Pincode Trends** Analyze top locations by transaction count and value
    """)


    # Data Source
    st.subheader("Data Source")
    st.markdown("""
    The dataset is extracted from the official [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse),  
    processed using SQL and Python, and visualized in real-time through this dashboard.
    """)

    # # Optional KPIs (if you want to show quick stats)
    # st.subheader("Project Summary Metrics (Sample)")
    # col1, col2, col3 = st.columns(3)
    # col1.metric("Total Transactions", "₹12.3 Cr")
    # col2.metric("Total Registered Users", "89 Lakh")
    # col3.metric("Insurance Transactions", "2.1 Cr")


elif select =="Interactive Explorer":

    tab1 , tab2 ,tab3 = st.tabs(["Aggregated Analysis" , "Map", "Top"])

    with tab1:

        # method= st.tabs(["Insurance" ,"Transaction" , "User"])
        method= st.radio("Select the method" , ["Insurance" ,"Transaction" , "User"])

        if method == "Insurance":
            
            col1  , col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the year",
                                    sorted(db.df_aggregated_insurance["year"].unique())
                                )
            agg_insu_tac_Y = Transaction_amount_count_Y(db.df_aggregated_insurance , years , "Insurance")


            col1 , col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarter",
                                    agg_insu_tac_Y["quarter"].min() , agg_insu_tac_Y["quarter"].max()
                                )
            agg_insu_tac_Y_Q = Transaction_amount_count_Y_Q(agg_insu_tac_Y , years ,quarters  , "Insurance")


            pass
        elif method=="Transaction":

            col1  , col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the year",
                                    sorted(db.df_aggregated_transaction["year"].unique())
                                )
            agg_tran_tac_Y = Transaction_amount_count_Y(db.df_aggregated_transaction, years , "Transaction")


            col1  , col2 = st.columns(2)
            with col1:
                stat = st.selectbox("Select the state " ,sorted(agg_tran_tac_Y["state"].unique()),key="state_by_year")

            agg_tran_tac_Y_state = Agg_Tran_Transaction_type(agg_tran_tac_Y , stat)


            col1 , col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarter",
                                    agg_tran_tac_Y["quarter"].min() , agg_tran_tac_Y["quarter"].max()
                                )
            agg_tran_tac_Y_Q = Transaction_amount_count_Y_Q(agg_tran_tac_Y , years ,quarters  , "Transaction")


            col1  , col2 = st.columns(2)
            with col1:
                stat2 = st.selectbox("Select the state " ,sorted(agg_tran_tac_Y_Q["state"].unique()),key="state_by_quarter")

            agg_tran_tac_Y_state_Q = Agg_Tran_Transaction_type(agg_tran_tac_Y_Q , stat2)
            pass


        elif method=="User":

            col1  , col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the year",
                                    sorted(db.df_aggregated_user["year"].unique())
                                )
            aguy_agg_user_Y = Agg_user_plot_1(db.df_aggregated_user, years)

            col1  , col2 = st.columns(2)
            with col1:
                stat = st.selectbox("Select the state " ,sorted(aguy_agg_user_Y["state"].unique()),key="state_by_year")

            aguy_agg_user_Y_state = Agg_user_plot_3(aguy_agg_user_Y , years ,stat)

            col1 , col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarter",
                                    aguy_agg_user_Y["quarter"].min() , aguy_agg_user_Y["quarter"].max()
                                )
            aguy_agg_user_Y_Q = Agg_user_plot_2(aguy_agg_user_Y , years ,quarters)

            

            col1  , col2 = st.columns(2)
            with col1:
                stat2 = st.selectbox("Select the state " ,sorted(aguy_agg_user_Y_Q["state"].unique()),key="state_by_quarter")

            aguy_agg_user_Y_state_Q= Agg_user_plot_4(aguy_agg_user_Y_Q , years ,quarters, stat2)



            pass

    with tab2:

        # method= st.tabs(["Insurance" ,"Transaction" , "User"])
        method2= st.radio("Select the method" , ["Map Insurance" ,"Map Transaction" , "Map User"])

        if method2 == "Map Insurance":
            col1  , col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the year",
                                    sorted(db.df_map_insurance["year"].unique()),
                                key="map_insurance_year")
            map_insu_tac_Y = Map_Transaction_amount_count_Y(db.df_map_insurance ,years ,"Insurance")

            col1  , col2 = st.columns(2)
            with col1:
                stat = st.selectbox("Select the state " ,sorted(map_insu_tac_Y["state"].unique()),key="insurance_state_by_year")

            map_insu_tac_Y_state = Map_Tran_Transaction_type_state(map_insu_tac_Y , years , "Insurance" ,stat)


            col1 , col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarter",
                                    map_insu_tac_Y["quarter"].min() , map_insu_tac_Y["quarter"].max()
                                ,key  = "ditrict_by_quarter")
            map_insu_tac_Y_Q = Map_Tran_Transaction_type_quarter(map_insu_tac_Y , quarters)

            map_insu_tac_Y_Q_state = Map_Tran_Transaction_type_state_quarter(map_insu_tac_Y_Q , years , "Insurance" ,stat , quarters)


            pass


        elif method2=="Map Transaction":

            col1, col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the year",
                                    sorted(db.df_map_transaction["year"].unique()),
                                    key="map_transaction_year")
            map_tran_tac_Y = Map_Transaction_amount_count_Y(db.df_map_transaction, years, "Transaction")

            col1, col2 = st.columns(2)
            with col1:
                stat = st.selectbox("Select the state", 
                                    sorted(map_tran_tac_Y["state"].unique()), 
                                    key="transaction_state_by_year")

            map_tran_tac_Y_state = Map_Tran_Transaction_type_state(map_tran_tac_Y, years, "Transaction", stat)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarter",
                                    map_tran_tac_Y["quarter"].min(),
                                    map_tran_tac_Y["quarter"].max(),
                                    key="transaction_quarter")

            map_tran_tac_Y_Q = Map_Tran_Transaction_type_quarter(map_tran_tac_Y, quarters)

            map_tran_tac_Y_Q_state = Map_Tran_Transaction_type_state_quarter(map_tran_tac_Y_Q, years, "Transaction", stat, quarters)

            pass
        elif method2=="Map User":

            col1, col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the year",
                                    sorted(db.df_map_user["year"].unique()),
                                    key="map_user_year")
            map_user_Y  = map_user_plot_1(db.df_map_user , years)

            with col1:
                stat = st.selectbox("Select the state", 
                                    sorted(map_user_Y["state"].unique()), 
                                    key="transaction_state_by_year")

            map_user_Y_state= map_user_plot_4(map_user_Y , years ,stat)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarter",
                                    map_user_Y["quarter"].min(),
                                    map_user_Y["quarter"].max(),
                                    key="user_quarter")

            map_user_Y_Q = map_user_plot_2(map_user_Y , years , quarters)

            map_user_Y_state_Q = map_user_plot_3(map_user_Y_Q , years , quarters ,stat)
            pass



    with tab3:

        # method= st.tabs(["Insurance" ,"Transaction" , "User"])
        method3= st.radio("Select the method" , ["Top Insurance" ,"Top Transaction" , "Top User"])

        if method3 == "Top Insurance":
            col1  , col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the year",
                                    sorted(db.df_top_insurance_district["year"].unique()),
                                key="top_insurance_year")
            top_insu_tac_Y = Map_Transaction_amount_count_Y(db.df_top_insurance_district ,years ,"Insurance")
            top_insu_tac_Y_pincode = Map_Transaction_amount_count_Y(db.df_top_insurance_pincode ,years ,"Insurance")

            col1  , col2 = st.columns(2)
            with col1:
                stat = st.selectbox("Select the state " ,sorted(top_insu_tac_Y["state"].unique()),key="top_insurance_state_by_year")

            top_insu_tac_Y_state = Map_Tran_Transaction_type_state(top_insu_tac_Y , years , "Insurance" ,stat)
            top_insu_tac_Y_state_pincode = Top_Tran_Transaction_type_state(top_insu_tac_Y_pincode , years , "Insurance" ,stat)


            col1 , col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarter",
                                    top_insu_tac_Y["quarter"].min() , top_insu_tac_Y["quarter"].max()
                                ,key  = "top_ditrict_by_quarter")
            top_insu_tac_Y_Q = Map_Tran_Transaction_type_quarter(top_insu_tac_Y , quarters)
            

            top_insu_tac_Y_Q_state = Map_Tran_Transaction_type_state_quarter(top_insu_tac_Y_Q , years , "Insurance" ,stat , quarters)

            top_insu_tac_Y_Q_pincode = Map_Tran_Transaction_type_quarter(top_insu_tac_Y_pincode , quarters)
            top_insu_tac_Y_Q_state_pincode = Top_Tran_Transaction_type_state_quarter(top_insu_tac_Y_Q_pincode , years , "Insurance" ,stat , quarters)


            
            pass
        elif method3=="Top Transaction":
            
            col1  , col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the year",
                                    sorted(db.df_top_transaction_district["year"].unique()),
                                key="top_transaction_year")
            top_tran_tac_Y = Map_Transaction_amount_count_Y(db.df_top_transaction_district ,years ,"Transaction")
            top_tran_tac_Y_pincode = Map_Transaction_amount_count_Y(db.df_top_transaction_pincode ,years ,"Transaction")

            col1  , col2 = st.columns(2)
            with col1:
                stat = st.selectbox("Select the state " ,sorted(top_tran_tac_Y["state"].unique()),key="top_transaction_state_by_year")

            top_tran_tac_Y_state = Map_Tran_Transaction_type_state(top_tran_tac_Y , years , "Transaction" ,stat)
            top_tran_tac_Y_state_pincode = Top_Tran_Transaction_type_state(top_tran_tac_Y_pincode , years , "Transaction" ,stat)


            col1 , col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarter",
                                    top_tran_tac_Y["quarter"].min() , top_tran_tac_Y["quarter"].max()
                                ,key  = "top_ditrict_by_quarter")
            top_tran_tac_Y_Q = Map_Tran_Transaction_type_quarter(top_tran_tac_Y , quarters)
            

            top_tran_tac_Y_Q_state = Map_Tran_Transaction_type_state_quarter(top_tran_tac_Y_Q , years , "Transaction" ,stat , quarters)

            top_tran_tac_Y_Q_pincode = Map_Tran_Transaction_type_quarter(top_tran_tac_Y_pincode , quarters)
            top_tran_tac_Y_Q_state_pincode = Top_Tran_Transaction_type_state_quarter(top_tran_tac_Y_Q_pincode , years , "Transaction" ,stat , quarters)




            pass
        elif method3=="Top User":

            col1, col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select the year",
                                    sorted(db.df_top_user["year"].unique()),
                                    key="top_user_year")

            col1, col2 = st.columns(2)
            with col1:
                stat = st.selectbox("Select the state",
                                    sorted(db.df_top_user["state"].unique()),
                                    key="top_user_state")

            Top_User_Registered_by_State_district(db.df_top_user_district, years, stat)

            Top_User_Registered_by_State_pincode(db.df_top_user_pincode, years, stat)

            pass


elif select =="Trend Insights":
    with st.expander("Market Expansion Trend (Transaction Growth)"):
        transaction_trend_growth(db.df_aggregated_transaction)

    with st.expander("User Engagement Trend (Registered Users & App Opens)"):
        user_engagement_trend(db.df_map_user)

    with st.expander("Quarterly Transaction Trend (All Years)"):
        quarterly_transaction_trend(db.df_aggregated_transaction)

    with st.expander("Quarterly User Engagement Trend (All Years)"):
        quarterly_user_engagement_trend(db.df_map_user)


    with st.expander("Quarterly Trend by Districts and Pincodes in Selected State"):
        quarterly_transaction_trend_by_state(db.df_top_transaction_district, db.df_top_transaction_pincode)


    
    pass

