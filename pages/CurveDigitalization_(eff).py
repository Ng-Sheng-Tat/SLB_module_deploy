import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import os
import numpy as np

def prediction():
    pass

def main():
    st.set_page_config(layout='wide')

    # Specify canvas parameters in application
    drawing_mode = 'line'

    h_line_color_1 = "blue"
    h_line_color_2 = "green"
    v_line_color_1 = "red"
    v_line_color_2 = "black"
    bg_color = "#eee"
    realtime_update = True
    accuracy = 1
    width = 800
    height = 800

    canvas_resized = False

    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'> <strong>Input<strong> </h2>", unsafe_allow_html=True)
        stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 2)
        bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg", "jpeg"])

        # Add sliders to control the positions of the horizontal and vertical lines
        st.markdown("<b><span style='color:green'>Y-min (%):</span></b>", unsafe_allow_html=True)
        st.slider("", 0, 100, 75,accuracy,key="ymin")

        # Original Code: h_line_min_position = st.sidebar.slider("", 0, 100, 75,accuracy,key="ymin")
        # now you can achieve the state session using st.session_state["ymin"], this bulky syntax is equivalent to h_line_min_position

        st.markdown("<b><span style='color:blue'>Y-max (%):</span></b>", unsafe_allow_html=True)
        st.slider("", 0, 100, 25,accuracy,key="ymax")

        st.markdown("<b><span style='color:red'>X-min (%):</span></b>", unsafe_allow_html=True)
        st.slider("", 0, 100, 25,accuracy,key="xmax")

        st.markdown("<b><span style='color:black'>X-max (%):</span></b>", unsafe_allow_html=True)
        st.slider("", 0, 100, 75,accuracy,key="xmin")

        x_sidebar_columns = st.columns([1,2.5,1,2.5])
        x_sidebar_columns[0].markdown("<p style='text-align: center;'> x-min: </p>", unsafe_allow_html=True)
        x_sidebar_columns[1].number_input("x-min", min_value=0, value=0, step=1, label_visibility = "collapsed", key = 'x_min') # access the variables through st.session_state["x_min"]
        x_sidebar_columns[2].markdown("<p style='text-align: center;'> x-min: </p>", unsafe_allow_html=True)
        x_sidebar_columns[3].number_input("x-max", min_value = st.session_state["x_min"], value = 30, step = 1, label_visibility = "collapsed", key = 'x_max') # st.session_state["x_max"]
        ymin_sidebar_columns = st.columns([1,2.5,1,2.5])
        ymin_sidebar_columns[0].markdown("<p style='text-align: center;'> y-min: </p>", unsafe_allow_html=True, )
        ymin_sidebar_columns[1].number_input("y-min", min_value=0, value =1, step = 1, label_visibility = "collapsed", key = 'ymin1') # st.session_state["ymin1"]
        ymin_sidebar_columns[2].markdown("<p style='text-align: center;'> x 10^ </p>", unsafe_allow_html=True)
        ymin_sidebar_columns[3].number_input("y-min-pow", step = 1, label_visibility = "collapsed", key = 'ymin2') # st.session_state["ymin1"]
        ymax_sidebar_columns = st.columns([1,2.5,1,2.5])
        ymax_sidebar_columns[0].markdown("<p style='text-align: center;'> y-max: </p>", unsafe_allow_html=True) 
        ymax_sidebar_columns[1].number_input("y-max", step = 1, min_value=0, value = 3, label_visibility = "collapsed", key = 'ymax1') # st.session_state["ymax1"]
        ymax_sidebar_columns[2].markdown("<p style='text-align: center;'> x 10^ </p>", unsafe_allow_html=True)
        ymax_sidebar_columns[3].number_input("y-max-pow", step = 1, label_visibility = "collapsed", key = 'ymax2') # st.session_state["ymax2"]
        control_columns = st.columns([1,1.8,1,1.3])
        control_columns[0].markdown("<p style='text-align: center;'> Precision: </p>", unsafe_allow_html=True)
        control_columns[1].number_input("Precision: ", min_value = 0, step = 1, label_visibility = "collapsed", key = 'precision') # st.session_state["precision"]
        control_columns[2].markdown("<p style='text-align: center;'> Curve No. </p>", unsafe_allow_html=True)
        control_columns[3].number_input("Number-of-Curves: ", min_value=0, step = 1, label_visibility = "collapsed", key = 'number_of_curve') # st.session_state["number_of_curve"]

    # Calculate the y-coordinates of the horizontal lines and the x-coordinates of the vertical lines based on the slider values
    h_line_min_y = int(height * st.session_state["ymin"] / 100)
    h_line_max_y = int(height * st.session_state["ymax"] / 100)
    v_line_min_x = int(width * st.session_state["xmax"] / 100)
    v_line_max_x = int(width * st.session_state["xmin"] / 100)
    if bg_image is not None:
        image = Image.open(bg_image)
        width, height = image.size
        max_length = 800
        if height > max_length:
            ratio = max_length / float(height)
            width = int(ratio * width)
            height = max_length
            image = image.resize((width, height), Image.ANTIALIAS)
            canvas_resized = True

    # Create a canvas component
    desc, apps_ = st.tabs(["Description", "Application"])
    with desc:
        st.markdown("<h2 style='text-align: center;'>Functionality Description 📜</h2>", unsafe_allow_html=True)
        st.markdown("""<h4 style='text-align: justify;'>The algorithm works U-net images fragmentation to segmentize the digital curve by identifying the potential separating lines beteen different regions. 
                    </h4>""", unsafe_allow_html=True)
        st.markdown("""
        <ul>
        <li style="font-size: 20px;"><strong>Input<strong>: Images, Axes-Range</li>
        <li style="font-size: 20px;"><strong>Output<strong>: % of each area at depth</li>
        </ul>
        """, unsafe_allow_html=True)
        
    with apps_:
        columrow = st.columns([1, 1])
        with columrow[0]:
            st.markdown("<h3 style='text-align: center;'>Input</h3>", unsafe_allow_html=True)
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
                stroke_width=stroke_width,
                background_color=bg_color,
                background_image=image if bg_image else None,
                update_streamlit=realtime_update,
                drawing_mode=drawing_mode,
                initial_drawing={
                    "version": "4.4.0",
                    "objects": [
                        {
                            "type": "line",
                            "version": "4.4.0",
                            "originX": "center",
                            "originY": "center",
                            "left": width / 2,
                            "top": h_line_min_y,
                            "width": width,
                            "height": 0,
                            "fill": h_line_color_2,
                            "stroke": h_line_color_2,
                            "strokeWidth": stroke_width,
                            "x1": -width / 2,
                            "x2": width / 2,
                            "y1": 0,
                            "y2": 0,
                        },
                        {
                            "type": "line",
                            "version": "4.4.0",
                            "originX": "center",
                            "originY": "center",
                            "left": width / 2,
                            "top": h_line_max_y,
                            "width": width,
                            "height": 0,
                            "fill": h_line_color_1,
                            "stroke": h_line_color_1,
                            "strokeWidth": stroke_width,
                            "x1": -width / 2,
                            "x2": width / 2,
                            "y1": 0,
                            "y2": 0,
                        },
                        {
                            "type": "line",
                            "version": "4.4.0",
                            "originX": "center",
                                            "originY": "center",
                            "left": v_line_min_x,
                            "top": height / 2,
                            "width": 0,
                            "height": height,
                            "fill": v_line_color_1,
                            "stroke": v_line_color_1,
                            "strokeWidth": stroke_width,
                            "x1": 0,
                            "x2": 0,
                            "y1": -height / 2,
                            "y2": height / 2,
                        },
                        {
                            "type": "line",
                            "version": "4.4.0",
                            "originX": "center",
                            "originY": "center",
                            "left": v_line_max_x,
                            "top": height / 2,
                            "width": 0,
                            "height": height,
                            "fill": v_line_color_2,
                            "stroke": v_line_color_2,
                            "strokeWidth": stroke_width,
                            "x1": 0,
                            "x2": 0,
                            "y1": -height / 2,
                            "y2": height / 2,
                        },
                    ],
                    "background": bg_color,
                },
                height=height if canvas_resized else None,
                width=width if canvas_resized else None,
            )
            
            # Add a button to save the line positions as a CSV file
            padsave = st.columns(3)
            with padsave[0]:
                st.empty()
            with padsave[1]:
                if st.button('Save line positions'):
                    df = pd.DataFrame({
                        'h_line_min_y': [h_line_min_y],
                        'h_line_max_y': [h_line_max_y],
                        'v_line_min_x': [v_line_min_x],
                        'v_line_max_x': [v_line_max_x],
                        'image_width': [image.size[0]] if bg_image else [None],
                        'image_height': [image.size[1]] if bg_image else [None],
                        'body_width': [width],
                        'body_height': [height]
                    })
                    df.to_csv('line_positions.csv', index=False)
                st.success('Line positions and image dimensions saved as CSV file')
            with padsave[2]:
                st.empty()

            # Save the uploaded image as prediction_target.jpg
            if bg_image is not None:
                image = Image.open(bg_image)
                image.save('prediction_target.jpg')
            padreset = st.columns(3)
            with padreset[0]:
                st.empty()
            with padreset[1]:
                if st.button('Reset line positions'):
                    df = pd.DataFrame({
                        'h_line_min_y': [0],
                        'h_line_max_y': [0],
                        'v_line_min_x': [0],
                        'v_line_max_x': [0],
                        'image_width': [None],
                        'image_height': [None],
                        'body_width': [0],
                        'body_height': [0]
                    })

                    df.to_csv('line_positions.csv', index=False)
                    st.success('Line positions and image dimensions reset to 0')
                if st.button("Run Prediction"):
                    prediction()
            with padreset[2]:
                st.empty()

            # Delete the prediction_target.jpg file
            if os.path.exists('prediction_target.jpg'):
                os.remove('prediction_target.jpg')

            
        with columrow[1]:
            st.markdown("<h3 style='text-align: center;'>Output</h3>", unsafe_allow_html=True)
            # to make the button centered aligned
            result_df = pd.DataFrame()
            result_df["depth"] = np.linspace(0, 50, 100)
            result_df["class1"] = np.linspace(0, 50, 100)
            result_df["class2"] = np.linspace(0, 50, 100)
            result_df["class3"] = np.linspace(0, 50, 100)

            padrow = st.columns(3)
            with padrow[0]:
                st.empty()
            with padrow[1]:
                st.download_button(
                    label = "Download data as CSV",
                    data = result_df.to_csv().encode('utf-8'),
                    file_name = "digitized_data.csv",
                    mime = 'text/csv',
                )
            with padrow[2]:
                st.empty()
            
            st.markdown("<p style='text-align: center;'>Result-Preview</p>", unsafe_allow_html=True)
            st.dataframe(result_df, width=500, height = 700)
if __name__ == "__main__":
    main()