import pandas as pd
import requests
import streamlit as st
from PIL import Image
import numpy as np

logo = Image.open('logo.png')

st.set_page_config(
    page_title = 'Find Online Courses of your Choice',
    page_icon = logo,
    layout = 'wide'
)

st.sidebar.title('InsightBig School')
st.sidebar.markdown('Browse various courses from well-known instructors and universities')
st.sidebar.markdown('')

providers_list = ['Udemy', 'edX', 'Coursera']
provider = st.sidebar.selectbox('PROVIDER', providers_list, key = 'providers_selectbox')

if provider == 'Udemy':
    #primary_category_list = ['Business', 'Design', 'Development', 'Finance & Accounting', 'Health & Fitness', 'IT & Software', 'Lifestyle', 'Marketing', 'Music', 'Office Productivity', 'Personal Development', 'Photography & Video', 'Teaching & Academics', 'Udemy Free Resource Center']
    #primary_category = st.sidebar.selectbox('PRIMARY CATEGORY', primary_category_list, key = 'primary_category_list')
    search = st.sidebar.text_input('SEARCH KEY TERM (eg: python, stocks, photoshop)', value = 'Machine Learning', key = 'search_term_input')
    category_list = list(pd.read_csv('udemy_categories.csv')['category'])
    category = st.sidebar.selectbox('CATEGORY', category_list, key = 'category_list')
    pricing = st.sidebar.selectbox('PRICING', ['All', 'Free', 'Paid'], key = 'pricing_list')
    level = st.sidebar.selectbox('LEVEL', ['All', 'Intermediate', 'Expert', 'Beginner'], key = 'level_list')
    order = st.sidebar.selectbox('SORT BY', ['Relevance', 'Most Viewed', 'Highest Rated', 'Newest'], key = 'sort_list')
    duration = st.sidebar.selectbox('DURATION', ['All', 'Medium', 'Long', 'Extra Long', 'Short'], key = 'duration_list')
    
    headers = {
  "Accept": "application/json, text/plain, */*",
  "Authorization": f"{secrets.UDEMY_AUTH}",
  "Content-Type": "application/json;charset=utf-8"}
    
    base_url = 'https://www.udemy.com/api-2.0/courses/?page=1&page_size=1000'
    search_url = base_url + f'&search={search}'
    if category.find('and') > 0:
        category = category.replace('and', '%26')
    else:
        pass
    category_url = search_url + f'&subcategory={category}'
    
    if pricing == 'Paid':
        pricing_url = category_url + '&price=price-paid'
    elif pricing == 'Free':
        pricing_url = category_url + '&price=price-free'
    elif pricing == 'All':
        pricing_url = category_url
    
    if level == 'All':
        level_url = pricing_url + '&instructional_level=all'
    elif level == 'Intermediate':
        level_url = pricing_url + '&instructional_level=intermediate'
    elif level == 'Expert':
        level_url = pricing_url + '&instructional_level=expert'
    elif level == 'Beginner':
        level_url = pricing_url + '&instructional_level=beginner'
        
    if order == 'Relevance':
        order_url = level_url + '&ordering=relevance'
    elif order == 'Most Viewed':
        order_url = level_url + '&ordering=most-viewed'
    elif order == 'Highest Rated':
        order_url = level_url + '&ordering=highest-rated'
    elif order == 'Newest':
        order_url = level_url + '&ordering=newest'
        
    if duration == 'All':
        final_url = order_url
    if duration == 'Short':
        final_url = order_url + '&duration=short'
    if duration == 'Medium':
        final_url = order_url + '&duration=medium'
    if duration == 'Long':
        final_url = order_url + '&duration=long'
    if duration == 'Extra Long':
        final_url = order_url + '&duration=extraLong'
    
    if st.sidebar.button('Search'):
        raw = requests.get(final_url, headers = headers).json()
        num = 0
        results = raw['results']
        if len(results) == 0:
            st.subheader('No Courses Found')
        while num < len(results):
            expander_title = results[num]['title'] 
            with st.expander(f'{expander_title}', expanded = True):
                course_image_url = results[num]['image_480x270']
                course_image_file = results[num]['image_480x270'][42:]
                course_image = Image.open(requests.get(results[num]['image_480x270'], stream = True).raw)
                course_title = results[num]['title']
                course_headline = results[num]['headline']
                column1, column2 = st.columns(2)
                column1.image(course_image)
                column2.header(f'{course_title}')
                column2.write(f'{course_headline}')
                if len(results[num]['visible_instructors']) > 1:
                    instructor_name = results[num]['visible_instructors'][1]['display_name']
                else:
                    instructor_name = results[num]['visible_instructors'][0]['display_name']
                column2.markdown(f'**Course Instructor:** {instructor_name}')
                course_price = results[num]['price']
                column2.markdown(f'**Course Price:** {course_price}')
                url = 'https://www.udemy.com' + results[num]['url']
                column2.markdown('**[View Course on Udemy >](%s)**' % url)
                st.markdown('')
                num += 1
    else:
        st.info('Hit the Search button at the bottom right corner to view courses matching your criteria')
        
elif provider == 'edX':
    edx = pd.read_csv('edx_courses.csv')
    try:
        edx = edx.drop('Unnamed: 0', axis = 1)
    except:
        pass
    
    subjects_list = list(edx['subject'].unique())
    subject = st.sidebar.selectbox('SUBJECT', subjects_list, key = 'edx_subject_selectbox')
    
    course_length_list = list(edx['course_length'].unique())
    course_length = st.sidebar.selectbox('COURSE LENGTH', course_length_list, key = 'edx_courselength_selectbox')
    
    course_type_expander = st.sidebar.expander('COURSE TYPE', expanded = True)
    course_type_expander.markdown('')
    course_type = course_type_expander.radio('', ('Self-Paced', 'Instructor-Led'), key = 'edx_coursetype_radio')
    course_type_expander.markdown('')
    
    levels_list = ['Introductory', 'Intermediate', 'Advanced']
    course_level_expander = st.sidebar.expander('COURSE LEVEL', expanded = True)
    course_level_expander.markdown('')
    course_level = course_level_expander.radio('', ('Introductory', 'Intermediate', 'Advanced'), key = 'edx_courselevel_radio')
    course_level_expander.markdown('')
    
    course_language_expander = st.sidebar.expander('COURSE LANGUAGE', expanded = True)
    course_language_expander.markdown('')
    course_language = course_language_expander.radio('', ('English', 'Español'), key = 'edx_language_radio')
    course_language_expander.markdown('')
        
    if st.sidebar.button('Search', key = 'edx_search_button'):
        edx_results = edx[(edx.subject == f'{subject}') & (edx.course_length == f'{course_length}') & (edx.course_type == f'{course_type}') & (edx.Level == f'{course_level}') & (edx.language == f'{course_language}')]
        if len(edx_results) == 0:
            st.warning('No courses matched your criteria')
            st.subheader(f'All courses on {subject}')
            edx_results = edx[edx.subject == f'{subject}'].reset_index()
            num = 0
            while num < len(edx_results):
                expander_title = edx_results.loc[num]['title']
                with st.expander(f'{expander_title}', expanded = True):
                    column1, column2, column3 = st.columns([2,1,1])
                    course_title = edx_results.title.loc[num]
                    column1.header(course_title)
                    course_summary = edx_results.summary.loc[num]
                    column1.markdown(course_summary)
                    column2.markdown(f'**Institution:** {edx_results.institution.loc[num]}')
                    column3.markdown(f'**Course Price:** {edx_results.price.loc[num]}')
                    column2.markdown(f'**Course Type:** {edx_results.course_type.loc[num]}')
                    column3.markdown(f'**No. of Enrolled Students:** {edx_results.n_enrolled.loc[num]}')
                    column2.markdown(f'**Instructors:** {edx_results.instructors.loc[num]}')
                    column3.markdown(f'**Course Level:** {edx_results.Level.loc[num]}')
                    column2.markdown(f'**Course Length:** {edx_results.course_length.loc[num]}')
                    column3.markdown(f'**Course Effort:** {edx_results.course_effort.loc[num]}')
                    column2.markdown(f'**Course Language:** {edx_results.language.loc[num]}')
                    num += 1
        else:
            edx_results = edx_results.reset_index()
            num = 0
            while num < len(edx_results):
                expander_title = edx_results.loc[num]['title']
                with st.expander(f'{expander_title}', expanded = True):
                    column1, column2, column3 = st.columns([2,1,1])
                    course_title = edx_results.title.loc[num]
                    column1.header(course_title)
                    course_summary = edx_results.summary.loc[num]
                    column1.markdown(course_summary)
                    column2.markdown(f'**Institution:** {edx_results.institution.loc[num]}')
                    column3.markdown(f'**Course Price:** {edx_results.price.loc[num]}')
                    column2.markdown(f'**Course Type:** {edx_results.course_type.loc[num]}')
                    column3.markdown(f'**No. of Enrolled Students:** {edx_results.n_enrolled.loc[num]}')
                    column2.markdown(f'**Instructors:** {edx_results.instructors.loc[num]}')
                    column3.markdown(f'**Course Level:** {edx_results.Level.loc[num]}')
                    column2.markdown(f'**Course Length:** {edx_results.course_length.loc[num]}')
                    column3.markdown(f'**Course Effort:** {edx_results.course_effort.loc[num]}')
                    column2.markdown(f'**Course Language:** {edx_results.language.loc[num]}')
                    column1.markdown('**[View Course on edX >](%s)**' % edx_results.course_url.loc[num])
                    num += 1
    else:
        st.info('Hit the Search button at the bottom right corner to view courses matching your criteria')
        
elif provider == 'Coursera':
    coursera = pd.read_csv('coursera_courses.csv').dropna()
    
    coursesubject_expander = st.sidebar.expander('PRIMARY COURSE SUBJECT', expanded = True)
    coursesubject_expander.markdown('')
    coursesubject_list = coursera.course_subject.unique()
    course_subject = coursesubject_expander.radio('', (coursesubject_list), key = 'coursera_course_subject_radio')
    coursesubject_expander.markdown('')
    
    secsubject_list = ['All']
    for i in range(len(coursera.course_sec_subject.unique())):
        secsubject_list.append(coursera.course_sec_subject.unique()[i])
    
    coursesecsubject_expander = st.sidebar.expander('SECONDARY COURSE SUBJECT (OPTIONAL)', expanded = False)
    coursesecsubject_expander.markdown('')
    course_secsubject = coursesecsubject_expander.radio('', (secsubject_list), key = 'coursera_secsubject_radio')
    coursesecsubject_expander.markdown('')
            
    courselanguage_expander = st.sidebar.expander('COURSE LANGUAGE', expanded = False)
    courselanguage_expander.markdown('')
    courselanguage_list = coursera.course_language.unique()
    courselanguage_list[0], courselanguage_list[1] = 'English', 'Spanish'
    course_language = courselanguage_expander.radio('', (courselanguage_list), key = 'coursera_course_language_radio')
    courselanguage_expander.markdown('')
    
    if st.sidebar.button('Search', key = 'coursera_search_button'):
        if course_secsubject == 'All':
            coursera_results = coursera[(coursera.course_subject == f'{course_subject}') & (coursera.course_language == f'{course_language}')].reset_index()
        elif course_secsubject != 'All':
            coursera_results = coursera[(coursera.course_subject == f'{course_subject}') & (coursera.course_sec_subject == f'{course_secsubject}') & (coursera.course_language == f'{course_language}')].reset_index()
           
        coursera_results = coursera_results.loc[0:200]
        
        if len(coursera_results) == 0:
            st.warning('No courses matched your criteria')
            st.subheader(f'All courses on {course_subject}')
            col1, col2 = st.columns(2)
            col1.caption('The courses are not ranked but ordered randomly')
            subject_query = course_subject.replace(' ', '-').lower()
            subject_url = f'https://www.coursera.org/browse/{subject_query}'
            col2.markdown(f'**[View {course_subject} on Coursera >](%s)**' % subject_url)
            
            num = 0
            while num < len(coursera_results):
                expander_title = coursera_results.loc[num]['course_title']
                with st.expander(f'{expander_title}', expanded = True):
                        st.title(f'{coursera_results.course_title[num]}')
                        col1, col2, col3 = st.columns(3)
                        col1.markdown(f'**University:** {coursera_results.course_provider[num]}')
                        col2.markdown(f'**Instructor(s):** {coursera_results.course_instructors[num]}')
                        col3.markdown(f'**Duration:** {coursera_results.course_duration[num]}')
                        st.write(f'{coursera_results.course_detail[num]}')
                        foot1, foot2 = st.columns(2)
                        if coursera_results.course_rating[num] != np.nan:
                            foot2.markdown(f'**Course rating: **{coursera_results.course_rating[num]}    ')
                        if coursera_results.course_nenroll[num] != np.nan:
                            foot2.markdown(f'**No.of students enrolled: **{coursera_results.course_nenroll[num]}')
                        foot1.markdown('**[View Course on Coursera >](%s)**' % coursera_results.course_url[num])
                        num += 1
                        
        else:
            st.header(f'{course_subject}')
            st.markdown(f'**{course_secsubject}**')
            st.markdown('')
            col1, col2 = st.columns(2)
            col1.caption('The courses are not ranked but ordered randomly')
            subject_query = course_subject.replace(' ', '-').lower()
            subject_url = f'https://www.coursera.org/browse/{subject_query}'
            col2.markdown(f'**[View {course_subject} on Coursera >](%s)**' % subject_url)
            num = 0
            while num < len(coursera_results):
                expander_title = coursera_results.loc[num]['course_title']
                with st.expander(f'{expander_title}', expanded = True):
                        st.title(f'{coursera_results.course_title[num]}')
                        col1, col2, col3 = st.columns(3)
                        col1.markdown(f'**University:** {coursera_results.course_provider[num]}')
                        col2.markdown(f'**Instructor(s):** {coursera_results.course_instructors[num]}')
                        col3.markdown(f'**Duration:** {coursera_results.course_duration[num]}')
                        st.write(f'{coursera_results.course_detail[num]}')
                        foot1, foot2 = st.columns(2)
                        if coursera_results.course_rating[num] != np.nan:
                            foot2.markdown(f'**Course rating: **{coursera_results.course_rating[num]}    ')
                        if coursera_results.course_nenroll[num] != np.nan:
                            foot2.markdown(f'**No.of students enrolled: **{coursera_results.course_nenroll[num]}')
                        foot1.markdown('**[View Course on Coursera >](%s)**' % coursera_results.course_url[num])
                        num += 1
    else:
        st.info('Hit the Search button at the bottom right corner to view courses matching your criteria')
