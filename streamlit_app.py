import streamlit as st
import pydeck as pdk
import pandas as pd
import requests
import plotly.express as px
import  streamlit_toggle as st_toggle

with st.sidebar:
    st.image('https://observasampa.prefeitura.sp.gov.br/assets/img/logo.png')
    text = """
    ## Dashboard Adensamento Construtivo
    ### Cidade de São Paulo - 1995 a 2022
    Este aplicativo, a partir da análise da base de dados do **IPTU** para os anos de 1995 a 2022, permite visualizar o adensamento construtivo da cidade de São Paulo neste período. O adensamento é calculado a partir da somatória da área construída por lote para cada setor da cidade, para cada ano.
    """
    st.markdown(text)

    st.markdown('#### **Desenvolvido por**: Henrique Pougy')
    col1, col2 = st.columns([0.5, 3])

    with col1:
        st.image('https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg', use_column_width=True)
    with col2:
        st.markdown('[linkedin](https://www.linkedin.com/in/henrique-pougy-8a008759?originalSubdomain=br)')

st.title('Adensamento Construtivo na Cidade de São Paulo', anchor=None)


tab1, tab2, tab3, tab4 = st.tabs(["Delta", "Commutes", "Jobs", "Statistical Model"])

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

    tooltip = {"html": "<b>Value per Square Meter:</b> {ds_nome} <br>"}

    r = pdk.Deck(
        layer,
        initial_view_state=view_state,
        map_style=pdk.map_styles.DARK,
        tooltip=tooltip
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

    #tem que atualizar o link do ngrok
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

with tab1:

    toggle1 = st_toggle.st_toggle_switch(label="Switch to 2D map", 
                        key="2D_tab1", 
                        default_value=False, 
                        label_after = False, 
                        inactive_color = '#D3D3D3', 
                        active_color="#11567f", 
                        track_color="#29B5E8"
                        )

    tipo = st.radio("Selecione o ano:", [2013, 2023, 'delta'])

    if not toggle1:

        r = gerar_mapa_delta(tipo=tipo)

        st.pydeck_chart(r)

    else:
        fig = gerar_mapa2d_delta(tipo=tipo)
        st.plotly_chart(fig, use_container_width=True)

with tab2:

    toggle2 = st_toggle.st_toggle_switch(label="Switch to 2D map", 
                        key="2D_tab2", 
                        default_value=False, 
                        label_after = False, 
                        inactive_color = '#D3D3D3', 
                        active_color="#11567f", 
                        track_color="#29B5E8"
                        )

    if not toggle2:

        data_url = 'https://raw.githubusercontent.com/h-pgy/alain_bertaud/streamlit_app/geojsons/commute_times.geojson'
        multipli_altura=100
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

    toggle3 = st_toggle.st_toggle_switch(label="Switch to 2D map", 
                        key="2D_tab3", 
                        default_value=False, 
                        label_after = False, 
                        inactive_color = '#D3D3D3', 
                        active_color="#11567f", 
                        track_color="#29B5E8"
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

    pass