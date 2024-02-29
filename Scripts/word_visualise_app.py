import streamlit as st
import pandas as pd
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
from st_material_table import st_material_table
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import numpy as np
import plotly.express as px
import copy
import stylecloud
# import SessionState
from PIL import Image
import time

# state = SessionState.get(position=0)
st.set_page_config(page_title='SciWo Analytics Dashboard', page_icon = "Group-669.ico", layout = 'wide', initial_sidebar_state = 'auto')
# stole from https://github.com/andfanilo/streamlit-echarts/blob/master/streamlit_echarts/frontend/src/utils.js Thanks andfanilo

# [theme]

# primaryColor="#d33682"
# backgroundColor="#002b36"
# secondaryBackgroundColor="#586e75"
# textColor="#fafafa"
# font="sans serif"
st.title('SciWo Analytics Dashboard')
# tab1, tab2= st.tabs(["2018-19 vs. 2020-21", "2019-20 vs. 2021-22"])
tab1, tab2= st.tabs(["SciWo 2022", "SciWo 2023"])


st.set_option('deprecation.showPyplotGlobalUse', False)
start_year = 2018
end_year = 2022
# ngrams = {'uni':(1,1),'bigram':(2,2),'trigram':(3,3)}
ngrams = {'bigram':(2,2),'trigram':(3,3)}


names = []
text_filter_dict = {"Title":{'cols':['Title'],'name':'title'},
               "Abstract":{'cols':['Abstract'],'name':'abstract'},
                "Title + Abstract (TA)":{'cols':['Title','Abstract'],'name':'ta'},
                "TA + Author Keywords (TAA)":{'cols':['Title','Abstract','AuthorKey'],'name':'taa'},
                "TAA + Scopus Keywords":{'cols':['Title','Abstract','AuthorKey','Eng_Controlled','Eng_Unctrolled','Eng_MainHeading'],'name':'taask'},
                "Author Keywords+Scopus Keywords":{'cols':['AuthorKey','Eng_Controlled','Eng_Unctrolled','Eng_MainHeading'],'name':'aksk'}}

# Write a page title



# st.sidebar.subheader('Select to Filter the data')

# st.sidebar.markdown('**Area of Research**')
# filter_method = st.sidebar.radio('Select from following', options=["CS","Mathematical Sciences","Life Sciences"])
# method = "_CountVec_gap_"
# field = ''
# if filter_method =="Mathematical Sciences":
#     field = "_mathScience"

# if filter_method =="Life Sciences":
#     field = "_lifeScience"

# st.sidebar.markdown('**Select Element for Analysis**')
# text_filter = st.sidebar.radio('Select Input Text Type', options=["Title","Abstract","Title + Abstract (TA)","TA + Author Keywords (TAA)","TAA + Scopus Keywords","Author Keywords+Scopus Keywords"])

with tab1:
    text_filter = "TA + Author Keywords (TAA)"

    text_type = text_filter_dict[text_filter]['name']

    # st.sidebar.markdown('**By Year Gap - Starting 2000**')
    # filter_gap = st.sidebar.radio('Filter By Year Gap', options=[1,2,3])
    filter_gap = 2
    names = []
    year = start_year
    while( year<end_year):
        first = year
        last = year+filter_gap
        if last>=end_year:
            last = end_year
        str_ = str(first)+'-'+str(last-1)
        names.append(str_)
        year = last
    print("year range",names)



    st.subheader(" Based on word frequencies in top 30 conferences/journals for each area of study")
    # st.markdown("For each area of study, ScImago's rankings are used to select the top 25-30 journals and conferences. All papers published in these prestigious conferences/journals during the last four years (2018-2021) were used for the study. Based on title, abstract, and author published keywords, the frequency of individual bigrams/trigrams and their ranking over the period of four years was calculated. Phrases with the highest improvement in rank over a window of two years were identified. The jury selected the most appropriate word of the year among these.")
    col1,col2 = st.columns(2)
        
    with col1:
        filter_method = st.selectbox("Area of study", ("Computer Science","Mathematical Sciences","Life Sciences"))
        method = "_CountVec_gap_"
        field = ''
        if filter_method =="Mathematical Sciences":
            field = "_mathScience"

        if filter_method =="Life Sciences":
            field = "_lifeScience"
    with col2:
        filter_bi = st.selectbox("Phrase type",("bigram","trigram"))
        filter_year =names[-1]
    word_ignore = ['cell rna seq','cell rna',"answer question","neural network deep",'cell cell','severe acute respiratory','alzheimers dementia alzheimers','syndrome coronavirus sars','alzheimers alzheimers disease','confidence interval ci','cd cd cell','cd cd','prospective teacher','primary secondary','log log log']
    xlsx = pd.ExcelFile("../Data/Paper_Details/New_Results/"+filter_bi+"_"+text_type+method+str(filter_gap)+field+".xlsx",engine='openpyxl')
    sheet = xlsx.parse(sheet_name=filter_year)
    sheet = sheet[~sheet['term'].isin(word_ignore)]
    sheet.reset_index(drop=True)

    if 'Unnamed: 0' in sheet.columns:
        del sheet['Unnamed: 0']
    sheet.columns =['Word','Frequency']
    dict_ = dict(sheet.values)
    sheet['Rank_New'] = sheet['Frequency'].rank(method='first',ascending = 0)
    sheet.sort_values(by=['Rank_New'],inplace=True)
    sheetNew = copy.deepcopy(sheet)



    sheet_old =pd.DataFrame()
    old =names.index(filter_year)
    if old!=0:
        sheet_old = xlsx.parse(sheet_name=names[old-1])
        if 'Unnamed: 0' in sheet_old.columns:
            del sheet_old['Unnamed: 0']
        sheet_old.columns =['Word','Frequency_old']
        sheet_old['Rank_Old'] = sheet_old['Frequency_old'].rank(method='first',ascending = 0)
        sheet_old.sort_values(by=['Rank_Old'],inplace=True)
        sheet = sheet.merge(sheet_old,on=['Word'],how='left')
        sheet['Rank_Old'] = sheet['Rank_Old'].fillna(1000)
        sheet['Rank Diff'] = sheet['Rank_Old']-sheet['Rank_New']
        del sheet['Frequency_old']
        sheet  = sheet.fillna('')



    st.subheader("Word Cloud")
    # create a mask based on the image we wish to include
    # my_mask = np.array(Image.open('square-solid.svg'))
    wordcloud = WordCloud(background_color="white",collocations=False,  
                width=600,
                height=300,
                contour_width=3,
                contour_color='red')
    title = filter_method +", Year:"+filter_year

    wordcloud.generate_from_frequencies(frequencies=dict_)
    fig = plt.figure(dpi=500,figsize=(10,20))
    plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis('off')
    # plt.show()
    # plt.title(title)
    # st.pyplot(fig)

    stylecloud.gen_stylecloud(text=dict_, 
                            icon_name = "fas fa-cloud",
                            palette="tableau.ColorBlind_10",
                            max_words = 200,
                            size = (1000,600))

    st.image('stylecloud.png',use_column_width=True)


    st.subheader("Word/Phrase Rank Comparisions")
    sheet = sheet.head(n=50)
    sheet.columns = ['Word/Phrase','Frequency','Current Rank (2021-2020)','Previous Rank (2019-2018)','Rank Change (+/-)']
    # sheet = sheet[['Word/Phrase','Rank Change (+/-)','Frequency','Current Rank (2021-2020)','Previous Rank (2019-2018)']]

    sheet['Current Rank (2021-2020)'] = sheet['Current Rank (2021-2020)'].astype('int')
    sheet['Previous Rank (2019-2018)'] = sheet['Previous Rank (2019-2018)'].astype('int')
    sheet['Rank Change (+/-)'] = sheet['Rank Change (+/-)'].astype('int')

    # st.dataframe(sheet)

    gb = GridOptionsBuilder.from_dataframe(sheet)
    #  ">=10 up": "green",
    #                     ">=5 up": "#C9D41A",
    #                     "Small Change": "blue",
    #                     ">=10 drop": "red",
    #                     ">=5 drop":"#23A4B7"}
    cellsytle_jscode = JsCode("""
    function(params) {
    if (params.value >= 10) {
    return {
    'color': 'white',
    'backgroundColor': '#28B463'}
    }
    else if (params.value >= 5) {
    return {
    'color': 'white',
    'backgroundColor': '#F1C40F'}
    }
    else if (params.value <= -10) {
    return {
    'color': 'white',
    'backgroundColor': '#C0392B'}
    }
    else if (params.value <= -5) {
    return {
    'color': 'white',
    'backgroundColor': '#D35400'}
    }
    else if (params.value > -5) {
    return {
    'color': 'white',
    'backgroundColor': '#2980B9'}
    }
    else if (params.value >= 0  ) {
    return {
    'color': 'white',
    'backgroundColor': 'blue'}
    }
    else {
    return {
    'color': 'black',
    'backgroundColor': 'white'}
    }
    };""")

    cellsytle_jscode_word = JsCode("""
    function(params) {
    if (params.value=="graph neural network" ||params.value=="natural language" ||params.value=="knowledge graph" ) {
    return {
    'color': 'white',
    'backgroundColor': 'green'}
    }

    else if(params.value=="local langlands correspondence" || params.value=="navier stokes equation" || params.value=="modular form") {
    return {
    'color': 'white',
    'backgroundColor': 'green'}
    }
    else if(params.value=="rna sequencing" || params.value=="tumor microenvironment" || params.value=="single cell") {
    return {
    'color': 'white',
    'backgroundColor': 'green'}
    }
    };""")

    gb.configure_column("Rank Change (+/-)",cellStyle=cellsytle_jscode)




    # gb.configure_pagination()
    gb.configure_column("Word/Phrase", cellStyle={'color': 'black'})
    gb.configure_column("Word/Phrase", cellStyle=cellsytle_jscode_word) 

    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=False)
    gridOptions = gb.build()
    AgGrid(sheet,gridOptions=gridOptions,allow_unsafe_jscode=True,fit_columns_on_grid_load=True,
        theme='streamlit',width="50%",enable_enterprise_modules=True)
    st.caption("<b>Note:</b> It should be noted that phrases that haven't appeared previously have been reranked from <b>Inf</b> to <b>1000</b> for visual purposes.",unsafe_allow_html=True)
    st.subheader("Ranking Visualisation")

    sheet_old2 =pd.DataFrame()
    if old!=0:
        print("old!=0",old)
        sheet_old2 = xlsx.parse(sheet_name=names[old-1])
        if 'Unnamed: 0' in sheet_old2.columns:
            del sheet_old2['Unnamed: 0']
        sheet_old2.columns =['Word','Frequency_old']
        
        sheet_old2['Rank_Old'] = sheet_old2['Frequency_old'].rank(method='first',ascending = 0)
        
        sheet_old2.sort_values(by=['Rank_Old'],inplace=True)
        sheetNew = sheetNew.merge(sheet_old,on=['Word'],how='left')
        sheetNew['Frequency_old'] = sheetNew['Frequency_old'].fillna(0)
        sheetNew['Rank_Old'] = sheetNew['Rank_Old'].fillna(1000)
        sheetNew['Rank Diff'] = sheetNew['Rank_Old']-sheetNew['Rank_New']


    top_50 = sheetNew.head(n=50)
    top_50['Rank_New'] = top_50['Rank_New'].astype('int')
    top_50['Rank_Old'] = top_50['Rank_Old'].astype('int')
    top_50['Rank Diff'] = top_50['Rank Diff'].astype('int')
    col1,col2,col3 = st.columns(3)
        
    with col1:
        values_current = st.slider('Current Rank (2021-2020)',0, 50, (0, 50),key="rank_new")
    with col2: 
        values_prev = st.slider(
        'Previous Rank (2019-2018)',0, int(top_50['Rank_Old'].max()), (0, 50),key="rank_old")

    top_50.sort_values(by=['Rank_New'],ascending=False,inplace=True)
    top_50['Bins'] = ''
    for index, row in top_50.iterrows():
        rank_diff = row['Rank Diff']
        if rank_diff >=10:
            top_50['Bins'][index] = ">=10 up"
        elif rank_diff >=5:
            top_50['Bins'][index] = ">=5 up"
        elif rank_diff >=0:
            top_50['Bins'][index] = "Small Change"
        elif rank_diff<=-10:
            top_50['Bins'][index] = ">=10 drop"
        elif rank_diff <=-5:
            top_50['Bins'][index] = ">=5 drop"
        elif rank_diff <0:
            top_50['Bins'][index] = "Small Change"

    # top = top_50[top_50['Rank_Old']<=50]

    top = top_50[top_50['Rank_Old'].between(values_prev[0], values_prev[1])]
    top = top[top['Rank_New'].between(values_current[0], values_current[1])]


    with col3: 
        values_diff = st.slider(
        'Rank Improvement',
        int(top_50['Rank Diff'].min()), int(top_50['Rank Diff'].max()),(int(top['Rank Diff'].min()), int(top['Rank Diff'].max())),key="rank_diff")

    top = top[top['Rank Diff'].between(values_diff[0], values_diff[1])]
    # with col4:
    #     # top = top[top['Rank Diff'].between(values_diff[0], values_diff[1])]

    #     st.button("Update PloSt")# on_click=_update_slider, kwargs={"new value": random.randint(-100, 100)})

    # if st.button("Update Plot"):
    #     if "rank_new" in st.session_state:
    #         st.write("mauz")
    #         top = top_50[top_50['Rank_New'].between(values_current[0], values_current[1])]
    #         new_Cmin = top['Rank_Old'].min()
    #         new_Cmax = top['Rank_Old'].max()
    #         # top = top[top['Rank_New'].between(values_current[0], values_current[1])]
    #         # st.session_state["rank_old"] = (new_Cmin,new_Cmax)
    #         st.write(new_Cmin,new_Cmax)

    print(set(top['Bins']))
    top = top.sort_values(by=['Bins'])
    fig1 = px.scatter(top, x="Rank_Old", y="Rank_New",size="Frequency",
                        size_max=10,text = "Word",color=top['Bins'],opacity = 0.001,
                        color_discrete_sequence=px.colors.qualitative.Dark24,
                        color_discrete_map={
                        ">=10 up": "green",
                        ">=5 up": "#C9D41A",
                        "Small Change": "blue",
                        ">=10 drop": "red",
                        ">=5 drop":"#23A4B7"},
                        hover_data=['Word','Frequency','Rank_New','Rank_Old'],
                        # range_x=[0,300],
                        # animation_frame="Rank_New", animation_group="Word",
                        labels={
                            "Rank_Old": "Previous Rank (2019-2018)",
                            "Rank_New": "Current Rank (2021-2020)",
                        "Bins": " Rank Imprv"

                        },
                    title="Word/Phrase Ranking (2021-2020 vs. 2019-2018) - "+filter_method+" ("+filter_bi+")"
                        )
    fig1.update_layout(
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 10,
            nticks = 10,

        ),
        width=1400,
        plot_bgcolor='rgba(0,0,0,0)',
        height=800,
        
        legend={'traceorder':'normal'}
        # plot_bgcolor = '#DCDCDC'
    )
    fig1.update_yaxes(automargin=False)
    fig1.for_each_trace(lambda t: t.update(textfont_color=t.marker.color))
    # fig1.for_each_trace(lambda t: t.update(textfont_size=(t.marker.size/(t.marker.sizeref*2.5))))
    fig1.update_xaxes( gridcolor='#F0F0F0',zeroline=True, zerolinewidth=1, zerolinecolor='#F0F0F0')
    fig1.update_yaxes( gridcolor='#F0F0F0',zeroline=True, zerolinewidth=1, zerolinecolor='#F0F0F0')
    # fig1["layout"].pop("updatemenus")
    #         fig1.update_traces(textposition='middle left')
    #         fig1.update_layout(xaxis_range=[-10,65])

    # st.write(str(fig1))
    st.plotly_chart(fig1, use_container_width=True, sharing="streamlit")
    

    

    #     bar_width = 0.35
    #     labels, values = zip(*dict_.items())
    #     # sort your values in descending order
    #     indSort = np.argsort(values)[::-1]

    # rearrange your data
    #     labels = np.array(labels)[indSort]
    #     values = np.array(values)[indSort]

    #     indexes = np.arange(len(labels))
    # #     plt.xticks(indexes + bar_width, labels)
    #     plt.bar(values,indexes)
    # st.pyplot(fig2,use_column_width=True)


with tab2:
    image = Image.open('wip.webp')
    st.markdown('Our team is working to bring up the our latest dashboard for SciWo 2023. Visit [Sciwo Home](https://www.indiasciencefest.org/sciwo/)')
    st.image(image, caption='Our team is working to bring up the our latest dashboard for SciWo2023.',use_column_width='always')
    





