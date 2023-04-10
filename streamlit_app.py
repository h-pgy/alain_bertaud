import streamlit as st
import pydeck as pdk
import pandas as pd
import requests
import plotly.express as px
import  streamlit_toggle as st_toggle

with st.sidebar:
    st.image('https://observasampa.prefeitura.sp.gov.br/assets/img/logo.webp', use_column_width=True)
    text = """
    ## Vertical Housing Development
    ### City of São Paulo - 2013 to 2023
    This app aims to explore the causes of the vertical housing development ocurred in the city of São Paulo during the last decade (2013-2023).

    Here, I analyse the relation between the ease of access to the job market in a given city district and the verticalization, measured in square-meters of vertical residential built area, ocurred on the district during the period.

    The model proposed, an OLS based on Alain Bertaud's *Order Without Design* shows that the proportion of the city's job market that is accessible by a less than one hour commute explains a striking 29% of the variability of the vertical residential growth ocurred, with a highly statisticaly significant p-value (p<10^-7).
    """
    st.markdown(text)

    st.markdown('#### **Developed by**: Henrique Pougy')
    col1, col2 = st.columns([0.5, 3])

    with col1:
        st.image('https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg', use_column_width=True)
    with col2:
        st.markdown('[linkedin](https://www.linkedin.com/in/henrique-pougy-8a008759?originalSubdomain=br)')

st.title('Vertical Housing Development and Access to the Job Market', anchor=None)


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Vertical Residential Growth", 
                                        "Commute Times", 
                                        "Distribution of Jobs", 
                                        "Job Market Accessibility",
                                        "Statistical Model"])

@st.cache_data
def load_dists_wgs84():

    url = 'https://raw.githubusercontent.com/h-pgy/alain_bertaud/streamlit_app/geojsons/dists_wgs84.geojson'
    with requests.get(url) as r:
        return r.json()

geojson=load_dists_wgs84()

@st.cache_resource
def gerar_pydcek(data_url:str, col_altura:str, multipli_altura:int=1):


    layer = pdk.Layer(
        "GeoJsonLayer",
        data_url,
        opacity=0.8,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        pickable=True,
        get_elevation =f"properties.{col_altura}*{multipli_altura}",
        get_fill_color=f"[255, 255, 255]",
        get_line_color=[230, 230, 255],
        auto_highlight=True,

    )

    view_state = pdk.ViewState(
        **{"latitude": -23.6, "longitude": -46.6, "zoom": 10, "maxZoom": 16, "pitch": 45, "bearing": 8}
    )

    r = pdk.Deck(
        layer,
        initial_view_state=view_state,
        map_style=pdk.map_styles.DARK,
    )

    return r

@st.cache_resource
def gerar_pyplot(df, col_altura:str):

    fig = px.choropleth(df, geojson=geojson, color=col_altura,
                        locations="ds_nome", featureidkey="properties.ds_nome",
                        projection="mercator", hover_data=["ds_nome"]
                    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

    return fig

@st.cache_resource
def gerar_mapa_delta(tipo:str):

    data_url = 'https://raw.githubusercontent.com/h-pgy/alain_bertaud/streamlit_app/geojsons/delta_pde.geojson'

    if tipo == 'delta':
        col_altura = 'delta_pde'
        multipli_altura=2000
    else:
        col_altura = f'area_construida_vertical_{tipo}'
        multipli_altura=1000
        
    r = gerar_pydcek(data_url, col_altura,
                     multipli_altura=multipli_altura)
    
    return r



@st.cache_data
def load_df(url):

    return pd.read_csv(url, sep=';')

@st.cache_data
def load_json(url):

    with requests.get(url) as r:
        return r.json()


@st.cache_resource
def gerar_mapa2d_delta(tipo:str):

    url = 'https://raw.githubusercontent.com/h-pgy/alain_bertaud/streamlit_app/generated_data/delta_area_construida_distrito.csv'

    df = load_df(url)

    if tipo == 'delta':
        col_altura = 'delta_pde'
    else:
        col_altura = f'area_construida_vertical_{tipo}'

    fig = gerar_pyplot(df, col_altura)
    
    return fig

@st.cache_resource
def gerar_mapa2d_modelo(tipo:str):

    if tipo == 'Absolute Error':
        col_altura = 'abs_error'
    elif tipo == 'Error Proportional to the True Value':
        col_altura = 'proportion_error'
    elif tipo == 'Predicted value':
        col_altura = 'predicted'

    fig = gerar_pyplot(df_final, col_altura)

    return fig

with tab1:

    with st.expander('Details', expanded=True):
        st.markdown("""
        #### About the data
        The data shown here is based on the Property Tax database made available by the city of São Paulo.

        More then 6 million registers, representing each formal property on the city during the years of 2013 and 2023, where processed.
        The total built area of vertical housing was obtained through the summation, for a given city district, of the areas of all the individual apartments built areas (here considered as floor space plus the unity's proportion to the commom areas and parking garage).
        The gross vertical housing growth was calculated through the subtraction of the total vertical housing built area of a given city block in 2023 from it's original built area in 2013. Then each city block's growth were summed by city district.
        """)

    
    
    def map_format_func(option)->str:

        if option == 'delta':
            return "Gross Vertical Residential Growth (sqms)"
        else:
            return f'Vertical Housing Total Built Area for year {option}'
    tipo = st.selectbox("Select the map type:", [2013, 2023, 'delta'], format_func=map_format_func)

    *_, col4 = st.columns(4)

    with col4:
        toggle1 = st.checkbox(label="Switch to 2D map", 
                        key="2D_tab1", 
                        value=False, 
                        )


    if not toggle1:

        r = gerar_mapa_delta(tipo=tipo)

        st.pydeck_chart(r)

    else:
        fig = gerar_mapa2d_delta(tipo=tipo)
        st.plotly_chart(fig, use_container_width=True)

with tab2:

    with st.expander('Details', expanded=True):
        st.markdown("""
        #### About the data
        The data shown here is based on the Origin and Destination survey conducted by the Sao Paulo Metropolitan Region's Subway Company on the year 2017.

        The survey contains data related to travels made by people on São Paulo Metropolitan region, with their origins and destinations geolocated, along with information about the motives of the trips.
        For this map, we've selected all the trips originated inside the city of São Paulo whose motive was related to work, that is:
        * "Going to work" or
        * "Looking for a job"

        Then we aggregated the trip data by city district, obtaining the **mean commute time** for the commutes originated on the district.
        """)

    *_, col4 = st.columns(4)

    with col4:
        toggle2 = st.checkbox(label="Switch to 2D map", 
                        key="2D_tab2", 
                        value=False, 
                        )

    if not toggle2:

        data_url = 'https://raw.githubusercontent.com/h-pgy/alain_bertaud/streamlit_app/geojsons/commute_times.geojson'
        multipli_altura=80
        col_altura='DURACAO'
        r = gerar_pydcek(data_url, col_altura,
                     multipli_altura=multipli_altura)

        st.pydeck_chart(r)

    else:
        url = 'https://raw.githubusercontent.com/h-pgy/alain_bertaud/streamlit_app/generated_data/media_duracao_viagem_trabalho_dist.csv'
        df = load_df(url)
        df.rename({'ds_origem_nome':'ds_nome'}, axis=1, inplace=True)
        fig = gerar_pyplot(df,'DURACAO')
        st.plotly_chart(fig, use_container_width=True)

with tab3:

    with st.expander('Details', expanded=True):
        st.markdown("""
        #### About the data
        The data shown here is based on the RAIS database provided by the Ministry of Labour of the Federal Government of Brazil.

        The data contains information about every formal job in Brazil. Companies are obliged by law to provide the data about their employees annually. 
        Anonymized microdata about the job relations, containing information about the location of work is provided by the Government. Maria Gorete da Silva geolocalized the registers in the city of São Paulo, by city district.

        The map bellow shows the, made by me, shows the percentage of the totality of jobs in the city that are located in a given city district.
        """)

    *_, col4 = st.columns(4)
    
    with col4:
        toggle3 = st.checkbox(label="Switch to 2D map", 
                        key="2D_tab3", 
                        value=False, 
                        )

    if not toggle3:

        data_url = 'https://raw.githubusercontent.com/h-pgy/alain_bertaud/streamlit_app/geojsons/percent_jobs_per_district.geojson'
        multipli_altura=1000
        col_altura='percent_empregos'
        r = gerar_pydcek(data_url, col_altura,
                    multipli_altura=multipli_altura)

        st.pydeck_chart(r)

    else:
        url = 'https://raw.githubusercontent.com/h-pgy/alain_bertaud/streamlit_app/generated_data/percent_empregos_por_dist.csv'
        df = load_df(url)
        fig = gerar_pyplot(df,'percent_empregos')
        st.plotly_chart(fig, use_container_width=True)

with tab4:

    with st.expander('Details', expanded=True):
        st.markdown("""
        #### About the data
        The data shown here was generated throught the analyzis of the data contained on tabs "Commute Times" and "Distribution of Jobs".

        For each city district, we calculated the mean travel time for work related trips originated on that district to every other city district (based on the Origin Destination Survey).

        Then, we calculated the percentage of jobs in relation to the whole job market of the city that is accessible within an one hour trip from each district in the city.

        The map above therefore shows the Job Market Accessibility for each district of the city.
        """)

    *_, col4 = st.columns(4)

    with col4:
        toggle4 = st.checkbox(label="Switch to 2D map", 
                        key="2D_tab4", 
                        value=False, 
                        )

    if not toggle4:

        data_url = 'https://raw.githubusercontent.com/h-pgy/alain_bertaud/streamlit_app/geojsons/job_market_access.geojson'
        multipli_altura=10000
        col_altura='percent_empregos_destino'
        r = gerar_pydcek(data_url, col_altura,
                    multipli_altura=multipli_altura)

        st.pydeck_chart(r)

    else:
        url = 'https://raw.githubusercontent.com/h-pgy/alain_bertaud/streamlit_app/generated_data/percent_jobs_acessible.csv'
        df = load_df(url)
        df.rename({'ds_origem_nome' : 'ds_nome'}, axis=1, inplace=True)
        df['percent_empregos_destino']=df['percent_empregos_destino']*100
        fig = gerar_pyplot(df,'percent_empregos_destino')
        st.plotly_chart(fig, use_container_width=True)


with tab5:

    with st.expander('Details', expanded=True):
        st.markdown("""
        #### About the model
        This tab shows the results of an Ordinary Least Squares Model (OLS) that predicts the gross vertical housing built area 
        growth for a given city district in São Paulo in the last decade (2013-2023) in function of the district's access to the city's job market.
        """)

        st.latex("y_i = a + b*x_i")

        st.markdown("""
        **Where**:
        * *i* = a given city district;
        * *y* = vertical residential built area growth;
        * *x* = percentage of the city's job market that is accessible by an one hour trip from that district
        
        As it can be seem bellow, the model, nevertheless it's simplicity, has an outstanding performance, with more than 29% of the variability explained by it.
        """)

    dados_modelo = load_json('https://raw.githubusercontent.com/h-pgy/alain_bertaud/streamlit_app/generated_data/dados_modelo.json')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('R-squared', dados_modelo['rsquared'])
    with col2:
        st.metric('Beta p-value','%.2E' % dados_modelo['pvalue_beta'])
    with col3:
        st.metric('Beta coefficient (1000 sqm)', '{:.2f}'.format(dados_modelo['beta']/1000))

    df_final = load_df('https://raw.githubusercontent.com/h-pgy/alain_bertaud/streamlit_app/generated_data/df_final.csv')

    predict = lambda x: dados_modelo['alfa'] + dados_modelo['beta']*x
    df_final['predicted'] = df_final['percent_empregos_destino'].apply(predict)
    df_final['abs_error'] = df_final['delta_pde'] - df_final['predicted']
    df_final['abs_error']  = df_final['abs_error'].abs()
    df_final['proportion_error'] = df_final['abs_error']/df_final['delta_pde']
    
    
    fig_modelo = px.scatter(df_final, x="percent_empregos_destino", y="delta_pde", 
                            hover_data=['ds_nome', 'predicted', 'abs_error'], 
                            title='Vertical Housing Growth vs. Access to Job Market',
                            trendline="ols", trendline_color_override='red')
    st.plotly_chart(fig_modelo, use_container_width=True)

    tipo = st.selectbox("Select the map data", options=['Absolute Error', 'Error Proportional to the True Value', 'Predicted value'],
                        index=2)
    fig = gerar_mapa2d_modelo(tipo)
    st.plotly_chart(fig, use_container_width=True)
    st.write(df_final)