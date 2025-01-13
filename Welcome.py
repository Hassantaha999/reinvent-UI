########################################
############ Python Modules ############
########################################
import streamlit as st
import os 


###########################
###### General Setup ###### 
###########################
### Setting Welcome page configurations 
st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
            #'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "mailto:hassanabdel999@gmail.com",
            'About': "## REINVENT UI"}
)


##########################
###### Welcome Page ######
##########################
### Abbvie Logo & Image
# logo_path = os.path.join("figures", "reinvent2_logo_modified.jpeg")    
image_path = os.path.join("figures", "reinvent2_logo_modified.jpeg")  
# st.logo(logo_path)
st.image(image_path, caption=f"REINVENT logo used in the REINVENT 2.0 paper")

### Title
st.title("REINVENT Web-based App")

### Welcome Text
st.markdown("""
This interactive web-based UI app of REINVENT allows users to generate input files to run [**REINVENT**](https://github.com/MolecularAI/REINVENT4) 
calculations. This app aims to streamline workflows for chemists and data scientists by allowing 
easy access to REINVENT’s functionalities directly from a browser. REINVENT is an open-source generative AI framework, developed by the Molecular AI department at AstraZeneca R&D, 
for the design of small molecules that uses recurrent neural networks (RNN) and transformer architectures to drive molecule generation. 
A paper describing the REINVENT software has been published as Open Access in the Journal of Cheminformatics: 
[**Reinvent 4: Modern AI–driven generative molecule design**](https://link.springer.com/article/10.1186/s13321-024-00812-5?utm_source=rct_congratemailt&utm_medium=email&utm_campaign=oa_20240221&utm_content=10.1186/s13321-024-00812-5).
""")

### Key Features
st.markdown("""
## Key Features
- **User-Friendly Interface**: An accessible UI that is easy to use and navigate.
- **Easy Parameter Customization**: Set custom preferences for molecular generation, such as docking scores, QED, TPSA, and other property optimizations.
- **Tools**: Additional tools are available to support users in setting up their REINVENT calculations:
  - Create scoring files to use in multiple projects.
  - Visualize transformer functions.
  - Visualize molecules (Chemical Sketcher).
  - Access a list of SMARTS patterns for various projects.
- **Analysis**: Inspect and visualize the results of REINVENT calculations.
- **UI State**: Save chosen parameters as a UI state (JSON file) for later reuse.
""")

### Installation & Prerequisites
st.markdown("""
## Installation & Prerequisites
Before running REINVENT calculations on your local machine using the input files generated with this 
web-based app, ensure the necessary software packages and dependencies are installed on your local machine. 
Refer to the [**REINVENT GitHub Repository**](https://github.com/MolecularAI/REINVENT4) for detailed instructions. 
**Please note that this web-based app is intended only for the generation of input files and other necessary files to run REINVENT calculations**. The actual REINVENT calculations must be performed on your local machine or a suitable computational environment.
""")

### Content of the Web-based App
st.header("Content of the Web-based App")
col1, col2, col3, col4 = st.columns([0.25, 0.25, 0.25, 0.25], gap="large", vertical_alignment="top")
docu = col1.page_link("pages/1_Documentation.py", label="Documentation", icon="📖")
app = col2.page_link("pages/2_REINVENT UI.py", label="REINVENT UI", icon="📂")
tools = col3.page_link("pages/3_Tools.py", label="Tools", icon="🔨")
analysis = col4.page_link("pages/4_Analysis.py", label="Analysis", icon="🔍")
st.markdown(f"""
- **Documentation**: Explains how REINVENT works and provides detailed descriptions for all parameters and options available for REINVENT calculations.
- **REINVENT UI**: Generates the necessary input files for REINVENT calculations.
- **Tools**: Various tools that could support users in setting up their REINVENT calculations:
- **Analysis**: Inspect and visualize the results of your REINVENT calculations.
""")

### General Workflow 
st.header("General Workflow")
st.markdown(f"""
    In the following a general workflow will be described for the user. 
    1. Navigate to the **REINVENT UI** page in the web-based app.
    2. Select your desired options and parameters for the REINVENT calculation.
        - Refer to the **Documentation** page for any clarification on parameters or options when needed. 
          For a more detailed explanation, visit the official documentation: [**REINVENT GitHub Repository**](https://github.com/MolecularAI/REINVENT4).
        - Utilize helpful tools, like the Chemical Sketcher, available on the **Tools** page to assist in generating input files.
    4. Upload all required files for your calculation.
    5. Download the generated ZIP file containing all necessary input and uploaded files.
    6. Extract the ZIP file, navigate to the folder, and run the REINVENT calculation on your local machine.
        - You can monitor and analyze the results of **RL**, **SL**, **TL** runs using TensorBoard with the following command:\n\n
            :red[tensorboard --logdir TB_DIR_NAME/ --bind_all]
    7. After completing the calculation, inspect and visualize the results using the **Analysis** page of the web-based app.
""")