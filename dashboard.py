import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# st.set_page_config(layout='wide')

st.title("HR Dashboard")
st.write("### SNK Grade 1 to 8 - HD - All Staff Members")

conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(worksheet="master_2")
data2 = conn.read(worksheet="classwise")

df = pd.DataFrame(data)
dashboard_data = df[df['Placement Chart Category'] != 'Resigned']

df2 = pd.DataFrame(data2)

academic_employees = dashboard_data['Category'].value_counts()['Academic']
nonacademic_employees = dashboard_data['Category'].value_counts()['Non-Academic']
cocurricular_employees = dashboard_data['Category'].value_counts()['Co-Curricular']
total_employees = academic_employees+cocurricular_employees+nonacademic_employees

female = dashboard_data['Gender'].value_counts()['Female']
male = dashboard_data['Gender'].value_counts()['Male']

academic = df[(df['Placement Chart Category'] != 'Resigned') & (df['Category'] == 'Academic')]
nonacademic = df[(df['Placement Chart Category'] != 'Resigned') & (df['Category'] == 'Non-Academic')]
cocurricular = df[(df['Placement Chart Category'] != 'Resigned') & (df['Category'] == 'Co-Curricular')]

bed = academic['Teaching Qualification'].value_counts()['B.Ed']
pursuing_bed = academic['Teaching Qualification'].value_counts()['Pursuing']
non_bed = academic['Teaching Qualification'].value_counts()['Non B.Ed']

new_joinee_list = academic[academic['Placement Chart Category'] == 'New Joinee']['Name'].to_list()
serving_notice_list = academic[academic['Placement Chart Category'] == 'Serving Notice']['Name'].to_list()
planning_resign_list = academic[academic['Placement Chart Category'] == 'Planning to Resign']['Name'].to_list()

staff_movement = df['Placement Chart Category'].value_counts().to_dict()
new_joinee = staff_movement.get('New Joinee',0)
serving_notice = staff_movement.get('Serving Notice',0)
planning_resign = staff_movement.get('Planning to Resign',0)
resigned = staff_movement.get('Resigned',0)

retiree = df[df['Age as on 31-May-2024'] >= 58]
retiree_category = retiree['Category'].value_counts().to_dict()
retiree_academic = retiree_category.get('Academic',0)
retiree_nonacademic = retiree_category.get('Non-Academic',0)
retiree_cocurricular = retiree_category.get('Co-Curricular',0)

vacancy_count = df2[df2['Type'] == 'Vacancy'].groupby(['School','Grade','Subject'],as_index=False).nunique()
vacancy_count.drop(columns=['Section','GS','Name'], inplace=True)
vacancy_count.rename(columns={'Type': 'Vacancies'}, inplace=True)
vacancy_schoolwise = vacancy_count['School'].value_counts().to_dict()
vacancy_s1 = vacancy_schoolwise.get('School 1',0)
vacancy_s2 = vacancy_schoolwise.get('School 2',0)
vacancy_s3 = vacancy_schoolwise.get('School 3',0)

st.subheader("Staff Overview")
st.write("#### Head Count")

tab_so1, tab_so2 = st.tabs(['Summary', 'Details'])

with tab_so1:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total", total_employees)
    col2.metric("Academic", academic_employees)
    col3.metric("Non-Academic", nonacademic_employees)
    col4.metric("Co-Curricular", cocurricular_employees)

with tab_so2:
    select_headcount = st.multiselect('Select Staff Member Category (Multiselect)',dashboard_data['Category'].dropna().unique(),dashboard_data['Category'].dropna().unique())
    st.dataframe(dashboard_data[dashboard_data['Category'].isin(select_headcount)][['User ID','Name','Category','School','Unit / Department','Co-ordinator/Leader','Senior HR']], hide_index=True)

"---"
st.write("#### Staff Transitions")
tab_st1, tab_st2 = st.tabs(['Summary','Details'])

with tab_st1:
    col_st1, col_st2, col_st3, col_st4 = st.columns(4)

    col_st1.metric("New Joinee", new_joinee)
    col_st2.metric("Serving Notice", serving_notice)
    col_st3.metric("Planning to Resign", planning_resign)
    col_st4.metric("Resigned", resigned)

with tab_st2:
    select_placement = st.multiselect('Select Placement(s) Chart Category (Multiselect)',df['Placement Chart Category'].dropna().unique(),df['Placement Chart Category'].dropna().unique())
    st.dataframe(df[df['Placement Chart Category'].isin(select_placement)][['User ID','Name','Placement Chart Category','Category','School','Unit / Department','Co-ordinator/Leader','Senior HR']], hide_index=True)

"---"
st.write("#### Open Positions")
tab_o1, tab_o2 = st.tabs(['Summary', 'Details'])

with tab_o1:
    col_op1, col_op2, col_op3, col_op4 = st.columns(4)

    col_op1.metric("Total Vacancies", len(vacancy_count['School']))
    col_op2.metric("School 1", vacancy_s1)
    col_op3.metric("School 2", vacancy_s2)
    col_op4.metric("School 3", vacancy_s3)

with tab_o2:
    st.dataframe(vacancy_count[['School','Grade','Subject','Vacancies']], hide_index=True)

"---"
st.write("#### Retirements")
st.write("As on 31-May-2024")
tab_r1, tab_r2 = st.tabs(['Summary', 'Details'])

with tab_r1:
    col_r1, col_r2, col_r3, col_r4 = st.columns(4)

    col_r1.metric("Total Retirements", retiree.count()['Name'])
    col_r2.metric("Academic", retiree_academic)
    col_r3.metric("Non-Academic", retiree_nonacademic)
    col_r4.metric("Co-Curricular", retiree_cocurricular)

with tab_r2:
    st.dataframe(retiree[['User ID','Name','Category','School','Unit / Department','DoB','Age as on 31-May-2024','Co-ordinator/Leader','Senior HR']], hide_index=True)

"---"
st.write("#### Teaching Qualification")
tab_tq1, tab_tq2 = st.tabs(['Summary', 'Details'])

with tab_tq1:
    col_tq1, col_tq2, col_tq3, col_tq4 = st.columns(4)

    col_tq1.metric("Total Academic Staff", academic_employees)
    col_tq2.metric("B.Ed", bed)
    col_tq3.metric("Pursuing B.Ed", pursuing_bed)
    col_tq4.metric("Non B.Ed", non_bed)

with tab_tq2:
    select_qualification = st.multiselect('Select Education Qualification (Multiselect) - Only Academic Category Staff Members',academic['Teaching Qualification'].dropna().unique(),academic['Teaching Qualification'].dropna().unique())
    st.dataframe(academic[academic['Teaching Qualification'].isin(select_qualification)][['User ID','Name','Teaching Qualification','Category','School','Unit / Department','Co-ordinator/Leader','Senior HR']], hide_index=True)  
"---"

st.subheader("Gender Compostion")
tab1, tab2 = st.tabs(['All', 'Categories'])

with tab1:
    st.write("All Categories (Academic, Non-Academic, Co-Curricular)")
    all_chart = px.pie(dashboard_data, values=dashboard_data['Gender'].value_counts(), names=dashboard_data['Gender'].value_counts().index, title='All Categories', color = ['Male', 'Female'], color_discrete_map={'Male':'#636EFA','Female':'#19D3F3'})
    all_chart.update_layout(title_x=0.35)
    st.plotly_chart(all_chart, use_container_width=True)

with tab2:
    st.write("Category Wise")
    col5, col6, col7 = st.columns(3)

    with col5:
        academic_chart = px.pie(academic, values=academic['Gender'].value_counts(), names=academic['Gender'].value_counts().index, title='Academic', color = ['Male', 'Female'], color_discrete_map={'Male':'slateblue','Female':'lightskyblue'})
        academic_chart.update_layout(showlegend=False, title_x=0.35)
        st.plotly_chart(academic_chart, use_container_width=True)

    with col6:
        nonacademic_chart = px.pie(nonacademic, values=nonacademic['Gender'].value_counts(), names=nonacademic['Gender'].value_counts().index, title='Non-Academic', color = ['Male', 'Female'], color_discrete_map={'Male':'slateblue','Female':'lightskyblue'})
        nonacademic_chart.update_layout(showlegend=True, title_x=0.25)
        nonacademic_chart.update_layout(legend=dict(yanchor="bottom",y=-0.1,xanchor="left",x=0.3))
        st.plotly_chart(nonacademic_chart, use_container_width=True)

    with col7:
        cocurricular_chart = px.pie(cocurricular, values=cocurricular['Gender'].value_counts(), names=cocurricular['Gender'].value_counts().index, title='Co-Curricular', color = ['Male', 'Female'], color_discrete_map={'Male':'slateblue','Female':'lightskyblue'})
        cocurricular_chart.update_layout(showlegend=False, title_x=0.25)
        st.plotly_chart(cocurricular_chart, use_container_width=True)

"---"
st.subheader("Age Distribution")

age_chart = px.histogram(dashboard_data,x='Age as on 31-May-2024')
age_chart.update_layout(bargap=0.1)
st.plotly_chart(age_chart)

"---"
st.subheader("Association Distribution")

asso_chart = px.histogram(dashboard_data,x='Association as on 31-May-2024')
asso_chart.update_layout(bargap=0.1)
st.plotly_chart(asso_chart)

"---"
st.subheader("Placement Chart")

select_school = st.selectbox('Select School', ['School 1', 'School 2', 'School 3'], index=1)

st.write("#### Placement Chart - ",select_school)

s2_g1 = data2[(data2['School'] == select_school) & (data2['Grade'] == 1)]
s2_g2 = data2[(data2['School'] == select_school) & (data2['Grade'] == 2)]
s2_g3 = data2[(data2['School'] == select_school) & (data2['Grade'] == 3)]
s2_g4 = data2[(data2['School'] == select_school) & (data2['Grade'] == 4)]
s2_g5 = data2[(data2['School'] == select_school) & (data2['Grade'] == 5)]
s2_g6 = data2[(data2['School'] == select_school) & (data2['Grade'] == 6)]
s2_g7 = data2[(data2['School'] == select_school) & (data2['Grade'] == 7)]
s2_g8 = data2[(data2['School'] == select_school) & (data2['Grade'] == 8)]

pivot_s2_g1 = s2_g1.pivot_table(index=['GS'], columns=['Subject'], values=['Name'],
                          aggfunc=lambda x: ''.join(str(v) for v in x)).reset_index()
pivot_s2_g2 = s2_g2.pivot_table(index=['GS'], columns=['Subject'], values=['Name'],
                          aggfunc=lambda x: ''.join(str(v) for v in x)).reset_index()
pivot_s2_g3 = s2_g3.pivot_table(index=['GS'], columns=['Subject'], values=['Name'],
                          aggfunc=lambda x: ''.join(str(v) for v in x)).reset_index()
pivot_s2_g4 = s2_g4.pivot_table(index=['GS'], columns=['Subject'], values=['Name'],
                          aggfunc=lambda x: ''.join(str(v) for v in x)).reset_index()
pivot_s2_g5 = s2_g5.pivot_table(index=['GS'], columns=['Subject'], values=['Name'],
                          aggfunc=lambda x: ''.join(str(v) for v in x)).reset_index()
pivot_s2_g6 = s2_g6.pivot_table(index=['GS'], columns=['Subject'], values=['Name'],
                          aggfunc=lambda x: ''.join(str(v) for v in x)).reset_index()
pivot_s2_g7 = s2_g7.pivot_table(index=['GS'], columns=['Subject'], values=['Name'],
                          aggfunc=lambda x: ''.join(str(v) for v in x)).reset_index()
pivot_s2_g8 = s2_g8.pivot_table(index=['GS'], columns=['Subject'], values=['Name'],
                          aggfunc=lambda x: ''.join(str(v) for v in x)).reset_index()

pivot_s2_g1.columns = ['GS'] + [item[1] for item in pivot_s2_g1.columns[1:]]
pivot_s2_g2.columns = ['GS'] + [item[1] for item in pivot_s2_g2.columns[1:]]
pivot_s2_g3.columns = ['GS'] + [item[1] for item in pivot_s2_g3.columns[1:]]
pivot_s2_g4.columns = ['GS'] + [item[1] for item in pivot_s2_g4.columns[1:]]
pivot_s2_g5.columns = ['GS'] + [item[1] for item in pivot_s2_g5.columns[1:]]
pivot_s2_g6.columns = ['GS'] + [item[1] for item in pivot_s2_g6.columns[1:]]
pivot_s2_g7.columns = ['GS'] + [item[1] for item in pivot_s2_g7.columns[1:]]
pivot_s2_g8.columns = ['GS'] + [item[1] for item in pivot_s2_g8.columns[1:]]

pivot_s2_g1.replace('nan','Vacancy', inplace=True)
pivot_s2_g2.replace('nan','Vacancy', inplace=True)
pivot_s2_g3.replace('nan','Vacancy', inplace=True)
pivot_s2_g4.replace('nan','Vacancy', inplace=True)
pivot_s2_g5.replace('nan','Vacancy', inplace=True)
pivot_s2_g6.replace('nan','Vacancy', inplace=True)
pivot_s2_g7.replace('nan','Vacancy', inplace=True)
pivot_s2_g8.replace('nan','Vacancy', inplace=True)


# def highlight_status(val):
#     if val == 'Vacancy':
#         return 'background-color: red'
#     elif val == 'Filled':
#         return 'background-color: blue'
#     else:
#         return ''
def newjoinee(val, new_joinee_list):
    return val in new_joinee_list

def serving_notice(val, serving_notice_list):
    return val in serving_notice_list

def serving_notice(val, serving_notice_list):
    return val in serving_notice_list

def planning_resign(val, planning_resign_list):
    return val in planning_resign_list


def highlight_pc_category(val):
    if val == 'Vacancy':
        return 'background-color: royalblue'
    elif val == 'New Joinee':
        return 'background-color: lightseagreen'
    elif val == 'Serving Notice':
        return 'background-color: crimson'
    elif val == 'Planning to Resign':
        return 'background-color: lightgrey'
    elif newjoinee(val, new_joinee_list):
        return 'background-color: lightseagreen'
    elif serving_notice(val, serving_notice_list):
        return 'background-color: crimson'
    elif planning_resign(val, planning_resign_list):
        return 'background-color: lightgrey'
    else:
        return ''

styled_df_g1 = pivot_s2_g1.copy().style.applymap(highlight_pc_category).hide(axis='index')
styled_df_g2 = pivot_s2_g2.copy().style.applymap(highlight_pc_category).hide(axis='index')
styled_df_g3 = pivot_s2_g3.copy().style.applymap(highlight_pc_category).hide(axis='index')
styled_df_g4 = pivot_s2_g4.copy().style.applymap(highlight_pc_category).hide(axis='index')
styled_df_g5 = pivot_s2_g5.copy().style.applymap(highlight_pc_category).hide(axis='index')
styled_df_g6 = pivot_s2_g6.copy().style.applymap(highlight_pc_category).hide(axis='index')
styled_df_g7 = pivot_s2_g7.copy().style.applymap(highlight_pc_category).hide(axis='index')
styled_df_g8 = pivot_s2_g8.copy().style.applymap(highlight_pc_category).hide(axis='index')

legend_data = [['Vacancy', 'New Joinee', 'Serving Notice', 'Planning to Resign']]
legend_data_table = pd.DataFrame(legend_data, columns=['1','2','3','4'])
styled_legend_data_table = legend_data_table.copy().style.applymap(highlight_pc_category).hide(axis='index')

st.write("###### Key")
st.write(styled_legend_data_table.to_html(), unsafe_allow_html=True)

st.write("#### Grade 1")
# st.dataframe(pivot_s2_g1, hide_index=True)
# table1 = pivot_s2_g1.copy().style.hide_index()
# st.write(table1.to_html(), unsafe_allow_html=True)
st.write(styled_df_g1.to_html(), unsafe_allow_html=True)

st.write("#### Grade 2")
# table2 = pivot_s2_g2.copy().style.hide_index()
# st.write(table2.to_html(), unsafe_allow_html=True)
st.write(styled_df_g2.to_html(), unsafe_allow_html=True)

st.write("#### Grade 3")
# table3 = pivot_s2_g3.copy().style.hide_index()
# st.write(table3.to_html(), unsafe_allow_html=True)
st.write(styled_df_g3.to_html(), unsafe_allow_html=True)

st.write("#### Grade 4")
# table4 = pivot_s2_g4.copy().style.hide_index()
# st.write(table4.to_html(), unsafe_allow_html=True)
st.write(styled_df_g4.to_html(), unsafe_allow_html=True)

st.write("#### Grade 5")
# table5 = pivot_s2_g5.copy().style.hide_index()
# st.write(table5.to_html(), unsafe_allow_html=True)
st.write(styled_df_g5.to_html(), unsafe_allow_html=True)

st.write("#### Grade 6")
# table6 = pivot_s2_g6.copy().style.hide_index()
# st.write(table6.to_html(), unsafe_allow_html=True)
st.write(styled_df_g6.to_html(), unsafe_allow_html=True)

st.write("#### Grade 7")
# table7 = pivot_s2_g7.copy().style.hide_index()
# st.write(table7.to_html(), unsafe_allow_html=True)
st.write(styled_df_g7.to_html(), unsafe_allow_html=True)

st.write("#### Grade 8")
# table8 = pivot_s2_g8.copy().style.hide_index()
# st.write(table8.to_html(), unsafe_allow_html=True)
st.write(styled_df_g8.to_html(), unsafe_allow_html=True)
