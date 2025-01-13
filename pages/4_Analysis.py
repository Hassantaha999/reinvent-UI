######################
### Python Modules ### 
######################
import streamlit as st
import pandas as pd
from functions import *
from data import * 


###########################
###### General Setup ###### 
###########################
### Configure the page 
st.set_page_config(
    page_title="Analysis",
    page_icon=":mag:",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
            #'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "mailto:hassanabdel999@gmail.com",
            'About': "## REINVENT UI"}
)

### To save the changes made in UI across a multi-page streamlit app 
for key in st.session_state:
    st.session_state[key] = st.session_state[key]

### Abbvie Logo & Image
# logo_path = os.path.join("figures", "reinvent2_logo_modified.jpeg")    
image_path = os.path.join("figures", "reinvent2_logo_modified.jpeg")  
# st.logo(logo_path)
st.image(image_path, caption=f"REINVENT logo used in the REINVENT 2.0 paper")

### Titel 
st.title("Analysis")
st.sidebar.header("Content", divider="gray")

### Tabs 
overview, mols, results = st.tabs(["General Overview", "Input Molecules", "Results Summary"])




##################
#### Overview ####
##################
with overview:
    st.header("General Overview", divider="gray")
    st.sidebar.subheader("General Overview")

    st.write(
        """
            This page contains some tools that may be helpful for the user in generating the desired input file 
            for a REINVENT calculation. It contains the following tools:
            - **Input Molecules**: visualize input molecules from a SMILES or SDF file. Accepts tow type of SMILES:
                - **Basic**: normal SMILES in each line
                    - **Example**: C1CC(CCC1C2=CNC3=C2C=CC=N3)NC(=O)C4=CC=CN(C4=O)CC5=CC(=C(C=C5)F)F
                - **Warheads**: Each line must contain the two warheads to be linked separated by the pipe symbol '|'. Each warhead 
                must be annotated with '\*' to locate the attachment points.
                    - **Example**: Oc1cncc(*)c1|*c1ccoc1
            - **Results Summary**: Inspect the CSV results summary file and select desired columns.
        """)




########################
### Input Molecules ###
########################
with mols:
    st.header("Input Molecules", divider="gray")
    st.sidebar.subheader("Input Molecules")

    smi_type = st.selectbox("Select kind of SMILES file", ["Basic", "Warheads"], index=0, 
                            help="The SMILES file must contain only the SMILES without any headers, comments, or mutliple columns!")
    smi_file = st.file_uploader("Upload SMILES File", type=["smi", "sdf"], #key=key+"_smiles_file", 
                                help="SMILES (.smi) and Structures Data File (.sdf) are the **ONLY** accepted format.")
    if smi_file:
        file_name = smi_file.name
        if (".sdf" in file_name): 
                smi_file = convert_sdf_smi(smi_file)
                
        if smi_type == "Basic": 
            df = pd.read_csv(smi_file, names=["SMILES"], header=None)
            df["Structure"] = df["SMILES"].apply(smi_to_png)
            st.write(f"Number of molecules contained in the SMILES file: **{len(df['SMILES'])}**.")
            cols = st.multiselect(label="Select Columns", options=list(df.columns), default=list(df.columns), placeholder="Choose columns...", 
                            help="Choose the columns you want to have in your table.") 
            st.dataframe(df, column_config={"Structure": st.column_config.ImageColumn(width="medium")}, key="df_basic")

        elif smi_type == "Warheads": 
            df = pd.read_csv(smi_file, names=["SMILES"], header=None)
            warheads_modified = []
            for smi in df["SMILES"]:
                warheads_modified.append(smi.replace("(*)", "[*]").replace("|*", "|[*]"))
            warheads1 = []
            warheads2 = []
            for smi in warheads_modified:
                wh1, wh2 = smi.split("|")
                warheads1.append(wh1)
                warheads2.append(wh2)
            df["SMILES"] = warheads_modified
            df["Warhead1 SMILES"] = warheads1
            df["Warhead2 SMILES"] = warheads2
            #df["Structure"] = df["SMILES"].apply(smi_to_png)
            df["Warhead1 Structure"] = df["Warhead1 SMILES"].apply(smi_to_png)
            df["Warhead2 Structure"] = df["Warhead2 SMILES"].apply(smi_to_png)
            st.write(f"Number of molecules contained in the SMILES file: **{len(df['SMILES'])}**.", key="write")
            cols = st.multiselect(label="Select Columns", options=list(df.columns), default=list(df.columns), placeholder="Choose columns...", 
                            help="Choose the columns you want to have in your table.") 
            st.dataframe(df, column_config={"Warhead1 Structure": st.column_config.ImageColumn(width="medium"), "Warhead2 Structure": st.column_config.ImageColumn(width="medium")}, key="df_warheads")




#########################
#### Results Summary ####
#########################
with results:
    st.header("Results Summary", divider="gray")
    st.sidebar.subheader("Results Summary")

    run_mode = st.selectbox("Select Run Mode", ["Reinforcement Learning/Staged Learning (RL/SL)", "Transfer Learning (TL)", "Sampling", "Scoring"], index=0)
    if (run_mode != "Scoring") and (run_mode != "Reinforcement Learning/Staged Learning (RL/SL)"): 
            mol_gen = st.selectbox("Type of Molecule Generator", ["Reinvent", "LibInvent", "LinkInvent", "Mol2Mol"])
    csv_file = st.file_uploader("Upload Summary File", type=["csv"],  
                                help="Upload the the results summary file of the REINVENT calculation (CSV is the **ONLY** accepted format).")
    if csv_file != None: 
        
        # Scoring & Sampling (Reinvent)
        if (run_mode == "Scoring") or (run_mode == "Sampling" and mol_gen == "Reinvent"):
            df = pd.read_csv(csv_file, index_col=False)
            df["Structure"] = df["SMILES"].apply(smi_to_png)
            cols = st.multiselect(label="Select Columns", options=list(df.columns), default=list(df.columns), placeholder="Choose columns...", 
                                    help="Choose the columns you want to have in your table.") 
            st.dataframe(df[cols], column_config={"Structure": st.column_config.ImageColumn(width="medium")})
        
        # Sampling (LinkInvent, LibInvent, Mol2Mol)
        elif run_mode == "Sampling":
            # LibInvent
            if mol_gen == "LibInvent":
                df = pd.read_csv(csv_file)
                df["Structure"] = df["SMILES"].apply(smi_to_png)
                df["Scaffold Structure"] = df["Scaffold"].apply(smi_to_png)
                df["R-groups Structure"] = df["R-groups"].apply(smi_to_png)
                cols = st.multiselect(label="Select Columns", options=list(df.columns), default=list(df.columns), placeholder="Choose columns...", 
                                        help="Choose the columns you want to have in your table.") 
                st.dataframe(df[cols], column_config={"Structure": st.column_config.ImageColumn(width="medium"), "Scaffold Structure": st.column_config.ImageColumn(width="medium"), 
                                                      "R-groups Structure": st.column_config.ImageColumn(width="medium")})
                
            # LinkInvent
            elif mol_gen == "LinkInvent":
                df = pd.read_csv(csv_file)
                warheads_modified = []
                for smi in df["Warheads"]:
                    warheads_modified.append(smi.replace("(*)", "[*]").replace("|*", "|[*]"))
                warheads1 = []
                warheads2 = []
                for smi in df["Warheads"]:
                    wh1, wh2 = smi.split("|")
                    warheads1.append(wh1)
                    warheads2.append(wh2)
                df["Warheads"] = warheads_modified
                df["Warhead1"] = warheads1
                df["Warhead2"] = warheads2
                df["Structure"] = df["SMILES"].apply(smi_to_png)
                df["Warhead1 Structure"] = df["Warhead1"].apply(smi_to_png)
                df["Linker Structure"] = df["Linker"].apply(smi_to_png)
                df["Warhead2 Structure"] = df["Warhead2"].apply(smi_to_png)
                cols = st.multiselect(label="Select Columns", options=list(df.columns), default=list(df.columns), placeholder="Choose columns...", 
                                        help="Choose the columns you want to have in your table.") 
                st.dataframe(df[cols], column_config={"Structure": st.column_config.ImageColumn(width="medium"), "Warhead1 Structure": st.column_config.ImageColumn(width="medium"), 
                                                      "Linker Structure": st.column_config.ImageColumn(width="medium"), "Warhead2 Structure": st.column_config.ImageColumn(width="medium")})
            
            # Mol2Mol
            elif mol_gen == "Mol2Mol":
                df = pd.read_csv(csv_file)
                df["Structure"] = df["SMILES"].apply(smi_to_png)
                df["Input Structure"] = df["Input_SMILES"].apply(smi_to_png)
                df.sort_values(by=["Input_SMILES"], ascending=[True], inplace=True)
                cols = st.multiselect(label="Select Columns", options=list(df.columns), default=list(df.columns), placeholder="Choose columns...", 
                                        help="Choose the columns you want to have in your table.") 
                st.dataframe(df[cols], column_config={"Structure": st.column_config.ImageColumn(width="medium"), "Input Structure": st.column_config.ImageColumn(width="medium")})

        # Transfer Learning (TL)
        elif run_mode == "Transfer Learning (TL)":
            # Mol2Mol
            if mol_gen == "Mol2Mol":
                df = pd.read_csv(csv_file)
                df["Source_Mol"] = df["Source_Mol"].apply(smi_to_png)
                df["Target_Mol"] = df["Target_Mol"].apply(smi_to_png)
                df.sort_values(by=["Target_Mol"], ascending=[True], inplace=True)
                cols = st.multiselect(label="Select Columns", options=list(df.columns), default=list(df.columns), placeholder="Choose columns...", 
                                        help="Choose the columns you want to have in your table.") 
                st.dataframe(df[cols], column_config={"Source_Mol": st.column_config.ImageColumn(width="medium"), "Target_Mol": st.column_config.ImageColumn(width="medium")})

        # Reinforcement Learning/Staged Learning (RL/SL) 
        elif run_mode == "Reinforcement Learning/Staged Learning (RL/SL)":
            df = pd.read_csv(csv_file)
            df["Structure"] = df["SMILES"].apply(smi_to_png)
            cols = st.multiselect(label="Select Columns", options=list(df.columns), default=list(df.columns), placeholder="Choose columns...", 
                                    help="Choose the columns you want to have in your table.") 
            st.dataframe(df[cols], column_config={"Structure": st.column_config.ImageColumn(width="medium")})