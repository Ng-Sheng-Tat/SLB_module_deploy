# streamlit run .\pythonname.py
import streamlit as st
from time import sleep
import plotly.graph_objs as go
from PIL import Image 
import numpy as np
import pandas as pd
import base64

def computation_function():
    sleep(3)
    
@st.cache_data
def read_img(imagein):
    return Image.open(imagein)

@st.cache_data
def plot_on_image(img, width_, height_):
    fig = go.Figure()
    # fig.add_trace(go.Image(z=img))
    # img = Image.fromarray(img.astype('uint8'), 'RGB')
    file_content = img.getvalue()
    base64_content = base64.b64encode(file_content).decode("utf-8")
    data_uri = f"data:{img.type};base64,{base64_content}"
    fig.add_layout_image(
        dict(
            source=data_uri,
            xref="x",
            yref="y",
            x=0,
            y=height_,
            sizex=width_,
            sizey=height_,
            sizing="contain",
            opacity=1,
            layer="below")
    )
    fig.add_trace(
        go.Scatter(x=np.linspace(0, width_, 3), y=np.linspace(0, height_, 3),  
                   mode='lines',line=dict(color='rgba(0,0,0,0)'))
        )
    fig.update_layout(height = 2/3*height_, width = 2/3*width_,xaxis = {'showgrid': False}, yaxis = {'showgrid': False}, 
                    plot_bgcolor='rgba(255,255,255,0)' )
    # paper_bgcolor='rgba(255,255,255,0)', 
    fig.update_yaxes(scaleanchor = 'x', scaleratio = 1)
    return fig

def predict(parameters):
    pass

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

@st.cache_data
def show_img(figurelist):
    imgrow1 = st.columns(3)
    imgrow2 = st.columns(3)
    imgrow3 = st.columns(3)

    imgrow1[0].image(figurelist[0], use_column_width = True)
    imgrow1[1].image(figurelist[1], use_column_width = True)
    imgrow1[2].image(figurelist[2], use_column_width = True)
    imgrow2[0].image(figurelist[3], use_column_width = True)
    imgrow2[1].image(figurelist[4], use_column_width = True)
    imgrow2[2].image(figurelist[5], use_column_width = True)
    imgrow3[0].image(figurelist[6], use_column_width = True)
    imgrow3[1].image(figurelist[7], use_column_width = True)
    imgrow3[2].image(figurelist[8], use_column_width = True)

def main():
    st.set_page_config(layout="wide",page_title="Curve Digitalization",page_icon="📈",)
    st.session_state
    st.markdown("<h1 style='text-align: center;'>Line Curve Digitalization</h1>", unsafe_allow_html=True)
    st.write("Vs code is here")
    st.write("I have made some changes can you capture it")
    desc, input_, output_ = st.tabs(["Description", "Input", "Output"])
    css = """
        <style>
        input[type="number"] {
            text-align: center;
        }
        </style>
        """
        # Render the custom CSS
    st.markdown(css, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'> <strong>Input<strong> </h2>", unsafe_allow_html=True)
        with st.spinner("Running 'Input Panel'"):
            x_sidebar_columns = st.columns([1,2.5,1,2.5])
            x_sidebar_columns[0].markdown("<p style='text-align: center;'> x-min: </p>", unsafe_allow_html=True)
            x_sidebar_columns[1].number_input("x-min", min_value=0, value=0, step=1, label_visibility = "collapsed", key = 'x_min')
            x_sidebar_columns[2].markdown("<p style='text-align: center;'> x-min: </p>", unsafe_allow_html=True)
            x_sidebar_columns[3].number_input("x-max", min_value = st.session_state["x_min"], value = 30, step = 1, label_visibility = "collapsed", key = 'x_max')
            ymin_sidebar_columns = st.columns([1,2.5,1,2.5])
            ymin_sidebar_columns[0].markdown("<p style='text-align: center;'> y-min: </p>", unsafe_allow_html=True, )
            ymin_sidebar_columns[1].number_input("y-min", min_value=0, value =1, step = 1, label_visibility = "collapsed", key = 'ymin1')
            ymin_sidebar_columns[2].markdown("<p style='text-align: center;'> x 10^ </p>", unsafe_allow_html=True)
            ymin_sidebar_columns[3].number_input("y-min-pow", step = 1, label_visibility = "collapsed", key = 'ymin2')
            ymax_sidebar_columns = st.columns([1,2.5,1,2.5])
            ymax_sidebar_columns[0].markdown("<p style='text-align: center;'> y-max: </p>", unsafe_allow_html=True)
            ymax_sidebar_columns[1].number_input("y-max", step = 1, min_value=0, value = 3, label_visibility = "collapsed", key = 'ymax1')
            ymax_sidebar_columns[2].markdown("<p style='text-align: center;'> x 10^ </p>", unsafe_allow_html=True)
            ymax_sidebar_columns[3].number_input("y-max-pow", step = 1, label_visibility = "collapsed", key = 'ymax2')
            control_columns = st.columns([1,1.8,1,1.3])
            control_columns[0].markdown("<p style='text-align: center;'> Precision: </p>", unsafe_allow_html=True)
            control_columns[1].number_input("Precision: ", min_value = 0, step = 1, label_visibility = "collapsed", key = 'precision')
            control_columns[2].markdown("<p style='text-align: center;'> Curve No. </p>", unsafe_allow_html=True)
            control_columns[3].number_input("Number-of-Curves: ", min_value=0, step = 1, label_visibility = "collapsed", key = 'number_of_curve')
            st.success("Running 'Input Panel'")
        st.divider()
        st.markdown("<h2 style='text-align: center;'> <strong>Output<strong> </h2>", unsafe_allow_html=True)
        with st.spinner("Running 'Output Panel"):
            outputpanelrow1 = st.columns([1, 1, 1])
            outputpanelrow1[0].checkbox("Graph 1", key= "output1")
            outputpanelrow1[1].checkbox("Graph 2", key= "output2")
            outputpanelrow1[2].checkbox("Graph 3", key= "output3")
            outputpanelrow2 = st.columns([1, 1, 1])
            outputpanelrow2[0].checkbox("Graph 4", key= "output4")
            outputpanelrow2[1].checkbox("Graph 5", key= "output5")
            outputpanelrow2[2].checkbox("Graph 6", key= "output6")
            outputpanelrow3 = st.columns([1, 1, 1])
            outputpanelrow3[0].checkbox("Graph 7", key= "output7")
            outputpanelrow3[1].checkbox("Graph 8", key= "output8")
            outputpanelrow3[2].checkbox("Graph 9", key= "output9")
            st.success("Running 'Output Panel'")
        st.divider()
    with desc:
        st.markdown("<h2 style='text-align: center;'>Functionality Description 📜</h2>", unsafe_allow_html=True)
        st.markdown("""<h4 style='text-align: justify;'>The algorithm works U-net images fragmentation to segmentize the digital curve by filtering the curves line that are potentially the data points. 
                    The ranges of axes are needed for interpolation.</h4>""", unsafe_allow_html=True)
        st.markdown("""
        <ul>
        <li style="font-size: 20px;"><strong>Input<strong>: Images, Axes-Range</li>
        <li style="font-size: 20px;"><strong>Output<strong>: Choosen data points containing the digitized curve in CSV format</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown("""
            <blockquote style="font-size: 18px;">
                <i>User will need to manually select the relevant predicted figures.</i>
            </blockquote>
            """, unsafe_allow_html=True)

    with input_:
        st.markdown("<h2 style='text-align: center;'>Input Parameters 📥</h2>", unsafe_allow_html=True)
        st.file_uploader("Upload an image to be segmented", type=["png", "jpeg", "jpg"], key = "img_raw")
        if "img" not in st.session_state:
            st.session_state["img"] = 0
        if "pos_y" not in st.session_state:
            st.session_state["pos_y"] = 0
        if "pos_x" not in st.session_state:
            st.session_state["pos_x"] = 0
        if st.session_state["img_raw"] is None:
            st.session_state["width_"] = 100
            st.session_state["height_"] = 100
            with st.spinner("Running 'read_img'"):
                st.session_state["veryimg"] = read_img("image1.png")
                st.success("Running 'read_img'")
            
        elif st.session_state["img_raw"] is not None:
            
            with st.spinner("Running 'read_img'"):
                st.session_state["img"] = read_img(st.session_state["img_raw"])
                st.success("Running 'read_img'")
            st.session_state["width_"], st.session_state["height_"] = st.session_state["img"].size
            st.session_state["img"] = np.array(st.session_state["img"])
            with st.spinner("Running 'plot_on_image'"):
                st.session_state["figure_to_plot"] = plot_on_image(st.session_state["img_raw"], st.session_state["width_"], st.session_state["height_"])
                st.success("Running 'plot_on_image'")
            with st.spinner("unning 'adding slider position'"):
                st.session_state["figure_to_plot"].add_vline(
                x = st.session_state["pos_x"], line_width = 5, line_dash = "dash", 
                line_color = "pink"
                )
                st.session_state["figure_to_plot"].add_hline(
                    y = st.session_state["pos_y"], line_width = 5, line_dash = "dash", 
                    line_color = "red"
                )
                st.success("Running 'adding slider position'")
            with st.sidebar:
                with st.spinner("Plotting the sliders"):
                    x_slide_1, x_slide_2 = st.columns([3, 7])
                    x_slide_1.markdown("<p style='text-align: center;'> x-position: </p>", unsafe_allow_html=True)
                    x_slide_2.slider("x-position", 0, st.session_state["width_"], 30, key = "pos_x", label_visibility = "collapsed")
                    y_slide_1, y_slide_2 = st.columns([3, 7])
                    y_slide_1.markdown("<p style='text-align: center;'> y-position: </p>", unsafe_allow_html=True)
                    y_slide_2.slider("y-position", 0, st.session_state["height_"], 30, key = "pos_y", label_visibility = "collapsed")
                    st.success("Plotting the sliders")
            with st.spinner("Plotting the figures"):
                place = st.empty()
                with place.container():
                    st.plotly_chart(st.session_state["figure_to_plot"], use_container_width=True)
                st.success("Plotting the figures")
                
        if st.button("Run Prediction"):
            predict(st.session_state["img"])

    with output_:
        st.markdown("<h2 style='text-align: center;'>Output Result 📝</h2>", unsafe_allow_html=True)
        dataframe = pd.DataFrame()
        dataframe['x'] = np.linspace(0, 50, 10)
        dataframe['y'] = np.linspace(0, 50, 10)
        csvdataframe = convert_df(dataframe)
        image_files = ["image1.png", "image2.png", "image3.png", "image4.png", "image5.png", "image6.png", "image7.png", "image8.png", "image9.png"]

        galarayrow1 = st.columns(4)
        galarayrow2 = st.columns(4)
        galarayrow3 = st.columns(4)
        
        with galarayrow2[-1]:
            st.download_button(
            label="Download data as CSV",
            data=csvdataframe,
            file_name='digitized_data.csv',
            mime='text/csv',
            )
        caplist = galarayrow1[0:3] + galarayrow2[0:3] + galarayrow3[0:3]
        for i in range(1, 10):
            if st.session_state[f"output{i}"]:
                write_style = f'<p style="text-align: center; color:LightGreen; font-weight: bold; font-style: italic;"> ✔️ Graph {i} </p>'
            else:
                write_style = f'<p style="text-align: center; color:Black; ">Graph {i}</p>'
            caplist[i-1].markdown(write_style, unsafe_allow_html=True) 
        st.divider()
        with st.spinner("Running 'show_img'"):
            show_img(image_files)
            st.success("Running 'show_img'")
        

if __name__ == "__main__":
    main()
