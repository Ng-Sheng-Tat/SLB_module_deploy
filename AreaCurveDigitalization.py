import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import os
import numpy as np

def prediction():
    st.success("Doing some prediction")
    result_df = pd.DataFrame()
    result_df["depth"] = np.linspace(0, 50, 100)
    result_df["class1"] = np.linspace(0, 50, 100)
    pass

def main():
    st.set_page_config(layout='wide')
    # Specify canvas parameters in application
    h_line_color_1 = "blue"
    h_line_color_2 = "green"
    v_line_color_1 = "red"
    v_line_color_2 = "black"
    bg_color = "#eee"
    accuracy = 1
    width = 800
    height = 800
    canvas_resized = False
    
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'> <strong>Input<strong> </h2>", unsafe_allow_html=True)
        stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 2)
        bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg", "jpeg"])
        if bg_image is not None:
            image = Image.open(bg_image)
            width, height = image.size
            height_red = 800
            if height > height_red:
                ratio = height_red / float(height)
                width_red = int(ratio * width)
                image_red = image.resize((width, height), Image.ANTIALIAS)
                canvas_resized = True
    
        # Add sliders to control the positions of the horizontal and vertical lines
        st.markdown("<b><span style='color:green'>Y-min (%):</span></b>", unsafe_allow_html=True)
        st.slider("", 0, 100, 25,accuracy, key = "ymin")

        st.markdown("<b><span style='color:blue'>Y-max (%):</span></b>", unsafe_allow_html=True)
        st.slider("", 0, 100, 75,accuracy, key = "ymax")

        st.markdown("<b><span style='color:red'>X-min (%):</span></b>", unsafe_allow_html=True)
        st.slider("", 0, 100, 25,accuracy, key = "xmin")

        st.markdown("<b><span style='color:black'>X-max (%):</span></b>", unsafe_allow_html=True)
        st.slider("", 0, 100, 75,accuracy, key = "xmax")

        x_sidebar_columns = st.columns([1,2.5,0.5,2.5])
        x_sidebar_columns[0].markdown("<p style='text-align: center;'> Depth: </p>", unsafe_allow_html=True)
        x_sidebar_columns[1].number_input("x-min", min_value=0, value=0, step=1, label_visibility = "collapsed", key = "depth_min") 
        x_sidebar_columns[2].markdown("<p style='text-align: center;'> ~ </p>", unsafe_allow_html=True)
        x_sidebar_columns[3].number_input("x-max", min_value = 0, value = 30, step = 1, label_visibility = "collapsed", key = "depth_max") 
        control_columns = st.columns([1,1.8,1,1.3])
        control_columns[0].markdown("<p style='text-align: center;'> Precision: </p>", unsafe_allow_html=True)
        control_columns[1].number_input("Precision: ", min_value = 0, key = "precision", step = 1, label_visibility = "collapsed") 
        control_columns[2].markdown("<p style='text-align: center;'> Curve No. </p>", unsafe_allow_html=True)
        control_columns[3].number_input("Number-of-Curves: ", key = "number_of_curve", min_value=0, step = 1, label_visibility = "collapsed") 

        if st.button('Reset line positions'):
            st.session_state['ymin'], st.session_state['xmin'] = 25
            st.session_state['ymax'], st.session_state['xmax'] = 75
            bg_image = None

        if st.button('Scan the image'):
            df = pd.DataFrame({
                'h_line_min_y': [h_line_min_y],
                'h_line_max_y': [h_line_max_y],
                'v_line_min_x': [v_line_min_x],
                'v_line_max_x': [v_line_max_x],
                'image_width': [image.size[0]] if bg_image else [None],
                'image_height': [image.size[1]] if bg_image else [None],
                'body_width': [width],
                'body_height': [height],
                'precision': [precision],
                'number_of_curve': [number_of_curve],

                })
            df.to_csv('user_input.csv', index=False)
            # Delete the prediction_target.jpg file
            if os.path.exists('prediction_target.jpg'):
                os.remove('prediction_target.jpg')

            if bg_image is not None:
                image = Image.open(bg_image)
                image.save('prediction_target.jpg')

    desc, input_, output_ = st.tabs(["Description", "Input", "Output"])
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

    with input_:
        st.markdown("<h3 style='text-align: center;'>Input</h3>", unsafe_allow_html=True)

        # Calculate the y-coordinates of the horizontal lines and the x-coordinates of the vertical lines based on the slider values
        h_line_min_y = int(height * st.session_state["ymin"] / 100)
        h_line_max_y = int(height * st.session_state["ymax"] / 100)
        v_line_min_x = int(width * st.session_state["xmax"] / 100)
        v_line_max_x = int(width * st.session_state["xmin"] / 100)

        # Create a canvas component
        st_canvas(
            # Fixed fill color with some opacity
            fill_color="rgba(255, 165, 0, 0.3)",  
            stroke_width=stroke_width,
            display_toolbar = False,
            background_color=bg_color,
            background_image=image if bg_image else None,
            update_streamlit=True,
            drawing_mode='line',
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
        
    with output_:
        # with columrow[1]:
        st.markdown("<h3 style='text-align: center;'>Output</h3>", unsafe_allow_html=True)
        # to make the button centered aligned

        # padrow = st.columns(3)

        # st.download_button(
        #     label = "Download data as CSV",
        #     # data = result_df.to_csv().encode('utf-8'),
        #     file_name = "digitized_data.csv",
        #     mime = 'text/csv',
        # )
        # with padrow[2]:
        #     st.empty()
        
        st.markdown("<p style='text-align: center;'>Result-Preview</p>", unsafe_allow_html=True)
        # st.dataframe(result_df, width=500, height = 700)        
    
if __name__ == "__main__":
    main()