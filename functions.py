########################################
############ Python Modules ############
########################################
import numpy as np
import pandas as pd 
import rdkit
from rdkit import Chem
from rdkit.Chem import PandasTools
import streamlit as st 
import zipfile
import io
import os 
import base64
import json
import shutil
from pathlib import Path
from datetime import datetime
from datetime import timedelta
from data import * 

# Path for Parent Working Directory (Dir: reinvent4)
pwd = os.getcwd()                            

#########################################
######### Python Functions ##############
#########################################
def clean_folder(base_dir, age_limit=1):
    """
    Clean up folders older than a specified time (e.g., 1 day).

    Args:
        base_dir (str): The base directory containing folders to clean.
        age_limit (int): The age limit in days for folders to be deleted. Defaults to 1 day.

    Returns:
        None
    """
    now = datetime.now()
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path):
            # Extract timestamp from folder name
            folder_time = folder.split("_")[-1]  # Assuming "user_TIMESTAMP"
            folder_datetime = datetime.strptime(folder_time, "%Y-%m-%d-%H-%M-%S")
            # Check folder age
            if now - folder_datetime > timedelta(days=age_limit):
                shutil.rmtree(folder_path)
                st.write(f"Deleted old folder: {folder_path}")


###########################################
###### Streamlit Functions (v1.40) ######
###########################################
def save_state(state, file_name):
    """
    Save the values of the widgets of the UI app into a JSON file.

    Args:
        state (dict): The state dictionary containing UI widget values.
        file_name (str): The name of the file to save the state to.

    Returns:
        str: The JSON string representation of the state.    
    """
    del state["change_param_dict"]
    UI_file_path = Path(state["user_folder"]) / file_name
    with open(UI_file_path, 'w') as json_file:
        json.dump(state, json_file, indent=4)
    json_str = json.dumps(state, indent=4)
    return json_str


def load_state(state_file):
    """
    Load the values of the widgets of the UI from a JSON file.

    Args:
        state_file (UploadedFile): The uploaded file containing the state in JSON format.

    Returns:
        dict: The state dictionary containing UI widget values.  
    """
    file_content = state_file.getvalue()
    state_dict = json.loads(file_content.decode())

    # Check what kind of run modes are available in the loaded UI state. 
    state_dict_modes = set()
    for key in state_dict.keys():
        if key.startswith("Scoring"):
            state_dict_modes.add("Scoring")
        elif key.startswith("Sampling"):
            state_dict_modes.add("Sampling")
        elif key.startswith("TL"):
            state_dict_modes.add("TL")
        elif key.startswith("RL"):
            state_dict_modes.add("RL")
        elif key.startswith("SL"):
            state_dict_modes.add("SL")
    # Inform the user about the run modes contained in the loaded UI and the current selected run mode. 
    st.info(f"""
            * The loaded UI state contains parameters for the following run modes: {", ".join(list(state_dict_modes))}\n 
            * The current selected run mode: **{st.session_state["run_mode"]}**
            """, 
            icon="ℹ️") 

    return state_dict 


def change_param(parameter, change_param_dict, state_dict, state, key, add_key=False):
    """
    Change a parameter based on the state and change parameter dictionary.

    Args:
        parameter (any): The parameter to change.
        change_param_dict (dict): A dictionary tracking if the parameter were already changed (via loading a UI state).
        state_dict (dict): The loaded UI state (JSON format) converted into dict. 
        state (bool): Whether a UI state was uploaded or not (Uploaded = True, Not Uploaded = False). 
        key (str): The key for the parameter in the dictionaries.
        add_key (bool, optional): Whether to add the key to the change parameter dictionary. Defaults to False.

    Returns:
        any: The updated parameter.
    """
    if add_key:
        if key not in state_dict_UI[st.session_state["run_mode"]].keys():
            state_dict_UI[st.session_state["run_mode"]][key] = key
        if key not in change_param_dict.keys():
            change_param_dict[key] = True
        
    if (state != None) & (change_param_dict != None):
        if (state) & (change_param_dict[key]):
            try:
                parameter = state_dict[key]
                del st.session_state[key]
                st.session_state[key] = state_dict[key]
            except:
               pass
            change_param_dict[key] = False 

    return parameter


def reset_values(run_mode):
    """
    Reset the session state values to the default values based on the selected run mode.

    Args:
        run_mode (str): The selected run mode.

    Returns:
        None
    """
    for key in state_dict_reset[run_mode].keys():
        key, value = state_dict_reset[run_mode][key]["key"], state_dict_reset[run_mode][key]["value"]
        # del st.session_state[key]
        st.session_state[key] = value
    st.rerun()


def write_show(text, file, col, empty_line=False, display=True):
    """
    Write a text into a file and display it to the user.

    Args:
        text (str): The text to write and display.
        file (str): The file path to write the text to.
        col (streamlit.columns): The Streamlit column to display the text in.
        empty_line (bool, optional): Whether to add an empty line after the text. Defaults to False.

    Returns:
        None
    """
    # Clean text from backslashes
    text_clean = text[1:] if text.startswith("\\") else text
    # Display text to user
    if display:
        col.write(text)
        if empty_line:
            col.write("\n")
    # Write text to file (TOML Input file)
    with open(file, "a") as f:
        f.write(text_clean)
        if empty_line:
            f.write("\n")


def save_uploaded_file(uploaded_file, save_folder): 
    """ 
    Save an uploaded file to a specified folder (e.g., User's temp folder). 

    Args:
        uploaded_file (UploadedFile): The file uploaded through the Streamlit file uploader.
        save_folder (str): Path to the folder where the file will be saved.

    Returns:
        str: Path to the saved file if successful, else None.
    """ 
    save_path = os.path.join(save_folder, uploaded_file.name) 
    try: 
        with open(save_path, "wb") as f: 
            f.write(uploaded_file.getbuffer()) 
            return save_path 
    except Exception as e: 
        st.error(f"Error saving file: {e}") 
        return None


def write_scor_component(component, toml_input, col, stages=False):
    """
    Write the headers for a scoring component to the TOML input file.

    Args:
        component (str): The name of the scoring component.
        toml_input (str): The TOML input file path.
        col (streamlit.columns): The Streamlit column to show the headers for the user in.
        stages (bool, optional): Whether the scoring component is for stages. Defaults to False.

    Returns:
        None
    """
    if stages:
        write_show(f'\# {component}: {scoring_component_entries[component]}\n', toml_input, col)
        write_show('[[stage.scoring.component]]\n', toml_input, col)
        write_show(f'[stage.scoring.component.{scoring_keys[component]}]\n', toml_input, col) 
        write_show(f'[[stage.scoring.component.{scoring_keys[component]}.endpoint]]\n', toml_input, col)
    else:
        write_show(f'\# {component}: {scoring_component_entries[component]}\n', toml_input, col)
        write_show('[[scoring.component]]\n', toml_input, col)
        write_show(f'[scoring.component.{scoring_keys[component]}]\n', toml_input, col) 
        write_show(f'[[scoring.component.{scoring_keys[component]}.endpoint]]\n', toml_input, col)


def trans_para_input(toml_input, col, state_dict, state, low_value=0.0, high_value=10.0, step=1.0, key=None, 
                     default=None, advanced=False, gen_scoring_file=False):
    """
    Take the parameters of the transformer as input from the user and write them to the TOML input file.

    Args:
        toml_input (str): The TOML input file path.
        col (streamlit.columns): The Streamlit column to write the parameters in.
        state_dict (dict): The loaded UI state (JSON format) converted into dict. 
        state (bool): Whether a UI state was uploaded or not (Uploaded = True, Not Uploaded = False). 
        low_value (int, optional): The default lower threshold value. Defaults to 0.
        high_value (int, optional): The default upper threshold value. Defaults to 10.
        step (int, optional): The step size for the number inputs. Defaults to 1.
        key (str, optional): A unique key for Streamlit widgets. Defaults to None.
        default (str, optional): The default transformer type. Defaults to None.
        advanced (bool, optional): Whether to show advanced options. Defaults to False.
        gen_scoring_file (bool, optional): Whether to generate a scoring file. Defaults to False.

    Returns:
        None
    """
    ## Needed variables
    low_value = float(low_value) if low_value != None else low_value      # Convert to float if not None
    high_value = float(high_value) if high_value != None else high_value  # Convert to float if not None
    step = float(step) if step != None else step                          # Convert to float if not None
    comp = key.split("_")[1]  # Get the component name from the key (e.g., "scoring_component_1" -> "component")
    type_index = {"Sigmoid": 0, "Reverse_Sigmoid": 1, "Double_Sigmoid": 2, "Right_Step": 3, "Left_Step": 4, "Step": 5, "Value_Mapping": 6}

    ## Widget for the transformer parameters
    use_transformer = st.toggle("Apply Transformer Function?", value=True, key=f"{key}_use_trans")
    use_transformer = change_param(use_transformer, st.session_state["change_param_dict"], state_dict, state, f"{key}_use_trans", add_key=True) if not gen_scoring_file else use_transformer # UI State
    trans_type = None
    if use_transformer:
        # Add default values for the transformer parameters to the reset dictionary
        if not gen_scoring_file:
            state_dict_reset[st.session_state["run_mode"]][f"{key}_trans_type"] = {"key": f"{key}_trans_type", "value": default}  # reset value
        # Widget for the transformer parameters
        trans_type = st.selectbox(label="Select type of transformer", options=["Sigmoid", "Reverse_Sigmoid", "Double_Sigmoid", 
                                                                               "Right_Step", "Left_Step", "Step", "Value_Mapping"], 
                                                                      index=type_index[default], key=f"{key}_trans_type",
                                                                      help="Use Value_Mapping only for MMP.")
        trans_type = change_param(trans_type, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_type", add_key=True) if not gen_scoring_file else trans_type # UI State
    else: 
        write_show('\n', toml_input, col)
    
    ## Transformer parameters based on the selected type
    if trans_type == "Sigmoid" or trans_type == "Reverse_Sigmoid":
        # Add default values for the transformer parameters to the reset dictionary
        if not gen_scoring_file:
            state_dict_reset[st.session_state["run_mode"]][f"{key}_trans_lower"] = {"key": f"{key}_trans_lower", "value": low_value}  # reset value
            state_dict_reset[st.session_state["run_mode"]][f"{key}_trans_upper"] = {"key": f"{key}_trans_upper", "value": high_value}  # reset value
        # Widget for the transformer parameters
        lower_threshold = st.number_input(label="Lower threshold", value=low_value, min_value=None, max_value=None, step=step, key=f"{key}_trans_lower", help="shifts the center of the sigmoid function")
        lower_threshold = change_param(lower_threshold, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_lower", add_key=True) if not gen_scoring_file else lower_threshold # UI State
        upper_threshold = st.number_input(label="Upper threshold", value=high_value, min_value=None, max_value=None, step=step, key=f"{key}_trans_upper", help="shifts the center of the sigmoid function")
        upper_threshold = change_param(upper_threshold, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_upper", add_key=True) if not gen_scoring_file else upper_threshold # UI State
        if advanced:
            k_factor = st.number_input(label="Scaling factor ($k$)", value=0.5, min_value=None, max_value=None, step=0.1, key=f"{key}_trans_k", help="adjusts the steepness of the sigmoid function")
            k_factor = change_param(k_factor, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_k", add_key=True) if not gen_scoring_file else k_factor # UI State
        else:
            k_factor = 0.5
        write_show(f'transform.type = "{trans_type}"\n', toml_input, col)
        write_show(f'transform.low = {lower_threshold}\n', toml_input, col)
        write_show(f'transform.high = {upper_threshold}\n', toml_input, col)
        write_show(f'transform.k = {k_factor:.2f}\n', toml_input, col, empty_line=True)
    elif trans_type == "Double_Sigmoid":
        # Add default values for the transformer parameters to the reset dictionary
        if not gen_scoring_file:
            state_dict_reset[st.session_state["run_mode"]][f"{key}_trans_lower"] = {"key": f"{key}_trans_lower", "value": low_value}  # reset value
            state_dict_reset[st.session_state["run_mode"]][f"{key}_trans_upper"] = {"key": f"{key}_trans_upper", "value": high_value}  # reset value
        # Widget for the transformer parameters
        lower_threshold = st.number_input(label="Lower threshold", value=low_value, min_value=None, max_value=None, step=step, key=f"{key}_trans_lower", help="shifts the center of the left sigmoid function")
        lower_threshold = change_param(lower_threshold, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_lower", add_key=True) if not gen_scoring_file else lower_threshold # UI State
        upper_threshold = st.number_input(label="Upper threshold", value=high_value, min_value=None, max_value=None, step=step, key=f"{key}_trans_upper", help="shifts the center of the right sigmoid function")
        upper_threshold = change_param(upper_threshold, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_upper", add_key=True) if not gen_scoring_file else upper_threshold # UI State
        if advanced:
            coef_div = st.number_input(label="Common scaling factor ($k$)", value=100.0, min_value=None, max_value=None, step=1.0, key=f"{key}_trans_div", help="adjusts the steepness of the double sigmoid function")
            coef_div = change_param(coef_div, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_div", add_key=True) if not gen_scoring_file else coef_div # UI State
            coef_si = st.number_input(label="Left scaling factor ($k_l$)", value=10.0, min_value=None, max_value=None, step=1.0, key=f"{key}_trans_si", help="adjusts the steepness of the left sigmoid function")
            coef_si = change_param(coef_si, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_si", add_key=True) if not gen_scoring_file else coef_si # UI State
            coef_se = st.number_input(label="Right scaling factor ($k_r$)", value=10.0, min_value=None, max_value=None, step=1.0, key=f"{key}_trans_se", help="adjusts the steepness of the right sigmoid function")
            coef_se = change_param(coef_se, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_se", add_key=True) if not gen_scoring_file else coef_se # UI State
        else:
            coef_div = 100.0
            coef_si = 10.0
            coef_se = 10.0
        write_show(f'transform.type = "{trans_type}"\n', toml_input, col)
        write_show(f'transform.low = {lower_threshold}\n', toml_input, col)
        write_show(f'transform.high = {upper_threshold}\n', toml_input, col)
        write_show(f'transform.coef_div = {coef_div:.2f}\n', toml_input, col)
        write_show(f'transform.coef_si = {coef_si:.2f}\n', toml_input, col)
        write_show(f'transform.coef_se = {coef_se:.2f}\n', toml_input, col, empty_line=True)
    elif trans_type == "Step":
        # Add default values for the transformer parameters to the reset dictionary
        if not gen_scoring_file:
            state_dict_reset[st.session_state["run_mode"]][f"{key}_trans_lower"] = {"key": f"{key}_trans_lower", "value": low_value}  # reset value
            state_dict_reset[st.session_state["run_mode"]][f"{key}_trans_upper"] = {"key": f"{key}_trans_upper", "value": high_value}  # reset value
        # Widget for the transformer parameters
        lower_threshold = st.number_input(label="Lower threshold", value=low_value, min_value=None, max_value=None, step=step, key=f"{key}_trans_lower")
        lower_threshold = change_param(lower_threshold, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_lower", add_key=True) if not gen_scoring_file else lower_threshold # UI State
        upper_threshold = st.number_input(label="Upper threshold", value=high_value, min_value=None, max_value=None, step=step, key=f"{key}_trans_upper")
        upper_threshold = change_param(upper_threshold, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_upper", add_key=True) if not gen_scoring_file else upper_threshold # UI State
        write_show(f'transform.type = "{trans_type}"\n', toml_input, col)
        write_show(f'transform.high = {upper_threshold}\n', toml_input, col)
        write_show(f'transform.low = {lower_threshold}\n', toml_input, col, empty_line=True)
    elif trans_type == "Left_Step":
        # Add default values for the transformer parameters to the reset dictionary
        if not gen_scoring_file:
            state_dict_reset[st.session_state["run_mode"]][f"{key}_trans_lower"] = {"key": f"{key}_trans_lower", "value": low_value}  # reset value
        # Widget for the transformer parameters
        lower_threshold = st.number_input(label="Lower threshold", value=low_value, min_value=None, max_value=None, step=step, key=f"{key}_trans_lower")
        lower_threshold = change_param(lower_threshold, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_lower", add_key=True) if not gen_scoring_file else lower_threshold # UI State
        write_show(f'transform.type = "{trans_type}"\n', toml_input, col)
        write_show(f'transform.low = {lower_threshold}\n', toml_input, col, empty_line=True)
    elif trans_type == "Right_Step":
        # Add default values for the transformer parameters to the reset dictionary
        if not gen_scoring_file:
            state_dict_reset[st.session_state["run_mode"]][f"{key}_trans_upper"] = {"key": f"{key}_trans_upper", "value": high_value}  # reset value
        # Widget for the transformer parameters
        upper_threshold = st.number_input(label="Upper threshold", value=high_value, min_value=None, max_value=None, step=step, key=f"{key}_trans_upper")
        upper_threshold = change_param(upper_threshold, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_upper", add_key=True) if not gen_scoring_file else upper_threshold # UI State
        write_show(f'transform.type = "{trans_type}"\n', toml_input, col)
        write_show(f'transform.high = {upper_threshold}\n', toml_input, col, empty_line=True)
    elif trans_type == "Value_Mapping":
        # Add default values for the transformer parameters to the reset dictionary
        if not gen_scoring_file:
            state_dict_reset[st.session_state["run_mode"]][f"{key}_trans_{comp}_threshold"] = {"key": f"{key}_trans_{comp}_threshold", "value": 0.5}        # reset value
            state_dict_reset[st.session_state["run_mode"]][f"{key}_trans_No_{comp}_threshold"] = {"key": f"{key}_trans_No_{comp}_threshold", "value": 0.0}  # reset value
        # Widget for the transformer parameters
        Comp_threshold = st.number_input(label=f"'{comp}' threshold", value=high_value, min_value=None, max_value=None, step=step, key=f"{key}_trans_{comp}_threshold")
        Comp_threshold = change_param(Comp_threshold, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_{comp}_threshold", add_key=True) if not gen_scoring_file else Comp_threshold # UI State
        No_comp_threshold = st.number_input(label=f"'No {comp}' threshold", value=low_value, min_value=None, max_value=None, step=step, key=f"{key}_trans_No_{comp}_threshold")
        No_comp_threshold = change_param(No_comp_threshold, st.session_state["change_param_dict"], state_dict, state, f"{key}_trans_No_{comp}_threshold", add_key=True) if not gen_scoring_file else No_comp_threshold # UI State
        write_show(f'transform.type = "value_mapping"\n', toml_input, col)
        write_show(f'[scoring.component.{comp}.endpoint.transform.mapping]\n', toml_input, col)
        write_show(f'{comp} = {Comp_threshold}\n', toml_input, col)
        write_show(f'"No {comp}" = {No_comp_threshold}\n', toml_input, col, empty_line=True)


def smarts_table(comp, key, with_status=True):
    """
    Display a table of SMARTS patterns for the user to select from.

    Args:
        comp (str): The name of the component.
        key (str): A unique key for Streamlit widgets.
        with_status (bool, optional): Whether to include a status column for selection. Defaults to True.

    Returns:
        pd.DataFrame: The edited DataFrame with user selections.
    """
    if with_status:
        columns = ["Fragment", "SMARTS Pattern", "Status"]
        data = []
        for pattern in smarts_patterns.keys():
            data.append([pattern, smarts_patterns[pattern], False])
        df = pd.DataFrame(data, columns=columns)
        edited_data = st.data_editor(df, num_rows="fixed", hide_index=True, column_config={
                    "Fragment": st.column_config.TextColumn(
                    "Fragment",
                    help=f"Fragment ({comp}-{key})",
                    disabled=True,
                    ),
                    "SMARTS Pattern": st.column_config.TextColumn(
                    "SMARTS Pattern",
                    help=f"SMARTS Pattern ({comp}-{key})",
                    default="component",
                    disabled=True,
                    ),
                    "Status": st.column_config.CheckboxColumn(
                    "Status",
                    help=f"If the user wants to include that specific pattern in the SMARTS list ({comp}-{key})",
                    width="medium",
                    default=False,
                    )
                })
    else:
        columns = ["Fragment", "SMARTS Pattern"]
        data = []
        for pattern in smarts_patterns.keys():
            data.append([pattern, smarts_patterns[pattern]])
        df = pd.DataFrame(data, columns=columns)
        edited_data = st.data_editor(df, num_rows="fixed", hide_index=True, column_config={
                    "Fragment": st.column_config.TextColumn(
                    "Fragment",
                    help=f"Fragment ({comp}-{key})",
                    disabled=True,
                    ),
                    "SMARTS Pattern": st.column_config.TextColumn(
                    "SMARTS Pattern",
                    help=f"SMARTS Pattern ({comp}-{key})",
                    default="component",
                    disabled=True,
                    )
                })
    return edited_data


def scoring_components(toml_input, col, state_dict, state, stages=False, num_stage=None, modus="Basic", 
                       needed_files=None, uploaded_files=None, gen_scoring_file=False, key=None):
    """
    Display and configure scoring components in a Streamlit app.

    Args:
        toml_input (str): The TOML input file path.
        col (streamlit.columns): The Streamlit column to place the scoring components in.
        state_dict (dict): The loaded UI state (JSON format) converted into dict. 
        state (bool): Whether a UI state was uploaded or not (Uploaded = True, Not Uploaded = False). 
        stages (bool, optional): Whether the scoring components are for stages. Defaults to False.
        num_stage (int, optional): The stage number. Defaults to None.
        modus (str, optional): The mode of the UI, either "Advanced" or "Basic". Defaults to "Basic".
        needed_files (dict, optional): A dictionary to track the needed files. Defaults to None.
        uploaded_files (dict, optional): A dictionary to track the uploaded files. Defaults to None.
        gen_scoring_file (bool, optional): Whether to generate a scoring file. Defaults to False.
        key (str, optional): A unique key for Streamlit widgets. Defaults to None.

    Returns:
        None
    """
    ## Define functions for input widgets (shape_weight & color_weight) that depend on each other
    def color_to_shape():
        st.session_state[f"{key}_{comp}_shape_weight_{i}"] = 1.0 - st.session_state[f"{key}_{comp}_color_weight_{i}"] 

    def shape_to_color():
        st.session_state[f"{key}_{comp}_color_weight_{i}"]  = 1.0 - st.session_state[f"{key}_{comp}_shape_weight_{i}"] 

    ## Add default values for the scoring components to the reset dictionary
    if not gen_scoring_file:
        #state_dict_reset[st.session_state["run_mode"]][f"{key}_scor_components"] = {"key": f"{key}_scor_components", "value": []}        # reset value
        state_dict_reset[st.session_state["run_mode"]][f"{key}_weight"] = {"key": f"{key}_weight", "value": "geometric"}        # reset value
        state_dict_reset[st.session_state["run_mode"]][f"{key}_parallel"] = {"key": f"{key}_parallel", "value": "true"}         # reset value
        #state_dict_reset[st.session_state["run_mode"]][f"{key}_scoring_file"] = {"key": f"{key}_scoring_file", "value": False}  # reset value
        state_dict_reset[st.session_state["run_mode"]][f"{key}_scoring_filename"] = {"key": f"{key}_scoring_filename", "value": "scoring_file"}  # reset value
        state_dict_reset[st.session_state["run_mode"]][f"{key}_scoring_filetype"] = {"key": f"{key}_scoring_filetype", "value": "json"}  # reset value

    ## Widget for the scoring components
    if not gen_scoring_file:
        scoring_file = st.toggle("Read scoring components from scoring file?", value=False, key=f"{key}_scoring_file", help="Scoring file must be of **TOML** or **JSON** format.")
        scoring_file = change_param(scoring_file, st.session_state["change_param_dict"], state_dict, state, f"{key}_scoring_file", add_key=True) if not gen_scoring_file else scoring_file # UI State
        scoring_weight = st.selectbox(options=["geometric", "arithmetic"], label="Select scoring function type", help="Components of the scoring function can be aggregated via a weighted arithmetic mean or a weighted geometric mean.", 
                                    index=0, key=f"{key}_weight") # Aggregation functions    
        scoring_weight = change_param(scoring_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_weight", add_key=True) if not gen_scoring_file else scoring_weight # UI State
        if modus == "Advanced":
            run_parallel = st.selectbox(options=["true", "false"], label="Run scoring components in parallel?", index=0, key=f"{key}_parallel")
            run_parallel = change_param(run_parallel, st.session_state["change_param_dict"], state_dict, state, f"{key}_parallel", add_key=True) if not gen_scoring_file else run_parallel # UI State
    else:
        scoring_file = None

    # If the user wants to use a stand-alone scoring file 
    if scoring_file:
        filename = st.text_input("Name of scoring file", value="scoring_file", key=f"{key}_scoring_filename")
        filename = change_param(filename, st.session_state["change_param_dict"], state_dict, state, f"{key}_scoring_filename", add_key=True) if not gen_scoring_file else filename # UI State
        filetype = st.selectbox(options=["json", "toml"], label="File format", index=0, key=f"{key}_scoring_filetype")
        filetype = change_param(filetype, st.session_state["change_param_dict"], state_dict, state, f"{key}_scoring_filetype", add_key=True) if not gen_scoring_file else filetype  # UI State
        if stages:
            scoring_file = st.file_uploader(f"Upload Scoring File (S{num_stage})", type=[filetype])
            if scoring_file:
                filename = scoring_file.name[:-5]
            write_show(f'\# Scoring Components (S{num_stage})\n', toml_input, col)
            write_show(f"[stage.scoring]\n", toml_input, col)
            write_show(f'type = "{scoring_weight}_mean"\n', toml_input, col)
            if modus == "Advanced":
                write_show(f'parallel = {run_parallel}\n', toml_input, col)
            else:
                write_show(f'parallel = false\n', toml_input, col)
            write_show(f'filename = "{filename}.{filetype}"\n', toml_input, col)
            write_show(f'filetype = "{filetype}"\n', toml_input, col, empty_line=True)
        else:
            scoring_file = st.file_uploader("Upload Scoring File", type=[filetype])
            if scoring_file:
                filename = scoring_file.name[:-5]
            write_show('\# Scoring Components Parameters\n', toml_input, col)
            write_show(f"[scoring]\n", toml_input, col)
            write_show(f'type = "{scoring_weight}_mean"\n', toml_input, col)
            if modus == "Advanced":
                write_show(f'parallel = {run_parallel}\n', toml_input, col)
            else:
                write_show(f'parallel = false\n', toml_input, col)
            write_show(f'filename = "{filename}.{filetype}"\n', toml_input, col)
            write_show(f'filetype = "{filetype}"\n', toml_input, col, empty_line=True)

        if scoring_file == None: 
            return "Must Be Added!"
        else: 
            return scoring_file

    else:
        if stages:
            if num_stage == None:
                write_show(f'\# Scoring Components\n', toml_input, col)
            else:
                write_show(f'\# Scoring Components (S{num_stage})\n', toml_input, col)
            write_show(f"[stage.scoring]\n", toml_input, col)
            write_show(f'type = "{scoring_weight}_mean"\n', toml_input, col)
            if modus == "Advanced":
                write_show(f'parallel = {run_parallel}\n', toml_input, col, empty_line=True)
            else:
                write_show(f'parallel = false\n', toml_input, col, empty_line=True)
        else:
            if not gen_scoring_file:
                write_show('\# Scoring Components Parameters\n', toml_input, col)
                write_show(f"[scoring]\n", toml_input, col)
                write_show(f'type = "{scoring_weight}_mean"\n', toml_input, col)
                if modus == "Advanced":
                    write_show(f'parallel = {run_parallel}\n', toml_input, col, empty_line=True)
                else:
                    write_show(f'parallel = false\n', toml_input, col, empty_line=True)

        ## Select scoring components
        scor_components = st.multiselect("Select scoring components", scor_comp, default=None, key=f"{key}_scor_components", placeholder="Choose an option")
        scor_components = change_param(scor_components, st.session_state["change_param_dict"], state_dict, state, f"{key}_scor_components", add_key=True) if not gen_scoring_file else scor_components # UI State 

        advanced = True if modus == "Advanced" else False 
        for i, comp in enumerate(scor_components):
            i += 1
            st.write(f"**{i}) Component: {comp}**")

            ## PMI Parameters
            if comp == "PMI":                    
                # Reset values
                if not gen_scoring_file:
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_name_{i}"] = {"key": f"{key}_{comp}_name_{i}", "value": "ScoringComponent"}  # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_weight_{i}"] = {"key": f"{key}_{comp}_weight_{i}", "value": 1.0}             # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_prop_{i}"] = {"key": f"{key}_{comp}_prop_{i}", "value": "npr1"}              # reset value
                with st.popover("PMI Parameters"):
                    # Input Widgets
                    comp_name = st.text_input(label="Name of scoring component in output file", value='ScoringComponent', key=f"{key}_{comp}_name_{i}")
                    comp_name = change_param(comp_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_name_{i}", add_key=True) if not gen_scoring_file else comp_name # UI State
                    comp_weight = st.number_input(label="Weight of scoring component", value=1.0, min_value=0.0, max_value=None, step=0.1, key=f"{key}_{comp}_weight_{i}")
                    comp_weight = change_param(comp_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_weight_{i}", add_key=True) if not gen_scoring_file else comp_weight # UI State
                    pmi_property = st.selectbox(f"Type of PMI Propertiy", ["npr1", "npr2"], index=0, key=f"{key}_{comp}_prop_{i}", help="npr1 - First Normalised PMI (i.e. I₁ / I₃) \n\n npr2 - Second Normalised PMI (i.e. I₂ / I₃) ")
                    pmi_property = change_param(pmi_property, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_prop_{i}", add_key=True) if not gen_scoring_file else pmi_property # UI State
                    # Write to TOML file and Display to user
                    write_scor_component(comp, toml_input, col, stages=stages)
                    write_show(f'name = "{comp_name}"\n', toml_input, col)
                    write_show(f'weight = {float(comp_weight):.2f}\n', toml_input, col)
                    write_show(f'params.property = "{pmi_property}"\n', toml_input, col)
                    trans_para_input(toml_input, col, state_dict, state, low_value=transformers_def_param[comp]["low_value"], high_value=transformers_def_param[comp]["high_value"], 
                                     step=1, key=f"{key}_{comp}_{i}", default=transformers_def_param[comp]["default_transformer"], advanced=advanced, gen_scoring_file=gen_scoring_file)

            ## CustomAlerts Parameters
            elif comp == "CustomAlerts":
                default_SMARTS = "[*;r8],,[*;r9],,[*;r10],,[*;r11],,[*;r12],,[*;r13],,[*;r14],,[*;r15],,[*;r16],,[*;r17],,[#8][#8],,[#6;+],,[#16][#16],,[#7;!n][S;!$(S(=O)=O)],,[#7;!n][#7;!n],,C#C,,C(=[O,S])[O,S],,[#7;!n][C;!$(C(=[O,N])[N,O])][#16;!s],,[#7;!n][C;!$(C(=[O,N])[N,O])][#7;!n],,[#7;!n][C;!$(C(=[O,N])[N,O])][#8;!o],,[#8;!o][C;!$(C(=[O,N])[N,O])][#16;!s],,[#8;!o][C;!$(C(=[O,N])[N,O])][#8;!o],,[#16;!s][C;!$(C(=[O,N])[N,O])][#16;!s]"
                # Reset values
                if not gen_scoring_file:
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_name_{i}"] = {"key": f"{key}_{comp}_name_{i}", "value": "ScoringComponent"}  # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_weight_{i}"] = {"key": f"{key}_{comp}_weight_{i}", "value": 1.0}             # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_smarts_{i}"] = {"key": f"{key}_{comp}_smarts_{i}", "value": default_SMARTS}  # reset value
                with st.popover("CustomAlerts Parameters"):
                    # Input Widgets
                    comp_name = st.text_input(label="Name of scoring component in output file", value='ScoringComponent', key=f"{key}_{comp}_name_{i}")
                    comp_name = change_param(comp_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_name_{i}", add_key=True) if not gen_scoring_file else comp_name  # UI State
                    comp_weight = st.number_input(label="Weight of scoring component", value=1.0, min_value=0.0, max_value=None, step=0.1, key=f"{key}_{comp}_weight_{i}")
                    comp_weight = change_param(comp_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_weight_{i}", add_key=True) if not gen_scoring_file else comp_weight # UI State
                    smarts_text = st.text_input(label="List of undesired SMARTS patterns", value=default_SMARTS, key=f"{key}_{comp}_smarts_{i}",
                                                help="The user could type in specific SMARTS pattern (must be separated with 2 commas ',,'), or choose form the pre-defined table of SMARTS pattern below.")
                    smarts_text = change_param(smarts_text, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_smarts_{i}", add_key=True) if not gen_scoring_file else smarts_text # UI State
                    smarts_df = smarts_table(comp, str(i))
                    if len(smarts_df[smarts_df["Status"] == True]) > 0: 
                        smarts_pattern = smarts_text.split(',,') + list(smarts_df[smarts_df["Status"] == True]["SMARTS"]) if smarts_text != '' else list(smarts_df[smarts_df["Status"] == True]["SMARTS"])
                    else:
                        smarts_pattern = f"{[f'{smart}' for smart in smarts_text.split(',,')]}"
                    # Write to TOML file and Display to user
                    write_scor_component(comp, toml_input, col, stages=stages)
                    write_show(f'name = "{comp_name}"\n', toml_input, col)
                    write_show(f'weight = {float(comp_weight):.2f}\n', toml_input, col)
                    write_show(f'params.smarts = {smarts_pattern}\n', toml_input, col, empty_line=True, display=False)
                    col.text(f"params.smarts = {smarts_pattern}")
                    col.write("\n")

            ## GroupCount Parameters
            elif comp == "GroupCount":
                # Reset values
                if not gen_scoring_file:
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_name_{i}"] = {"key": f"{key}_{comp}_name_{i}", "value": "ScoringComponent"}  # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_weight_{i}"] = {"key": f"{key}_{comp}_weight_{i}", "value": 1.0}             # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_smarts_{i}"] = {"key": f"{key}_{comp}_smarts_{i}", "value": "[CX3]=[OX1]"}   # reset value
                with st.popover("GroupCount Parameters"):
                    # Input Widgets
                    comp_name = st.text_input(label="Name of scoring component in output file", value='ScoringComponent', key=f"{key}_{comp}_name_{i}")
                    comp_name = change_param(comp_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_name_{i}", add_key=True) if not gen_scoring_file else comp_name # UI State
                    comp_weight = st.number_input(label="Weight of scoring component", value=1.0, min_value=0.0, max_value=None, step=0.1, key=f"{key}_{comp}_weight_{i}")
                    comp_weight = change_param(comp_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_weight_{i}", add_key=True) if not gen_scoring_file else comp_weight # UI State
                    smarts_text = st.text_input(label="SMARTS patterns to be counted", value="[CX3]=[OX1]", key=f"{key}_{comp}_smarts_{i}",
                                                help="Count how many times the SMARTS pattern is found")
                    smarts_text = change_param(smarts_text, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_smarts_{i}", add_key=True) if not gen_scoring_file else smarts_text # UI State
                    smarts_df = smarts_table(comp, str(i), with_status=False)
                    # Write to TOML file and Display to user
                    write_scor_component(comp, toml_input, col, stages=stages)
                    write_show(f'name = "{comp_name}"\n', toml_input, col)
                    write_show(f'weight = {float(comp_weight):.2f}\n', toml_input, col)
                    write_show(f'params.smarts = "{smarts_text}"\n', toml_input, col)
                    trans_para_input(toml_input, col, state_dict, state, low_value=transformers_def_param[comp]["low_value"], high_value=transformers_def_param[comp]["high_value"], 
                                     step=1, key=f"{key}_{comp}_{i}", default=transformers_def_param[comp]["default_transformer"], advanced=advanced, gen_scoring_file=gen_scoring_file)

            ## MatchingSubstructure Parameters
            elif comp == "MatchingSubstructure":
                # Reset values
                if not gen_scoring_file:
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_name_{i}"] = {"key": f"{key}_{comp}_name_{i}", "value": "ScoringComponent"}  # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_weight_{i}"] = {"key": f"{key}_{comp}_weight_{i}", "value": 1.0}             # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_smarts_{i}"] = {"key": f"{key}_{comp}_smarts_{i}", "value": "[CX3]=[OX1]"}   # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_chirality_{i}"] = {"key": f"{key}_{comp}_chirality_{i}", "value": "false"}   # reset value
                with st.popover("MatchingSubstructure Parameters"):
                    # Input Widgets
                    comp_name = st.text_input(label="Name of scoring component in output file", value='ScoringComponent', key=f"{key}_{comp}_name_{i}")
                    comp_name = change_param(comp_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_name_{i}", add_key=True) if not gen_scoring_file else comp_name # UI State
                    comp_weight = st.number_input(label="Weight of scoring component", value=1.0, min_value=0.0, max_value=None, step=0.1, key=f"{key}_{comp}_weight_{i}")
                    comp_weight = change_param(comp_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_weight_{i}", add_key=True) if not gen_scoring_file else comp_weight # UI State
                    smarts_text = st.text_input(label="SMARTS pattern", value="[CX3]=[OX1]", key=f"{key}_{comp}_smarts_{i}",
                                                help="preserve the final score when the SMARTS pattern is found, otherwise penalize it (multiply by 0.5)")
                    smarts_text = change_param(smarts_text, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_smarts_{i}", add_key=True) if not gen_scoring_file else smarts_text # UI State
                    smarts_df = smarts_table(comp, str(i), with_status=False)
                    use_chirality = st.selectbox(options=["true", "false"], label="Check for chirality?", index=1, key=f"{key}_{comp}_chirality_{i}")
                    use_chirality = change_param(use_chirality, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_chirality_{i}", add_key=True) if not gen_scoring_file else use_chirality # UI State
                    # Write to TOML file and Display to user
                    write_scor_component(comp, toml_input, col, stages=stages)
                    write_show(f'name = "{comp_name}"\n', toml_input, col)
                    write_show(f'weight = {float(comp_weight):.2f}\n', toml_input, col)
                    write_show(f'params.smarts = "{smarts_text}"\n', toml_input, col)
                    write_show(f'params.use_chirality = {use_chirality}\n', toml_input, col, empty_line=True)

            ## TanimotoSimilarity Parameters
            elif comp == "TanimotoSimilarity":
                # Reset values
                if not gen_scoring_file:
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_name_{i}"] = {"key": f"{key}_{comp}_name_{i}", "value": "ScoringComponent"}  # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_weight_{i}"] = {"key": f"{key}_{comp}_weight_{i}", "value": 1.0}             # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_smiles_{i}"] = {"key": f"{key}_{comp}_smiles_{i}", "value": "CC(=O)OC1=CC=CC=C1C(=O)O,,CC(=O)OC1=CC=CC=C1C(=O)O"}   # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_upload_{i}"] = {"key": f"{key}_{comp}_upload_{i}", "value": False}           # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_radius_{i}"] = {"key": f"{key}_{comp}_radius_{i}", "value": 1}               # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_counts_{i}"] = {"key": f"{key}_{comp}_counts_{i}", "value": "true"}          # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_features_{i}"] = {"key": f"{key}_{comp}_features_{i}", "value": "true"}      # reset value
                with st.popover("TanimotoSimilarity Parameters"):
                    # Input Widgets
                    comp_name = st.text_input(label="Name of scoring component in output file", value='ScoringComponent', key=f"{key}_{comp}_name_{i}")
                    comp_name = change_param(comp_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_name_{i}", add_key=True) if not gen_scoring_file else comp_name # UI State
                    comp_weight = st.number_input(label="Weight of scoring component", value=1.0, min_value=0.0, max_value=None, step=0.1, key=f"{key}_{comp}_weight_{i}")
                    comp_weight = change_param(comp_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_weight_{i}", add_key=True) if not gen_scoring_file else comp_weight # UI State
                    smiles_text = st.text_input(label="List of SMILES to match against", value="CC(=O)OC1=CC=CC=C1C(=O)O,,CC(=O)OC1=CC=CC=C1C(=O)O", 
                                                key=f"{key}_{comp}_smiles_{i}", help="Must be separated with 2 commas ',,'")
                    smiles_text = change_param(smiles_text, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_smiles_{i}", add_key=True) if not gen_scoring_file else smiles_text # UI State
                    upload = st.toggle("Read SMILES from a SMILES file?", value=False, key=f"{key}_{comp}_upload_{i}")
                    upload = change_param(upload, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_upload_{i}", add_key=True) if not gen_scoring_file else upload # UI State
                    if upload: 
                        smiles_upload = st.file_uploader(f"Upload SMILES file ({key}-{comp}-{i})", type=["smi", "sdf"], help="SMILES (.smi) and Structures Data File (.sdf) are the **ONLY** accepted format.")
                        if smiles_upload:
                            smiles_file = save_uploaded_file(smiles_upload, Path(st.session_state["user_folder"]))
                            file_name = smiles_upload.name
                            if (".sdf" in file_name): 
                                smiles_file = convert_sdf_smi(smiles_file)
                            smiles_list = read_smiles(smiles_file)
                            smiles_list = smiles_list # smiles_text.split(',,') + smiles_list if smiles_text != "" else smiles_list
                        else:
                            smiles_list = smiles_text.split(',,')
                    else:
                        smiles_list = smiles_text.split(',,')
                    radius = st.number_input(label="Morgan fingerprint radius", value=1, min_value=0, max_value=None, step=1, key=f"{key}_{comp}_radius_{i}")
                    radius = change_param(radius, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_radius_{i}", add_key=True) if not gen_scoring_file else radius # UI State
                    use_counts = st.selectbox(options=["true", "false"], label="Use counts", index=0, key=f"{key}_{comp}_counts_{i}")
                    use_counts = change_param(use_counts, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_counts_{i}", add_key=True) if not gen_scoring_file else use_counts # UI State
                    use_features = st.selectbox(options=["true", "false"], label="Use features", index=0, key=f"{key}_{comp}_features_{i}")
                    use_features = change_param(use_features, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_features_{i}", add_key=True) if not gen_scoring_file else use_features # UI State
                    # Write to TOML file and Display to user
                    write_scor_component(comp, toml_input, col, stages=stages)
                    write_show(f'name = "{comp_name}"\n', toml_input, col)
                    write_show(f'weight = {float(comp_weight):.2f}\n', toml_input, col)
                    write_show(f'params.smiles = {smiles_list}\n', toml_input, col)
                    write_show(f'params.radius = {radius}\n', toml_input, col)
                    write_show(f'params.use_counts = {use_counts}\n', toml_input, col)
                    write_show(f'params.use_features = {use_features}\n', toml_input, col, empty_line=True)
            
            ## MMP Parameters
            elif comp == "MMP":
                # Reset values
                if not gen_scoring_file:
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_name_{i}"] = {"key": f"{key}_{comp}_name_{i}", "value": "ScoringComponent"}  # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_weight_{i}"] = {"key": f"{key}_{comp}_weight_{i}", "value": 1.0}             # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_smiles_{i}"] = {"key": f"{key}_{comp}_smiles_{i}", "value": "CC(=O)OC1=CC=CC=C1C(=O)O,,CC(=O)OC1=CC=CC=C1C(=O)O"}   # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_upload_{i}"] = {"key": f"{key}_{comp}_upload_{i}", "value": False}           # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_num_of_cuts_{i}"] = {"key": f"{key}_{comp}_num_of_cuts_{i}", "value": 1}               # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_max_variable_heavies_{i}"] = {"key": f"{key}_{comp}_max_variable_heavies_{i}", "value": 40}          # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_max_variable_ratio_{i}"] = {"key": f"{key}_{comp}_max_variable_ratio_{i}", "value": 0.33}      # reset value
                with st.popover("MMP Parameters"):
                    # Input Widgets
                    comp_name = st.text_input(label="Name of scoring component in output file", value='ScoringComponent', key=f"{key}_{comp}_name_{i}")
                    comp_name = change_param(comp_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_name_{i}", add_key=True) if not gen_scoring_file else comp_name # UI State
                    comp_weight = st.number_input(label="Weight of scoring component", value=1.0, min_value=0.0, max_value=None, step=0.1, key=f"{key}_{comp}_weight_{i}")
                    comp_weight = change_param(comp_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_weight_{i}", add_key=True)  if not gen_scoring_file else comp_weight # UI State
                    smiles_text = st.text_input(label="List of reference SMILES to be similar to", value="CC(=O)OC1=CC=CC=C1C(=O)O,,CC(=O)OC1=CC=CC=C1C(=O)O", 
                                                key=f"{key}_{comp}_smiles_{i}", help="SMILES must be comma-separated with 2 commas (,,)")
                    smiles_text = change_param(smiles_text, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_smiles_{i}", add_key=True)  if not gen_scoring_file else smiles_text # UI State
                    upload = st.toggle("Read SMILES from a SMILES file?", value=False, key=f"{key}_{comp}_upload_{i}")
                    upload = change_param(upload, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_upload_{i}", add_key=True) if not gen_scoring_file else upload # UI State
                    if upload: 
                        smiles_upload = st.file_uploader(f"Upload SMILES file ({key}-{comp}-{i})", type=["smi", "sdf"], help="SMILES (.smi) and Structures Data File (.sdf) are the **ONLY** accepted format.")
                        if smiles_upload:
                            smiles_file = save_uploaded_file(smiles_upload, Path(st.session_state["user_folder"]))
                            file_name = smiles_upload.name
                            if (".sdf" in file_name): 
                                smiles_file = convert_sdf_smi(smiles_file)
                            smiles_list = read_smiles(smiles_file)
                            smiles_list = smiles_list #smiles_text.split(',,') + smiles_list if smiles_text != "" else smiles_list
                        else:
                            smiles_list = smiles_text.split(',,')
                    else:
                        smiles_list = smiles_text.split(',,')
                    num_of_cuts = st.number_input(label="Number of bonds to cut in fragmentation", value=1, min_value=0, max_value=None, step=1, key=f"{key}_{comp}_num_of_cuts_{i}")
                    num_of_cuts = change_param(num_of_cuts, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_num_of_cuts_{i}", add_key=True) if not gen_scoring_file else num_of_cuts # UI State
                    max_variable_heavies = st.number_input(label="Max heavy atom change in MMPs", value=40, min_value=0, max_value=None, step=1, key=f"{key}_{comp}_max_variable_heavies_{i}")
                    max_variable_heavies = change_param(max_variable_heavies, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_max_variable_heavies_{i}", add_key=True) if not gen_scoring_file else max_variable_heavies # UI State
                    max_variable_ratio = st.number_input(label="Max ratio of heavy atoms in MMPs", value=0.33, min_value=0.0, max_value=1.0, step=0.01, key=f"{key}_{comp}_max_variable_ratio_{i}")
                    max_variable_ratio = change_param(max_variable_ratio, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_max_variable_ratio_{i}", add_key=True) if not gen_scoring_file else max_variable_ratio # UI State
                    # Write to TOML file and Display to user
                    write_scor_component(comp, toml_input, col, stages=stages)
                    write_show(f'name = "{comp_name}"\n', toml_input, col)
                    write_show(f'weight = {float(comp_weight):.2f}\n', toml_input, col)
                    write_show(f'params.reference_smiles = {smiles_list}\n', toml_input, col)
                    write_show(f'params.num_of_cuts = {num_of_cuts}\n', toml_input, col)
                    write_show(f'params.max_variable_heavies = {max_variable_heavies}\n', toml_input, col)
                    write_show(f'params.max_variable_ratio = {max_variable_ratio}\n', toml_input, col)
                    trans_para_input(toml_input, col, state_dict, state, low_value=transformers_def_param[comp]["low_value"], high_value=transformers_def_param[comp]["high_value"], 
                                     step=1, key=f"{key}_{comp}_{i}", default=transformers_def_param[comp]["default_transformer"], advanced=advanced, gen_scoring_file=gen_scoring_file)

            ## ROCSSimilarity Parameters
            elif comp == "ROCSSimilarity":
                # Reset values
                if not gen_scoring_file:
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_name_{i}"] = {"key": f"{key}_{comp}_name_{i}", "value": "ScoringComponent"}                     # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_weight_{i}"] = {"key": f"{key}_{comp}_weight_{i}", "value": 1.0}                                # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_color_weight_{i}"] = {"key": f"{key}_{comp}_color_weight_{i}", "value": 0.5}                    # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_shape_weight_{i}"] = {"key": f"{key}_{comp}_shape_weight_{i}", "value": 0.5}                    # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_custom_cff_{i}"] = {"key": f"{key}_{comp}_custom_cff_{i}", "value": "path/to/ROCs/forcefield"}  # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_similarity_measure_{i}"] = {"key": f"{key}_{comp}_similarity_measure_{i}", "value": "Tanimoto"} # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_max_stereocenters_{i}"] = {"key": f"{key}_{comp}_max_stereocenters_{i}", "value": 4}            # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_ewindow_{i}"] = {"key": f"{key}_{comp}_ewindow_{i}", "value": 10}
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_maxconfs_{i}"] = {"key": f"{key}_{comp}_maxconfs_{i}", "value": 200}
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_rocs_input_{i}"] = {"key": f"{key}_{comp}_rocs_input_{i}", "value": "YOUR_ROCS_QUERY.sdf"}
                with st.popover("ROCSSimilarity Parameters"):
                    # Input Widgets
                    comp_name = st.text_input(label="Name of scoring component in output file", value='ScoringComponent', key=f"{key}_{comp}_name_{i}")
                    comp_name = change_param(comp_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_name_{i}", add_key=True) if not gen_scoring_file else comp_name # UI State
                    comp_weight = st.number_input(label="Weight of scoring component", value=1.0, min_value=0.0, max_value=None, step=0.1, key=f"{key}_{comp}_weight_{i}")
                    comp_weight = change_param(comp_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_weight_{i}", add_key=True) if not gen_scoring_file else comp_weight # UI State
                    color_weight = st.slider(label="Weighting between shape and color scores, color weight:", value=0.5, min_value=0.0, max_value=1.0, step=0.01, key=f"{key}_{comp}_color_weight_{i}", on_change=color_to_shape)
                    color_weight = change_param(color_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_color_weight_{i}", add_key=True) if not gen_scoring_file else color_weight # UI State
                    shape_weight = st.slider(label="Weighting between shape and color scores, shape weight:", value=0.5, min_value=0.0, max_value=1.0, step=0.01, key=f"{key}_{comp}_shape_weight_{i}", on_change=shape_to_color)
                    shape_weight = change_param(shape_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_shape_weight_{i}", add_key=True) if not gen_scoring_file else shape_weight # UI State
                    if modus == "Advanced":
                        custom_cff = st.text_input(label="Path to custom ROCs forecfield", value="path/to/ROCs/forcefield", key=f"{key}_{comp}_custom_cff_{i}")
                        custom_cff = change_param(custom_cff, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_custom_cff_{i}", add_key=True) if not gen_scoring_file else custom_cff # UI State
                    similarity_measure = st.selectbox(label="How to compare shapes", options=["Tanimoto", "RefTversky", "FitTversky"], index=0, key=f"{key}_{comp}_similarity_measure_{i}")
                    similarity_measure = change_param(similarity_measure, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_similarity_measure_{i}", add_key=True) if not gen_scoring_file else similarity_measure # UI State
                    max_stereocenters = st.number_input(label="Max number of stereo centers to enumerate", value=4, min_value=0, max_value=None, step=1, key=f"{key}_{comp}_max_stereocenters_{i}")
                    max_stereocenters = change_param(max_stereocenters, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_max_stereocenters_{i}", add_key=True) if not gen_scoring_file else max_stereocenters # UI State
                    ewindow =  st.number_input(label="Energy window for conformers (kJ/mol)", value=10, min_value=0, max_value=None, step=1, key=f"{key}_{comp}_ewindow_{i}")
                    ewindow = change_param(ewindow, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_ewindow_{i}", add_key=True) if not gen_scoring_file else ewindow # UI State
                    maxconfs = st.number_input(label="Max number of confs per compound", value=200, min_value=0, max_value=None, step=1, key=f"{key}_{comp}_maxconfs_{i}")
                    maxconfs = change_param(maxconfs, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_maxconfs_{i}", add_key=True) if not gen_scoring_file else maxconfs # UI State
                    rocs_input = st.text_input(label="Input file with molecules", value="YOUR_ROCS_QUERY.sdf", key=f"{key}_{comp}_rocs_input_{i}")
                    rocs_input = change_param(rocs_input, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_rocs_input_{i}", add_key=True) if not gen_scoring_file else rocs_input # UI State
                    # Upload SDF or SQ File
                    sdf_upload = st.file_uploader(f"Upload SDF or SQ File ({key}-{comp}-{i})", type=["sq", "sdf"], help="Structures Data File (.sdf) and .SQ Files are the **ONLY** accepted format.")
                    needed_files[f"SDF File ({key}-{comp}-{i})"] = False          
                    if sdf_upload:
                        rocs_input = sdf_upload.name
                        sdf_upload = save_uploaded_file(sdf_upload, Path(st.session_state["user_folder"]))
                        uploaded_files[f"SDF File ({key}-{comp}-{i})"] = sdf_upload
                        needed_files[f"SDF File ({key}-{comp}-{i})"] = True                
                    # Write to TOML file and Display to user
                    write_scor_component(comp, toml_input, col, stages=stages)
                    write_show(f'name = "{comp_name}"\n', toml_input, col)
                    write_show(f'weight = {float(comp_weight):.2f}\n', toml_input, col)
                    write_show(f'params.color_weight = {color_weight:.2f}\n', toml_input, col)
                    write_show(f'params.shape_weight = {shape_weight:.2f}\n', toml_input, col)
                    if modus == "Advanced":
                        write_show(f'params.custom_cff = {custom_cff}\n', toml_input, col)
                    write_show(f'params.similarity_measure = "{similarity_measure}"\n', toml_input, col)
                    write_show(f'params.max_stereocenters = {max_stereocenters}\n', toml_input, col)
                    write_show(f'params.ewindow = {ewindow}\n', toml_input, col)
                    write_show(f'params.maxconfs = {maxconfs}\n', toml_input, col)
                    write_show(f'params.rocs_input = "{rocs_input}"\n', toml_input, col)
                    trans_para_input(toml_input, col, state_dict, state, low_value=transformers_def_param[comp]["low_value"], high_value=transformers_def_param[comp]["high_value"], 
                                     step=1, key=f"{key}_{comp}_{i}", default=transformers_def_param[comp]["default_transformer"], advanced=advanced, gen_scoring_file=gen_scoring_file)

            ## DockStream Parameters
            elif comp == "DockStream":
                # Reset values
                if not gen_scoring_file:
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_name_{i}"] = {"key": f"{key}_{comp}_name_{i}", "value": "ScoringComponent"}                                             # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_weight_{i}"] = {"key": f"{key}_{comp}_weight_{i}", "value": 1.0}                                                        # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_config_path_{i}"] = {"key": f"{key}_{comp}_config_path_{i}", "value": "./dockstream_config.json"}                       # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_docker_path_{i}"] = {"key": f"{key}_{comp}_docker_path_{i}", "value": "/apps/miniforge3/envs/DockerStream/docker.py"}   # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_python_path_{i}"] = {"key": f"{key}_{comp}_python_path_{i}", "value": "/apps/anaconda/anaconda3/bin/python"}            # reset value
                with st.popover("DockStream Parameters"):
                    # Input Widgets
                    comp_name = st.text_input(label="Name of scoring component in output file", value='ScoringComponent', key=f"{key}_{comp}_name_{i}")
                    comp_name = change_param(comp_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_name_{i}", add_key=True) if not gen_scoring_file else comp_name # UI State
                    comp_weight = st.number_input(label="Weight of scoring component", value=1.0, min_value=0.0, max_value=None, step=0.1, key=f"{key}_{comp}_weight_{i}")
                    comp_weight = change_param(comp_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_weight_{i}", add_key=True) if not gen_scoring_file else comp_weight # UI State
                    config_path = st.text_input(label="Path for the Dockstream config file (.json)", value="./dockstream_config.json", key=f"{key}_{comp}_config_path_{i}")
                    config_path = change_param(config_path, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_config_path_{i}", add_key=True) if not gen_scoring_file else config_path # UI State
                    docker_path = st.text_input(label="Path for the Dockstream file (docker.py)", value="/apps/miniforge3/envs/DockerStream/docker.py", key=f"{key}_{comp}_docker_path_{i}")
                    docker_path = change_param(docker_path, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_docker_path_{i}", add_key=True) if not gen_scoring_file else docker_path # UI State
                    python_path = st.text_input(label="Path for python interpreter", value="/apps/anaconda/anaconda3/bin/python", key=f"{key}_{comp}_python_path_{i}")
                    python_path = change_param(python_path, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_python_path_{i}", add_key=True) if not gen_scoring_file else python_path # UI State
                    # Upload Docking Config file and Grid Folder
                    config_upload = st.file_uploader(f"Upload dockstream config file ({key}-{comp}-{i})", type=["json"], help="Json is the **ONLY** accepted format.")
                    grid_upload = st.file_uploader(f"Upload grid folder ({key}-{comp}-{i})", help="Upload the grid folder for the docking calculation.")
                    needed_files[f"Docking Config ({key}-{comp}-{i})"] = False    
                    needed_files[f"Docking Grid ({key}-{comp}-{i})"] = False          
                    if config_upload:
                        config_path = config_upload.name
                        config_upload = save_uploaded_file(config_upload, Path(st.session_state["user_folder"]))
                        uploaded_files[f"Docking Config ({key}-{comp}-{i})"] = config_upload
                        needed_files[f"Docking Config ({key}-{comp}-{i})"] = True   
                    if grid_upload: 
                        grid_upload = save_uploaded_file(grid_upload, Path(st.session_state["user_folder"]))
                        uploaded_files[f"Docking Grid ({key}-{comp}-{i})"] = grid_upload
                        needed_files[f"Docking Grid ({key}-{comp}-{i})"] = True         
                    # Write to TOML file and Display to user
                    write_scor_component(comp, toml_input, col, stages=stages)
                    write_show(f'name = "{comp_name}"\n', toml_input, col)
                    write_show(f'weight = {float(comp_weight):.2f}\n', toml_input, col)
                    write_show(f'params.configuration_path = "{config_path}"\n', toml_input, col)
                    write_show(f'params.docker_script_path = "{docker_path}"\n', toml_input, col)
                    write_show(f'params.docker_python_path = "{python_path}"\n', toml_input, col)
                    trans_para_input(toml_input, col, state_dict, state, low_value=transformers_def_param[comp]["low_value"], high_value=transformers_def_param[comp]["high_value"], 
                                     step=1, key=f"{key}_{comp}_{i}", default=transformers_def_param[comp]["default_transformer"], advanced=advanced, gen_scoring_file=gen_scoring_file)
                
            ## AutoQSAR Parameters 
            elif comp == "AutoQSAR":
                # Reset values
                if not gen_scoring_file:
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_name_{i}"] = {"key": f"{key}_{comp}_name_{i}", "value": "ScoringComponent"}        # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_weight_{i}"] = {"key": f"{key}_{comp}_weight_{i}", "value": 1.0}           # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_autoqsar_path_{i}"] = {"key": f"{key}_{comp}_autoqsar_path_{i}", "value": "/apps/schrodinger/advsuite2024-1/utilities/autoqsar"}       # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_model_name_{i}"] = {"key": f"{key}_{comp}_model_name_{i}", "value": "autoqsar_model.qzip"}   # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_pred_col_{i}"] = {"key": f"{key}_{comp}_pred_col_{i}", "value": "r_autoqsar_Pred_Y"}      # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_cache_dir_{i}"] = {"key": f"{key}_{comp}_cache_dir_{i}", "value": "./"}       # reset value
                with st.popover("AutoQSAR Parameters"):
                    # Input Widgets
                    comp_name = st.text_input(label="Name of scoring component in output file", value='ScoringComponent', key=f"{key}_{comp}_name_{i}")
                    comp_name = change_param(comp_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_name_{i}", add_key=True) if not gen_scoring_file else comp_name # UI State
                    comp_weight = st.number_input(label="Weight of scoring component", value=1.0, min_value=0.0, max_value=None, step=0.1, key=f"{key}_{comp}_weight_{i}")
                    comp_weight = change_param(comp_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_weight_{i}", add_key=True) if not gen_scoring_file else comp_weight # UI State
                    autoqsar_path = st.text_input(label="Path for the execution file of AutoQSAR", value="/apps/schrodinger/advsuite2024-1/utilities/autoqsar", key=f"{key}_{comp}_autoqsar_path_{i}")
                    autoqsar_path = change_param(autoqsar_path, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_autoqsar_path_{i}", add_key=True) if not gen_scoring_file else autoqsar_path # UI State
                    model_name = st.text_input(label="Name of AutoQSAR model file", value="autoqsar_model.qzip", help="Must be of Qzip format!", key=f"{key}_{comp}_model_name_{i}")
                    model_name = change_param(model_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_model_name_{i}", add_key=True) if not gen_scoring_file else model_name # UI State
                    pred_col = st.text_input(label="Choose the predicted property", value="r_autoqsar_Pred_Y", key=f"{key}_{comp}_pred_col_{i}")
                    pred_col = change_param(pred_col, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_pred_col_{i}", add_key=True) if not gen_scoring_file else pred_col # UI State
                    cache_dir = st.text_input(label="Path for cache directory", value="./", key=f"{key}_{comp}_cache_dir_{i}", disabled=True)
                    cache_dir = change_param(cache_dir, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_cache_dir_{i}", add_key=True) if not gen_scoring_file else cache_dir # UI State
                    # Upload model file
                    model_upload = st.file_uploader(f"Upload AutoQSAR model ({key}-{comp}-{i})", type=["qzip"], help="Qzip is the **ONLY** accepted format.")
                    needed_files[f"AutoQSAR Model ({key}-{comp}-{i})"] = False          
                    if model_upload:
                        model_name = model_upload.name
                        model_upload = save_uploaded_file(model_upload, Path(st.session_state["user_folder"]))
                        uploaded_files[f"AutoQSAR Model ({key}-{comp}-{i})"] = model_upload
                        needed_files[f"AutoQSAR Model ({key}-{comp}-{i})"] = True     
                    # Write to TOML file and Display to user
                    write_scor_component(comp, toml_input, col, stages=stages)
                    write_show(f'name = "{comp_name}"\n', toml_input, col)
                    write_show(f'weight = {float(comp_weight):.2f}\n', toml_input, col)
                    write_show(f'params.autoqsar_exec = "{autoqsar_path}"\n', toml_input, col)
                    write_show(f'params.model_file = "{model_name}"\n', toml_input, col)
                    write_show(f'params.cache_dir = "{cache_dir}"\n', toml_input, col)
                    write_show(f'params.pred_col = "{pred_col}"\n', toml_input, col)
                    trans_para_input(toml_input, col, state_dict, state, low_value=transformers_def_param[comp]["low_value"], high_value=transformers_def_param[comp]["high_value"], 
                                     step=1, key=f"{key}_{comp}_{i}", default=transformers_def_param[comp]["default_transformer"], advanced=advanced, gen_scoring_file=gen_scoring_file)
                
            ## DeepQSAR Parameters
            elif comp == "DeepQSAR":
                # Reset values
                if not gen_scoring_file:
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_name_{i}"] = {"key": f"{key}_{comp}_name_{i}", "value": "ScoringComponent"}        # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_weight_{i}"] = {"key": f"{key}_{comp}_weight_{i}", "value": 1.0}           # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_deepautoqsar_path_{i}"] = {"key": f"{key}_{comp}_deepautoqsar_path_{i}", "value": "/apps/schrodinger/advsuite2024-1/run"}       # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_model_name_{i}"] = {"key": f"{key}_{comp}_model_name_{i}", "value": "deepqsar_model.qzip"}   # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_cache_dir_{i}"] = {"key": f"{key}_{comp}_cache_dir_{i}", "value": "./"}       # reset value
                with st.popover("DeepQSAR Parameters"):
                    # Input Widgets
                    comp_name = st.text_input(label="Name of scoring component in output file", value='ScoringComponent', key=f"{key}_{comp}_name_{i}")
                    comp_name = change_param(comp_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_name_{i}", add_key=True) if not gen_scoring_file else comp_name # UI State
                    comp_weight = st.number_input(label="Weight of scoring component", value=1.0, min_value=0.0, max_value=None, step=0.1, key=f"{key}_{comp}_weight_{i}")
                    comp_weight = change_param(comp_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_weight_{i}", add_key=True) if not gen_scoring_file else comp_weight # UI State
                    deepautoqsar_path = st.text_input(label="Path for the execution file of DeepQSAR", value="/apps/schrodinger/advsuite2024-1/run", key=f"{key}_{comp}_deepautoqsar_path_{i}")
                    deepautoqsar_path = change_param(deepautoqsar_path, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_deepautoqsar_path_{i}", add_key=True) if not gen_scoring_file else deepautoqsar_path # UI State
                    model_name = st.text_input(label="Name of DeepQSAR model file", value="deepqsar_model.qzip", help="Must be of (.qzip) format!", key=f"{key}_{comp}_model_name_{i}")
                    model_name = change_param(model_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_model_name_{i}", add_key=True) if not gen_scoring_file else model_name # UI State
                    cache_dir = st.text_input(label="Path for cache directory", value="./", key=f"{key}_{comp}_cache_dir_{i}", disabled=True)
                    cache_dir = change_param(cache_dir, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_cache_dir_{i}", add_key=True) if not gen_scoring_file else cache_dir # UI State
                    # Upload model file
                    model_upload = st.file_uploader(f"Upload DeepQSAR model ({key}-{comp}-{i})", type=["qzip"], help="Qzip is the **ONLY** accepted format.")
                    needed_files[f"DeepQSAR Model ({key}-{comp}-{i})"] = False          
                    if model_upload:
                        model_name = model_upload.name
                        model_upload = save_uploaded_file(model_upload, Path(st.session_state["user_folder"]))
                        uploaded_files[f"DeepQSAR Model ({key}-{comp}-{i})"] = model_upload
                        needed_files[f"DeepQSAR Model ({key}-{comp}-{i})"] = True     
                    # Write to TOML file and Display to user
                    write_scor_component(comp, toml_input, col, stages=stages)
                    write_show(f'name = "{comp_name}"\n', toml_input, col)
                    write_show(f'weight = {float(comp_weight):.2f}\n', toml_input, col)
                    write_show(f'params.deepautoqsar_exec = "{deepautoqsar_path}"\n', toml_input, col)
                    write_show(f'params.model_file = "{model_name}"\n', toml_input, col)
                    write_show(f'params.cache_dir = "{cache_dir}"\n', toml_input, col)
                    trans_para_input(toml_input, col, state_dict, state, low_value=transformers_def_param[comp]["low_value"], high_value=transformers_def_param[comp]["high_value"], 
                                     step=1, key=f"{key}_{comp}_{i}", default=transformers_def_param[comp]["default_transformer"], advanced=advanced, gen_scoring_file=gen_scoring_file)
                
            ## pADME Parameters
            elif comp == "pADME":
                # Reset values
                if not gen_scoring_file:
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_name_{i}"] = {"key": f"{key}_{comp}_name_{i}", "value": "ScoringComponent"}        # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_weight_{i}"] = {"key": f"{key}_{comp}_weight_{i}", "value": 1.0}           # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_padme_model_{i}"] = {"key": f"{key}_{comp}_padme_model_{i}", "value": list(transformers_def_param[comp].keys())[0]}       # reset value
                with st.popover("pADME Parameters"):
                    # Input Widgets
                    comp_name = st.text_input(label="Name of scoring component in output file", value='ScoringComponent', key=f"{key}_{comp}_name_{i}")
                    comp_name = change_param(comp_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_name_{i}", add_key=True) if not gen_scoring_file else comp_name # UI State
                    comp_weight = st.number_input(label="Weight of scoring component", value=1.0, min_value=0.0, max_value=None, step=0.1, key=f"{key}_{comp}_weight_{i}")
                    comp_weight = change_param(comp_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_weight_{i}", add_key=True) if not gen_scoring_file else comp_weight # UI State
                    padme_models = st.selectbox(label="Select pADME model", options=PADME_models, index=0, key=f"{key}_{comp}_padme_model_{i}", 
                                                help="**Note**: The user must ensure that REINVENT has access to the user-defined ADME models.")
                    padme_models = change_param(padme_models, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_padme_model_{i}", add_key=True) if not gen_scoring_file else padme_models # UI State
                    # Write to TOML file and Display to user
                    write_scor_component(comp, toml_input, col, stages=stages)
                    write_show(f'name = "{comp_name}"\n', toml_input, col)
                    write_show(f'weight = {float(comp_weight):.2f}\n', toml_input, col)
                    write_show(f'params.property_name = "{padme_models}"\n', toml_input, col)
                    trans_para_input(toml_input, col, state_dict, state, low_value=transformers_def_param[comp][padme_models]["low_value"], high_value=transformers_def_param[comp][padme_models]["high_value"], 
                                     step=1, key=f"{key}_{comp}_{i}", default=transformers_def_param[comp][padme_models]["default_transformer"], advanced=advanced, gen_scoring_file=gen_scoring_file)

            ## ReactionFilter Parameters
            elif comp == "ReactionFilter":
                # Reset values
                if not gen_scoring_file:
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_name_{i}"] = {"key": f"{key}_{comp}_name_{i}", "value": "ScoringComponent"}     # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_weight_{i}"] = {"key": f"{key}_{comp}_weight_{i}", "value": 1.0}                # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_filter_type_{i}"] = {"key": f"{key}_{comp}_filter_type_{i}", "value": "IdenticalMurckoScaffold"}         # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_reaction_smarts_{i}"] = {"key": f"{key}_{comp}_reaction_smarts_{i}", "value": "[F, Cl]"}         # reset value
                with st.popover("ReactionFilter Parameters"):
                    # Input Widgets
                    comp_name = st.text_input(label="Name of scoring component in output file", value='ScoringComponent', key=f"{key}_{comp}_name_{i}")
                    comp_name = change_param(comp_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_name_{i}", add_key=True) if not gen_scoring_file else comp_name # UI State
                    comp_weight = st.number_input(label="Weight of scoring component", value=1.0, min_value=0.0, max_value=None, step=0.1, key=f"{key}_{comp}_weight_{i}")
                    comp_weight = change_param(comp_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_weight_{i}", add_key=True) if not gen_scoring_file else comp_weight # UI State
                    filter_type = st.selectbox(f"Select filter type", ["IdenticalMurckoScaffold", "IdenticalTopologicalScaffold", "ScaffoldSimilarity", "PenalizeSameSmiles"], index=0, key=f"{key}_{comp}_filter_type_{i}")
                    filter_type = change_param(filter_type, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_filter_type_{i}", add_key=True) if not gen_scoring_file else filter_type # UI State
                    reaction_smarts = st.text_input(label="RDKit reaction SMARTS", value="[F, Cl]", key=f"{key}_{comp}_reaction_smarts_{i}")
                    reaction_smarts = change_param(reaction_smarts, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_reaction_smarts_{i}", add_key=True) if not gen_scoring_file else reaction_smarts # UI State
                    smarts_df = smarts_table(comp, str(i))
                    if len(smarts_df[smarts_df["Status"] == True]) > 0: 
                        smarts_pattern = reaction_smarts.split(',,') + list(smarts_df[smarts_df["Status"] == True]["SMARTS"]) if reaction_smarts != '' else list(smarts_df[smarts_df["Status"] == True]["SMARTS"])
                    else:
                        smarts_pattern = f"{[f'{smart}' for smart in reaction_smarts.split(',,')]}"
                    # Write to TOML file and Display to user
                    write_scor_component(comp, toml_input, col, stages=stages)
                    write_show(f'name = "{comp_name}"\n', toml_input, col)
                    write_show(f'weight = {float(comp_weight):.2f}\n', toml_input, col)
                    write_show(f'params.type = "{filter_type}"\n', toml_input, col)
                    write_show(f'params.reaction_smarts = "{smarts_pattern}"\n', toml_input, col, empty_line=True, display=False)
                    col.text(f'params.reaction_smarts = "{smarts_pattern}"')
                    col.write("\n")

            ## All other scoring components 
            else:
                # Reset values
                if not gen_scoring_file:
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_name_{i}"] = {"key": f"{key}_{comp}_name_{i}", "value": "ScoringComponent"}     # reset value
                    state_dict_reset[st.session_state["run_mode"]][f"{key}_{comp}_weight_{i}"] = {"key": f"{key}_{comp}_weight_{i}", "value": 1.0}                # reset value
                with st.popover(f"{comp} Parameters"):
                    # Input Widgets
                    comp_name = st.text_input(label="Name of scoring component in output file", value='ScoringComponent', key=f"{key}_{comp}_name_{i}")
                    comp_name = change_param(comp_name, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_name_{i}", add_key=True) if not gen_scoring_file else comp_name # UI State
                    comp_weight = st.number_input(label="Weight of scoring component", value=1.0, min_value=0.0, max_value=None, step=0.1, key=f"{key}_{comp}_weight_{i}")
                    comp_weight = change_param(comp_weight, st.session_state["change_param_dict"], state_dict, state, f"{key}_{comp}_weight_{i}", add_key=True) if not gen_scoring_file else comp_weight # UI State
                    # Write to TOML file and Display to user
                    write_scor_component(comp, toml_input, col, stages=stages)
                    write_show(f'name = "{comp_name}"\n', toml_input, col)
                    write_show(f'weight = {float(comp_weight):.2f}\n', toml_input, col)
                    trans_para_input(toml_input, col, state_dict, state, low_value=transformers_def_param[comp]["low_value"], high_value=transformers_def_param[comp]["high_value"], 
                                     step=1, key=f"{key}_{comp}_{i}", default=transformers_def_param[comp]["default_transformer"], advanced=advanced, gen_scoring_file=gen_scoring_file)
        
    return None


def mol_generator(toml_input, col, state_dict, state, needed_files=None, uploaded_files=None, key=None):
    """
    Display and configure molecule generator options in a Streamlit app.

    Args:
        toml_input (str): The TOML input file path.
        col (streamlit.columns): The Streamlit column to place the molecule generator options in.
        state_dict (dict): The loaded UI state (JSON format) converted into dict. 
        state (bool): Whether a UI state was uploaded or not (Uploaded = True, Not Uploaded = False). 
        needed_files (dict, optional): A dictionary to track the needed files. Defaults to None.
        uploaded_files (dict, optional): A dictionary to track the uploaded files. Defaults to None.
        key (str, optional): A unique key for Streamlit widgets. Defaults to None.

    Returns:
        None
    """
    ## Molecule Generator Options 
    mol_gen = st.selectbox("Type of Molecule Generator", ["Reinvent", "LibInvent", "LinkInvent", "Mol2Mol"], index=0, key=key+"_mol_gen",
                           help="""The prior models provided by REINVENT are the default models, but other 
                                   models obtained by transfer learning (TL) or reinforcement learning (RL) could also be used.""")
    mol_gen = change_param(mol_gen, st.session_state["change_param_dict"], state_dict, state, key+"_mol_gen")  # UI State
    if mol_gen == "Reinvent":
        model = "reinvent.prior"    
        model_type = st.toggle("Upload external models", value=False, key=key+"_model_type",
                               help="The user could upload other RL/TL models if this is set to true.")
        if model_type: 
            # Upload Model File
            model_file = st.file_uploader("Upload Model File", type=["model", "chkpt", "prior"],
                                            help="Upload another RL or TL model.")
            if model_file:
                save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                model = model_file.name
                uploaded_files["Model"] = model_file
                needed_files["Model"] = True
        else:
            uploaded_files["Model"] = rf"{pwd}\prior_models\{model}"
            needed_files["Model"] = True

    else:
        if mol_gen == "LibInvent":
            model = "libinvent.prior"    
            model_type = st.toggle("Upload external models", value=False, key=key+"_model_type",
                                help="The user could upload other RL/TL models if this is set to true.")
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Model File", type=["model", "chkpt", "prior"],
                                              help="Upload another RL or TL model.")
                if model_file:
                    save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    model = model_file.name
                    uploaded_files["Model"] = model_file
                    needed_files["Model"] = True
            else:
                uploaded_files["Model"] = rf"{pwd}\prior_models\{model}"
                needed_files["Model"] = True

            smiles_file = st.text_input("Name of SMILES file", "scaffold", help="""One scaffold per line. Each scaffold must be 
                                        annotated by '\*' to locate the attachment points. Up to 4 attachments points are allowed. **Example**: [\*:1]Cc2ccc1cncc(C[*:2])c1c2)""", 
                                        key=key+f"_{mol_gen}_smi_file")    
            # Upload SMILES File 
            needed_files["SMILES"] = False
            smi_path, smi_name = SMILES_file(key+mol_gen, key, mol_gen=mol_gen, mol2mol=model)
            if smi_path != None: 
                smiles_file = smi_name
                uploaded_files["SMILES"] = smi_path
                needed_files["SMILES"] = True

        elif mol_gen == "LinkInvent":
            model = "linkinvent.prior"    
            # Upload Model File
            model_type = st.toggle("Upload external models", value=False, key=key+"_model_type",
                                help="The user could upload other RL/TL models if this is set to true.")
            if model_type: 
                # Upload Model File
                model_file = st.file_uploader("Upload Model File", type=["model", "chkpt", "prior"],
                                              help="Upload another RL or TL model.")
                if model_file:
                    save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    model = model_file.name
                    #uploaded_files["Model"] = model_file
                    needed_files["Model"] = True
            else:
                #uploaded_files["Model"] = rf"{pwd}\prior_models\{model}"
                needed_files["Model"] = True

            smiles_file = st.text_input("Name of SMILES file", "warhead", help="""Each line must contain the two warheads to be 
                            linked separated by the pipe symbol. Each warhead must be annotated with '\*' to locate 
                            the attachment points. **Example**: Oc1cncc(*)c1|*c1ccoc1""", key=key+f"_{mol_gen}_smi_file")
            # Upload SMILES File 
            needed_files["SMILES"] = False
            smi_path, smi_name = SMILES_file(key+mol_gen, key, mol_gen=mol_gen, mol2mol=model)
            if smi_path != None: 
                smiles_file = smi_name
                uploaded_files["SMILES"] = smi_path
                needed_files["SMILES"] = True
        
        elif mol_gen == "Mol2Mol":
            model = st.selectbox("Select prior model", ["mol2mol_similarity", "mol2mol_medium_similarity",
                                                        "mol2mol_high_similarity", "mol2mol_mmp",
                                                        "mol2mol_scaffold", "mol2mol_scaffold_generic"], index=0, key=key+f"_{mol_gen}")
            
            # Upload Model File
            model_type = st.toggle("Upload external models", value=False, key=key+"_model_type",
                                help="The user could upload other RL/TL models if this is set to true.")
            if model_type: 
                model_file = st.file_uploader("Upload Model File", type=["model", "chkpt", "prior"],
                                              help="Upload another RL or TL model.")
                if model_file:
                    save_uploaded_file(model_file, Path(st.session_state["user_folder"]))
                    model = model_file.name
                    #uploaded_files["Model"] = model_file
                    needed_files["Model"] = True
            else:
                #uploaded_files["Model"] = rf"{pwd}\prior_models\{model}.prior"
                needed_files["Model"] = True            
            
            smiles_file = st.text_input("Name of SMILES file", "input_molecules", help="1 compound per line", key=key+f"_{mol_gen}_smi_file")
            # Upload SMILES File 
            needed_files["SMILES"] = False
            smi_path, smi_name = SMILES_file(key+mol_gen, key, mol_gen=mol_gen, mol2mol=model)
            if smi_path != None: 
                smiles_file = smi_name
                uploaded_files["SMILES"] = smi_path
                needed_files["SMILES"] = True

            st.write("**Sampling Strategy**")
            sample_strategy = st.selectbox("Algorithm", ["multinomial", "beamsearch"], index=0, key=key+f"_{mol_gen}_sample_strategy",
                                            help="""Two sample strategies are implemented in REINVENT 4: **multinomial** and **beam search**. 
                                            Generally, multinomial is more “explorative” compared to beam search which is deterministic. 
                                            Multinomial sampling is recommended for RL, whereas beam search can be very powerful for sampling.""")
            if sample_strategy == "beamsearch":
                temperature = st.number_input("Temperature", min_value=0.0, max_value=None, value=1.0, step=1.0, key=key+f"_{mol_gen}_temperature",
                                                help="""Higher temperature setting allows beam search to explore a greater variety of 
                                                        candidate sequence paths through the token graph. A lower temperature setting 
                                                        makes it increasingly focus on the most likely predictions at each step.""")
            else:
                distance_threshold = st.number_input("Distance threshold", min_value=0, max_value=None, value=100, step=1, key=key+f"_{mol_gen}_distance_threshold")
            st.write("**Similarity's Type and Parameters**")
            pairs_type = st.selectbox(label="Similarity type", options=["Tanimoto", "RefTversky", "FitTversky"], index=0)
            pairs_upper_threshold = st.slider("Upper similarity threshold", min_value=0.0, max_value=1.0, value=1.0, step=0.01)
            pairs_lower_threshold = st.slider("Lower similarity threshold", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
            pairs_min_cardinality = st.number_input("Minimum cardinality", min_value=1, max_value=None, value=1, step=1)
            pairs_max_cardinality = st.number_input("Maximum cardinality", min_value=1, max_value=None, value=199, step=1,
                                                    help="Maximum number of cmpds that can be compared with a certain one.")

    ## Write to the TOML input file 
    write_show(f'\# {mol_gen} Generator Parameters\n', toml_input, col)
    write_show(f'model_file = "{model}"\n', toml_input, col)
    if mol_gen in ["LibInvent", "LinkInvent", "Mol2Mol"]:
        write_show(f'smiles_file = "{smiles_file}"\n', toml_input, col)
    if mol_gen == "Mol2Mol":
        write_show(f'sample_strategy = "{sample_strategy}"\n', toml_input, col)
        if sample_strategy == "beamsearch":
            write_show(f'temperature = {temperature}\n', toml_input, col, empty_line=True)
        else:
            write_show(f"distance_threshold = {distance_threshold}\n", toml_input, col, empty_line=True)
        write_show('\# Type of similarity and its parameters\n', toml_input, col)
        write_show(f'pairs.type = "{pairs_type}"\n', toml_input, col)
        write_show(f'pairs.upper_threshold = {pairs_upper_threshold}\n', toml_input, col)
        write_show(f'pairs.lower_threshold = {pairs_lower_threshold}\n', toml_input, col)
        write_show(f'pairs.min_cardinality = {int(pairs_min_cardinality)}\n', toml_input, col)
        write_show(f'pairs.max_cardinality = {int(pairs_max_cardinality)}\n', toml_input, col, empty_line=True)


def similarity_function(toml_input, col):
    """
    Display and configure similarity function parameters in a Streamlit app.

    Args:
        toml_input (str): The TOML input file path.
        col (streamlit.columns): The Streamlit column to place the similarity function parameters in.

    Returns:
        None
    """
    st.write("**Similarity's Type and Parameters**")
    pairs_type = st.selectbox(label="Type of similarity functions", options=["Tanimoto", "RefTversky", "FitTversky"], index=0)
    pairs_upper_threshold = st.slider("Upper threshold", min_value=0.0, max_value=1.0, value=1.0, step=0.01)
    pairs_lower_threshold = st.slider("Lower threshold", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
    pairs_min_cardinality = st.number_input("Minimal cardinality", min_value=1, max_value=None, value=1, step=1)
    pairs_max_cardinality = st.number_input("Maximal cardinality", min_value=1, max_value=None, value=100, step=1)
    write_show('\# Type of similarity and its parameters\n', toml_input, col)
    write_show(f'pairs.type = "{pairs_type}"\n', toml_input, col)
    write_show(f'pairs.upper_threshold = {pairs_upper_threshold}\n', toml_input, col)
    write_show(f'pairs.lower_threshold = {pairs_lower_threshold}\n', toml_input, col)
    write_show(f'pairs.min_cardinality = {int(pairs_min_cardinality)}\n', toml_input, col)
    write_show(f'pairs.max_cardinality = {int(pairs_max_cardinality)}\n', toml_input, col, empty_line=True)


def diversity_filter(col_write, file_write, state_dict, state, global_DF=True, num_stage=None, key=None):
    """
    Display and configure diversity filter parameters in a Streamlit app.

    Args:
        col_write (streamlit.columns): The Streamlit column to write the filter parameters.
        file_write (str): The file to write the filter parameters to.
        state_dict (dict): The loaded UI state (JSON format) converted into dict. 
        state (bool): Whether a UI state was uploaded or not (Uploaded = True, Not Uploaded = False). 
        global_DF (bool, optional): Whether the filter is global. Defaults to True.
        stages (bool, optional): Whether the filter is for stages. Defaults to False.
        num_stage (int, optional): The stage number. Defaults to None.
        key (str, optional): A unique key for Streamlit widgets. Defaults to None.

    Returns:
        None
    """
    ## Global Diversity Filter
    if global_DF == True:
        div_type = st.selectbox(f"Select similarity criteria", ["IdenticalMurckoScaffold", "IdenticalTopologicalScaffold", "ScaffoldSimilarity", "PenalizeSameSmiles"], index=0, key=f"{key}_type")
        div_type = change_param(div_type, st.session_state["change_param_dict"], state_dict, state, f"{key}_type")  # UI State
        bucket_size = st.number_input(f"Number of compounds per bucket", min_value=0, max_value=None, value=25, step=1,
                                        help="Each bucket holds the same scaffold.", key=f"{key}_bucket")
        bucket_size = change_param(bucket_size, st.session_state["change_param_dict"], state_dict, state, f"{key}_bucket")  # UI State
        minscore = st.number_input(f"Minimum score", min_value=0.0, max_value=1.0, value=0.4, step=0.1,
                                    help="Keep those compounds that have a score value equal or higher to this minimum score value.",
                                    key=f"{key}_minscore")
        minscore = change_param(minscore, st.session_state["change_param_dict"], state_dict, state, f"{key}_minscore")  # UI State
        if div_type == "ScaffoldSimilarity":
            minsimilarity = st.number_input(f"Minimum similarity", min_value=0.0, max_value=1.0, value=0.4, step=0.1,
                                            help="The minimum similarity is calculated with respect any existing bucket.",
                                            key=f"{key}_minsimilarity")
            minsimilarity = change_param(minsimilarity, st.session_state["change_param_dict"], state_dict, state, f"{key}_minsimilarity")  # UI State
        if div_type == "PenalizeSameSmiles":
            penalty_multiplier = st.number_input(f"Penalize same SMILES", min_value=0.0, max_value=1.0, value=0.5, step=0.1,
                                                    help="""This option avoids generating the same molecule again and again. 
                                                            It is especially useful when the user wants to make only small 
                                                            changes in the molecule.""",
                                                    key=f"{key}_penalty")
            penalty_multiplier = change_param(penalty_multiplier, st.session_state["change_param_dict"], state_dict, state, f"{key}_penalty")  # UI State
        write_show('\# Diversity Filter Parameters\n', file_write, col_write)
        write_show('[diversity_filter]\n', file_write, col_write)
        write_show(f'type = "{div_type}"\n', file_write, col_write)
        write_show(f'bucket_size = {int(bucket_size)}\n', file_write, col_write)
        if div_type == "ScaffoldSimilarity":
            write_show(f'minscore = {float(minscore)}\n', file_write, col_write)
            write_show(f'minsimilarity = {float(minsimilarity)}\n', file_write, col_write, empty_line=True)
        elif div_type == "PenalizeSameSmiles":
            write_show(f'minscore = {float(minscore)}\n', file_write, col_write)
            write_show(f'penalty_multiplier = {float(penalty_multiplier)}\n', file_write, col_write, empty_line=True)
        else:
            write_show(f'minscore = {float(minscore)}\n', file_write, col_write, empty_line=True)
    ## Separate Diversity Filters for Stages
    else:
        ## Add default values for the scoring components to the reset dictionary
        state_dict_reset[st.session_state["run_mode"]][f"{key}_type"] = {"key": f"{key}_type", "value": "IdenticalMurckoScaffold"}        # reset value
        state_dict_reset[st.session_state["run_mode"]][f"{key}_bucket"] = {"key": f"{key}_bucket", "value": 25}         # reset value
        state_dict_reset[st.session_state["run_mode"]][f"{key}_minscore"] = {"key": f"{key}_minscore", "value": 0.4}  # reset value
        state_dict_reset[st.session_state["run_mode"]][f"{key}_minsimilarity"] = {"key": f"{key}_minsimilarity", "value": 0.4}  # reset value
        state_dict_reset[st.session_state["run_mode"]][f"{key}_penalty"] = {"key": f"{key}_penalty", "value": 0.5}  # reset value
        ## Input Widgets 
        with st.popover(f"Diversity Filter Parameters (S{num_stage})"):
            div_type = st.selectbox(f"Select similarity criteria", ["IdenticalMurckoScaffold", "IdenticalTopologicalScaffold", "ScaffoldSimilarity", "PenalizeSameSmiles"], index=0, key=f"{key}_type")
            div_type = change_param(div_type, st.session_state["change_param_dict"], state_dict, state, f"{key}_type", add_key=True)  # UI State
            bucket_size = st.number_input(f"Number of compounds per bucket", min_value=0, max_value=None, value=25, step=1, key=f"{key}_bucket",
                                          help="Each bucket holds the same scaffold.")
            bucket_size = change_param(bucket_size, st.session_state["change_param_dict"], state_dict, state, f"{key}_bucket", add_key=True)  # UI State
            minscore = st.number_input(f"Minimum score", min_value=0.0, max_value=1.0, value=0.4, step=0.1, key=f"{key}_minscore",
                                       help="Keep those compounds that have a score value equal or higher to this minimum score value.")
            minscore = change_param(minscore, st.session_state["change_param_dict"], state_dict, state, f"{key}_minscore", add_key=True)  # UI State
            if div_type == "ScaffoldSimilarity":
                minsimilarity = st.number_input(f"Minimum similarity", min_value=0.0, max_value=1.0, value=0.4, step=0.1, key=f"{key}_minsimilarity",
                                                help="The minimum similarity is calculated with respect any existing bucket.")
                minsimilarity = change_param(minsimilarity, st.session_state["change_param_dict"], state_dict, state, f"{key}_minsimilarity", add_key=True)  # UI State
            if div_type == "PenalizeSameSmiles":
                penalty_multiplier = st.number_input(f"Penalize same SMILES", min_value=0.0, max_value=1.0, value=0.5, step=0.1, key=f"{key}_penalty_multiplier",
                                                        help="""This option avoids generating the same molecule again and again. 
                                                             It is especially useful when the user wants to make only small 
                                                             changes in the molecule.""")
                penalty_multiplier = change_param(penalty_multiplier, st.session_state["change_param_dict"], state_dict, state, f"{key}_penalty", add_key=True)  # UI State
            write_show(f'\# Diversity Filter Parameters (S{num_stage})\n', file_write, col_write)
            write_show('[stage.diversity_filter]\n', file_write, col_write)
            write_show(f'type = "{div_type}"\n', file_write, col_write)
            write_show(f'bucket_size = {int(bucket_size)}\n', file_write, col_write)
            if div_type == "ScaffoldSimilarity":
                write_show(f'minscore = {float(minscore)}\n', file_write, col_write)
                write_show(f'minsimilarity = {float(minsimilarity)}\n', file_write, col_write, empty_line=True)
            elif div_type == "PenalizeSameSmiles":
                write_show(f'minscore = {float(minscore)}\n', file_write, col_write)
                write_show(f'penalty_multiplier = {float(penalty_multiplier)}\n', file_write, col_write, empty_line=True)
            else:
                write_show(f'minscore = {float(minscore)}\n', file_write, col_write, empty_line=True)


def copy_file_tempdir(uploaded_file, temp_dir):
    """
    Copy an uploaded file to a temporary directory.

    Args:
        uploaded_file (UploadedFile): The uploaded file to copy.
        temp_dir (str): The path to the temporary directory.

    Returns:
        None
    """
    path = os.path.join(temp_dir, uploaded_file.name)
    with open(path, "wb") as f:
            f.write(uploaded_file.getvalue())


def download_files(uploaded_files, col):
    """
    Provide download buttons for uploaded files, including the TOML input file and model file.
    If multiple files are uploaded, create a zip file containing all files and provide a download button for it.

    Args:
        uploaded_files (dict): A dictionary containing the uploaded files.
        col (streamlit.columns): The Streamlit column to place the download buttons in.

    Returns:
        None
    """
    # TOML Input File 
    with open(uploaded_files["TOML Input"], "r") as toml:
        col.download_button(
            label="Download TOML Input", 
            data=toml, 
            file_name=os.path.basename(uploaded_files["TOML Input"]), 
            help=os.path.basename(uploaded_files["TOML Input"])
        )

    # Check if other files are uploaded and create a zip file
    if len([file for file in uploaded_files.values() if (file != None)]) > 1:
        # Create an in-memory buffer to store the zip file
        zip_buffer = io.BytesIO()
        # Zip the uploaded files
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            # Zip the toml input file 
            with open(uploaded_files["TOML Input"], "r") as toml:
                zip_file.writestr(os.path.basename(uploaded_files["TOML Input"]), toml.read())
            # Zip the other uploaded files
            for uploaded_file in list(uploaded_files.keys())[1:]:
                if uploaded_files[uploaded_file] != None:
                    # Write each uploaded file into the zip file
                    if isinstance(uploaded_files[uploaded_file], str):
                        if "Model" in uploaded_file:
                            file = open(uploaded_files[uploaded_file], "rb")
                        else:
                            file = open(uploaded_files[uploaded_file], "r")
                        file_name = os.path.basename(uploaded_files[uploaded_file])
                        file_content = file.read()
                        zip_file.writestr(file_name, file_content)
                        col.download_button(
                            label=f"Download {uploaded_file}",
                            data=file_content,
                            file_name=file_name,
                            help=file_name
                            )
                        file.close()  
                    else:
                        zip_file.writestr(uploaded_files[uploaded_file].name, uploaded_files[uploaded_file].getvalue())
                        col.download_button(
                            f"Download {uploaded_file}", 
                            uploaded_files[uploaded_file].getvalue(), 
                            file_name=uploaded_files[uploaded_file].name, 
                            help=uploaded_files[uploaded_file].name
                            )

        # Ensure buffer's pointer is at the start
        zip_buffer.seek(0)
        # list of files contained in the zip file 
        files_list = ""
        for i, fi in enumerate(zip_file.namelist()):
            files_list += f"{i+1}. {fi}\n\n"
        # Download button to download the zip file
        col.download_button(
            label="Download all Files as Zip File",
            data=zip_buffer,
            file_name="reinvent_calc.zip",
            mime="application/zip",
            help=f"Files in Zip File:\n\n {files_list}"
        )
    

def bash_script(key, state_dict, state):
    """
    Generate a bash script for running a calculation, optionally on an HPC cluster.

    Args:
        key (str): A unique key for Streamlit widgets.

    Returns:
        str: The path to the generated bash script, or None if the script is not enabled.
    """
    bash_file = os.path.join(Path(st.session_state["user_folder"]), f"run_script_{key}.sh")  
    script = st.toggle("Bash Run Script", value=False, key=key+"_bash_script")
    script = change_param(script, st.session_state["change_param_dict"], state_dict, state, key+"_bash_script")  # UI State

    if script:
        inputfile_name = st.text_input(value=f"{key}_input", label="Name of input file (.toml)", key=key+"_inputfile_name")
        inputfile_name = change_param(inputfile_name, st.session_state["change_param_dict"], state_dict, state, key+"_inputfile_name")  # UI State
        logfile_name = st.text_input(value="logfile", label="Name of log file (.log)", key=key+"_logfile_name")
        logfile_name = change_param(logfile_name, st.session_state["change_param_dict"], state_dict, state, key+"_logfile_name")  # UI State
        conda_env = st.text_input(value="reinvent4", label="Name of Conda Environment", key=key+"_conda_env")
        conda_env = change_param(conda_env, st.session_state["change_param_dict"], state_dict, state, key+"_conda_env")  # UI State
        cluster_calc = st.toggle("Run Calculation on HPC-Cluster?", value=False, key=key+"_cluster_calc")
        cluster_calc = change_param(cluster_calc, st.session_state["change_param_dict"], state_dict, state, key+"_cluster_calc")  # UI State

        if cluster_calc:
            job_name = st.text_input(value="reinvent", label="Name of Job", key=key+"_job_name")
            job_name = change_param(job_name, st.session_state["change_param_dict"], state_dict, state, key+"_job_name")  # UI State
            partition_name = st.text_input(value="cdd_gpuq", label="Name of Partition", key=key+"_partition_name")
            partition_name = change_param(partition_name, st.session_state["change_param_dict"], state_dict, state, key+"_partition_name")  # UI State
            num_nodes = st.number_input(f"Number of Nodes", min_value=1, max_value=None, value=1, step=1, key=key+"_num_nodes")
            num_nodes = change_param(num_nodes, st.session_state["change_param_dict"], state_dict, state, key+"_num_nodes")  # UI State
            gpus_per_node = st.number_input(f"Number of GPUs per Node", min_value=1, max_value=None, value=1, step=1, key=key+"_gpus_per_node")
            gpus_per_node = change_param(gpus_per_node, st.session_state["change_param_dict"], state_dict, state, key+"_gpus_per_node")  # UI State
            time = st.text_input("Set a time limit for the total run time of the job (DD-HH:MM:SS)", value="00-12:00:00", key=key+"_time") 
            time = change_param(time, st.session_state["change_param_dict"], state_dict, state, key+"_time")  # UI State

        text = ""
        with open(bash_file, "w") as fout:

            if cluster_calc:
                fout.write("#!/bin/bash\n")
                text += "#!/bin/bash\n"
                fout.write(f"#SBATCH --job-name={job_name}\n")
                text += f"#SBATCH --job-name={job_name}\n"
                fout.write(f"#SBATCH --partition={partition_name}\n")
                text += f"#SBATCH --partition={partition_name}\n"
                fout.write(f"#SBATCH --nodes={num_nodes}\n")
                text += f"#SBATCH --nodes={num_nodes}\n"
                fout.write(f"#SBATCH --gpus-per-node={gpus_per_node}\n")
                text += f"#SBATCH --gpus-per-node={gpus_per_node}\n"
                fout.write(f"#SBATCH --time={time}\n\n")
                text += f"#SBATCH --time={time}\n\n"

            else:
                fout.write("#!/bin/bash\n\n")
                text += "#!/bin/bash\n\n"

            fout.write("# activate the conda environment where the reinvent4 package is installed\n")
            text += "# activate the conda environment where the reinvent4 package is installed\n"
            fout.write(f"conda activate {conda_env}\n\n")
            text += f"conda activate {conda_env}\n\n"
            fout.write("# run the reinvent calculation\n")
            text += "# run the reinvent calculation\n"
            fout.write(f"reinvent -l {logfile_name}.log {inputfile_name}.toml")
            text += f"reinvent -l {logfile_name}.log {inputfile_name}.toml"

        st.code(text, language="bash")
        return bash_file
    
    else:
        return None


def SMILES_file(key, run_mode, title="SMILES", mol_gen=None, mol2mol=None):
    """
    Handle the upload and processing of a SMILES or SDF file, including conversion and visualization.

    Args:
        key (str): A unique key for Streamlit widgets.
        run_mode (str): The run mode, e.g., "Reinforcement Learning (RL)".
        title (str, optional): The title for Upload widget. Defaults to "SMILES".
        mol_gen (str, optional): The molecule generator, e.g., "Reinvent". Defaults to None.
        mol2mol (str, optional): The specific Mol2Mol mode. Defaults to None.

    Returns:
        tuple: The path to the temporary SMILES file and its name, or (None, None) if no file is uploaded.
    """
    smi_file = st.file_uploader(f"Upload {title} File", type=["smi", "sdf"], 
                                help="SMILES (.smi) and Structures Data File (.sdf) are the **ONLY** accepted format.")
    if smi_file:
        # Name of smiles file 
        smi_name = smi_file.name

        # Save uploaded .smi of .sdf into the temp_files folder
        smi_temp = save_uploaded_file(smi_file, Path(st.session_state["user_folder"]))

        # Convert to .smi if the file is .sdf 
        if (".sdf" in smi_file.name): 
            smi_temp = convert_sdf_smi(smi_temp)
            smi_name = os.path.basename(smi_temp)

        # Read molecules and create column of structures 
        if mol_gen == "LinkInvent":
            df = pd.read_csv(smi_temp, names=["SMILES"], header=None)
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
            df["Warhead1 Structure"] = df["Warhead1 SMILES"].apply(smi_to_png)
            df["Warhead2 Structure"] = df["Warhead2 SMILES"].apply(smi_to_png)
        else:
            df = pd.read_csv(smi_temp, names=["SMILES"], header=None)
            df["Structure"] = df["SMILES"].apply(smi_to_png)

        # Check the tokens if supported 
        if run_mode in ["RL", "SL", "TL", "Sampling"]:
            check_smiles(list(df["SMILES"]), run_mode, mol_gen, mol2mol=mol2mol)
        
        # Visualize molecules 
        show_mols = st.toggle("Show Molecules", key=f"{key}_show_mols", value=False, help="Show the SMILES and structures of the different molecules.")
        if show_mols:
            if mol_gen == "LinkInvent":
                st.write(f"Number of molecules contained in the SMILES file: **{len(df['SMILES'])}**.")
                if f"{key}_smiles_df" not in st.session_state:
                    st.dataframe(df, column_config={"Warhead1 Structure": st.column_config.ImageColumn(width="medium"), "Warhead2 Structure": st.column_config.ImageColumn(width="medium")}, key=f"{key}_smiles_df")
                else:   
                    st.dataframe(df, column_config={"Warhead1 Structure": st.column_config.ImageColumn(width="medium"), "Warhead2 Structure": st.column_config.ImageColumn(width="medium")})
            else:
                st.write(f"Number of molecules contained in the SMILES file: **{len(df['Structure'])}**.")
                if f"{key}_smiles_df" not in st.session_state:
                    st.data_editor(df, column_config={"Structure": st.column_config.ImageColumn(width="medium")}, key=f"{key}_smiles_df") 
                else:
                    st.data_editor(df, column_config={"Structure": st.column_config.ImageColumn(width="medium")})

        return smi_temp, smi_name

    else:
        return None, None


#####################################
##### Cheminformatics Functions ##### 
#####################################
def smi_to_png(smi: str) -> str:
    """
    Convert a SMILES string to a PNG image and return it as a data URI.

    Args:
        smi (str): The SMILES string representing the molecule.

    Returns:
        str: A data URI containing the PNG image of the molecule.
    """
    try:
        mol = rdkit.Chem.MolFromSmiles(smi)
        pil_image = rdkit.Chem.Draw.MolToImage(mol)

        with io.BytesIO() as buffer:
            pil_image.save(buffer, "png")
            data = base64.encodebytes(buffer.getvalue()).decode("utf-8")
        
        return f"data:image/png;base64,{data}"

    except Exception as e:
        st.error(f"An error occured: {e}") 


def convert_sdf_smi(sdf_file):
    """
    Convert an SDF file to a SMILES file.

    Args:
        sdf_file (str): The path to the SDF file.

    Returns:
        str: The path to the generated SMILES file.
    """
    try:
        df = PandasTools.LoadSDF(sdf_file, molColName='Molecule', smilesName='SMILES')
        smi_file = f'{sdf_file[:-4]}.smi'
        df.to_csv(smi_file, columns=["SMILES"], index=False, header=False)
        return smi_file
    
    except Exception as e:
        st.error(f"An error occured: {e}") 


def read_smiles(smiles_file):
    """
    Read a file containing SMILES strings and return them as a list.

    Args:
        smiles_file (str): The path to the file containing SMILES strings.

    Returns:
        list: A list of SMILES strings.
    """
    smiles_list = []
    smiles_file = open(smiles_file, "r")
    smiles_content = smiles_file.read().splitlines()
    for smi in smiles_content:
        smiles_list.append(smi)
    return smiles_list


def convert_smiles_smarts(pattern, convert_to="smarts"):
    """
    Convert between SMILES and SMARTS representations.

    Args:
        pattern (str): The input SMILES or SMARTS string.
        convert_to (str, optional): The target format, either "smarts" or "smiles". Defaults to "smarts".

    Returns:
        str: The converted SMARTS or SMILES string, or "Invalid structure" if the conversion fails.
    """
    if convert_to == "smarts": 
        try:
            mol = Chem.MolFromSmiles(pattern)
            if mol:
                return Chem.MolToSmarts(mol)
            else:
                return "Invalid structure"
        except Exception as e:
            st.error(f"An error occured during conversion of SMILES to SMARTS: {e}") 

    elif convert_to == "smiles":
        try:
            mol = Chem.MolFromSmarts(pattern)
            if mol:
                return Chem.MolToSmiles(mol)
            else:
                return "Invalid structure"   
        except Exception as e:
            st.error(f"An error occured during conversion of SMARTS to SMILES: {e}") 


def check_smiles(list_smiles, run_mode, mol_gen, mol2mol="Mol2mol (high, medium, low similarities)"):
    """
    Check a list of SMILES strings for unsupported tokens based on the selected molecule generator.

    Args:
        list_smiles (list): A list of SMILES strings to check.
        run_mode (str): The run mode (e.g., "Scoring").
        mol_gen (str): The molecule generator (e.g., "Reinvent").
        mol2mol (str, optional): The specific Mol2Mol mode. Defaults to "Mol2mol (high, medium, low similarities)".

    Returns:
        None
    """
    if mol_gen == "Reinvent":
        tokens_list = chem_tokens["Reinvent"].split(", ")
    elif mol_gen == "LibInvent":
        tokens_list = chem_tokens["LibInvent"]["Scaffold"].split(", ") + chem_tokens["LibInvent"]["Decorator"].split(", ")
    elif mol_gen == "LinkInvent":
        tokens_list = chem_tokens["LinkInvent"]["Warheads"].split(", ") + chem_tokens["LinkInvent"]["Linker"].split(", ")
    elif mol_gen == "Mol2Mol": 
        if mol2mol in ["mol2mol_similarity", "mol2mol_medium_similarity", "mol2mol_high_similarity"]:
            mol2mol = "Mol2mol (high, medium, low similarities)"
        elif mol2mol == "mol2mol_mmp":
            mol2mol = "Mol2mol (mmp)"
        elif mol2mol == "mol2mol_scaffold":
            mol2mol = "Mol2mol (scaffold)"
        elif mol2mol == "mol2mol_scaffold_generic":
            mol2mol = "Mol2mol (scaffold-generic)"
        tokens_list = chem_tokens["Mol2Mol"][mol2mol].split(", ")

    if run_mode != "Scoring":
        line = 0 
        for smile in list_smiles:
            i = 0
            while i < len(smile):
                if smile[i] in tokens_list:
                    if smile[i:i+2] in tokens_list:
                        i += 2
                    elif smile[i:i+3] in tokens_list:
                        i += 3
                    elif smile[i:i+4] in tokens_list:
                        i += 4
                    elif smile[i:i+5] in tokens_list:
                        i += 5
                    elif smile[i:i+6] in tokens_list:
                        i += 6
                    else:
                        i += 1
                elif smile[i:i+2] in tokens_list:
                    i += 2
                elif smile[i:i+3] in tokens_list:
                    i += 3
                elif smile[i:i+4] in tokens_list:
                    i += 4
                elif smile[i:i+5] in tokens_list:
                    i += 5
                elif smile[i:i+6] in tokens_list:
                    i += 6
                else: 
                    st.warning(f"""**Warning!!!**\n\n A non-supported token was found in line {line+1} (Token: '{smile[i]}').
                               \n\n Either select the correct molecule generator **OR** correct your SMILES.""")
                    break
            line += 1 


#################################
##### Transformer Functions ##### 
##############################################################################################
# Transformer functions used in the REINVENT4 (V4.0). 
# Source: (https://github.com/MolecularAI/REINVENT4/blob/main/reinvent/scoring/transforms/)
##############################################################################################
def hard_sigmoid(x: np.ndarray, k: float) -> np.ndarray:
    """
    Apply a hard sigmoid function to the input array.

    Args:
        x (np.ndarray): Input array.
        k (float): Scaling factor.

    Returns:
        np.ndarray: Transformed array with hard sigmoid applied.
    """
    return (k * x > 0).astype(np.float32)


def stable_sigmoid(x: np.ndarray, k: float, base_10: bool = True) -> np.ndarray:
    """
    Apply a stable sigmoid function to the input array.

    Args:
        x (np.ndarray): Input array.
        k (float): Scaling factor.
        base_10 (bool): Whether to use base 10 for the logarithm. Defaults to True.

    Returns:
        np.ndarray: Transformed array with stable sigmoid applied.
    """
    h = k * x
    if base_10:
        h = h * np.log(10)
    hp_idx = h >= 0
    y = np.zeros_like(x)
    y[hp_idx] = 1.0 / (1.0 + np.exp(-h[hp_idx]))
    y[~hp_idx] = np.exp(h[~hp_idx]) / (1.0 + np.exp(h[~hp_idx]))
    return y.astype(np.float32)


def sigmoid(values, k, low, high):
    """
    Apply a sigmoid function to the input values.

    Args:
        values (array-like): Input values.
        k (float): Scaling factor.
        low (float): Lower bound.
        high (float): Upper bound.

    Returns:
        np.ndarray: Transformed values with sigmoid applied.
    """
    values = np.array(values, dtype=np.float32)
    x = values - (high + low) / 2
    if (high - low) == 0:
        k = 10.0 * k
        transformed = hard_sigmoid(x, k)
    else:
        k = 10.0 * k / (high - low)
        transformed = stable_sigmoid(x, k)
    return transformed


def reverse_sigmoid(values, k, low, high):
    """
    Apply a reverse sigmoid function to the input values.

    Args:
        values (array-like): Input values.
        k (float): Scaling factor.
        low (float): Lower bound.
        high (float): Upper bound.

    Returns:
        np.ndarray: Transformed values with reverse sigmoid applied.
    """
    values = np.array(values, dtype=np.float32)
    x = values - (high + low) / 2
    if (high - low) == 0:
        k = 10.0 * k
        transformed = hard_sigmoid(x, k)
    else:
        k = 10.0 * k / (high - low)
        transformed = stable_sigmoid(x, k)
    return 1.0 - transformed


def double_sigmoid(x: np.ndarray, x_left: float, x_right: float, k: float, k_left: float, k_right: float) -> np.ndarray:
    """
    Compute double sigmoid based on stable sigmoid.

    Args:
        x (np.ndarray):  Input array.
        x_left (float):  Left sigmoid x value for which the output is 0.5. (low in previous implementation)
        x_right (float): Right sigmoid x value for which the output is 0.5. (high in previous implementation)
        k (float):       Common scaling factor. (coef_div in previous implementation)
        k_left (float):  Scaling left factor. (coef_si in previous implementation)
        k_right (float): Scaling right factor. (coef_se in previous implementation)

    Returns:
        np.ndarray: Transformed array with double sigmoid applied.
    """
    x_center = (x_right - x_left) / 2 + x_left

    xl = x[x < x_center] - x_left
    xr = x[x >= x_center] - x_right

    if k == 0:
        sigmoid_left = hard_sigmoid(xl, k_left)
        sigmoid_right = 1 - hard_sigmoid(xr, k_right)
    else:
        k_left = k_left / k  
        k_right = k_right / k 
        sigmoid_left = stable_sigmoid(xl, k_left)
        sigmoid_right = 1 - stable_sigmoid(xr, k_right)

    d_sigmoid = np.zeros_like(x)
    d_sigmoid[x < x_center] = sigmoid_left
    d_sigmoid[x >= x_center] = sigmoid_right
    return d_sigmoid


def step(values, low, high):
    """
    Apply a step function to the input values.

    Args:
        values (array-like): Input values.
        low (float): Lower bound.
        high (float): Upper bound.

    Returns:
        np.ndarray: Transformed values with step function applied.
    """
    transformed = [1.0 if low <= x <= high else 0.0 for x in values]
    return np.array(transformed, dtype=float)


def left_step(values, low):
    """
    Apply a left step function to the input values.

    Args:
        values (array-like): Input values.
        low (float): Lower bound.

    Returns:
        np.ndarray: Transformed values with left step function applied.
    """
    transformed = [1.0 if x <= low else 0.0 for x in values]
    return np.array(transformed, dtype=float)


def right_step(values, high):
    """
    Apply a right step function to the input values.

    Args:
        values (array-like): Input values.
        high (float): Upper bound.

    Returns:
        np.ndarray: Transformed values with right step function applied.
    """
    transformed = [1.0 if x >= high else 0.0 for x in values]
    return np.array(transformed, dtype=float)