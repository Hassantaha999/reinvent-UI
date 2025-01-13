######################
### Python Modules ### 
######################
import streamlit as st
import os 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from PIL import Image 
from io import BytesIO
from pathlib import Path
import toml 
import json 
from functions import *
from data import * 


###########################
###### General Setup ###### 
###########################
### Configure the page 
st.set_page_config(
    page_title="Tools",
    page_icon=":toolbox:",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
            #'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "mailto:hassanabdel999@gmail.com",
            'About': "## REINVENT UI"}
)

### Create a unique sub-folder for each user in the temp_files folder 
pwd = os.getcwd()                            # Path for Parent Working Directory (Dir: reinvent4)
BASE_DIR = os.path.join(pwd, "temp_files")   # Base directory for temporary files
Path(BASE_DIR).mkdir(exist_ok=True)          # Create the base directory if it doesn't exist
if "user_folder" not in st.session_state:
    # Use the current time to create a unique identifier (formatted as YYYY-MM-DD-HH-MM-SS)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    user_folder = os.path.join(BASE_DIR, f"user_{timestamp}")
    Path(user_folder).mkdir(exist_ok=True)
    st.session_state.user_folder = user_folder
else:
    user_folder = st.session_state.user_folder

### To save the changes made in UI across a multi-page streamlit app 
for key in st.session_state:
    st.session_state[key] = st.session_state[key]

### Decide if you want to have the "SMARTSviewer" & "Chemical Sketcher" in your Streamlit UI app 
smarts_viewer = False
if smarts_viewer:
    from streamlit_ketcher import st_ketcher


#########################
######### Tools #########
#########################
### Abbvie Logo & Image
# logo_path = os.path.join("figures", "reinvent2_logo_modified.jpeg")    
image_path = os.path.join("figures", "reinvent2_logo_modified.jpeg")  
# st.logo(logo_path)
st.image(image_path, caption=f"REINVENT logo used in the REINVENT 2.0 paper")

### Titel 
st.title("Tools")
st.sidebar.header("Content", divider="gray")

### Tabs
if smarts_viewer:
    overview, scoring_file, transformer, chem_sketch, smarts_view, smarts_pattern = st.tabs(["General Overview", "Scoring File", "Transformer Functions", "Chemical Sketcher", "SMARTSview", "SMARTS Pattern"])
else:
    overview, scoring_file, transformer, smarts_pattern = st.tabs(["General Overview", "Scoring File", "Transformer Functions", "SMARTS Pattern"])


##################
#### Overview ####
##################
with overview:
    st.header("General Overview", divider="gray")
    st.sidebar.subheader("General Overview")

    if smarts_viewer: 
        st.write(
            """
             This page contains some tools that may be helpful for the user in generating the desired input file 
             for a REINVENT calculation. It contains the following tools: 
             - **Scoring File**: generate scoring files to use for the different REINVENT calculations. 
             - **Transformer Functions**: visualize the transformer functions and adjust there parameters. 
             - **Chemical Sketcher**: Chemical Sketch tool to generate SMILES strings from drawn or edited molecules. ([**Github Repository**](https://github.com/streamlit/streamlit-ketcher)). 
             - **SMARTSview**: An API to the [**SMARTS.plus**](https://smarts.plus/) service provided by the University of Hamburg that enables the user to create an easy to comprehend visualization for SMARTS expressions. 
                - If the user wants to draw the molecule and directly get the SMARTS pattern of the drawn fragment, 
                he may do so with the [**PubChem Online Sketcher**](https://pubchem.ncbi.nlm.nih.gov//edit3/index.html) or
                [**RCSB Chemical Sketch Tool**](https://www.rcsb.org/chemical-sketch).
             - **SMARTS Pattern**: A list of possible SMARTS patterns for different chemical fragments. 
            """)
    else: 
        st.write(
            """
             This page contains some tools that may be helpful for the user in generating the desired input file 
             for a REINVENT calculation. It contains the following tools: 
             - **Scoring File**: generate scoring files to use for the different REINVENT calculations. 
             - **Transformer Functions**: visualize the transformer functions and adjust there parameters. 
             - **SMARTS Pattern**: A list of possible SMARTS patterns for different chemical fragments. 
            """)

#######################
#### Scoring File  ####
#######################
with scoring_file:
    st.header("Scoring File", divider="gray")
    st.sidebar.subheader("Scoring File")

    col1, col2 = st.columns([0.40, 0.60], gap="large", vertical_alignment="top")

    ## Input Options 
    col1.header("Input Options")

    ## Preview of Scoring File 
    col2.header("Preview of Scoring File")

    with col1:
        # User Input 
        modus = col1.selectbox("Select Mode", ("Basic", "Advanced"), index=0, key="modus")
        format = col1.selectbox("Select format", ("TOML", "JSON"), key="format")
        scoring_file_name = col1.text_input("Name of scoring file", value=f"scoring_file", key="scoring_file")
    
    # Define Paths for scoring files
    scoring_json_f = f"{st.session_state['user_folder']}/{scoring_file_name}.json"
    if os.path.exists(scoring_json_f):
        os.remove(scoring_json_f)
    scoring_toml_f = os.path.join(Path(st.session_state["user_folder"]), f"{scoring_file_name}.toml")  
    if os.path.exists(scoring_toml_f):
        os.remove(scoring_toml_f)
    
    with col1:
        with st.expander("**Scoring Components**"):
            # Select scoring components
            scor_comp = scoring_components(scoring_toml_f, col2, None, None, modus=modus, needed_files=None, 
                                           uploaded_files=None, gen_scoring_file=True, 
                                           key="scoring")
        # Check if file was created 
        if os.path.exists(scoring_toml_f):
            # Convert TOML file into JSON file 
            if format == "JSON":
                # Open temp TOML file and read it's content 
                with open(scoring_toml_f, "r") as source:
                    toml_content = toml.loads(source.read())
                # remove TOML file 
                os.remove(scoring_toml_f)
                # open JSON file and write the scoring file content 
                with open(scoring_json_f, "w") as json_f:
                    json_f.write(json.dumps(toml_content, indent=4))
                    # Download JSON file 
                with open(scoring_json_f, "r") as json:       
                    st.download_button("Download Scoring File", 
                                       data=json, 
                                       file_name=f"{scoring_file_name}.json", 
                                       help=f"{scoring_file_name}.json")
            else:
                if os.path.exists(scoring_json_f):
                    os.remove(scoring_json_f)
                # Download TOML file       
                with open(scoring_toml_f, "r") as toml:          
                    st.download_button("Download Scoring File", 
                                        data=toml, 
                                        file_name=f"{scoring_file_name}.toml", 
                                        help=f"{scoring_file_name}.toml")


####################
### Transformers ###
####################
with transformer:
  st.header("Transformer Functions", divider="gray")
  st.sidebar.subheader("Transformer Functions")
  
  st.write("""The user may use the following interactive widget to adjust the different transformer parameters 
            and to see how they affect the transformer function. **Important to note here is that these changes don't 
            affect the parameters values in the Reinvent UI.**""")

  transformer_type = st.selectbox(label="**Select type of transformer**", options=["Sigmoid", "Reverse Sigmoid", "Double Sigmoid", 
                                                                                   "Right Step", "Left Step", "Step"], 
                                                                          index=0)
  
  if transformer_type == "Sigmoid":

    col1, col2 = st.columns([0.25, 0.75], gap="large", vertical_alignment="top") 

    with col1:
        values_min = st.number_input("min. X-Value", min_value=None, max_value=None, value=-100.0, step=1.0)
        values_max = st.number_input("max. X-Value", min_value=None, max_value=None, value=100.0, step=1.0)
        center = (values_min + values_max) / 2
        low, high = st.slider("Select Thresholds", values_min, values_max, (((values_min + center) / 2), ((values_max + center) / 2)))
        center = (low + high) / 2
        k = st.number_input("Scaling Factor (k)", min_value=None, max_value=None, value=1.0, step=0.1)
        # if high-low != 0:
        #     st.write(f"K = {(10 * k) / (high-low):.2f}, B = {(high+low)/2:.2f}")
        # else:
        #     st.write(f"K = {(10 * k):.2f}, B = {(high+low)/2:.2f}")

    with col2:
        fig = plt.figure(figsize=(4, 3))
        x = np.linspace(values_min, values_max, 100)  # Define the range of x-values
        y = sigmoid(x, k, low, high) # Calculate the sigmoid values
        plt.plot(x, y)  # Plot the graph
        plt.xlabel("x") # Add X-label
        plt.ylabel("f(x)") # Add Y-label
        plt.title("Sigmoid Function") # Add title
        plt.xlim([values_min-(0.1 * values_max), values_max+(0.1 * values_max)]) # Set limits slightly bigger than range of function
        if k != 0.0:
          plt.vlines(center, 0.0, 1.0, color="red", linestyles="--", label="Center of Sigmoid") # draw a vertical line at the center of the sigmoid function 
        plt.grid(True) # Grid
        plt.legend(loc="upper left", prop={'size': 7})
        st.pyplot(fig=fig) # Show the plot


  elif transformer_type == "Reverse Sigmoid":

    col1, col2 = st.columns([0.25, 0.75], gap="large", vertical_alignment="top") 

    with col1:
        values_min = st.number_input("min. X-Value", min_value=None, max_value=None, value=-100.0, step=1.0)
        values_max = st.number_input("max. X-Value", min_value=None, max_value=None, value=100.0, step=1.0)
        center = (values_min + values_max) / 2
        low, high = st.slider("Select Thresholds", values_min, values_max, (((values_min + center) /2), ((values_max + center) /2)))
        center = (low + high) / 2
        k = st.number_input("Scaling Factor (k)", min_value=None, max_value=None, value=1.0, step=0.1)
        # if high-low != 0:
        #     st.write(f"K = {(10 * k) / (high-low):.2f}, B = {(high+low)/2:.2f}")
        # else:
        #     st.write(f"K = {(10 * k):.2f}, B = {(high+low)/2:.2f}")

    with col2:
        fig = plt.figure(figsize=(4, 3))
        x = np.linspace(values_min, values_max, 100)  # Define the range of x-values
        y = reverse_sigmoid(x, k, low, high) # Calculate the reverse sigmoid values 
        plt.plot(x, y) # Plot the graph
        plt.xlabel("x") # Add X-label
        plt.ylabel("f(x)") # Add Y-label
        plt.title("Reverse Sigmoid Function") # Add title
        plt.xlim([values_min-(0.1 * values_max), values_max+(0.1 * values_max)]) # Set limits slightly bigger than range of function
        if k != 0.0:
          plt.vlines(center, 0.0, 1.0, color="red", linestyles="--", label="Center of Reverse Sigmoid") # draw a vertical line at the center of the sigmoid function 
        plt.grid(True) # Grid
        plt.legend(loc="upper right", prop={'size': 7})
        st.pyplot(fig=fig) # Show the plot


  elif transformer_type == "Double Sigmoid":

    col1, col2 = st.columns([0.30, 0.70], gap="large", vertical_alignment="top") 

    with col1:
        values_min = st.number_input("min. X-Value", min_value=None, max_value=None, value=-100.0, step=1.0)
        values_max = st.number_input("max. X-Value", min_value=None, max_value=None, value=100.0, step=1.0)
        center = (values_min + values_max) / 2
        low, high = st.slider("Select Thresholds", values_min, values_max, (((values_min + center) /2), ((values_max + center) /2)))
        k = st.number_input("Common Scaling Factor ($k$)", min_value=None, max_value=None, value=1.0, step=0.1)
        k_low = st.number_input("Scaling Left Factor ($k_l$)", min_value=None, max_value=None, value=1.0, step=0.1)
        k_high = st.number_input("Scaling Right Factor ($k_r$)", min_value=None, max_value=None, value=1.0, step=0.1)

    with col2:
        fig = plt.figure(figsize=(4, 4))
        x = np.linspace(values_min, values_max, 100)  # Define the range of x-values
        y = double_sigmoid(x, low, high, k, k_low, k_high) # Calculate the double sigmoid values
        plt.plot(x, y) # Plot the graph
        plt.xlabel("x") # Add X-label
        plt.ylabel("f(x)") # Add Y-label
        plt.title("Double Sigmoid Function") # Add title
        plt.xlim([values_min-(0.1 * values_max), values_max+(0.1 * values_max)]) # Set limits slightly bigger than range of function
        plt.grid(True) # Grid
        st.pyplot(fig=fig) # Show the plot


  elif transformer_type == "Right Step":

    col1, col2 = st.columns([0.25, 0.75], gap="large", vertical_alignment="top") 

    with col1:
        values_min = st.number_input("min. X-Value", min_value=None, max_value=None, value=-100.0, step=1.0)
        values_max = st.number_input("max. X-Value", min_value=None, max_value=None, value=100.0, step=1.0)
        center = (values_min + values_max) / 2
        low = st.slider("Select Threshold", values_min, values_max, center)

    with col2:
        fig = plt.figure(figsize=(4, 3))
        x = np.linspace(values_min, values_max, 100) # Define the range of x-values
        y = right_step(x, low) # Calculate the right step values
        plt.plot(x, y) # Plot the graph
        plt.xlabel("x") # Add X-label 
        plt.ylabel("f(x)") # Add Y-label
        plt.title("Right Step Function") # Add title
        plt.xlim([values_min-(0.1 * values_max), values_max+(0.1 * values_max)]) # Set limits slightly bigger than range of function
        plt.grid(True) # Grid
        st.pyplot(fig=fig) # Show the plot
    

  elif transformer_type == "Left Step":

    col1, col2 = st.columns([0.25, 0.75], gap="large", vertical_alignment="top") 

    with col1:
        values_min = st.number_input("min. X-Value", min_value=None, max_value=None, value=-100.0, step=1.0)
        values_max = st.number_input("max. X-Value", min_value=None, max_value=None, value=100.0, step=1.0)
        center = (values_min + values_max) / 2
        low = st.slider("Select Threshold", values_min, values_max, center)

    with col2:
        fig = plt.figure(figsize=(4, 3))
        x = np.linspace(values_min, values_max, 100) # Define the range of x-values
        y = left_step(x, low) # Calculate the left step values
        plt.plot(x, y) # Plot the graph
        plt.xlabel("x") # Add X-label 
        plt.ylabel("f(x)") # Add Y-label
        plt.title("Left Step Function") # Add title
        plt.xlim([values_min-(0.1 * values_max), values_max+(0.1 * values_max)]) # Set limits slightly bigger than range of function
        plt.grid(True) # Grid
        st.pyplot(fig=fig) # Show the plot


  elif transformer_type == "Step":

    col1, col2 = st.columns([0.25, 0.75], gap="large", vertical_alignment="top") 

    with col1:
        values_min = st.number_input("min. X-Value", min_value=None, max_value=None, value=-100.0, step=1.0)
        values_max = st.number_input("max. X-Value", min_value=None, max_value=None, value=100.0, step=1.0)
        center = (values_min + values_max) / 2
        low, high = st.slider("Select Thresholds", values_min, values_max, (((values_min + center) /2), ((values_max + center) /2)))

    with col2:
        fig = plt.figure(figsize=(4, 3))
        x = np.linspace(values_min, values_max, 100) # Define the range of x-values
        y = step(x, low, high) # Calculate the step values
        plt.plot(x, y)  # Plot the graph
        plt.xlabel("x") # Add X-label 
        plt.ylabel("f(x)") # Add Y-label
        plt.title("Step Function") # Add title
        plt.xlim([values_min-(0.1 * values_max), values_max+(0.1 * values_max)]) # Set limits slightly bigger than range of function
        plt.grid(True) # Grid
        st.pyplot(fig=fig) # Show the plot
    

###########################
#### Chemical Sketcher ####
###########################
if smarts_viewer:
    with chem_sketch:
        st.header("Chemical Sketcher", divider="gray")
        st.sidebar.subheader("Chemical Sketcher")

        molecule = st.text_input("Enter molecule SMILE:", 
                                value="C[N+]1=CC=C(/C2=C3\C=CC(=N3)/C(C3=CC=CC(C(N)=O)=C3)=C3/C=C/C(=C(\C4=CC=[N+](C)C=C4)C4=N/C(=C(/C5=CC=CC(C(N)=O)=C5)C5=CC=C2N5)C=C4)N3)C=C1")
        smile_code = st_ketcher(molecule)
        st.markdown(f"""Smile code:  
                ``{smile_code}``""")


######################
#### SMARTSviewer ####
######################
if smarts_viewer:
    with smarts_view:
        st.header("SMARTSview", divider="gray", help="source: SMARTSviewer smartsview.zbh.uni-hamburg.de, ZBH Center for Bioinformatics, University of Hamburg")
        st.sidebar.subheader("SMARTSview")

        def smiles_to_smarts():
            st.session_state["tools_user_smarts"] = convert_smiles_smarts(st.session_state["tools_user_smiles"], convert_to="smarts")

        def smarts_to_smiles():
            st.session_state["tools_user_smiles"]  = convert_smiles_smarts(st.session_state["tools_user_smarts"], convert_to="smiles")

        # SMILES pattern 
        user_smiles = st.text_input("Enter a SMILES string:",  key="tools_user_smiles", on_change=smiles_to_smarts, value="*C(=O)[CH2]N")
        # SMARTs pattern 
        user_smarts = st.text_input("Enter a SMARTS pattern:", key="tools_user_smarts", on_change=smarts_to_smiles, value="N[CX4H2][CX3](=[OX1])[O,N]") # glycine as default 
        user_smarts = user_smarts.replace("%", "%25").replace("&", "%26").replace("+", "%2B").replace("#", "%23").replace(";", "%3B")
        vis_mode = st.selectbox("Select Visualization Mode", options=["Complete visualization", "ID-Mapping", "Element symbols", "Structure Diagram-Like"], index=0)
        vis_mode_dic = {"Complete visualization": "0", "ID-Mapping": "1", 
                        "Element symbols": "2", "Structure Diagram-Like": "3"}
        show_labels = st.selectbox("Show Atom Labels?", options=["true", "false"], index=1)
        show_labels = "0" if show_labels == "false" else "1"
        api_url = f"""
                https://smarts.plus/smartsview/download_rest?smarts={user_smarts};filetype=png;vmode={vis_mode_dic[vis_mode]};vbonds=0;textdesc=1;depsymbols=1;smartsheading=0;trim=1;labels={show_labels};detectarom=1;smileslikearom=1;
                """
        response = requests.get(api_url, verify=True)

        if response.status_code == 200: 
            #st.write(response.content)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption="Image from SMARTS.plus API")
        else:
            st.error("Failed to fetch image. Status code:", str(response.status_code))


#############################
###### SMARTS Patterns ######
#############################
with smarts_pattern:
    st.header("SMARTS Pattern", divider="gray")
    st.sidebar.subheader("SMARTS Pattern")
    st.write(
            """
             The following table will include a list of many possible SMARTS pattern ([source](https://www.daylight.com/dayhtml_tutorials/languages/smarts/smarts_examples.html#C)) for different chemical fragments 
             that might be helpful for the user in setting up the options and prameters for a REINVENT calculation.  
            """)
    data = { 
        "Fragments": [pattern for pattern in smarts_patterns.keys()],
        "SMARTS Pattern": [smart for smart in smarts_patterns.values()]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, width=1000, height=500, hide_index=True)