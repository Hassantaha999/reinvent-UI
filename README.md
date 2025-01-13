![Version](https://img.shields.io/badge/version-1.0.0--beta-blue)

# REINVENT UI App

## Description
This interactive web-based UI app of REINVENT allows users to generate input files to run [**REINVENT**](https://github.com/MolecularAI/REINVENT4) 
calculations. This app aims to streamline workflows for chemists and data scientists by allowing 
easy access to REINVENT’s functionalities directly from a browser. REINVENT is an open-source generative AI framework, developed by the Molecular AI department at AstraZeneca R&D, 
for the design of small molecules that uses recurrent neural networks (RNN) and transformer architectures to drive molecule generation. 
A paper describing the REINVENT software has been published as Open Access in the Journal of Cheminformatics: 
[**Reinvent 4: Modern AI–driven generative molecule design**](https://link.springer.com/article/10.1186/s13321-024-00812-5?utm_source=rct_congratemailt&utm_medium=email&utm_campaign=oa_20240221&utm_content=10.1186/s13321-024-00812-5).



## Installation & Prerequisites
Before running REINVENT calculations on your local machine using the input files generated with this 
web-based app, ensure the necessary software packages and dependencies are installed on your local machine. 
Refer to the [**REINVENT GitHub Repository**](https://github.com/MolecularAI/REINVENT4) for detailed instructions. 
**Please note that this web-based app is intended only for the generation of input files and other necessary files to run REINVENT calculations.** The actual REINVENT calculations must be performed on your local machine or a suitable computational environment.

To run the web-based REINVENT app locally on your machine, follow these steps:
  1) Install the Conda environment using the "requirements. txt" file:
        ```
        conda create --name streamlit --file requirements.txt
        ```
     Note: To enable the "SMARTSview" functionality, you must also install "streamlit-ketcher" using pip (not working with "conda"):

                pip install streamlit-ketcher
                
  2) Activate the Conda environment:
        ```
        conda activate streamlit 
        ```

  3) Navigate to the app folder (e.g., "reinvent4") and run the app with one of the following commands: 
        ```
      streamlit run Welcome.py 
        ```
      **OR**
        ```
      python -m streamlit run Welcome.py
        ```


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



## Content of the Web-based App
- **Documentation**: Explains how REINVENT works and provides detailed descriptions for all parameters and options available for REINVENT calculations.
- **REINVENT UI**: Generates the necessary input files for REINVENT calculations.
- **Tools**: Various tools that could support users in setting up their REINVENT calculations:
- **Analysis**: Inspect and visualize the results of your REINVENT calculations.



## General Workflow 
In the following a general workflow will be described for the user. 
1. Navigate to the **REINVENT UI** page in the web-based app.
2. Select your desired options and parameters for the REINVENT calculation.
    - Refer to the **Documentation** page for any clarification on parameters or options when needed. 
        For a more detailed explanation, visit the official documentation: [**REINVENT GitHub Repository**](https://github.com/MolecularAI/REINVENT4).
    - Utilize helpful tools, like the Chemical Sketcher, available on the **Tools** page to assist in generating input files.
4. Upload all required files for your calculation.
5. Download the generated ZIP file containing all necessary input and uploaded files.
6. Extract the ZIP file, navigate to the folder, and run the REINVENT calculation on your local machine.
    - You can monitor and analyze the results of **RL**, **SL**, **TL** runs using TensorBoard with the following command:
        ``` 
        tensorboard --logdir TB_DIR_NAME/ --bind_all
        ``` 
7. After completing the calculation, inspect and visualize the results using the **Analysis** page of the web-based app.


## Acknowledgments
I would like to express my sincere gratitude to:
- Hendrik Göddeke ([LinkedIn](https://www.linkedin.com/in/hgoeddeke/))
- Marta Pinto ([LinkedIn](https://www.linkedin.com/in/marta-pinto-9137b324/))
- Frank Oellien ([LinkedIn](https://www.linkedin.com/in/frankoellien/))
- Udo Lange

for their guidance and support and for valuable feedback and contributions to the project.


## License 
This project is licensed under the terms of the Apache 2.0 License. See the [LICENSE](https://github.com/Hassantaha999/reinvent-UI/blob/main/LICENSE) file for details.
