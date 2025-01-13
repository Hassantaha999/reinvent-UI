############################
###### Python Modules ###### 
############################
import streamlit as st
import os
from datetime import datetime
from pathlib import Path
import pandas as pd
from functions import *
from data import * 


###########################
###### General Setup ###### 
###########################
### Setting page configurations
st.set_page_config(
    page_title="Reinvent App",
    page_icon=":open_file_folder:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
            #'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "mailto:hassanabdel999@gmail.com",
            'About': "## REINVENT UI"}
)

### Create a unique sub-folder for each user in the temp_files folder 
pwd = os.getcwd()                            # Path for Parent Working Directory (Dir: REINVENT Streamlit)
BASE_DIR = os.path.join(pwd, "temp_files")   # Base directory for temporary files
Path(BASE_DIR).mkdir(exist_ok=True)          # Create the base directory if it doesn't exist
if "user_folder" not in st.session_state:
    # Use the current time to create a unique identifier (formatted as User_YYYY-MM-DD-HH-MM-SS)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    user_folder = os.path.join(BASE_DIR, f"user_{timestamp}")
    Path(user_folder).mkdir(exist_ok=True)
    st.session_state.user_folder = user_folder
else:
    user_folder = st.session_state.user_folder

### Clean temp_files sub-folders 
clean_temp_folder = True    # Whether to clean up folder (to save disk space) or not
age_limit = 30              # Clean up folders that are older than a specific time frame (e.g., 30 day) 
if clean_temp_folder:
    clean_folder(BASE_DIR, age_limit=age_limit)

### To save the changes made in UI across a multi-page streamlit app 
for key in st.session_state:
    st.session_state[key] = st.session_state[key]

### Initialize the change_param_dict (to saves the UI state) for the different run modes
if "change_param_dict" not in st.session_state:
    st.session_state["change_param_dict"] = {state_dict_UI[run_mode][param]: True for run_mode in state_dict_UI.keys() for param in state_dict_UI[run_mode].keys()}


#########################
###### REINVENT UI ######
#########################
### Abbvie Logo & Image
# logo_path = os.path.join("figures", "reinvent2_logo_modified.jpeg")    
image_path = os.path.join("figures", "reinvent2_logo_modified.jpeg")  
# st.logo(logo_path)
st.image(image_path, caption=f"REINVENT logo used in the REINVENT 2.0 paper")

### Titel of UI 
st.title("Input File Generation")

### Sidebar for General Options
with st.sidebar:
    ## Save & Load UI State widgets
    save, load = st.columns([0.5, 0.5], gap="small", vertical_alignment="top")
    # Save State: save the current UI state defined by the user to a json file. 
    ### (At the end of this script!) ###
    # Load State: load a previously defined UI state by the user from a json file. 
    with load.popover("Load UI State"): 
        state = False
        state_dict = None
        state_file = st.file_uploader("Upload UI State File", type=["json"], help="**JSON** file format is the only accepted format.")
        if state_file:
            state = True
            state_dict = load_state(state_file)
        else:
            st.session_state["change_param_dict"] = {state_dict_UI[run_mode][param]: True for run_mode in state_dict_UI.keys() for param in state_dict_UI[run_mode].keys()}
    ## User experience 
    modus = st.radio("Select Mode", ("Basic", "Advanced"), index=0, key="modus")
    modus = change_param(modus, st.session_state["change_param_dict"], state_dict, state, "modus")  # UI State
    ## Reinvent run mode 
    run_mode = st.selectbox("Select Run Mode", ["Reinforcement Learning (RL)", "Staged Learning (SL)", 
                                                "Transfer Learning (TL)", "Sampling", "Scoring"], index=0, key="run_mode")
    run_mode = change_param(run_mode, st.session_state["change_param_dict"], state_dict, state, "run_mode")  # UI State
    ## Number of stages for Staged Learning run mode 
    if run_mode == "Staged Learning (SL)":
        num_stages = st.number_input("Number of Stages", value=2, min_value=1, max_value=None, step=1, key=f"{run_mode_prefix[run_mode]}_num_stages")
        num_stages = change_param(num_stages, st.session_state["change_param_dict"], state_dict, state, f"{run_mode_prefix[run_mode]}_num_stages")  # UI State
    ## TOML input file name
    toml_name = st.text_input("Name of Toml Input File", value=f"{run_mode_prefix[run_mode]}_input", key=f"{run_mode_prefix[run_mode]}_toml_file")
    ## Run Mode Info & Reset values widgets
    mode_info, reset = st.columns([0.55, 0.45], gap="small", vertical_alignment="top")
    ## Reset button: reset the values of the different widgets to the default values (only for widgets where this is possible!)
    if reset.button("Reset Values"):
        reset_values(run_mode)

### Main Content of the Reinvent UI App 
## Create 2 columns (1st col (left): input options, 2nd col (right): preview of the input file)
col1, col2 = st.columns([0.50, 0.50], gap="large", vertical_alignment="top")

## Input Options 
col1.divider()
col1.header("Input Options")

## Preview of TOML Input File 
col2.divider()
col2.header("Preview of Input File")

###############################
###### Scoring Run Mode #######
###############################
if run_mode == "Scoring":

    # Sidebar options
    with st.sidebar:
        # Run mode info 
        with mode_info.popover("Run Mode Info"):
            st.write("""In the scoring run mode of REINVENT4, input SMILES strings are evaluated using a customizable scoring function, 
                        and the results are saved in a CSV file with columns for SMILES, total score, and individual component scores 
                        in both raw and transformed forms. The scoring function combines weighted components, either as a weighted 
                        sum or product, with user-defined weights determining the relative importance of each component.""")

    # Name of Toml input file 
    toml_input = Path(st.session_state['user_folder']) / f"{toml_name}.toml"
    if toml_input.exists():
        toml_input.unlink() # Remove the file cross-platform

    # Uploaded files 
    uploaded_files = {"TOML Input": toml_input, "Scoring SMILES": None}

    # Needed files 
    needed_files = {"TOML Input": True, "Scoring SMILES": False}

    # Titel 
    write_show(f"\### REINVENT4 TOML input ###\n", toml_input, col2)
    write_show(f"\### Scoring Run Mode ###\n", toml_input, col2, empty_line=True)

    # General options
    with col1.expander("**General Options**"):
        write_show('\# General Input\n', toml_input, col2)
        write_show('run_type = "scoring"\n', toml_input, col2)
        if modus == "Advanced":
            use_cuda = st.selectbox("Run on GPU?", ["true", "false"], index=0, key=f"{run_mode}_use_cuda")
            use_cuda = change_param(use_cuda, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_use_cuda")  # UI State
            write_show(f'use_cuda = {use_cuda}\n', toml_input, col2)
        else:
            write_show(f'use_cuda = true\n', toml_input, col2)
        json_file = st.text_input("Name of the Json input file", value="Scoring_input", key=f"{run_mode}_json_file") 
        json_file = change_param(json_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_json_file")  # UI State
        write_show(f'json_out_config = "{json_file}.json"\n', toml_input, col2, empty_line=True)

    # Run Mode Parameters
    with col1.expander("**Run Mode Parameters**"):
        write_show('\# Parameters for Calculation\n', toml_input, col2)
        write_show('[parameters]\n', toml_input, col2)
        smiles_name = st.text_input("Name of file with list of SMILES to score (.smi)", value="to_score", help="1 molecule per line", key=f"{run_mode}_smiles_file")
        smiles_name = change_param(smiles_name, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_smiles_file")  # UI State
        # Upload SMILES File 
        smi_path, smi_name = SMILES_file(run_mode, run_mode)
        if smi_path != None: 
            smiles_name = smi_name
            uploaded_files["Scoring SMILES"] = smi_path
            needed_files["Scoring SMILES"] = True
        else:
            smiles_name += ".smi"
        output_csv = st.text_input(label="Name of output file (.csv)", value="scored", key=f"{run_mode}_output_csv")
        output_csv = change_param(output_csv, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_output_csv")  # UI State
        write_show(f'smiles_file = "{smiles_name}"\n', toml_input, col2)
        write_show(f'output_csv = "{output_csv}.csv"\n', toml_input, col2, empty_line=True)
    
    # Scoring Components
    with col1.expander("**Scoring Components Parameters**"):
        scor_comp = scoring_components(toml_input, col2, state_dict, state, modus=modus, 
                                       needed_files=needed_files, uploaded_files=uploaded_files, 
                                       gen_scoring_file=False, key=run_mode)
        # Upload Scoring File 
        if scor_comp != None: 
            if type(scor_comp) == str:
                needed_files["Scoring File"] = False
            else:
                uploaded_files["Scoring File"] = scor_comp
                needed_files["Scoring File"] = True

    # Additional options 
    with col1.expander("**Additional Options**"):
        # Bash File 
        bash_name = bash_script(run_mode, state_dict, state)
        if bash_name != None: 
            uploaded_files["Bash Run Script"] = bash_name
        else:
            # Remove Bash Script File if option was set to false 
            bash_path = Path(st.session_state["user_folder"]) / f"run_script_{run_mode}.sh"
            if bash_path.exists():
                bash_path.unlink()  

    # Download Fles 
    col1.divider()
    col1.subheader("Download Files")
    download_files(uploaded_files, col1)

    # Summary of Needed Files 
    col1.divider()
    col1.subheader("Summary of Files")
    needed_files = {
        "File": list(needed_files.keys()),
        "Status": list(needed_files.values())      
    }
    df = pd.DataFrame(needed_files)
    edited_data = col1.data_editor(df, num_rows="fixed", hide_index=True, column_config={
                "File": st.column_config.TextColumn(
                "File",
                help="Files needed for REINVENT calculation",
                width="large",
                default=False,
                disabled=True,
                ),
                "Status": st.column_config.CheckboxColumn(
                "Status",
                help="Status of needed files",
                width="small",
                default=False,
                disabled=True
                )
            })   




## Sampling Run Mode
if run_mode == "Sampling":

    # Sidebar options
    with st.sidebar:
        with mode_info.popover("Run Mode Info"):
            st.write("""Sampling generates SMILES from a starting model, which can be one of the priors provided by REINVENT or 
                        a model previously generated using RL or TL. It is important to note that this run mode does not involve 
                        scoring or reinforcement learning (RL), so the agent is not updated during the process. Therefore, 
                        instead of using "prior" or "agent," this mode simply uses "model_file".""")

    # Name of Toml input file 
    toml_input = Path(st.session_state['user_folder']) / f"{toml_name}.toml"
    if toml_input.exists():
        toml_input.unlink() # Remove the file cross-platform

    # Uploaded Files 
    uploaded_files = {"TOML Input": toml_input, "Model": None, "SMILES": None}

    # Needed Files 
    needed_files = {"TOML Input": True, "Model": False}

    # Titel 
    write_show(f"\### REINVENT4 TOML input ###\n", toml_input, col2)
    write_show(f"\### Sampling Run Mode ###\n", toml_input, col2, empty_line=True)

    # General Options
    with col1.expander("**General Options**"):
        write_show('\# General Options\n', toml_input, col2)
        write_show('run_type = "sampling"\n', toml_input, col2)
        if modus == "Advanced":
            use_cuda = st.selectbox("Run on GPU?", ["true", "false"], index=0, key=f"{run_mode}_use_cuda")
            use_cuda = change_param(use_cuda, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_use_cuda")  # UI State
            write_show(f'use_cuda = {use_cuda}\n', toml_input, col2)
        else:
            write_show(f'use_cuda = true\n', toml_input, col2)
        json_file = st.text_input("Name of the Json input file", value="Sampling_input", key=f"{run_mode}_json_file")
        json_file = change_param(json_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_json_file")  # UI State
        write_show(f'json_out_config = "{json_file}.json"\n', toml_input, col2, empty_line=True)

    # Generic Parameters
    with col1.expander("**Run Mode Parameters**"):
        #tb_logdir = st.text_input("Name of the TensorBoard logging directory", "TensorBoard_Sampling", key=f"{run_mode}_tb_logs")
        #tb_logdir = change_param(tb_logdir, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_tb_logs")  # UI State
        output_file = st.text_input("Name of the output file", value="sampling", key=f"{run_mode}_output_csv", 
                                    help="Name of the CSV file with samples SMILES and NLLs.")
        output_file = change_param(output_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_output_csv")  # UI State
        num_smiles = st.number_input("Number of output molecules", min_value=0, max_value=None, value=100, step=1, key=f"{run_mode}_num_smiles",
                                     help="Number of SMILES to sample.\n\n **Note**: This is multiplied by the number of input SMILES.")
        num_smiles = change_param(num_smiles, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_num_smiles")  # UI State
        if modus == "Advanced":
            unique_molecules = st.selectbox("Remove all duplicated canonicalized SMILES?", ["true", "false"], index=0, key=f"{run_mode}_unique_molecules",
                                            help="If 'true' only return unique canonicalized SMILES.")
            unique_molecules = change_param(unique_molecules, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_unique_molecules")  # UI State
            randomize_smiles = st.selectbox("Shuffle atoms in SMILES randomly?", ["true", "false"], index=0, key=f"{run_mode}_randomize_smiles",
                                            help="If 'true' shuffle atoms in input SMILES randomly.")
            randomize_smiles = change_param(randomize_smiles, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_randomize_smiles")  # UI State
        else:
            unique_molecules = "true"
            randomize_smiles = "true"
        write_show('[parameters]\n', toml_input, col2)
        write_show('\# Generic Parameters\n', toml_input, col2)
        #write_show(f'tb_logdir = "{tb_logdir}"\n', toml_input, col2)
        write_show(f'output_file = "{output_file}.csv"\n', toml_input, col2)
        write_show(f'num_smiles = {num_smiles}\n', toml_input, col2)
        write_show(f'unique_molecules = {unique_molecules}\n', toml_input, col2)
        write_show(f'randomize_smiles = {randomize_smiles}\n', toml_input, col2, empty_line=True)

    # Molecule Generators
    with col1.expander("**Molecule Generator**"):
        # mol_generator(toml_input, col2, state_dict, state, needed_files=needed_files, uploaded_files=uploaded_files, key=run_mode)
        mol_gen = st.selectbox("Type of Molecule Generator", ["Reinvent", "LibInvent", "LinkInvent", "Mol2Mol"], index=0, key=f"{run_mode}_mol_gen",
                            help="""The prior models provided by REINVENT are the default models, but other 
                                    models obtained by transfer learning (TL) or reinforcement learning (RL) could also be used.""")
        mol_gen = change_param(mol_gen, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_mol_gen")  # UI State
        # Reinvent Generator
        if mol_gen == "Reinvent":
            model = "reinvent.prior"    
            model_type = st.toggle("Upload external model", value=False, key=f"{run_mode}_{mol_gen}_ext_model",
                                help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_ext_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Model File", type=["model", "chkpt", "prior"],
                                                help="Upload another RL/TL model.")
                if model_file:
                    model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    uploaded_files["Model"] = model_file
                    needed_files["Model"] = True
            else:
                uploaded_files["Model"] = os.path.join(pwd, "prior_models", model)
                needed_files["Model"] = True
        # Other Generator
        else:
            # LibInvent Generator
            if mol_gen == "LibInvent":
                model = "libinvent.prior"    
                model_type = st.toggle("Upload external model", value=False, key=f"{run_mode}_{mol_gen}_ext_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
                model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_ext_model")  # UI State
                if model_type: 
                    # Upload Model File
                    model_file = st.file_uploader("Upload Model File", type=["model", "chkpt", "prior"],
                                                help="Upload another RL/TL model.")
                    if model_file:
                        model = model_file.name
                        model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                        uploaded_files["Model"] = model_file
                        needed_files["Model"] = True
                else:
                    uploaded_files["Model"] = os.path.join(pwd, "prior_models", model)
                    needed_files["Model"] = True

                smiles_file = st.text_input("Name of SMILES file", "scaffold", key=f"{run_mode}_{mol_gen}_smi_file",
                                            help="""One scaffold per line. Each scaffold must be 
                                            annotated by '\*' to locate the attachment points. Up to 4 attachments points are allowed.\n\n **Example**: [\*:1]Cc2ccc1cncc(C[*:2])c1c2)""")    
                smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
                # Upload SMILES File 
                needed_files["SMILES"] = False
                smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}", run_mode, mol_gen=mol_gen)
                if smi_path != None: 
                    smiles_file = smi_name
                    uploaded_files["SMILES"] = smi_path
                    needed_files["SMILES"] = True
                else:
                    smiles_file += ".smi"
            # LinkInvent Generator
            elif mol_gen == "LinkInvent":
                model = "linkinvent.prior"    
                # Upload Model File
                model_type = st.toggle("Upload external model", value=False, key=f"{run_mode}_{mol_gen}_ext_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
                model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_ext_model")  # UI State
                if model_type: 
                    # Upload Model File
                    model_file = st.file_uploader("Upload Model File", type=["model", "chkpt", "prior"],
                                                help="Upload another RL/TL model.")
                    if model_file:
                        model = model_file.name
                        model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                        uploaded_files["Model"] = model_file
                        needed_files["Model"] = True
                else:
                    uploaded_files["Model"] = os.path.join(pwd, "prior_models", model)
                    needed_files["Model"] = True

                smiles_file = st.text_input("Name of SMILES file", "warhead", help="""Each line must contain the two warheads to be 
                                linked separated by the pipe symbol '|'. Each warhead must be annotated with '\*' to locate 
                                the attachment points.\n\n **Example**: Oc1cncc(*)c1|*c1ccoc1""", key=f"{run_mode}_{mol_gen}_smi_file")
                smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
                # Upload SMILES File 
                needed_files["SMILES"] = False
                smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}", run_mode, mol_gen=mol_gen)
                if smi_path != None: 
                    smiles_file = smi_name
                    uploaded_files["SMILES"] = smi_path
                    needed_files["SMILES"] = True
                else:
                    smiles_file += ".smi"
            # Mol2Mol Generator
            elif mol_gen == "Mol2Mol":
                #tb_dir = st.text_input("Name of the TensorBoard logging directory", "tb_logs", key=f"{run_mode}_{mol_gen}_tb_logs")
                #tb_dir = change_param(tb_dir, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_tb_logs")  # UI State
                model = st.selectbox("Select prior model", ["mol2mol_similarity", "mol2mol_medium_similarity",
                                                            "mol2mol_high_similarity", "mol2mol_mmp",
                                                            "mol2mol_scaffold", "mol2mol_scaffold_generic"], index=0, key=f"{run_mode}_{mol_gen}_model_type")
                model = change_param(model, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_model_type")  # UI State
                mol2mol = model 
                # Upload Model File
                model_type = st.toggle("Upload external model", value=False, key=f"{run_mode}_{mol_gen}_ext_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
                model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_ext_model")  # UI State
                if model_type: 
                    model_file = st.file_uploader("Upload Model File", type=["model", "chkpt", "prior"],
                                                help="Upload another RL/TL model.")
                    if model_file:
                        model = model_file.name
                        model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                        uploaded_files["Model"] = model_file
                        needed_files["Model"] = True
                else:
                    model += ".prior"
                    uploaded_files["Model"] = os.path.join(pwd, "prior_models", model)
                    needed_files["Model"] = True  
                # SMILES File 
                smiles_file = st.text_input("Name of SMILES file", "input_molecules", help="1 compound per line.", key=f"{run_mode}_{mol_gen}_smi_file")
                smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
                # Upload SMILES File 
                needed_files["SMILES"] = False
                smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}", run_mode, mol_gen=mol_gen, mol2mol=mol2mol)
                if smi_path != None: 
                    smiles_file = smi_name
                    uploaded_files["SMILES"] = smi_path
                    needed_files["SMILES"] = True
                else:
                    smiles_file += ".smi"
                # Sampling Strategy
                st.write("**Sampling Strategy**")
                sample_strategy = st.selectbox("Algorithm", ["multinomial", "beamsearch"], index=0, key=f"{run_mode}_{mol_gen}_sample_strategy",
                                                help="""Two sample strategies are implemented in REINVENT 4: **multinomial** and **beam search**. 
                                                        Generally, multinomial is more “explorative” compared to beam search which is deterministic. 
                                                        Multinomial sampling is recommended for RL, whereas beam search can be very powerful for sampling.""")
                sample_strategy = change_param(sample_strategy, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_sample_strategy")  # UI State
                if sample_strategy == "beamsearch":
                    temperature = st.number_input("Temperature", min_value=0.0, max_value=None, value=1.0, step=1.0, key=f"{run_mode}_{mol_gen}_temperature",
                                                    help="""Higher temperature setting allows beam search to explore a greater variety of 
                                                            candidate sequence paths through the token graph. A lower temperature setting 
                                                            makes it increasingly focus on the most likely predictions at each step.""")
                    temperature = change_param(temperature, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_temperature")  # UI State
                else:
                   distance_threshold = st.number_input("Distance threshold", min_value=0, max_value=None, value=100, step=1, key=f"{run_mode}_{mol_gen}_distance_threshold")
                   distance_threshold = change_param(distance_threshold, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_distance_threshold")  # UI State
                
        # Write to the TOML input file 
        write_show(f'\# {mol_gen} Generator Parameters\n', toml_input, col2)
        write_show(f'model_file = "{model}"\n', toml_input, col2)
        if mol_gen in ["LibInvent", "LinkInvent", "Mol2Mol"]:
            write_show(f'smiles_file = "{smiles_file}"\n', toml_input, col2)
            if mol_gen == "Mol2Mol":
                write_show(f'sample_strategy = "{sample_strategy}"\n', toml_input, col2)
                if sample_strategy == "beamsearch":
                    write_show(f'temperature = {temperature}\n', toml_input, col2, empty_line=True)
                else:
                    write_show(f"distance_threshold = {distance_threshold}\n", toml_input, col2, empty_line=True)

    # Additional options 
    with col1.expander("**Additional Options**"):
        # Bash File 
        bash_name = bash_script(run_mode, state_dict, state)
        if bash_name != None: 
            uploaded_files["Bash Run Script"] = bash_name
        else:
            # Remove Bash Script File if option was set to false 
            bash_path = Path(st.session_state["user_folder"]) / f"run_script_{run_mode}.sh"
            if bash_path.exists():
                bash_path.unlink()  

    # Download Fles 
    col1.divider()
    col1.subheader("Download Files")
    download_files(uploaded_files, col1)

    # Summary of Needed Files 
    col1.divider()
    col1.subheader("Summary of Files")
    needed_files = {
        "File": list(needed_files.keys()),
        "Status": list(needed_files.values())      
    }
    df = pd.DataFrame(needed_files)
    edited_data = col1.data_editor(df, num_rows="fixed", hide_index=True, column_config={
                "File": st.column_config.TextColumn(
                "File",
                help="Files needed for REINVENT calculation",
                width="large",
                default=False,
                disabled=True,
                ),
                "Status": st.column_config.CheckboxColumn(
                "Status",
                help="Status of needed files",
                width="small",
                default=False,
                disabled=True
                )
            })




## Transfer Learning (TL) Run Mode
if run_mode == "Transfer Learning (TL)":
    run_mode = run_mode_prefix[run_mode]
    # Sidebar options
    with st.sidebar:
        with mode_info.popover("Run Mode Info"):
            st.write("""Transfer Learning (TL) optimizes a more general model to generate molecules that are closer to a defined 
                        set of input molecules. The output is a new model file which can be used for RL or sampling. TL is not 
                        recommended to be used in combination with LibInvent and Linkinvent because both generators use constraints 
                        that leave only a small portion of the molecule to be optimizable.""")

    # Name of Toml input file 
    toml_input = Path(st.session_state['user_folder']) / f"{toml_name}.toml"
    if toml_input.exists():
        toml_input.unlink() # Remove the file cross-platform

    # Uploaded Files 
    uploaded_files = {"TOML Input": toml_input, "Model": None, "SMILES": None, "Validation SMILES": None}
    
    # Needed Files 
    needed_files = {"TOML Input": True, "Model": False, "SMILES": False, "Validation SMILES": False} 

    # Titel 
    write_show(f"\### REINVENT4 TOML input ###\n", toml_input, col2)
    write_show(f"\### Transfer Learning (TL) Run Mode ###\n", toml_input, col2, empty_line=True)

    # General Options
    with col1.expander("**General Options**"):
        write_show('\# General Options\n', toml_input, col2)
        write_show('run_type = "transfer_learning"\n', toml_input, col2)
        if modus == "Advanced":
            use_cuda = st.selectbox("Run on GPU?", ["true", "false"], index=0, key=f"{run_mode}_use_cuda")
            use_cuda = change_param(use_cuda, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_use_cuda")  # UI State
            #number_of_cpus = st.number_input(value=1, min_value=1, max_value=None, label="Number of CPUs for pair generation", step=1, f"{run_mode}_num_cpus")
            #number_of_cpus = change_param(number_of_cpus, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_num_cpus")  # UI State
            write_show(f'use_cuda = {use_cuda}\n', toml_input, col2)
            #write_show(f'number_of_cpus = {number_of_cpus}\n', toml_input, col2)
        else:
            write_show(f'use_cuda = true\n', toml_input, col2)
            #write_show(f'number_of_cpus = 1\n', toml_input, col2)
        tb_dir = st.text_input("Name of the TensorBoard Logging Directory", value="TensoBoard_TL", key=f"{run_mode}_tb_dir")
        tb_dir = change_param(tb_dir, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_tb_dir")  # UI State
        json_file = st.text_input("Name of the Json input file", value="TL_input", key=f"{run_mode}_json_file")
        json_file = change_param(json_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_json_file")  # UI State
        write_show(f'tb_logdir = "{tb_dir}"\n', toml_input, col2)
        write_show(f'json_out_config = "{json_file}.json"\n', toml_input, col2, empty_line=True)

    write_show('[parameters]\n', toml_input, col2, empty_line=False)

    # Parameters
    with col1.expander("**Run Mode Parameters**"):
        # Input Widgets
        num_epochs = st.number_input("Number of steps (epochs) to train the prior model", min_value=0, max_value=None, value=10, step=1, key=f"{run_mode}_num_epochs")
        num_epochs = change_param(num_epochs, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_num_epochs")  # UI State
        save_every_n_epochs = st.number_input("Save checkpoint model file every N steps (epochs)", min_value=0, max_value=None, value=5, step=1, key=f"{run_mode}_save_epochs")
        save_every_n_epochs = change_param(save_every_n_epochs, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_save_epochs")  # UI State
        batch_size = st.number_input("How many molecules are generated in each step (epoch)", min_value=0, max_value=None, value=128, step=1, key=f"{run_mode}_batch_size")
        batch_size = change_param(batch_size, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_batch_size")  # UI State
        num_refs = st.number_input("Number of reference molecules randomly chosen for similarity", min_value=0, max_value=None, value=50, step=1, key=f"{run_mode}_num_refs",
                                   help="Must be 0 for large datasets (>200 molecules).")
        num_refs = change_param(num_refs, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_num_refs")  # UI State
        sample_batch_size = st.number_input("Number of sampled molecules to compute sample loss", min_value=0, max_value=None, value=100, step=1, key=f"{run_mode}_sample_batch_size")
        sample_batch_size = change_param(sample_batch_size, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_sample_batch_size")  # UI State
        # Write to TOML input file
        write_show('\# TL Parameters\n', toml_input, col2)
        write_show(f'num_epochs = {int(num_epochs)}\n', toml_input, col2,)
        write_show(f'save_every_n_epochs = {int(save_every_n_epochs)}\n', toml_input, col2,)
        write_show(f'batch_size = {int(batch_size)}\n', toml_input, col2,)
        write_show(f'num_refs = {int(num_refs)}\n', toml_input, col2,)
        write_show(f'sample_batch_size = {int(sample_batch_size)}\n', toml_input, col2, empty_line=True)

    # Molecule Generator
    with col1.expander("**Molecule Generator**"):
        mol_gen = st.selectbox("Type of molecule generator", ["Reinvent", "LibInvent", "LinkInvent", "Mol2Mol"], index=0, key=f"{run_mode}_mol_gen")
        # Reinvent Generator
        if mol_gen == "Reinvent":
            input_model_file = "reinvent.prior"    
            model_type = st.toggle("Upload external model", value=False, key=f"{run_mode}_{mol_gen}_ext_model",
                                help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_ext_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Model File", type=["model", "chkpt", "prior"],
                                                help="Upload another RL/TL model.")
                if model_file:
                    input_model_file = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    uploaded_files["Model"] = model_file
                    needed_files["Model"] = True
            else:
                uploaded_files["Model"] = os.path.join(pwd, "prior_models", input_model_file)
                needed_files["Model"] = True
            # SMILES File 
            smiles_file = st.text_input("Name of SMILES file", "input_molecules", key=f"{run_mode}_{mol_gen}_smi_file",
                                        help="Read 1st column.")    
            smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
            # Upload SMILES File 
            needed_files["SMILES"] = False
            smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}", run_mode, mol_gen=mol_gen)
            if smi_path != None: 
                smiles_file = smi_name
                uploaded_files["SMILES"] = smi_path
                needed_files["SMILES"] = True
            else:
                smiles_file += ".smi"

        # LibInvent Generator
        elif mol_gen == "LibInvent":
            input_model_file = "libinvent.prior"    
            model_type = st.toggle("Upload external model", value=False, key=f"{run_mode}_{mol_gen}_ext_model",
                                   help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_ext_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Model File", type=["model", "chkpt", "prior"],
                                              help="Upload another RL/TL model.")
                if model_file:
                    input_model_file = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    uploaded_files["Model"] = model_file
                    needed_files["Model"] = True
            else:
                uploaded_files["Model"] =os.path.join(pwd, "prior_models", input_model_file)
                needed_files["Model"] = True

            smiles_file = st.text_input("Name of SMILES file", "input_molecules", key=f"{run_mode}_{mol_gen}_smi_file",
                                        help="Read first 2 columns: scaffold, R-groups.")    
            smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
            # Upload SMILES File 
            needed_files["SMILES"] = False
            smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}", run_mode, mol_gen=mol_gen)
            if smi_path != None: 
                smiles_file = smi_name
                uploaded_files["SMILES"] = smi_path
                needed_files["SMILES"] = True
            else:
                smiles_file += ".smi"

        # LinkInvent Generator
        elif mol_gen == "LinkInvent":
            input_model_file = "linkinvent.prior"    
            # Upload Model File
            model_type = st.toggle("Upload external model", value=False, key=f"{run_mode}_{mol_gen}_ext_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_ext_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Model File", type=["model", "chkpt", "prior"],
                                              help="Upload another RL/TL model.")
                if model_file:
                    input_model_file = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    uploaded_files["Model"] = model_file
                    needed_files["Model"] = True
            else:
                uploaded_files["Model"] = os.path.join(pwd, "prior_models", input_model_file)
                needed_files["Model"] = True

            smiles_file = st.text_input("Name of SMILES file", "input_molecules", help="Read first 2 columns: warheads, linker.", key=f"{run_mode}_{mol_gen}_smi_file")
            smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
            # Upload SMILES File 
            needed_files["SMILES"] = False
            smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}", run_mode, mol_gen=mol_gen)
            if smi_path != None: 
                smiles_file = smi_name
                uploaded_files["SMILES"] = smi_path
                needed_files["SMILES"] = True
            else:
                smiles_file += ".smi"

        # Mol2Mol Generator
        elif mol_gen == "Mol2Mol":
            input_model_file = st.selectbox("Select prior model", ["mol2mol_similarity", "mol2mol_medium_similarity",
                                                                   "mol2mol_high_similarity", "mol2mol_mmp",
                                                                   "mol2mol_scaffold", "mol2mol_scaffold_generic"], 
                                                                   index=0, key=f"{run_mode}_{mol_gen}_model_type")
            input_model_file = change_param(input_model_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_model_type")  # UI State
            mol2mol = input_model_file 
            # Upload Model File
            model_type = st.toggle("Upload external model", value=False, key=f"{run_mode}_{mol_gen}_ext_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_ext_model")  # UI State
            if model_type: 
                model_file = st.file_uploader("Upload Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    input_model_file = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    uploaded_files["Model"] = model_file
                    needed_files["Model"] = True
            else:
                input_model_file += ".prior"
                uploaded_files["Model"] = os.path.join(pwd, "prior_models", input_model_file)
                needed_files["Model"] = True  
            # SMILES File 
            smiles_file = st.text_input("Name of SMILES file", "input_molecules", help="Read 1st column.", key=f"{run_mode}_{mol_gen}_smi_file")
            smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
            # Upload SMILES File 
            needed_files["SMILES"] = False
            smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}", run_mode, mol_gen=mol_gen, mol2mol=mol2mol)
            if smi_path != None: 
                smiles_file = smi_name
                uploaded_files["SMILES"] = smi_path
                needed_files["SMILES"] = True
            else:
                smiles_file += ".smi"

        # Output model file 
        output_model_file = st.text_input("Name of output model", value=f"TL_{mol_gen}", key=f"{run_mode}_{mol_gen}_output_model")
        output_model_file = change_param(output_model_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_output_model")  # UI State
        # Validation SMILES File 
        validation_smiles_file = st.text_input("Name of validation SMILES file", value="validation_molecules", key=f"{run_mode}_{mol_gen}_validation_smiles")
        validation_smiles_file = change_param(validation_smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_validation_smiles")  # UI State
        needed_files["Validation SMILES"] = False
        if mol_gen == "Mol2Mol":
            smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}_validation", run_mode, title="Validation SMILES", mol_gen=mol_gen, mol2mol=mol2mol)
        else:
            smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}_validation", run_mode, title="Validation SMILES", mol_gen=mol_gen)
        if smi_path != None: 
            validation_smiles_file = smi_name
            uploaded_files["Validation SMILES"] = smi_path
            needed_files["Validation SMILES"] = True
        else:
            validation_smiles_file += ".smi"

        # Similarity's Type and Parameters
        if mol_gen == "Mol2Mol":
            st.write("**Similarity's Type and Parameters**")
            pairs_type = st.selectbox(label="Similarity type", options=["Tanimoto", "RefTversky", "FitTversky"], index=0, key=f"{run_mode}_{mol_gen}_pairs_type", disabled=True)
            #pairs_type = change_param(pairs_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_pairs_type")  # UI State
            pairs_upper_threshold = st.slider("Upper similarity threshold", min_value=0.0, max_value=1.0, value=1.0, step=0.01, key=f"{run_mode}_{mol_gen}_pairs_upper")
            pairs_upper_threshold = change_param(pairs_upper_threshold, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_pairs_upper")  # UI State
            pairs_lower_threshold = st.slider("Lower similarity threshold", min_value=0.0, max_value=1.0, value=0.7, step=0.01, key=f"{run_mode}_{mol_gen}_pairs_lower")
            pairs_lower_threshold = change_param(pairs_lower_threshold, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_pairs_lower")  # UI State
            pairs_min_cardinality = st.number_input("Minimum cardinality", min_value=1.0, max_value=None, value=1.0, step=1.0, key=f"{run_mode}_{mol_gen}_pairs_min")
            pairs_min_cardinality = change_param(pairs_min_cardinality, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_pairs_min")  # UI State
            pairs_max_cardinality = st.number_input("Maximum cardinality", min_value=1.0, max_value=None, value=199.0, step=1.0,
                                                    help="Maximum number of cmpds that can be compared with a certain one.", key=f"{run_mode}_{mol_gen}_pairs_max")
            pairs_max_cardinality = change_param(pairs_max_cardinality, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_pairs_max")  # UI State
        
        # Write to TOML input file 
        write_show(f'\# {mol_gen} molecule generator\n', toml_input, col2)
        write_show(f'input_model_file = "{input_model_file}"\n', toml_input, col2)
        write_show(f'smiles_file = "{smiles_file}"\n', toml_input, col2)
        write_show(f'output_model_file = "{output_model_file}.model"\n', toml_input, col2)
        write_show(f'validation_smiles_file = "{validation_smiles_file}"\n', toml_input, col2, empty_line=True)
        if mol_gen == "Mol2Mol":
            write_show('\# Type of similarity and its parameters\n', toml_input, col2)
            write_show(f'pairs.type = "{pairs_type}"\n', toml_input, col2)
            write_show(f'pairs.upper_threshold = {pairs_upper_threshold}\n', toml_input, col2)
            write_show(f'pairs.lower_threshold = {pairs_lower_threshold}\n', toml_input, col2)
            write_show(f'pairs.min_cardinality = {int(pairs_min_cardinality)}\n', toml_input, col2)
            write_show(f'pairs.max_cardinality = {int(pairs_max_cardinality)}\n', toml_input, col2, empty_line=True)

    # Additional options 
    with col1.expander("**Additional Options**"):
        # Bash File 
        bash_name = bash_script(run_mode, state_dict, state)
        if bash_name != None: 
            uploaded_files["Bash Run Script"] = bash_name
        else:
            # Remove Bash Script File if option was set to false 
            bash_path = Path(st.session_state["user_folder"]) / f"run_script_{run_mode}.sh"
            if bash_path.exists():
                bash_path.unlink()  
    
    # Download Fles 
    col1.divider()
    col1.subheader("Download Files")
    download_files(uploaded_files, col1)

    # Summary of Needed Files 
    col1.divider()
    col1.subheader("Summary of Files")
    needed_files = {
        "File": list(needed_files.keys()),
        "Status": list(needed_files.values())      
    }
    df = pd.DataFrame(needed_files)
    edited_data = col1.data_editor(df, num_rows="fixed", hide_index=True, column_config={
                "File": st.column_config.TextColumn(
                "File",
                help="Files needed for REINVENT calculation",
                width="large",
                default=False,
                disabled=True,
                ),
                "Status": st.column_config.CheckboxColumn(
                "Status",
                help="Status of needed files",
                width="small",
                default=False,
                disabled=True
                )
            })
    



## Reinforcement Learning (RL) Run Mode
if run_mode == "Reinforcement Learning (RL)":
    run_mode = run_mode_prefix[run_mode]
    # Sidebar options
    with st.sidebar:
        with mode_info.popover("Run Mode Info"):
            st.write("""Reinforcement Learning (RL) is used to iteratively bias the molecules generated by an agent 
                        (normally a prior or TL agent) via a policy gradient scheme. The aim is to drive a pre-trained 
                        model such that the generated molecules satisfies a predefined property profile.""")

    # Name of Toml input file 
    toml_input = Path(st.session_state['user_folder']) / f"{toml_name}.toml"
    if toml_input.exists():
        toml_input.unlink() # Remove the file cross-platform

    # Uploaded Files 
    uploaded_files = {"TOML Input": toml_input, "Prior Model": None, "Agent Model": None}
    # Needed Files 
    needed_files = {"TOML Input": True, "Prior Model": False, "Agent Model": False}

    # Titel 
    write_show(f"\### REINVENT4 TOML input ###\n", toml_input, col2)
    write_show(f"\### Reinforcement Learning (RL) Run Mode ###\n", toml_input, col2, empty_line=True)
    
    # General Options
    with col1.expander("**General Options**"):
        write_show('\# General Options\n', toml_input, col2)
        write_show('run_type = "staged_learning"\n', toml_input, col2)
        if modus == "Advanced":
            use_cuda = st.selectbox("Run on GPU?", ["true", "false"], index=0, key=f"{run_mode}_use_cuda")
            use_cuda = change_param(use_cuda, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_use_cuda")  # UI State
            write_show(f'use_cuda = {use_cuda}\n', toml_input, col2)
        else:
            write_show(f'use_cuda = true\n', toml_input, col2)
        tb_dir = st.text_input("Name of the TensorBoard Logging Directory", value="TensorBoard_RL", key=f"{run_mode}_tb_dir")
        tb_dir = change_param(tb_dir, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_tb_dir")  # UI State
        json_file = st.text_input("Name of the Json input file", value="RL_input", key=f"{run_mode}_json_file")
        json_file = change_param(json_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_json_file")  # UI State
        write_show(f'tb_logdir = "{tb_dir}"\n', toml_input, col2)
        write_show(f'json_out_config = "{json_file}.json"\n', toml_input, col2, empty_line=True)

    write_show('[parameters]\n', toml_input, col2, empty_line=False)

    # Run Mode Parameters
    with col1.expander("**Run Mode Parameters**"):
        summary_csv_prefix = st.text_input("Prefix for the summary file", value="summary_RL", key=f"{run_mode}_summary_csv")
        summary_csv_prefix = change_param(summary_csv_prefix, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_summary_csv")  # UI State
        use_checkpoint = st.selectbox("Use checkpoint?", ["true", "false"], index=1,
                                      help="If 'true' use diversity filter from agent_file if present.", key=f"{run_mode}_use_checkpoint")
        use_checkpoint = change_param(use_checkpoint, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_use_checkpoint")  # UI State
        #purge_memories = st.selectbox("Purge all Diversity Filter Memories after each Stage?", ["true", "false"], index=0, key=f"{run_mode}_purge_memories")
        #purge_memories = change_param(purge_memories, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_purge_memories")  # UI State
        batch_size = st.number_input("Number of molecules generated per run (epoch)", min_value=0, max_value=None, value=128, step=1)
        batch_size = change_param(batch_size, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_batch_size")  # UI State
        if modus == "Advanced":
            unique_sequences = st.selectbox("Canonicalize output SMILES and remove duplicates after each step (epoch)?", ["true", "false"], index=0,
                                            help="If true remove all duplicates raw sequences in each step.", key=f"{run_mode}_unique_sequences")
            unique_sequences = change_param(unique_sequences, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_unique_sequences")  # UI State
            randomize_smiles = st.selectbox("Shuffle Atoms in SMILES Randomly?", ["true", "false"], index=0,
                                            help="If true shuffle atoms in SMILES randomly.", key=f"{run_mode}_randomize_smiles")
            randomize_smiles = change_param(randomize_smiles, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_randomize_smiles")  # UI State
        else:
            unique_sequences = "true"
            randomize_smiles = "true"
        write_show('\# RL Parameters\n', toml_input, col2)
        write_show(f'summary_csv_prefix = "{summary_csv_prefix}"\n', toml_input, col2)
        write_show(f'use_checkpoint = {use_checkpoint}\n', toml_input, col2)
        #write_show(f'purge_memories = {purge_memories}\n', toml_input, col2)
        write_show(f'batch_size = {int(batch_size)}\n', toml_input, col2)
        write_show(f'unique_sequences = {unique_sequences}\n', toml_input, col2)
        write_show(f'randomize_smiles = {randomize_smiles}\n', toml_input, col2, empty_line=True)
    
    # Molecule Generator
    with col1.expander("**Molecule Generator**"):
        mol_gen = st.selectbox("Type of molecule generator", ["Reinvent", "LibInvent", "LinkInvent", "Mol2Mol"], index=0, key=f"{run_mode}_mol_gen")
        mol_gen = change_param(mol_gen, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_mol_gen")  # UI State
        # Reinvent Generator        
        if mol_gen == "Reinvent":
            # Prior Model
            prior_model = "reinvent.prior"    
            model_type = st.toggle("Upload external prior model", value=False, key=f"{run_mode}_{mol_gen}_prior_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_prior_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Prior Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    prior_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    uploaded_files["Prior Model"] = model_file
                    needed_files["Prior Model"] = True
            else:
                uploaded_files["Prior Model"] = os.path.join(pwd, "prior_models", prior_model)
                needed_files["Prior Model"] = True
            # Agent Model
            agent_model = "reinvent.prior"    
            model_type = st.toggle("Upload external agent model", value=False, key=f"{run_mode}_{mol_gen}_agent_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_agent_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Agent Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    agent_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    if agent_model != prior_model:
                        uploaded_files["Agent Model"] = model_file
                    needed_files["Agent Model"] = True
            else:
                if agent_model != prior_model:
                    uploaded_files["Agent Model"] = os.path.join(pwd, "prior_models", agent_model)
                needed_files["Agent Model"] = True 
            # Inception Parameters
            inception = st.toggle("Inception?", value=False, key=f"{run_mode}_{mol_gen}_inception", 
                                  help="List of molecules provided by the user as SMILES strings to guide the reinforcement learning into the desired part of the chemical space.")
            inception = change_param(inception, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_inception")  # UI State
            if inception:
                st.markdown("**Inception Parameters**")
                # Inception SMILES File 
                smiles_file = st.text_input("Name of SMILES file for guidance", value="inception_molecules", help="1 molecule per line.", key=f"{run_mode}_{mol_gen}_smi_file")
                smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
                needed_files["Inception SMILES"] = False
                smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}_inception", run_mode, title="Inception SMILES", mol_gen=mol_gen)
                if smi_path != None: 
                    smiles_file = smi_name
                    uploaded_files["Inception SMILES"] = smi_path
                    needed_files["Inception SMILES"] = True
                else:
                    smiles_file += ".smi"
                memory_size = st.number_input("Number of total SMILES held in memory", min_value=0, max_value=None, value=100, step=1,
                                              help="""Top N scored molecules. As the RL run progresses and generates better molecules, 
                                              the initial inception molecules are removed from this memory and replaced by those with higher scores.""",
                                              key=f"{run_mode}_{mol_gen}_memory_size")
                memory_size = change_param(memory_size, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_memory_size")  # UI State
                sample_size = st.number_input("Number of SMILES randomly chosen after each epoch", min_value=0, max_value=None, value=10, step=1,
                                              help="Number of randomly sampled molecules from the memory to be used in computing the inception loss.",
                                              key=f"{run_mode}_{mol_gen}_sample_size")
                sample_size = change_param(sample_size, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_sample_size")  # UI State

        # LibInvent Generator
        elif mol_gen == "LibInvent":
            # Prior Model
            prior_model = "libinvent.prior"    
            model_type = st.toggle("Upload external prior model", value=False, key=f"{run_mode}_{mol_gen}_prior_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_prior_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Prior Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    prior_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    uploaded_files["Prior Model"] = model_file
                    needed_files["Prior Model"] = True
            else:
                uploaded_files["Prior Model"] = os.path.join(pwd, "prior_models", prior_model)
                needed_files["Prior Model"] = True
            # Agent Model
            agent_model = "libinvent.prior"    
            model_type = st.toggle("Upload external agent model", value=False, key=f"{run_mode}_{mol_gen}_agent_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_agent_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Agent Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    agent_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    if agent_model != prior_model:
                        uploaded_files["Agent Model"] = model_file
                    needed_files["Agent Model"] = True
            else:
                if agent_model != prior_model:
                    uploaded_files["Agent Model"] = os.path.join(pwd, "prior_models", agent_model)
                needed_files["Agent Model"] = True 
            # SMILES file 
            smiles_file = st.text_input("Name of SMILES file", "scaffolds", help="""One scaffold per line. Each scaffold must be 
                                        annotated by '\*' to locate the attachment points. Up to 4 attachments points are allowed. **Example**: [\*:1]Cc2ccc1cncc(C[*:2])c1c2)""", 
                                        key=f"{run_mode}_{mol_gen}_smi_file")   
            smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
            smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}", run_mode, mol_gen=mol_gen)
            needed_files[f"SMILES"] = False       
            if smi_path: 
                smiles_file = smi_name
                uploaded_files["SMILES"] = smi_path
                needed_files["SMILES"] = True
            else:
                smiles_file += ".smi"
        
        # LinkInvent Generator
        elif mol_gen == "LinkInvent":
            # Prior Model
            prior_model = "linkinvent.prior"    
            model_type = st.toggle("Upload external prior model", value=False, key=f"{run_mode}_{mol_gen}_prior_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_prior_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Prior Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    prior_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    uploaded_files["Prior Model"] = model_file
                    needed_files["Prior Model"] = True
            else:
                uploaded_files["Prior Model"] = os.path.join(pwd, "prior_models", prior_model)
                needed_files["Prior Model"] = True
            # Agent Model
            agent_model = "linkinvent.prior"    
            model_type = st.toggle("Upload external agent model", value=False, key=f"{run_mode}_{mol_gen}_agent_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_agent_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Agent Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    agent_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    if agent_model != prior_model:
                        uploaded_files["Agent Model"] = model_file
                    needed_files["Agent Model"] = True
            else:
                if agent_model != prior_model:
                    uploaded_files["Agent Model"] = os.path.join(pwd, "prior_models", agent_model)
                needed_files["Agent Model"] = True 
            # SMILES file 
            smiles_file = st.text_input("Name of SMILES file", "warheads", help="""Each line must contain the two warheads to be 
                                        linked separated by the pipe symbol. Each warhead must be annotated with '\*' to locate 
                                        the attachment points. **Example**: Oc1cncc(*)c1|*c1ccoc1""", 
                                        key=f"{run_mode}_{mol_gen}_smi_file")
            smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
            smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}", run_mode, mol_gen=mol_gen)
            needed_files[f"SMILES"] = False       
            if smi_path: 
                smiles_file = smi_name
                uploaded_files["SMILES"] = smi_path
                needed_files["SMILES"] = True
            else:
                smiles_file += ".smi"

        # Mol2Mol Generator
        elif mol_gen == "Mol2Mol":
            prior_model = st.selectbox("Select prior model", ["mol2mol_similarity", "mol2mol_medium_similarity",
                                                        "mol2mol_high_similarity", "mol2mol_mmp",
                                                        "mol2mol_scaffold", "mol2mol_scaffold_generic"], index=0, key=f"{run_mode}_{mol_gen}_model_type")
            prior_model = change_param(prior_model, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_model_type")  # UI State
            agent_model = prior_model
            mol2mol = prior_model
            # Prior Model
            model_type = st.toggle("Upload external prior model", value=False, key=f"{run_mode}_{mol_gen}_prior_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_prior_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Prior Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    prior_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    uploaded_files["Prior Model"] = model_file
                    needed_files["Prior Model"] = True
            else:
                prior_model += ".prior"
                uploaded_files["Prior Model"] = os.path.join(pwd, "prior_models", prior_model)
                needed_files["Prior Model"] = True
            # Agent Model
            model_type = st.toggle("Upload external agent model", value=False, key=f"{run_mode}_{mol_gen}_agent_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_agent_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Agent Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    agent_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    if agent_model != prior_model:
                        uploaded_files["Agent Model"] = model_file
                    needed_files["Agent Model"] = True
            else:
                agent_model += ".prior"
                if agent_model != prior_model:
                    uploaded_files["Agent Model"] = os.path.join(pwd, "prior_models", agent_model)
                needed_files["Agent Model"] = True
            # SMILES file 
            smiles_file = st.text_input("Name of SMILES file", "input_molecules", help="1 compound per line.", key=f"{run_mode}_{mol_gen}_smi_file")
            smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
            smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}", run_mode, mol_gen=mol_gen, mol2mol=mol2mol)
            needed_files[f"SMILES"] = False       
            if smi_path: 
                smiles_file = smi_name
                uploaded_files["SMILES"] = smi_path
                needed_files["SMILES"] = True
            else:
                smiles_file += ".smi"

           # Sampling Strategy
            st.write("**Sampling Strategy**")
            sample_strategy = st.selectbox("Algorithm", ["multinomial", "beamsearch"], index=0, key=f"{run_mode}_{mol_gen}_sample_strategy",
                                            help="""Two sample strategies are implemented in REINVENT 4: **multinomial** and **beam search**. 
                                                    Generally, multinomial is more “explorative” compared to beam search which is deterministic. 
                                                    Multinomial sampling is recommended for RL, whereas beam search can be very powerful for sampling.""")
            sample_strategy = change_param(sample_strategy, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_sample_strategy")  # UI State
            if sample_strategy == "beamsearch":
                temperature = st.number_input("Temperature", min_value=0.0, max_value=None, value=1.0, step=1.0, key=f"{run_mode}_{mol_gen}_temperature",
                                                help="""Higher temperature setting allows beam search to explore a greater variety of 
                                                        candidate sequence paths through the token graph. A lower temperature setting 
                                                        makes it increasingly focus on the most likely predictions at each step.""")
                temperature = change_param(temperature, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_temperature")  # UI State
            else:
               distance_threshold = st.number_input("Distance threshold", min_value=0, max_value=None, value=100, step=1, key=f"{run_mode}_{mol_gen}_distance_threshold")
               distance_threshold = change_param(distance_threshold, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_distance_threshold")  # UI State
            
        # Write to TOML input file 
        write_show(f'\# {mol_gen} Molecule Generator\n', toml_input, col2)
        if mol_gen == "Reinvent":
            write_show(f'prior_file = "{prior_model}"\n', toml_input, col2)
            write_show(f'agent_file = "{agent_model}"\n', toml_input, col2, empty_line=True)
            if inception:
                write_show('\# Inception Parameters: guide RL in the initial phase\n', toml_input, col2)
                write_show('[inception]\n', toml_input, col2)
                write_show(f'smiles_file = "{smiles_file}"\n', toml_input, col2)
                write_show(f'memory_size = {int(memory_size)}\n', toml_input, col2)
                write_show(f'sample_size = {int(sample_size)}\n', toml_input, col2, empty_line=True)
        elif mol_gen in ["LinkInvent", "LibInvent"]:
            write_show(f'prior_file = "{prior_model}"\n', toml_input, col2)
            write_show(f'agent_file = "{agent_model}"\n', toml_input, col2)
            write_show(f'smiles_file = "{smiles_file}"\n', toml_input, col2, empty_line=True)
        elif mol_gen == "Mol2Mol":
            write_show(f'prior_file = "{prior_model}"\n', toml_input, col2)
            write_show(f'agent_file = "{agent_model}"\n', toml_input, col2)
            write_show(f'smiles_file = "{smiles_file}"\n', toml_input, col2)
            write_show(f'sample_strategy = "{sample_strategy}"\n', toml_input, col2)
            if sample_strategy == "beamsearch":
                write_show(f'temperature = {temperature}\n', toml_input, col2, empty_line=True)
            else:
                write_show(f"distance_threshold = {distance_threshold}\n", toml_input, col2, empty_line=True)

    # Learning Strategy
    with col1.expander("**Learning Strategy**"):
        ls_type = st.selectbox("Type of Learning Strategy", ["dap"], index=0, disabled=True, 
                               help="""DAP recommended for practical use. It provides the most rapid learning and is robust. 
                                       Use of default values is also recommended. If the learning is too slow, you can increase 
                                       the learning rate.""",
                               key=f"{run_mode}_ls_type")
        #ls_type = change_param(ls_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_ls_type")  # UI State
        sigma = st.number_input("Sigma of the RL reward function", min_value=0, max_value=None, value=128, step=1, key=f"{run_mode}_sigma")
        sigma = change_param(sigma, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_sigma")  # UI State
        lr = st.number_input("Learning rate", min_value=0.0, max_value=None, value=0.0001, step=0.00001, format="%.5f", key=f"{run_mode}_lr")
        lr = change_param(lr, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_lr")  # UI State
        write_show('\# Learning Strategy Parameters\n', toml_input, col2)
        write_show('[learning_strategy]\n', toml_input, col2)
        write_show(f'type = "{ls_type}"\n', toml_input, col2)
        write_show(f'sigma = {int(sigma)}\n', toml_input, col2)
        write_show(f'rate = {float(lr)}\n', toml_input, col2, empty_line=True)

    # Diversity Filter
    with col1.expander(f"**Diversity Filter**"):
        div_filter = st.toggle("Diversity Filter", value=False, key=f"{run_mode}_div_filter")
        div_filter = change_param(div_filter, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_div_filter")  # UI State
        if div_filter:
            diversity_filter(col2, toml_input, state_dict, state, global_DF=True, num_stage=None, key=f"{run_mode}_div_filter")
    
    # Stage Parameters
    with col1.expander("**Stage Parameters**"):
        # Genral Stage Parameters 
        name_chk = st.text_input("Name of generated model", value="RL_calc", 
                                 help="This model can then be re-used as an agent in another calculation.", key=f"{run_mode}_chk")
        name_chk = change_param(name_chk, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_chk")  # UI State
        st.write("**Termination Parameters**")
        termination_Criterion = st.selectbox("Termination Criterion", ["simple"], index=0, disabled=True,
                                             help="A stage terminates if the supplied maximum score or the maximum number of steps is reached.", 
                                             key=f"{run_mode}_termination")
        #termination_Criterion = change_param(termination_Criterion, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_termination")  # UI State
        max_score = st.number_input("Maximum score", min_value=0.0, max_value=1.0, value=0.6, step=0.01, key=f"{run_mode}_max_score")
        max_score = change_param(max_score, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_max_score")  # UI State
        min_steps = st.number_input("Minimum number of steps", min_value=0, max_value=None, value=10, step=1, key=f"{run_mode}_min_steps")
        min_steps = change_param(min_steps, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_min_steps")  # UI State
        max_steps = st.number_input("Maximum number of steps", min_value=0, max_value=None, value=100, step=1, key=f"{run_mode}_max_steps")
        max_steps = change_param(max_steps, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_max_steps")
        write_show(f"\# Stage Parameters\n", toml_input, col2)
        write_show(f"[[stage]]\n", toml_input, col2)
        write_show(f'chkpt_file = "{name_chk}.chkpt"\n', toml_input, col2)
        write_show(f'termination = "{termination_Criterion}"\n', toml_input, col2)
        write_show(f"max_score = {max_score:.2f}\n", toml_input, col2)
        write_show(f"min_steps = {min_steps}\n", toml_input, col2)
        write_show(f"max_steps = {max_steps}\n", toml_input, col2, empty_line=True)
        # Scoring Components 
        st.write(f"**Scoring Components**")
        scor_comp = scoring_components(toml_input, col2, state_dict, state, modus=modus, 
                                       needed_files=needed_files, uploaded_files=uploaded_files, 
                                       gen_scoring_file=False, key=run_mode)
        # Upload Scoring File 
        if scor_comp != None: 
            if type(scor_comp) == str:
                needed_files["Scoring File"] = False
            else:
                uploaded_files["Scoring File"] = scor_comp
                needed_files["Scoring File"] = True

    # Additional options 
    with col1.expander("**Additional Options**"):
        # Bash File 
        bash_name = bash_script(run_mode, state_dict, state)
        if bash_name != None: 
            uploaded_files["Bash Run Script"] = bash_name
        else:
            # Remove Bash Script File if option was set to false 
            bash_path = Path(st.session_state["user_folder"]) / f"run_script_{run_mode}.sh"
            if bash_path.exists():
                bash_path.unlink()  
    
    # Download Fles 
    col1.divider()
    col1.subheader("Download Files")
    download_files(uploaded_files, col1)

    # Summary of Needed Files 
    col1.divider()
    col1.subheader("Summary of Files")
    needed_files = {
        "File": list(needed_files.keys()),
        "Status": list(needed_files.values())      
    }
    df = pd.DataFrame(needed_files)
    edited_data = col1.data_editor(df, num_rows="fixed", hide_index=True, column_config={
                "File": st.column_config.TextColumn(
                "File",
                help="Files needed for REINVENT calculation",
                width="large",
                default=False,
                disabled=True,
                ),
                "Status": st.column_config.CheckboxColumn(
                "Status",
                help="Status of needed files",
                width="small",
                default=False,
                disabled=True
                )
            })




if run_mode == "Staged Learning (SL)":
    run_mode = run_mode_prefix[run_mode]
    # Sidebar options
    with st.sidebar:
        with mode_info.popover("Run Mode Info"):
            st.write("""Multiple successive and consecutive RL runs with varying parameters. The main purpose is to allow the 
                        user to optimize a prior model conditioned on a calculated target profile by varying the scoring function 
                        in stages. Multiple stages can be provided at once (automatic SL). After each stage a checkpoint file is 
                        written to disk which can be used for the next stage (manual SL). A stage terminates if the supplied maximum 
                        score or the maximum number of steps is reached. In the latter case all stages will be terminated.""")

    # Name of Toml input file 
    toml_input = Path(st.session_state['user_folder']) / f"{toml_name}.toml"
    if toml_input.exists():
        toml_input.unlink() # Remove the file cross-platform

    # Uploaded Files 
    uploaded_files = {"TOML Input": toml_input, "Prior Model": None, "Agent Model": None}
    # Needed Files 
    needed_files = {"TOML Input": True, "Prior Model": False, "Agent Model": False}

    # Titel 
    write_show(f"\### REINVENT4 TOML input ###\n", toml_input, col2)
    write_show(f"\### Staged Learning (SL) Run Mode ###\n", toml_input, col2, empty_line=True)
    
    # General Options
    with col1.expander("**General Options**"):
        write_show('\# General Options\n', toml_input, col2)
        write_show('run_type = "staged_learning"\n', toml_input, col2)
        if modus == "Advanced":
            use_cuda = st.selectbox("Run on GPU?", ["true", "false"], index=0, key=f"{run_mode}_use_cuda")
            use_cuda = change_param(use_cuda, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_use_cuda")  # UI State
            write_show(f'use_cuda = {use_cuda}\n', toml_input, col2)
        else:
            write_show(f'use_cuda = true\n', toml_input, col2)
        tb_dir = st.text_input("Name of the TensorBoard Logging Directory", value="TensorBoard_SL", key=f"{run_mode}_tb_dir")
        tb_dir = change_param(tb_dir, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_tb_dir")  # UI State
        json_file = st.text_input("Name of the Json input file", value="SL_input", key=f"{run_mode}_json_file")
        json_file = change_param(json_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_json_file")  # UI State
        write_show(f'tb_logdir = "{tb_dir}"\n', toml_input, col2)
        write_show(f'json_out_config = "{json_file}.json"\n', toml_input, col2, empty_line=True)

    write_show('[parameters]\n', toml_input, col2, empty_line=False)

    # Run Mode Parameters
    with col1.expander("**Run Mode Parameters**"):
        summary_csv_prefix = st.text_input("Prefix for the summary file", value="summary_SL", key=f"{run_mode}_summary_csv")
        summary_csv_prefix = change_param(summary_csv_prefix, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_summary_csv")  # UI State
        use_checkpoint = st.selectbox("Use checkpoint?", ["true", "false"], index=1,
                                      help="If 'true' use diversity filter from agent_file if present.", key=f"{run_mode}_use_checkpoint")
        use_checkpoint = change_param(use_checkpoint, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_use_checkpoint")  # UI State
        #purge_memories = st.selectbox("Purge all Diversity Filter Memories after each Stage?", ["true", "false"], index=0, key=f"{run_mode}_purge_memories")
        #purge_memories = change_param(purge_memories, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_purge_memories")  # UI State
        batch_size = st.number_input("Number of molecules generated per run (epoch)", min_value=0, max_value=None, value=128, step=1)
        batch_size = change_param(batch_size, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_batch_size")  # UI State
        if modus == "Advanced":
            unique_sequences = st.selectbox("Canonicalize output SMILES and remove duplicates after each step (epoch)?", ["true", "false"], index=0,
                                            help="If true remove all duplicates raw sequences in each step.", key=f"{run_mode}_unique_sequences")
            unique_sequences = change_param(unique_sequences, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_unique_sequences")  # UI State
            randomize_smiles = st.selectbox("Shuffle Atoms in SMILES Randomly?", ["true", "false"], index=0,
                                            help="If true shuffle atoms in SMILES randomly.", key=f"{run_mode}_randomize_smiles")
            randomize_smiles = change_param(randomize_smiles, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_randomize_smiles")  # UI State
        else:
            unique_sequences = "true"
            randomize_smiles = "true"
        write_show('\# SL Parameters\n', toml_input, col2)
        write_show(f'summary_csv_prefix = "{summary_csv_prefix}"\n', toml_input, col2)
        write_show(f'use_checkpoint = {use_checkpoint}\n', toml_input, col2)
        #write_show(f'purge_memories = {purge_memories}\n', toml_input, col2)
        write_show(f'batch_size = {int(batch_size)}\n', toml_input, col2)
        write_show(f'unique_sequences = {unique_sequences}\n', toml_input, col2)
        write_show(f'randomize_smiles = {randomize_smiles}\n', toml_input, col2, empty_line=True)
    
    # Molecule Generator
    with col1.expander("**Molecule Generator**"):
        mol_gen = st.selectbox("Type of molecule generator", ["Reinvent", "LibInvent", "LinkInvent", "Mol2Mol"], index=0, key=f"{run_mode}_mol_gen")
        mol_gen = change_param(mol_gen, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_mol_gen")  # UI State
        # Reinvent Generator        
        if mol_gen == "Reinvent":
            # Prior Model
            prior_model = "reinvent.prior"    
            model_type = st.toggle("Upload external prior model", value=False, key=f"{run_mode}_{mol_gen}_prior_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_prior_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Prior Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    prior_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    uploaded_files["Prior Model"] = model_file
                    needed_files["Prior Model"] = True
            else:
                uploaded_files["Prior Model"] = os.path.join(pwd, "prior_models", prior_model)
                needed_files["Prior Model"] = True
            # Agent Model
            agent_model = "reinvent.prior"    
            model_type = st.toggle("Upload external agent model", value=False, key=f"{run_mode}_{mol_gen}_agent_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_agent_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Agent Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    agent_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    if agent_model != prior_model:
                        uploaded_files["Agent Model"] = model_file
                    needed_files["Agent Model"] = True
            else:
                if agent_model != prior_model:
                    uploaded_files["Agent Model"] = os.path.join(pwd, "prior_models", agent_model)
                needed_files["Agent Model"] = True 
            # Inception Parameters
            inception = st.toggle("Inception?", value=False, key=f"{run_mode}_{mol_gen}_inception",
                                  help="List of molecules provided by the user as SMILES strings to guide the reinforcement learning into the desired part of the chemical space.")
            inception = change_param(inception, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_inception")  # UI State
            if inception:
                st.markdown("**Inception Parameters**")
                # Inception SMILES File 
                smiles_file = st.text_input("Name of SMILES file for guidance", value="inception_molecules", help="1 molecule per line.", key=f"{run_mode}_{mol_gen}_smi_file")
                smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
                needed_files["Inception SMILES"] = False
                smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}_inception", run_mode, title="Inception SMILES", mol_gen=mol_gen)
                if smi_path != None: 
                    smiles_file = smi_name
                    uploaded_files["Inception SMILES"] = smi_path
                    needed_files["Inception SMILES"] = True
                else:
                    smiles_file += ".smi"
                memory_size = st.number_input("Number of total SMILES held in memory", min_value=0, max_value=None, value=100, step=1,
                                              help="""Top N scored molecules. As the RL run progresses and generates better molecules, 
                                              the initial inception molecules are removed from this memory and replaced by those with higher scores.""",
                                              key=f"{run_mode}_{mol_gen}_memory_size")
                memory_size = change_param(memory_size, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_memory_size")  # UI State
                sample_size = st.number_input("Number of SMILES randomly chosen after each epoch", min_value=0, max_value=None, value=10, step=1,
                                              help="Number of randomly sampled molecules from the memory to be used in computing the inception loss.",
                                              key=f"{run_mode}_{mol_gen}_sample_size")
                sample_size = change_param(sample_size, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_sample_size")  # UI State

        # LibInvent Generator
        elif mol_gen == "LibInvent":
            # Prior Model
            prior_model = "libinvent.prior"    
            model_type = st.toggle("Upload external prior model", value=False, key=f"{run_mode}_{mol_gen}_prior_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_prior_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Prior Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    prior_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    uploaded_files["Prior Model"] = model_file
                    needed_files["Prior Model"] = True
            else:
                uploaded_files["Prior Model"] = os.path.join(pwd, "prior_models", prior_model)
                needed_files["Prior Model"] = True
            # Agent Model
            agent_model = "libinvent.prior"    
            model_type = st.toggle("Upload external agent model", value=False, key=f"{run_mode}_{mol_gen}_agent_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_agent_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Agent Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    agent_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    if agent_model != prior_model:
                        uploaded_files["Agent Model"] = model_file
                    needed_files["Agent Model"] = True
            else:
                if agent_model != prior_model:
                    uploaded_files["Agent Model"] = os.path.join(pwd, "prior_models", agent_model)
                needed_files["Agent Model"] = True 
            # SMILES file 
            smiles_file = st.text_input("Name of SMILES file", "scaffolds", help="""One scaffold per line. Each scaffold must be 
                                        annotated by '\*' to locate the attachment points. Up to 4 attachments points are allowed. **Example**: [\*:1]Cc2ccc1cncc(C[*:2])c1c2)""", 
                                        key=f"{run_mode}_{mol_gen}_smi_file")   
            smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
            smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}", run_mode, mol_gen=mol_gen)
            needed_files[f"SMILES"] = False       
            if smi_path: 
                smiles_file = smi_name
                uploaded_files["SMILES"] = smi_path
                needed_files["SMILES"] = True
            else:
                smiles_file += ".smi"
        
        # LinkInvent Generator
        elif mol_gen == "LinkInvent":
            # Prior Model
            prior_model = "linkinvent.prior"    
            model_type = st.toggle("Upload external prior model", value=False, key=f"{run_mode}_{mol_gen}_prior_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_prior_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Prior Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    prior_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    uploaded_files["Prior Model"] = model_file
                    needed_files["Prior Model"] = True
            else:
                uploaded_files["Prior Model"] = os.path.join(pwd, "prior_models", prior_model)
                needed_files["Prior Model"] = True
            # Agent Model
            agent_model = "linkinvent.prior"    
            model_type = st.toggle("Upload external agent model", value=False, key=f"{run_mode}_{mol_gen}_agent_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_agent_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Agent Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    agent_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    if agent_model != prior_model:
                        uploaded_files["Agent Model"] = model_file
                    needed_files["Agent Model"] = True
            else:
                if agent_model != prior_model:
                    uploaded_files["Agent Model"] = os.path.join(pwd, "prior_models", agent_model)
                needed_files["Agent Model"] = True 
            # SMILES file 
            smiles_file = st.text_input("Name of SMILES file", "warheads", help="""Each line must contain the two warheads to be 
                                        linked separated by the pipe symbol. Each warhead must be annotated with '\*' to locate 
                                        the attachment points. **Example**: Oc1cncc(*)c1|*c1ccoc1""", 
                                        key=f"{run_mode}_{mol_gen}_smi_file")
            smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
            smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}", run_mode, mol_gen=mol_gen)
            needed_files[f"SMILES"] = False       
            if smi_path: 
                smiles_file = smi_name
                uploaded_files["SMILES"] = smi_path
                needed_files["SMILES"] = True
            else:
                smiles_file += ".smi"

        # Mol2Mol Generator
        elif mol_gen == "Mol2Mol":
            prior_model = st.selectbox("Select prior model", ["mol2mol_similarity", "mol2mol_medium_similarity",
                                                        "mol2mol_high_similarity", "mol2mol_mmp",
                                                        "mol2mol_scaffold", "mol2mol_scaffold_generic"], index=0, key=f"{run_mode}_{mol_gen}_model_type")
            prior_model = change_param(prior_model, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_model_type")  # UI State
            agent_model = prior_model
            mol2mol = prior_model
            # Prior Model
            model_type = st.toggle("Upload external prior model", value=False, key=f"{run_mode}_{mol_gen}_prior_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_prior_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Prior Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    prior_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    uploaded_files["Prior Model"] = model_file
                    needed_files["Prior Model"] = True
            else:
                prior_model += ".prior"
                uploaded_files["Prior Model"] = os.path.join(pwd, "prior_models", prior_model)
                needed_files["Prior Model"] = True
            # Agent Model
            model_type = st.toggle("Upload external agent model", value=False, key=f"{run_mode}_{mol_gen}_agent_model",
                                    help="The user could upload other RL/TL models if this is set to true.")
            model_type = change_param(model_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_agent_model")  # UI State
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Agent Model File", type=["model", "chkpt", "prior"],
                                               help="Upload another RL/TL model.")
                if model_file:
                    agent_model = model_file.name
                    model_file = save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    if agent_model != prior_model:
                        uploaded_files["Agent Model"] = model_file
                    needed_files["Agent Model"] = True
            else:
                agent_model += ".prior"
                if agent_model != prior_model:
                    uploaded_files["Agent Model"] = os.path.join(pwd, "prior_models", agent_model)
                needed_files["Agent Model"] = True
            # SMILES file 
            smiles_file = st.text_input("Name of SMILES file", "input_molecules", help="1 compound per line.", key=f"{run_mode}_{mol_gen}_smi_file")
            smiles_file = change_param(smiles_file, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_smi_file")  # UI State
            smi_path, smi_name = SMILES_file(f"{run_mode}_{mol_gen}", run_mode, mol_gen=mol_gen, mol2mol=mol2mol)
            needed_files[f"SMILES"] = False       
            if smi_path: 
                smiles_file = smi_name
                uploaded_files["SMILES"] = smi_path
                needed_files["SMILES"] = True
            else:
                smiles_file += ".smi"

            # Sampling Strategy
            st.write("**Sampling Strategy**")
            sample_strategy = st.selectbox("Algorithm", ["multinomial", "beamsearch"], index=0, key=f"{run_mode}_{mol_gen}_sample_strategy",
                                            help="""Two sample strategies are implemented in REINVENT 4: **multinomial** and **beam search**. 
                                            Generally, multinomial is more “explorative” compared to beam search which is deterministic. 
                                            Multinomial sampling is recommended for RL, whereas beam search can be very powerful for sampling.""")
            sample_strategy = change_param(sample_strategy, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_sample_strategy")  # UI State
            if sample_strategy == "beamsearch":
                temperature = st.number_input("Temperature", min_value=0.0, max_value=None, value=1.0, step=1.0, key=f"{run_mode}_{mol_gen}_temperature",
                                                help="""Higher temperature setting allows beam search to explore a greater variety of 
                                                        candidate sequence paths through the token graph. A lower temperature setting 
                                                        makes it increasingly focus on the most likely predictions at each step.""")
                temperature = change_param(temperature, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_temperature")  # UI State
            else:
               distance_threshold = st.number_input("Distance threshold", min_value=0, max_value=None, value=100, step=1, key=f"{run_mode}_{mol_gen}_distance_threshold")
               distance_threshold = change_param(distance_threshold, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_{mol_gen}_distance_threshold")  # UI State
            
        # Write to TOML input file 
        write_show(f'\# {mol_gen} Molecule Generator\n', toml_input, col2)
        if mol_gen == "Reinvent":
            write_show(f'prior_file = "{prior_model}"\n', toml_input, col2)
            write_show(f'agent_file = "{agent_model}"\n', toml_input, col2, empty_line=True)
            if inception:
                write_show('\# Inception Parameters: guide RL in the initial phase\n', toml_input, col2)
                write_show('[inception]\n', toml_input, col2)
                write_show(f'smiles_file = "{smiles_file}"\n', toml_input, col2)
                write_show(f'memory_size = {int(memory_size)}\n', toml_input, col2)
                write_show(f'sample_size = {int(sample_size)}\n', toml_input, col2, empty_line=True)
        elif mol_gen in ["LinkInvent", "LibInvent"]:
            write_show(f'prior_file = "{prior_model}"\n', toml_input, col2)
            write_show(f'agent_file = "{agent_model}"\n', toml_input, col2)
            write_show(f'smiles_file = "{smiles_file}"\n', toml_input, col2, empty_line=True)
        elif mol_gen == "Mol2Mol":
            write_show(f'prior_file = "{prior_model}"\n', toml_input, col2)
            write_show(f'agent_file = "{agent_model}"\n', toml_input, col2)
            write_show(f'smiles_file = "{smiles_file}"\n', toml_input, col2)
            write_show(f'sample_strategy = "{sample_strategy}"\n', toml_input, col2)
            if sample_strategy == "beamsearch":
                write_show(f'temperature = {temperature}\n', toml_input, col2, empty_line=True)
            else:
                write_show(f"distance_threshold = {distance_threshold}\n", toml_input, col2, empty_line=True)

    # Learning Strategy
    with col1.expander("**Learning Strategy**"):
        ls_type = st.selectbox("Type of Learning Strategy", ["dap"], index=0, disabled=True, 
                               help="""DAP recommended for practical use. It provides the most rapid learning and is robust. 
                                       Use of default values is also recommended. If the learning is too slow, you can increase 
                                       the learning rate.""",
                               key=f"{run_mode}_ls_type")
        #ls_type = change_param(ls_type, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_ls_type")  # UI State
        sigma = st.number_input("Sigma of the RL reward function", min_value=0, max_value=None, value=128, step=1, key=f"{run_mode}_sigma")
        sigma = change_param(sigma, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_sigma")  # UI State
        lr = st.number_input("Learning rate", min_value=0.0, max_value=None, value=0.0001, step=0.00001, format="%.5f", key=f"{run_mode}_lr")
        lr = change_param(lr, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_lr")  # UI State
        write_show('\# Learning Strategy Parameters\n', toml_input, col2)
        write_show('[learning_strategy]\n', toml_input, col2)
        write_show(f'type = "{ls_type}"\n', toml_input, col2)
        write_show(f'sigma = {int(sigma)}\n', toml_input, col2)
        write_show(f'rate = {float(lr)}\n', toml_input, col2, empty_line=True)

    # Diversity Filter
    with col1.expander(f"**Global Diversity Filter**"):
        div_filter_global = st.toggle("Global Diversity Filter", value=False, key=f"{run_mode}_div_filter", 
                               help="A global diversity filter would overwrite all separate diversity filters!")
        div_filter_global = change_param(div_filter_global, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_div_filter")  # UI State
        if div_filter_global:
            diversity_filter(col2, toml_input, state_dict, state, global_DF=True, num_stage=None, key=f"{run_mode}_div_filter")
    
    # Stage Parameters
    for i in range(1, num_stages+1):
        ## Add default values for the scoring components to the reset dictionary
        state_dict_reset[st.session_state["run_mode"]][f"{run_mode}_S{i}_chk"] = {"key": f"{run_mode}_S{i}_chk", "value": f"SL_calc_S{i}"}        # reset value
        #state_dict_reset[st.session_state["run_mode"]][f"{run_mode}_S{i}_termination"] = {"key": f"{run_mode}_S{i}_termination", "value": "simple"}         # reset value
        state_dict_reset[st.session_state["run_mode"]][f"{run_mode}_S{i}_max_score"] = {"key": f"{run_mode}_S{i}_max_score", "value": 0.6}  # reset value
        state_dict_reset[st.session_state["run_mode"]][f"{run_mode}_S{i}_min_steps"] = {"key": f"{run_mode}_S{i}_min_steps", "value": 10}  # reset value
        state_dict_reset[st.session_state["run_mode"]][f"{run_mode}_S{i}_max_steps"] = {"key": f"{run_mode}_S{i}_max_steps", "value": 100}  # reset value

        with col1.expander(f"**Stage {i} Parameters**"):           
            # Genral Stage Parameters 
            name_chk = st.text_input("Name of generated model", value=f"SL_calc_S{i}", 
                                    help="This model can then be re-used as an agent in another calculation.", key=f"{run_mode}_S{i}_chk")
            name_chk = change_param(name_chk, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_S{i}_chk", add_key=True)  # UI State
            st.write(f"**Termination Parameters (S{i})**")
            termination_Criterion = st.selectbox("Termination Criterion", ["simple"], index=0, disabled=True,
                                                help="A stage terminates if the supplied maximum score or the maximum number of steps is reached.", 
                                                key=f"{run_mode}_S{i}_termination")
            #termination_Criterion = change_param(termination_Criterion, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_S{i}_termination", add_key=True)  # UI State
            max_score = st.number_input("Maximum score", min_value=0.0, max_value=1.0, value=0.6, step=0.01, key=f"{run_mode}_S{i}_max_score")
            max_score = change_param(max_score, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_S{i}_max_score", add_key=True)  # UI State
            min_steps = st.number_input("Minimum number of steps", min_value=0, max_value=None, value=10, step=1, key=f"{run_mode}_S{i}_min_steps")
            min_steps = change_param(min_steps, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_S{i}_min_steps", add_key=True)  # UI State
            max_steps = st.number_input("Maximum number of steps", min_value=0, max_value=None, value=100, step=1, key=f"{run_mode}_S{i}_max_steps")
            max_steps = change_param(max_steps, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_S{i}_max_steps", add_key=True)
            write_show(f"\# Stage Parameters (S{i})\n", toml_input, col2)
            write_show(f"[[stage]]\n", toml_input, col2)
            write_show(f'chkpt_file = "{name_chk}.chkpt"\n', toml_input, col2)
            write_show(f'termination = "{termination_Criterion}"\n', toml_input, col2)
            write_show(f"max_score = {max_score:.2f}\n", toml_input, col2)
            write_show(f"min_steps = {min_steps}\n", toml_input, col2)
            write_show(f"max_steps = {max_steps}\n", toml_input, col2, empty_line=True)

            # Diversity Filter  
            st.write(f"**Diversity Filter (S{i})**")
            div_filter = st.toggle(f"Separate diversity filter for **stage {i}**?", value=False, key=f"{run_mode}_S{i}_div_filter",
                                          help="A global diversity filter would overwrite all these separate diversity filters!")
            div_filter = change_param(div_filter, st.session_state["change_param_dict"], state_dict, state, f"{run_mode}_S{i}_div_filter", add_key=True)  # UI State
            if div_filter:
                diversity_filter(col2, toml_input, state_dict, state, global_DF=False, 
                                 num_stage=i, key=f"{run_mode}_S{i}_div_filter")

            # Scoring Components 
            st.write(f"**Scoring Components (S{i})**")
            scor_comp = scoring_components(toml_input, col2, state_dict, state, stages=True, num_stage=i, 
                                           modus=modus, needed_files=needed_files, uploaded_files=uploaded_files, 
                                           gen_scoring_file=False, key=f"{run_mode}-S{i}")
            # Upload Scoring File 
            if scor_comp != None: 
                if type(scor_comp) == str:
                    needed_files[f"Scoring File (S{i})"] = False
                else:
                    uploaded_files[f"Scoring File (S{i})"] = scor_comp
                    needed_files[f"Scoring File (S{i})"] = True

    # Additional options 
    with col1.expander("**Additional Options**"):
        # Bash File 
        bash_name = bash_script(run_mode, state_dict, state)
        if bash_name != None: 
            uploaded_files["Bash Run Script"] = bash_name
        else:
            # Remove Bash Script File if option was set to false 
            bash_path = Path(st.session_state["user_folder"]) / f"run_script_{run_mode}.sh"
            if bash_path.exists():
                bash_path.unlink()  

    # Download Fles 
    col1.divider()
    col1.subheader("Download Files")
    download_files(uploaded_files, col1)

    # Summary of Needed Files 
    col1.divider()
    col1.subheader("Summary of Files")
    needed_files = {
        "File": list(needed_files.keys()),
        "Status": list(needed_files.values())      
    }
    df = pd.DataFrame(needed_files)
    edited_data = col1.data_editor(df, num_rows="fixed", hide_index=True, column_config={
                "File": st.column_config.TextColumn(
                "File",
                help="Files needed for REINVENT calculation",
                width="large",
                default=False,
                disabled=True,
                ),
                "Status": st.column_config.CheckboxColumn(
                "Status",
                help="Status of needed files",
                width="small",
                default=False,
                disabled=True
                )
            })


## Save State: save the current UI state of options and widgets into a json file. 
# (At the end of the script --> to account for any changes in st.session_state dict after re-running the script)
with save.popover("Save UI State"): 
    UI_state_name = st.text_input("Name of UI State File (Json)", value="reinvent_UI_state", key="UI_state_name")
    UI_state_data = save_state(dict(st.session_state), UI_state_name+".json")
    st.download_button(
        label="Download UI State File", 
        data=UI_state_data, 
        file_name=f"{UI_state_name}.json", 
        help=f"{UI_state_name}.json"
        )