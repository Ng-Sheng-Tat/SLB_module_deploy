import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image
import dataiku
import plotly.graph_objs as go

import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import os
import io
import base64

folderspath = "/opt/dataiku/data/managed_folders/DKU_TUT_VISUALIZATION_1/bzQqi3wQ"
folderspath = os.path.abspath(folderspath)
os.chdir(folderspath)

app.config.external_stylesheets = [dbc.themes.DARKLY]

# build your Dash app
app.layout = html.Div()

# variables
coldepth = dbc.Row(
            html.Div(["Depth : ", 
            dcc.Input(
                id='depthminin',
                type='number',
                value = 0,
                style={'width': '38%', 'textAlign' : 'center', 'vertical-align': 'middle'}
            ), "     ~     ", 
            dcc.Input(
                id='depthmaxin',
                type='number',
                value = 100,
                style={'width': '38%', 'textAlign' : 'center', 'vertical-align': 'middle'}
            ), "  (m) "
            ]), style={
            'width': '80%',
            'height': '50px',
            'textAlign': 'left',
            'padding-left': '20px', 
            'vertical-align': 'middle',
            'padding-top': '10px',
        },)

coly = dbc.Row(
            html.Div(["y-axis : ", 
            dcc.Input(
                id='yminin',
                type='number',
                value = 1,
                style={'width': '20%', 'textAlign' : 'center', 'vertical-align': 'middle'}
            ), "  x  10^  ", 
            dcc.Input(
                id='ymininpower',
                type='number',
                value = 1,
                style={'width': '10%', 'textAlign' : 'center', 'vertical-align': 'middle'}
            ), "     ~     ", 
            dcc.Input(
                id='ymaxin',
                type='number',
                value=100,
                style={'width': '20%', 'textAlign' : 'center', 'vertical-align': 'middle'}
            ), "  x  10^  ", 
            dcc.Input(
                id='ymaxinpower',
                type='number',
                value = 2,
                style={'width': '10%', 'textAlign' : 'center', 'vertical-align': 'middle'}
            ),
            ]), style={
            'width': '80%',
            'height': '50px',
            'textAlign': 'left',
            'padding-left': '20px',
            'vertical-align': 'middle',
        },)

nlines = dbc.Row(
           html.Div(["n : ", 
            dcc.Input(
                id='n',
                type='number',
                value = 3,
                style={'width': '20%', 'textAlign' : 'center', 'vertical-align': 'middle'}
            ),
            ]), style={
            'width': '80%',
            'height': '50px',
            'textAlign': 'left',
            'padding-left': '20px',
            'vertical-align': 'middle',
        },)

preci = dbc.Row(
           html.Div(["Precision : ", 
            dcc.Input(
                id='precision',
                type='number',
                value = 100,
                style={'width': '20%', 'textAlign' : 'center', 'vertical-align': 'middle'}
            ),
            ]), style={
            'width': '80%',
            'height': '50px',
            'textAlign': 'left',
            'padding-left': '20px',
            'vertical-align': 'middle',
        },)

uploadrow = dcc.Upload(
        id='uploadimg',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '80%',
            'height': '70px',
            'lineHeight': '70px',
            'borderWidth': '3px',
            'borderStyle': 'dashed',
            'borderRadius': '10px',
            'textAlign': 'center',
            'float': 'center',
        },
        # Allow multiple files to be uploaded
        multiple=True
    )

# DEFINE APP LAYOUT
app.layout = html.Div(
    children=[
    html.H1(
        children='Intelligent Learners',
        style={'textAlign': 'center'}
    ),
    html.Div(
        children='The function of this webapps is to digitize your curve into numerical formats! Hope this up to your satisfactory level!',
        style={'textAlign': 'center'}
    ),html.Br(), 
    dbc.Row([
        dbc.Col([
            coldepth,
            coly, 
            nlines,
            preci, 
        ]),
        dbc.Col([uploadrow], style = {'padding-top': '5px',
                       'padding-left': '60px'})
    ]), html.Br(),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Br(),
    "Depth Range : ", html.Div(id = "depthminoutid"), "  ~  ",  html.Div(id = "depthmaxoutid"),
    html.Br(),
    "y-axis Range : ", html.Div(id='yminoutid') , "  ~  ",  html.Div(id = "ymaxoutid"),
    html.Div(id='noutid'),
    html.Div(id='precisionoutid'),
    html.Div(id='outimg'),
    # html.Div(id='outimg'),
    html.Br(),
    html.Hr(),
    dcc.Graph(id = "graph"),
    html.Hr(),
    dcc.Slider(
        id = 'slider-position', 
        min = 0, 
        max = 3000, # this is hardcoded, future will be an issue
        step = 1, 
        value = 2,
        marks={0: '0', 3000: 'max_depth'}
    ), html.Hr(),
    dcc.Slider(
        id = 'slider-position-2', 
        min = 0, 
        max = 800, # this is hardcoded, future will be an issue
        step = 1, 
        value = 3,
        marks={0: '0', 800: 'max_y'}
    ), html.Hr(),
    html.Div(id='sliderx'),
    html.Hr(),
    html.Div(id='slidery'),
    html.Hr(),
    html.Button('Predict', id='predict', n_clicks=0),
    html.Hr(), 
    dcc.Graph(id = "graph1"),
    html.Hr(), 
    html.Div([
            dcc.Checklist(
                id='checklist',                      
                options=[
                    {'label':x, 'value':x, 'disabled': False} for x in ["graph_1", "graph_2", "graph_3"]
                ], labelStyle= {"margin":"1rem"},style = {'display': 'flex'}, inline=True, 
            ),
    ]),
    html.Div(id='checklistout'),
    html.Button("Download", id = 'btn-download'), 
    dcc.Download(id = 'download-dataframe'), 
    ])


# callbacks
@app.callback(
    Output('depthminoutid', 'children'),
    Output('depthmaxoutid', 'children'),
    Output('yminoutid', 'children'),
    Output('ymaxoutid', 'children'),
    Output('precisionoutid', 'children'),
    Output('noutid', 'children'),
    Input("submit-val", "n_clicks"), 
    State('depthminin', 'value'), 
    State('depthmaxin','value'), 
    State('yminin', 'value'), 
    State('ymininpower', 'value'), 
    State('ymaxin', 'value'), 
    State('ymaxinpower', 'value'),
    State('precision', 'value'),
    State('n','value'),
    prevent_initial_call = True,
)
def datapoint_val(n_clicks, depthminin, depthmaxin, ysmall, ysmallpower, ybig, ybigpower, precision, n):  
    smallval = min(depthminin, depthmaxin)
    bigval = max(depthminin, depthmaxin)
    temp1 = ysmall*10**ysmallpower
    temp2 = ybig*10**ybigpower
    minval = min(temp1, temp2)
    maxval = max(temp1, temp2)
    # xdata = np.linspace(smallval, bigval,n)
    return smallval, bigval, minval, maxval, precision, n

@app.callback(Output('outimg', 'children'),
              Input('uploadimg', 'contents'),
              State('uploadimg', 'filename'),)
def update_output(contents, filenames):
    if contents is not None:
        children = [html.Div([
            html.H5(filenames),
        ])]
        return children

@app.callback(
    Output("graph", "figure"),
    Output("sliderx", "children"),
    Output("slidery", "children"),
    Input('uploadimg', 'contents'),
    Input('uploadimg', 'filename'),
    Input("slider-position", "value"), 
    Input("slider-position-2", "value"),
)
def slicing(contents, filenames, pos_x, pos_y):
    if filenames is not None:
        print(contents)
        source = contents[0]
        indexof_ = source.find(',')
        to_decode = source[indexof_+1:]
        image_bytes = base64.b64decode(to_decode)
        image_stream = io.BytesIO(image_bytes)
        im = Image.open(image_stream)
    else:
        im = Image.open(r"slb.jpg")
    width_, height_ = im.size
    # Create figure
    fig = px.imshow(im)
    # width = 100
    xdata = np.linspace(0, width_, 50)
    ydata = np.linspace(0, height_, 50)
    # Add trace
    fig.add_trace(
        go.Scatter(x=xdata, y=ydata,  mode='lines',line=dict(color='rgba(0,0,0,0)'))
        )
    fig.update_layout(height = 2/3*height_, width = 2/3*width_)
    fig.update_layout(xaxis = {'showgrid': False}, yaxis = {'showgrid': False}, 
                    plot_bgcolor='rgba(255,255,255,0)') # paper_bgcolor='rgba(255,255,255,0)', 

    fig.update_yaxes(scaleanchor = 'x', scaleratio = 1)

    fig.add_vline(
        x = pos_x, line_width = 5, line_dash = "dash", 
        line_color = "pink"
    )
    fig.add_hline(
        y = pos_y, line_width = 5, line_dash = "dash", 
        line_color = "red"
    )
    return fig, pos_x, pos_y

# using the uploaded images, runs the prediction using keras weight input, output figure to be plotted
@app.callback(
    Output("graph1", "figure"),
    Input("predict", "n_clicks"), 
    State('uploadimg', 'contents'),
    State('uploadimg', 'filename'),
    State("sliderx", "children"),
    State("slidery", "children"),
    prevent_initial_call = True,
)
def datapoint_val(n_clicks, contents, filenames, x_pos, y_pos):  
    print("Starts here")
    print(x_pos*y_pos)
    if filenames is not None:
        source = contents[0]
        indexof_ = source.find(',')
        to_decode = source[indexof_+1:]
        image_bytes = base64.b64decode(to_decode)
        image_stream = io.BytesIO(image_bytes)
        im = Image.open(image_stream)
    else:
        im = Image.open(r"slb.jpg")
    width_, height_ = im.size
    # Create figure
    fig = px.imshow(im)
    # xdata = np.linspace(smallval, bigval,n)
    return fig

@app.callback(
    Output('download-dataframe', 'data'),
    Input("btn-download", "n_clicks"),
    [State(component_id='checklist', component_property='value')], 
    State('depthminin', 'value'), 
    State('depthmaxin','value'), 
    State('precision', 'value'),
    prevent_initial_call = True,
)
def download(n_clicks, options, depthmin, depthmax, precision):
    df = pd.DataFrame()
    df["depth"] = np.linspace(depthmin, depthmax, precision)
    for i in options:
        df[i] = np.linspace(0, 100, precision)
    return dcc.send_data_frame(df.to_excel, "excelname.xlsx", sheet_name="Sheet_name_1")



### streamlit - background images sliders
# streamlit run .\pythonname.py

import streamlit as st
from time import sleep
import plotly.express as px
import plotly.graph_objs as go
from PIL import Image 
import numpy as np

def computation_function():
    sleep(3)
            
def main():
    st.set_page_config(layout="wide")
    st.write("# Lithology Facies")
    desc, calc = st.tabs(["Description", "Application"])
    with desc:
        st.title("**Functionality Description**")
        st.write("""
            The algorithm works by blar blar blar
            The computation is done by blar blar blar
        
        """)
    with calc:
        st.title("**Accessing the segmentation models**")
        im = st.file_uploader("Upload an image to be segmented", type=["png", "jpeg", "jpg"])
        if im is not None:
            img = Image.open(im)
            width_, height_ = img.size
            st.write(width_, height_)
            img_array = np.array(img)
            # Create figure
            # width = 100
            fig = go.Figure()
            fig.add_trace(go.Image(z=img_array))
            xdata = np.linspace(0, width_, 50)
            ydata = np.linspace(0, height_, 50)
            # Add trace
            fig.add_trace(
                go.Scatter(x=xdata, y=ydata,  mode='lines',line=dict(color='rgba(0,0,0,0)'))
                )
            
            fig.update_layout(height = 2/3*height_, width = 2/3*width_)
            fig.update_layout(xaxis = {'showgrid': False}, yaxis = {'showgrid': False}, 
                            plot_bgcolor='rgba(255,255,255,0)') # paper_bgcolor='rgba(255,255,255,0)', 

            fig.update_yaxes(scaleanchor = 'x', scaleratio = 1)
            pos_x = st.slider("x-position", 0, width_, 30)
            pos_y = st.slider("y-position", 0, height_, 30)
            fig.add_vline(
            x = pos_x, line_width = 5, line_dash = "dash", 
                line_color = "pink"
            )
            fig.add_hline(
                y = pos_y, line_width = 5, line_dash = "dash", 
                line_color = "red"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        # with st.form(key="Submission"):
        depthmin, depthmax = st.columns(2)
        try:
            with depthmin:
                st.write("**Minimum Depth**")
                depth1 = st.number_input("Enter the depth: ", value = 0.0, min_value = 0.0, step = 1.0, key = "1")
                st.write(depth1)

            with depthmax:
                st.write("**Maximum Depth**")
                depth2 = st.number_input("Enter the depth: ", value = 100.0, min_value = depth1, step = 1.0, key = "2")
                st.write(depth2)

            # depth_p = st.slider('**Select a range of depth values:**',depth1, depth2)


            # with depthpred:
            #     # depth_p = st.number_input("Enter the depth: ", value = 2.0, min_value = depth1, max_value = depth2, step = 1.0, key = "3")
            #     depthpred.write("**Predict Depth**")
            #     depthpred.write(depth_p)
            
        except:
            st.write("Invalid Input")
            # st.exception()
        btn_pred = st.form_submit_button("Predict")

        if btn_pred:
            with st.spinner("Doing some expensive computation"):
                computation_function()
                st.success("Implement Successfully")
            
        
if __name__ == "__main__":
    main()

