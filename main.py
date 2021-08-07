import streamlit as st
import pandas as pd
import plotly.express as px


class Covid19:

    def __init__(self):
        self.csv_file = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv')
        self.country = sorted(list(set([i for i in self.csv_file['Country']])))

    def global_spread(self):
        fig=px.choropleth(self.csv_file,locations='Country',locationmode='country names',color='Confirmed',animation_frame="Date")
        st.plotly_chart(fig)

    def global_death(self):
        fig=px.choropleth(self.csv_file,locations='Country',locationmode='country names',color='Deaths',animation_frame="Date")
        st.plotly_chart(fig)

    def global_infection_rate(self):
        countries=list(self.csv_file['Country'].unique())
        max_infection_rates=[]
        for c in countries:
            MIR=self.csv_file[self.csv_file.Country==c].Confirmed.diff().max()
            max_infection_rates.append(MIR)
        df_MIR=pd.DataFrame()
        df_MIR['Country']=countries
        df_MIR['Max Infection Rate']=max_infection_rates
        df_MIR.head()
        fig = px.bar(df_MIR,x='Country',y='Max Infection Rate',color='Country',log_y='true')
        st.plotly_chart(fig)

    def country_wise_spread(self, choice):
        df_country=self.csv_file[self.csv_file.Country == choice]
        df_country=df_country[['Date','Confirmed','Deaths','Recovered']]
        df_country['Infection Rate']=df_country['Confirmed'].diff()
        df_country['Deaths Rate']=df_country['Deaths'].diff()
        fig = px.line(df_country,x='Date',y=['Confirmed','Infection Rate','Deaths Rate','Recovered','Deaths'],title='Country :- {}'.format(choice))
        st.plotly_chart(fig)

    def main_screen(self):
        st.title('Covid-19 Data Visualization')
        menu = ['<select>', 'Global Spread of Covid-19', 'Global Death of Covid-19', 'Global Maximum Infection Rate', 'Country wise Covid-19 Spread']
        choice = st.sidebar.selectbox('Menu', menu)

        if choice == '<select>':
            pass

        elif choice == 'Global Spread of Covid-19':
            st.subheader('Global Spread of Covid-19')
            self.global_spread()

        elif choice == 'Global Death of Covid-19':
            st.subheader('Global Death of Covid-19')
            self.global_death()

        elif choice == 'Global Maximum Infection Rate':
            st.subheader('Global Maximum Infection Rate')
            self.global_infection_rate()

        else:
            st.subheader('Country wise Covid-19 Spread')
            choice1 = st.selectbox('Select Country',self.country)
            self.country_wise_spread(choice1)



if __name__ == '__main__':
    c = Covid19()
    c.main_screen()