########################################
############ Python Modules ############
########################################
import streamlit as st
import os 
from functions import *
from data import *


###########################
###### General Setup ###### 
###########################
### Setting page configurations
st.set_page_config(
    page_title="Documentation",
    page_icon=":open_book:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
            #'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "mailto:hassanabdel999@gmail.com",
            'About': "## REINVENT UI"}
)


#################################################
############ Documentation Modules ##############
#################################################
### To perserve the user-input across a multi-page streamlit app 
for key in st.session_state:
    st.session_state[key] = st.session_state[key]

### Abbvie Logo & Image
# logo_path = os.path.join("figures", "reinvent2_logo_modified.jpeg")    
image_path = os.path.join("figures", "reinvent2_logo_modified.jpeg")  
# st.logo(logo_path)
st.image(image_path, caption=f"REINVENT logo used in the REINVENT 2.0 paper")

### Titel 
st.title("Documentation")
st.sidebar.header("Content", divider="gray")

### Tabs
Tabs = [
   "Introduction", "General Remarks", "Run Modes", "Molecule Generators",
   "Scoring Components", "Non-Scoring Components", "Transformer Functions", "Supported Chemistry (Tokens)", "Publications"
]
introduction, notes, run_modes, mol_generators, scoring, non_scoring, transformer, tokens, pubs = st.tabs(Tabs)


####################
### Introduction ###
####################
with introduction:
  st.header("Introduction", divider="gray")
  st.sidebar.subheader("Introduction")

  ## Important Notes
  st.markdown(
  """
  REINVENT is a modern open-source generative AI framework for the design of small molecules developed at AstraZeneca that uses 
  recurrent neural networks (RNNs) and transformers as deep learning architectures based on SMILES strings as molecular representation
  molecules. 

  REINVENT4 includes 4 types of molecule generators (**Reinvent**, **Libinvent**, **Linkinvent** and **Mol2Mol**) and uses a 
  Reinforcement Learning (RL) algorithm to generate optimized molecules compliant with a user defined property profile defined 
  as a multi-component score. Transfer Learning (TL) can be used to create or pre-train a model that generates molecules closer 
  to a set of input.

  **REINVENT involves a two-step process**: 
  1) The first step is to train a prior RNN to generate SMILES through supervised learning. This model is trained to correctly predict 
  the next character of a SMILES string given a starting token or incomplete string. REINVENT 4 provides a range of off-the-shelf 
  ready–made priors. These are pre–trained on ChEMBL (except of the Mol2Mol prior which is trained on PubChem) to generate valid smiles 
  and are specific to each generator. However, these generated SMILES do not necessarily satisfy any specific design criteria and the 
  number of SMILES that satisfy all constraints is nearly intractable for the prior model. 

  2) The second step is to fine-tune the prior model according to some specified scoring function to generate a higher fraction of 
  desired SMILES more efficiently. Reinforcement learning (RL) is used in REINVENT to fine tune pre-trained RNNs. Commonly the RL setup 
  consist of an actor (agent) and an environment in which the actor takes a set of actions (individual steps for building sequence of 
  tokens that which be translated into SMILES) and receives a reward. The set of actions is referred to as policy, and the reward 
  after completing the policy is known as a policy iteration. During this step, the agent developes a policy that maximizes the likelihood of 
  generating a molecule with a favorable reward. This reward is influenced by the prior, the diversity filter and the scoring funtion.
  """
  ) 

  # Prior Models 
  st.markdown("### Prior Models")
  parameters = {"Generator": ["Reinvent", "Libinvent", "Linkinvent", "Mol2Mol", "", "", "", "", "", "", "Mol2Mol"],
                "Dataset": ["ChEMBL 25", "ChEMBL 27", "ChEMBL 27", "ChEMBL 28", "", "", "", "", "", "", "PubChem"],
                "Notes": ["Published in Ref. [1, 2]", "Published in [Ref. 3]", "Published in [Ref. 4]", 
                          "Published in [Ref. 5]", "Similarity", "Medium similarity", "High similarity", "Scaffold", 
                          "Generic scaffold", "Matched molecular pairs", "Published in [Ref. 6]"]}
  df = st.data_editor(parameters, hide_index=True, use_container_width=True)

  # References & Notes
  col1, col2, col3, col4, col5, col6 = st.columns([0.166, 0.166, 0.166, 0.166, 0.166, 0.166], gap="medium", vertical_alignment="top")
  col1.link_button("Ref. 1", "https://jcheminf.biomedcentral.com/articles/10.1186/s13321-024-00812-5")
  col2.link_button("Ref. 2", "https://pubs.acs.org/doi/10.1021/acs.jcim.0c00915")
  col3.link_button("Ref. 3", "https://pubs.acs.org/doi/10.1021/acs.jcim.1c00469")
  col4.link_button("Ref. 4", "https://pubs.rsc.org/en/content/articlelanding/2023/dd/d2dd00115b")
  col5.link_button("Ref. 5", "https://jcheminf.biomedcentral.com/articles/10.1186/s13321-022-00599-3")
  col6.link_button("Ref. 6", "https://chemrxiv.org/engage/chemrxiv/article-details/653632fcc3693ca993ec6a24")


#######################
### General Remarks ###
#######################
with notes:
  st.header("General Remarks", divider="gray")
  st.sidebar.subheader("General Remarks")

  ## Important Notes
  st.markdown("""
      In the following important notes will be mentioned that the user should keep in mind when using this REINVENT UI.
              
      ### General Notes
        - REINVENT UI supports **.smi** and **.sdf** formats for molecule files. The **.sdf** file will be converted 
        internally into a **.smi** file and will then be available for download.
        - The user may save the options and parameters chosen using the "**Save UI State**" option on the left sidebar. The saved UI state file (JSON) 
          could then be used in another session/project using the "**Load UI State**" option to load the saved options and parameters. 
        - The user must make any change to the input widget when loading a UI state for the changes to take effect.
        - The user may use the "**Reset Values**" button to reset all the options and parameters to their default values.
                
      ### Run Mode Specific Notes
        ##### Reinforcement/Staged Learning (RL/SL)
        - The minimal required files to run a RL/SL calculation with REINVENT are the following files: 
          - TOML input file 
          - Prior model file (Priors or RL/TL models)
          - Agent model file (Priors or RL/TL models)
          - SMILES file (only necessary when using the **Libinvent**, **Linkinvent**, and **Mol2Mol** molecule 
                generators **OR** when inception molecules are used for the **Reinvent** molecule generator)

        ##### Transfer Learning (TL)
        - The minimal required files to run a TL calculation with REINVENT are the following files: 
          - TOML input file 
          - Model file (Priors or RL/TL models)
          - SMILES file 
          - Validation SMILES file 

        ##### Sampling
        - The minimal required files to run a Sampling calculation with REINVENT are the following files: 
          - TOML input file 
          - Model file (Priors or RL/TL models)
          - SMILES file (only necessary when using the **Libinvent**, **Linkinvent**, and **Mol2Mol** molecule generators)

        ##### Scoring
        - The minimal required files to run a scoring calculation with REINVENT are the following files: 
          - TOML input file 
          - Scoring SMILES file 
  """)


#################
### Run Modes ###
#################
with run_modes:
  st.header("Run Modes", divider="gray")
  st.sidebar.subheader("Run Modes")

  ## Run Modes Paramters 
  st.markdown(
  """
  REINVENT 4 supports 4 different run modes:

  1) **Scoring:** User can score molecules provided as SMILES strings.

  2) **Sampling:** Generates molecules given an input model. This running mode does not use any scoring or reinforcement learning 
  and therefore, the agent is not updated during the run.
  
  3) **Transfer Learning (TL):** Transfer learning optimizes a more general model to generate molecules that are closer to a defined 
     set of input molecules. The user provides a prior and a SMILES file (e.g. a chemical series). TL will compute the negative log 
     likelihood from the molecules and computes the loss from the resulting mean negative log likelihood over all molecules. 
     This will drive the current prior towards a model which is increasingly closer to the provided molecules.

  4) **Reinforcement Learning (RL):** Reinforcement Learning is the main molecule optimization method in REINVENT. 
     In generative molecular design, the goal is to drive a prior model such that the generated molecules satisfies a predefined 
     property profile. The agent is rewarded when the action is beneficial to the goal or receives negative feedback when the action 
     isn’t beneficial. 

  5) **Staged Learning (SL)**: Staged learning, also known as **Curriculum Learning (CL)**, is implemented as a multi–stage RL. 
     The main purpose is to allow the user to optimize a prior model conditioned on a calculated target profile by varying 
     the scoring function in stages. Staged learning requires both a prior and an agent model. The prior is only being 
     used as a reference. The agent is the model that is being trained in the run. At the beginning of a staged learning, 
     run prior and agent will typically be the same model file. When a run terminates, either because the termination criterion 
     has been reached, or the user terminates the run explicitly, a checkpoint file representing the current state of the agent 
     will be written to disk. This checkpoint can be reused as the agent later.
  """)

  st.subheader("Run Modes Parameters")
  st.write("This is a summary of TOML parameters for each run mode.")
  run_mode = st.selectbox("**Select Run Mode**", ["Reinforcement/Staged Learning (RL/SL)", "Transfer Learning (TL)", 
                                                  "Sampling", "Scoring"], index=0)

  if run_mode == "Reinforcement/Staged Learning (RL/SL)":
      #st.write("Run reinforcement learning (RL) and/or Staged learning (SL). SL is simply a multi-stage RL learning.")
      parameters = {"Parameter": run_modes_parameters["Reinforcement/Staged Learning (RL/SL)"].keys(),
                    "Description": run_modes_parameters['Reinforcement/Staged Learning (RL/SL)'].values()}
      df = st.dataframe(parameters, hide_index=True, use_container_width=True)
    
  elif run_mode == "Transfer Learning (TL)":
      #st.write("Run transfer learning on a set of input SMILES.")
      parameters = {"Parameter": run_modes_parameters["Transfer Learning (TL)"].keys(),
                    "Description": run_modes_parameters['Transfer Learning (TL)'].values()}
      df = st.dataframe(parameters, hide_index=True, use_container_width=True)

  elif run_mode == "Sampling":
      #st.write("Sample a number of SMILES with associated NLLs.")
      parameters = {"Parameter": run_modes_parameters["Sampling"].keys(),
                    "Description": run_modes_parameters['Sampling'].values()}
      df = st.dataframe(parameters, hide_index=True, use_container_width=True)

  elif run_mode == "Scoring":
      #st.write("Interface to the scoring component. Does not use any models.")
      parameters = {"Parameter": run_modes_parameters["Scoring"].keys(),
                    "Description": run_modes_parameters['Scoring'].values()}
      df = st.dataframe(parameters, hide_index=True, use_container_width=True)


#######################
# Molecule Generators #
#######################
with mol_generators:
  st.header("Molecule Generators", divider="gray")
  st.sidebar.subheader("Molecule Generators")

  ## Important Notes
  st.markdown(
  """
  **REINVENT 4 includes 4 types of molecule generators**:
  1) :violet[Reinvent]: **atom by atom generation**. This is the classical de-novo algorithm described in the very first 
  publication of Reinvent.

  2) :orange[LibInvent:] **R–group replacement and library design.** A scaffold is supplied to the RNN based generator serving 
  as a template and constraint in building the new molecule. The generator will decorate this scaffold with suitable R–groups. 
  Up to four attachment points are supported. Naturally this generator can also be used to create AI-guided libraries.

  3) :blue[LinkInvent:] **fragment linking and scaffold hopping.** Two “warheads” or fragments are supplied to the RNN based 
  generator as constraints. The generator will create a suitable linker joining the two warheads. Generally, the linker can be 
  any type of scaffold (subject to the training set of the prior).

  4) :red[Mol2Mol]: **find molecules like the provided molecules.** 
  A molecule is supplied to the generator as restraint. The generator will find a second molecule within a 
  defined similarity. Depending on the similarity radius the molecule will be relatively like the supplied molecule but, 
  importantly, the scaffold can change within the limits of the given similarity.
  """
  )

  st.image(os.path.join("figures", "molecule_generators.png"), 
           caption=f"Types of molecule generators in REINVENT4 (source: Reinvent4 paper).")


##########################
### Scoring Components ###
##########################
with scoring:
  st.header("Scoring Components", divider="gray")
  st.sidebar.subheader("Scoring Components")

  st.markdown(
  """
  REINVENT employs a composite scoring function consisting of different user-defined components. The individual components of the 
  scoring function can be either combined as a weighted sum or as a weighted product. A weight needs to be set for each component 
  to determine its relative importance with respect to the other components, reflecting their importance in the overall score. 
  
  Scoring components can be classified into 6 categories:
  - Basic Molecular Physical Properties
  - Similarity and Cheminformatics Components
  - Physics/Structure/Ligand based Components
  - QSAR/QSPR Model-related Components
  - Scoring Components about Drug-Likeness, Synthesizability & Reactions
  - LinkInvent Linker-specific Physchem Properties

  """
  )

  #st.write("This is a list of currently supported scoring components together with their parameters.")
  scoring_type = st.selectbox(label="**Select category of scoring components**", options=["Basic Molecular Physical Properties", "Similarity and Cheminformatics Components", 
                                                                                  "Physics/Structure/Ligand based Components", "QSAR/QSPR Model-related Components", 
                                                                                  "Scoring Components about Drug-Likeness, Synthesizability & Reactions",
                                                                                  "LinkInvent Linker-specific Physchem Properties", #"Generic Scoring Components", 
                                                                                  ], index=0)
  
  if scoring_type == "Basic Molecular Physical Properties":
    parameters = {"Scoring Component": scoring_component["Basic Molecular Physical Properties"].keys(),
                  "Description":       scoring_component["Basic Molecular Physical Properties"].values()}
    df = st.dataframe(parameters, hide_index=True, use_container_width=True)

  elif scoring_type == "Similarity and Cheminformatics Components":
    parameters = {"Scoring Component": scoring_component["Similarity and Cheminformatics Components"].keys(),
                  "Description":       list(scoring_component["Similarity and Cheminformatics Components"].values())}
    parameters["Description"][-1] += f""" is a tool for the calculation of 3D shape and chemical (“color”) similarity. It provides two similarity measures: Tanimoto and Tversky. Tanimoto calculates the ratio of features shared by A and B to the total number of features present in A and B. Tversky introduces two weighing factors, alpha and beta. Alpha determines the weight given to the features present in both molecules, while beta controls the weight placed on features unique to each molecule. alpha = beta = 0.5 makes it identical to using the Tanimoto measure. In ROCS, RefTversky uses default settings alpha=0.95 and beta=0.05, whereas FitTversky uses alpha=0.05  and beta=0.95 [Ref. 2]. Taking into account these definitions, Tversky similarity values are recommended for Hit Identification (HI) and Lead Generation (LG), while Tanimoto should be use for Lead Optimization.""" 
    parameters["Description"][-2] += " [Ref. 1]" 
    df = st.dataframe(parameters, hide_index=True, use_container_width=True)

    col1, col2 = st.columns([0.1, 0.6], gap="small")
    col1.link_button(":red[Ref. 1]", "https://pubs.acs.org/doi/10.1021/acs.jcim.8b00173")
    col2.link_button(":red[Ref. 2]", "https://doi.org/10.1007/s10822-016-9959-3")

  elif scoring_type == "Physics/Structure/Ligand based Components":
    parameters = {"Scoring Component": scoring_component["Physics/Structure/Ligand based Components"].keys(),
                  "Description":       scoring_component["Physics/Structure/Ligand based Components"].values()}
    df = st.dataframe(parameters, hide_index=True, use_container_width=True)

  elif scoring_type == "QSAR/QSPR Model-related Components":
    parameters = {"Scoring Component": scoring_component["QSAR/QSPR Model-related Components"].keys(),
                  "Description":       scoring_component["QSAR/QSPR Model-related Components"].values()}
    df = st.dataframe(parameters, hide_index=True, use_container_width=True)

  elif scoring_type == "Scoring Components about Drug-Likeness, Synthesizability & Reactions":
    parameters = {"Scoring Component": scoring_component["Scoring Components about Drug-Likeness, Synthesizability & Reactions"].keys(),
                  "Description":       list(scoring_component["Scoring Components about Drug-Likeness, Synthesizability & Reactions"].values())}
    parameters["Description"][0] += " [Ref. 1]" 
    parameters["Description"][1] += " [Ref. 2]" 
    df = st.dataframe(parameters, hide_index=True, use_container_width=True)

    col1, col2 = st.columns([0.1, 0.6], gap="small")
    col1.link_button(":red[Ref. 1]", "https://www.nature.com/articles/nchem.1243")
    col2.link_button(":red[Ref. 2]", "https://doi.org/10.1186/1758-2946-1-8")

  #elif scoring_type == "Generic Scoring Components":
  #  parameters = {"Scoring Component": scoring_component["Generic Scoring Components"].keys(),
  #                "Description":       scoring_component["Generic Scoring Components"].values()}
  #  df = st.dataframe(parameters, hide_index=True, use_container_width=True)

  elif scoring_type == "LinkInvent Linker-specific Physchem Properties":
    parameters = {"Scoring Component": scoring_component["LinkInvent Linker-specific Physchem Properties"].keys(),
                  "Description":       scoring_component["LinkInvent Linker-specific Physchem Properties"].values()}
    df = st.dataframe(parameters, hide_index=True, use_container_width=True)


##############################
### Non-Scoring Components ###
##############################
with non_scoring:
  st.header("Non-Scoring Components", divider="gray")
  st.sidebar.subheader("Non-Scoring Components")

  st.markdown(
  """
  ### Inception Molecules
  Inception molecules are molecules provided by the user as SMILES strings at the beginning of the run to guide the RL into a 
  desired part of the chemical space. 

  ### Sampling Algorithms
  REINVENT4 supports two different techniques can be used to sample target molecules with a molecular transformer: 
  **multinomial sampling** and **beam search**. **Multinomial sampling** is a probabilistic method that selects the most probable 
  token at each step, without considering the impact on future tokens. It allows fast and non–deterministic generation of compounds. 
  In contrast, **beam search** maintains a list of the top-k candidates, known as the “beam width”. Each candidate is scored based 
  on the probability of the current token and the accumulated probability of previous tokens. **Beam search** is a deterministic 
  approach that always generates unique compounds. However, it is computationally more expensive than **multinomial sampling**.  

  ### Learning Strategies
  REINVENT4 uses the Difference between Augmented and Posterior (DAP) as learning strategy. [:red[Ref. 1]]

  ### Diversity Filters
  REINVENT4 has implemented 3 different types of filters to control the diversity of the generated molecules. 
  To this end, molecules are classified in buckets which hold a certain scaffold. Scaffolds can be computed as:
    1) Topological Scaffolds (determined disregarding elements and bond types; unlabeled graphs). 
    2) Murcko Scaffolds (labelled graphs).
    3) Similar Scaffolds. 
  """
  )

  st.link_button(":red[Ref. 1]", "https://pubs.acs.org/doi/10.1021/acs.jcim.1c00469")


####################
### Transformers ###
####################
with transformer:
  st.header("Transformer Functions", divider="gray")
  st.sidebar.subheader("Transformer Functions")

  st.write("""
           The total score of a compound is derived from various scoring components specified by the user, 
           combined using an aggregation function (e.g., arithmetic or geometric mean). Each scoring component 
           should ideally return a value between 0 and 1, where higher values indicate "better" and lower values 
           indicate "worse." However, some components may not naturally produce values within this range or might 
           represent the inverse relationship. To address this and standardize the outputs, transformer functions 
           can be applied to the scoring components. These functions scale the component values to fall within 
           the 0 to 1 range, ensuring consistency across all components.
           """)

  st.write("**REINVENT4 supports 7 types of transformer functions:**")
  
  parameters = {"Transformer": ["Sigmoid", "Reverse Sigmoid", "Double Sigmoid", 
                                      "Right Step", "Left Step", "Step", "Value Mapping"],
                "Description": ["S–shaped logistic function", "Reverse sigmoid function", "Two–sided sigmoid function", 
                                "Heaviside step function, can be shifted along x", "Left–sided step function", 
                                "Two–sided step function", "Maps a categorical value (string) to a user–supplied number"]}
  df = st.dataframe(parameters, hide_index=True, use_container_width=True)
  
  transformer_type = st.selectbox(label="**Select type of transformer**", options=["Sigmoid", "Reverse Sigmoid", "Double Sigmoid", 
                                                                                   "Right Step", "Left Step", "Step"], 
                                                                          index=0)
  
  if transformer_type == "Sigmoid":
    st.write("#### Mathematical Formula for the Sigmoid Function")
    st.write(r"- **1st case**: Upper Threshold $$=$$ Lower Threshold $$\rightarrow$$ Hard Sigmoid ")
    st.latex(r'''f(x; K; B) = \begin{cases} 
                0 & K * (x - B)\leq 0 \\
                1 & K * (x - B) > 0  
                \end{cases}''')
    st.write(r' $$B = Upper = Lower \rightarrow$$ shifts the center of the sigmoid function ')
    st.write(r' $$K = 10\ *\ k \rightarrow$$ scaling factor ')
    st.write(r"- **2nd case**: Upper Threshold $$\neq$$ Lower Threshold $$\rightarrow$$ Stable Sigmoid ")
    st.latex(r' f(x; K; B) = \frac{1}{1 + e^{-\ K\ *\ (x\ -\ B)}} ')
    st.write(r' $$B = \frac{Upper\ +\ Lower}{2} \rightarrow$$ shifts the center of the sigmoid function ')
    st.write(r' $$K = \frac{10\ *\ k}{Upper\ -\ Lower} \rightarrow$$ adjusts the steepness of the sigmoid function ')

    st.write("#### TOML Input Parameters")
    parameters = {"Parameter": ["Type of Transformer", "Lower Threshold", "Upper Threshold", "Scaling Factor (k)"],
                  "TOML Input Parameter": ['transform.type', 'transform.low', 'transform.high', 'transform.k']}
    df = st.dataframe(parameters, hide_index=True, use_container_width=True)

  elif transformer_type == "Reverse Sigmoid":
    st.write("#### Mathematical Formula for the Reverse Sigmoid Function")
    st.write(r"- **1st case**: Upper Threshold $$=$$ Lower Threshold $$\rightarrow$$ Hard Reverse Sigmoid ")
    st.latex(r'''f(x; K; B) = 1 - \begin{cases} 
                0 & K * (x - B) \leq 0 \\
                1 & K * (x - B) > 0  
                \end{cases}''')
    st.write(r' $$B = Upper = Lower \rightarrow$$ shifts the center of the reverse sigmoid function ')
    st.write(r' $$K = 10\ *\ k \rightarrow$$ scaling factor')
    st.write(r"- **2nd case**: Upper Threshold $$\neq$$ Lower Threshold $$\rightarrow$$ Stable Reverse Sigmoid ")
    st.latex(r' f(x; K; B) = 1 - \frac{1}{1 + e^{-\ K\ *\ (x\ -\ B)}} ')
    st.write(r' $$B = \frac{Upper\ +\ Lower}{2} \rightarrow$$ shifts the center of the reverse sigmoid function ')
    st.write(r' $$K = \frac{10\ *\ k}{Upper\ -\ Lower} \rightarrow$$ adjusts the steepness of the reverse sigmoid function ')

    st.write("#### TOML Input Parameters")
    parameters = {"Parameter": ["Type of Transformer", "Lower Threshold", "Upper Threshold", "Scaling Factor (k)"],
                  "TOML Input Parameter": ['transform.type', 'transform.low', 'transform.high', 'transform.k']}
    df = st.dataframe(parameters, hide_index=True, use_container_width=True)

  elif transformer_type == "Double Sigmoid":
    st.write("#### Mathematical Formula for the Double Sigmoid Function")
    st.latex(r' x_{center} = \frac{Upper - Lower}{2} + Lower ')
    st.latex(r' X_{L} = X_{x < x_{center}} - Lower ')
    st.latex(r' X_{R} = X_{x \geq x_{center}} - Upper ')
    st.write(r' $$Lower \rightarrow$$ shifts the center of the left sigmoid function  ')
    st.write(r' $$Upper \rightarrow$$ shifts the center of the right sigmoid function  ')
    st.write(r"- **1st case**: k $$=$$ 0 $$\rightarrow$$ Hard Sigmoids ")
    st.latex(r'''f_{L}(x_{L}; K_{L}) = \begin{cases} 
                0 & K_{L} * x_{L}\leq 0 \\
                1 & K_{L} * x_{L} > 0  
                \end{cases}''')
    st.latex(r'''f_{R}(x_{R}; K_{R}) = 1 - \begin{cases} 
                0 & K_{R} * x_{R}\leq 0 \\
                1 & K_{R} * x_{R} > 0  
                \end{cases}''')
    st.write(r' $$K_{L} \rightarrow$$ scaling left factor ')
    st.write(r' $$K_{R} \rightarrow$$ scaling right factor ')
    st.write(r"- **2nd case**: k $$\neq$$ 0 $$\rightarrow$$ Stable Sigmoids ")
    st.latex(r' f_{L}(x_{L}, K_{L}) = \frac{1}{1 + e^{-\ K_{L}\ *\ x_{L}}} ')
    st.latex(r' f_{R}(x_{R}; K_{R}) = 1 - \frac{1}{1 + e^{-\ K_{R}\ *\ x_{R}}} ')
    st.write(r' $$K \rightarrow$$ adjusts the steepness of the double sigmoid function ')
    st.write(r' $$K_{L} = K_{L} / K  \rightarrow$$ adjusts the steepness of the left sigmoid function ')
    st.write(r' $$K_{R} = K_{R} / K \rightarrow$$ adjusts the steepness of the right sigmoid function ')

    st.write("#### TOML Input Parameters")
    parameters = {"Parameter": ["Type of Transformer", "Lower Threshold", "Upper Threshold", "Common Scaling Factor (k)", "Scaling Left Factor (k_l)", "Scaling Right Factor (k_r)"],
                  "TOML Input Parameter": ['transform.type', 'transform.low', 'transform.high', 'transform.coef_div', 'transform.coef_si', 'transform.coef_se']}
    df = st.dataframe(parameters, hide_index=True, use_container_width=True)

  elif transformer_type == "Right Step":
    st.write("#### Mathematical Formula for the Right Step Function")
    st.latex(r'''f(x) = \begin{cases} 
                0 & x\ <\ Upper \\
                1 &  x\ \geq\ Upper\\
                \end{cases}''')
    st.write(r' $$Upper \rightarrow$$ shifts the upper threshold of the right step function  ')
    
    st.write("#### TOML Input Parameters")
    parameters = {"Parameter": ["Type of Transformer", "Upper Threshold"],
                  "TOML Input Parameter": ['transform.type', 'transform.high']}
    df = st.dataframe(parameters, hide_index=True, use_container_width=True)

  elif transformer_type == "Left Step":
    st.write("#### Mathematical Formula for the Left Step Function")
    st.latex(r'''f(x) = \begin{cases} 
                0 & x\ >\ Lower \\
                1 &  x\ \leq\ Lower\\
                \end{cases}''')
    st.write(r' $$Lower \rightarrow$$ shifts the lower threshold of the left step function  ')
    
    st.write("#### TOML Input Parameters")
    parameters = {"Parameter": ["Type of Transformer", "Lower Threshold"],
                  "TOML Input Parameter": ['transform.type', 'transform.low']}
    df = st.dataframe(parameters, hide_index=True, use_container_width=True)
  
  elif transformer_type == "Step":
    st.write("#### Mathematical Formula for the Step Function")
    st.latex(r'''f(x) = \begin{cases} 
                0 & x\ \leq\ Lower \\
                1 &  Lower\ \leq\ x\ \leq\ Upper\\
                0 & x\ \geq\ Upper \\
                \end{cases}''')
    st.write(r' $$Lower \rightarrow$$ shifts the lower threshold of the step function  ')
    st.write(r' $$Upper \rightarrow$$ shifts the upper threshold of the step function ')
    
    st.write("#### TOML Input Parameters")
    parameters = {"Parameter": ["Type of Transformer", "Lower Threshold", "Upper Threshold"],
                  "TOML Input Parameter": ['transform.type', 'transform.low', 'transform.high']}
    df = st.dataframe(parameters, hide_index=True, use_container_width=True)

  st.write("#### Visualization of the Transformer Function")
  st.write("""The user may use an interactive widget to adjust the different transformer parameters 
            and to see how they affect the transformer function in the **Tools** page.""")

####################################
### Supported Chemistry (Tokens) ###
####################################
with tokens: 
  st.header("Supported Chemistry (Tokens)", divider="gray")
  st.sidebar.subheader("Supported Chemistry (Tokens)")
   
  st.write("""
    The supported chemistry expressed as tokens for each generator are listed below. Basically, all priors support the same elements. 
    The main differences are the ring sizes and that Mol2Mol accepts and generates chiral centers at C and (quaternary) N. 
    Mol2Mol also supports double bond isomers. 
  """)

  # Reinvent Generator 
  st.write("## Reinvent")
  st.code(chem_tokens["Reinvent"], 
           language="markdown", wrap_lines=True)
  
  # LibInvent Generator 
  st.write("## LibInvent")
  st.write("#### Scaffold (Accepted Tokens)")
  st.code(chem_tokens["LibInvent"]["Scaffold"], 
           language="markdown", wrap_lines=True)
  st.write("#### Decorator (Included Tokens)")
  st.code(chem_tokens["LibInvent"]["Decorator"], 
           language="markdown", wrap_lines=True)

  ## Linkinvent Generator
  st.write("## Linkinvent")
  st.write("#### Warheads (Accepted Tokens)")
  st.code(chem_tokens["LinkInvent"]["Warheads"], 
           language="markdown", wrap_lines=True)
  st.write("#### Linker (Included Tokens)")
  st.code(chem_tokens["LinkInvent"]["Linker"], 
           language="markdown", wrap_lines=True)
  
  ## Mol2Mol Generator
  st.write("## Mol2Mol")
  st.write("#### Mol2mol (high, medium, low similarities)")
  st.code(chem_tokens["Mol2Mol"]["Mol2mol (high, medium, low similarities)"], 
           language="markdown", wrap_lines=True)
  st.write("#### Mol2mol (mmp)")
  st.code(chem_tokens["Mol2Mol"]["Mol2mol (mmp)"], 
           language="markdown", wrap_lines=True)
  st.write("#### Mol2mol (scaffold)")
  st.code(chem_tokens["Mol2Mol"]["Mol2mol (scaffold)"], 
           language="markdown", wrap_lines=True)
  st.write("#### Mol2mol (scaffold-generic)")
  st.code(chem_tokens["Mol2Mol"]["Mol2mol (scaffold-generic)"], 
           language="markdown", wrap_lines=True)


####################
### Publications ###
####################
with pubs: 
  st.header("Publications", divider="gray")
  st.sidebar.subheader("Publications")
   
  st.write("""
    List of publications relevant to the REINVENT software package:

    * [Reinvent 4: Modern AI–driven generative molecule design](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-024-00812-5)
    * [Molecular de-novo design through deep reinforcement learning](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-017-0235-x)
    * [REINVENT 2.0: An AI Tool for De Novo Drug Design](https://pubs.acs.org/doi/full/10.1021/acs.jcim.0c00915)
    * [Randomized SMILES strings improve the quality of molecular generative models](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0393-0)
    * [Memory-assisted reinforcement learning for diverse molecular de novo design](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-020-00473-0)
    * [Chemformer: a pre-trained transformer for computational chemistry](https://iopscience.iop.org/article/10.1088/2632-2153/ac3ffb/meta)
    * [Molecular optimization by capturing chemist’s intuition using deep neural networks](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-021-00497-0)
    * [Improving de novo molecular design with curriculum learning](https://www.nature.com/articles/s42256-022-00494-4)
    * [DockStream: a docking wrapper to enhance de novo molecular design](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-021-00563-7)
    * [De novo design with deep generative models based on 3D similarity scoring](https://www.sciencedirect.com/science/article/pii/S0968089621003163)
    * [LibINVENT: Reaction-based Generative Scaffold Decoration for in Silico Library Design](https://pubs.acs.org/doi/full/10.1021/acs.jcim.1c00469)
    * [Link-INVENT: generative linker design with reinforcement learning](https://pubs.rsc.org/en/content/articlehtml/2023/dd/d2dd00115b)
    * [Exhaustive local chemical space exploration using a transformer model](https://www.nature.com/articles/s41467-024-51672-4)
  """)