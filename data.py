#########################
##### Reinvent Data ##### 
#########################

### Run modes mapping dict
run_mode_prefix = {
            "Reinforcement Learning (RL)": "RL", 
            "Staged Learning (SL)": "SL", 
            "Transfer Learning (TL)": "TL", 
            "Sampling": "Sampling", 
            "Scoring": "Scoring"
            }


### Scoring components
scor_comp = [
            ## Basic molecular physical properties
            "SlogP", "MolecularWeight", "TPSA", "GraphLength", "NumAtomStereoCenters", "HBondAcceptors", "HBondDonors", 
            "NumRotBond", "Csp3", "numsp", "numsp2", "numsp3", "NumHeavyAtoms", "NumHeteroAtoms", "NumRings", 
            "NumAromaticRings", "NumAliphaticRings", "PMI", "MolVolume", 

            ## Similiarity and cheminformatics components
            "CustomAlerts", "GroupCount", "MatchingSubstructure", "TanimotoSimilarity", "MMP", "ROCSSimilarity",   
    
            ## Physics/structure/ligand based components
            "DockStream", #"Icolos", #"MAIZE",                                                                     
            
            ## QSAR/QSPR model-related components
            "AutoQSAR", "DeepQSAR", "pADME", #"ChemProp", #"Qptuna",                                                  
            
            ## Scoring components about drug-likeness, synthesizability & reactions
            "QED", "SAScore", "ReactionFilter",                                                                    
            
            ## Generic scoring components
            #"ExternalProcess", #"REST",                                                                           
            
            ## LinkInvent linker-specific physchem properties
            "FragmentMolecularWeight", "FragmentGraphLength", "FragmentHBondAcceptors", "FragmentHBondDonors", "FragmentNumRotBond", 
            "Fragmentnumsp", "Fragmentnumsp2", "Fragmentnumsp3", "FragmentNumRings", "FragmentNumAromaticRings", "FragmentNumAliphaticRings", 
            #"FragmentEffectiveLength", #"FragmentLengthRatio", 
        ]


### Internally (Reinvent)-correct name of all available scoring components
scoring_keys = {
            ## Basic molecular physical properties
            "SlogP": 'SlogP', "MolecularWeight": 'MolecularWeight', "TPSA": 'TPSA', "GraphLength": 'GraphLength', 
            "NumAtomStereoCenters": "NumAtomStereoCenters", "HBondAcceptors": "HBondAcceptors", 
            "HBondDonors": "HBondDonors", "NumRotBond": "NumRotBond", "Csp3": "Csp3", 'numsp': 'numsp', 
            'numsp2': 'numsp2', 'numsp3': 'numsp3', 'NumHeavyAtoms': 'NumHeavyAtoms', 'NumHeteroAtoms': 'NumHeteroAtoms',
            'NumRings': 'NumRings', 'NumAromaticRings': 'NumAromaticRings', 'NumAliphaticRings': 'NumAliphaticRings', 'PMI': 'PMI', 
            'MolVolume': 'MolVolume',

            ## Similiarity and cheminformatics components
            "CustomAlerts": 'custom_alerts', 'GroupCount': 'GroupCount', "MatchingSubstructure": "MatchingSubstructure", 
            "TanimotoSimilarity": 'TanimotoDistance', "MMP": "MMP", "ROCSSimilarity": 'ROCSSimilarity',   

            ## Physics/structure/ligand based components
            'DockStream': 'DockStream', #'Icolos': 'Icolos', 'Mazie': 'Mazie',

            ## QSAR/QSPR model-related components
            "AutoQSAR": "AutoQSAR", "DeepQSAR": "DeepQSAR", "pADME": "PADME", #"ChemProp": "ChemProp", "Qptuna": "Qptuna",             

            ## Scoring components about drug-likeness, synthesizability & reactions
            "QED": "QED", "SAScore": "SAScore", "ReactionFilter": "ReactionFilter",     

            ## Generic scoring components
            #"ExternalProcess": "ExternalProcess", "REST": "REST",    

            ## LinkInvent linker-specific physchem properties
            "FragmentMolecularWeight": "FragmentMolecularWeight", "FragmentGraphLength": "FragmentGraphLength", 
            "FragmentHBondAcceptors": "FragmentHBondAcceptors", "FragmentHBondDonors": "FragmentHBondDonors", 
            "FragmentNumRotBond": "FragmentNumRotBond", "Fragmentnumsp": "Fragmentnumsp", "Fragmentnumsp2": "Fragmentnumsp2", 
            "Fragmentnumsp3": "Fragmentnumsp3", "FragmentNumRings": "FragmentNumRings", "FragmentNumAromaticRings": 
            "FragmentNumAromaticRings", "FragmentNumAliphaticRings": "FragmentNumAliphaticRings", #"FragmentEffectiveLength": 
            #"FragmentEffectiveLength", #"FragmentLengthRatio": #"FragmentLengthRatio", 
        }


### Define the default transformer function for each scoring component ("Sigmoid" or "Step" or "Value_Mapping")
transformer_defaults = {    
            ## Basic molecular physical properties
            'SlogP': 'Sigmoid', 'MolecularWeight': 'Sigmoid', 'TPSA': 'Sigmoid', 'GraphLength': 'Sigmoid',
            'NumAtomStereoCenters': 'Step', 'HBondAcceptors': 'Step', 'HBondDonors': 'Step', 'NumRotBond': 'Step',
            'Csp3': 'Step', 'numsp': 'Step', 'numsp2': 'Step', 'numsp3': 'Step', 'NumHeavyAtoms': 'Step',
            'NumHeteroAtoms': 'Step', 'NumRings': 'Step', 'NumAromaticRings': 'Step', 'NumAliphaticRings': 'Step',
            'PMI': 'Sigmoid', 'MolVolume': 'Sigmoid', 

            ## Similiarity and cheminformatics components
            'CustomAlerts': None, 'GroupCount': 'Step', 'MatchingSubstructure': None, 
            'TanimotoSimilarity': None, 'MMP': "Value_Mapping", 'ROCSSimilarity': 'Sigmoid',

            ## Physics/structure/ligand based components
            'DockStream': 'Sigmoid', #'Icolos': None, #'MAIZE': None,

            ## QSAR/QSPR model-related components
            'AutoQSAR': 'Sigmoid', 'DeepQSAR': 'Sigmoid', 'pADME': 'Sigmoid', #"ChemProp": None, #"Qptuna": None,

            ## Scoring components about drug-likeness, synthesizability & reactions
            'QED': 'Sigmoid', 'SAScore': 'Sigmoid', 'ReactionFilter': None,

            ## Generic scoring components
            #'ExternalProcess': None, #'REST': None,

            ## LinkInvent linker-specific physchem properties  
            "FragmentMolecularWeight": 'Sigmoid', "FragmentGraphLength": 'Sigmoid', "FragmentHBondAcceptors": 'Step', "FragmentHBondDonors": 'Step', 
            "FragmentNumRotBond": 'Step', "Fragmentnumsp": 'Step', "Fragmentnumsp2": 'Step', "Fragmentnumsp3": 'Step', "FragmentNumRings": 'Step', 
            "FragmentNumAromaticRings": 'Step', "FragmentNumAliphaticRings": 'Step', #"FragmentEffectiveLength": None, #"FragmentLengthRatio": None,
        }


### Scoring components that don't use transformers 
transformers_false = [key for key in transformer_defaults.keys() if transformer_defaults[key] == None]


### Default transformer parameters for the different scoring components
transformers_def_param = {
  ## Basic molecular physical properties
  "SlogP":                            {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
  "MolecularWeight":                  {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
  "TPSA":                             {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
  "GraphLength":                      {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
  "NumAtomStereoCenters":             {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "HBondAcceptors":                   {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "HBondDonors":                      {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "NumRotBond":                       {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "Csp3":                             {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "numsp":                            {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "numsp2":                           {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "numsp3":                           {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "NumHeavyAtoms":                    {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "NumHeteroAtoms":                   {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "NumRings":                         {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "NumAromaticRings":                 {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "NumAliphaticRings":                {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "PMI":                              {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
  "MolVolume":                        {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   

  ## Similiarity and cheminformatics components
  "CustomAlerts":                     {"default_transformer":   None, "low_value": None, "high_value": None},                                   
  "GroupCount":                       {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "MatchingSubstructure":             {"default_transformer":   None, "low_value": None, "high_value": None},                                   
  "TanimotoSimilarity":               {"default_transformer":   None, "low_value": None, "high_value": None},                                   
  "MMP":                              {"default_transformer": "Value_Mapping", "low_value": 0, "high_value": 0.5},                                   
  "ROCSSimilarity":                   {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   

  ## Physics/structure/ligand based components
  "DockStream":                       {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
  #"Icolos":                          {"default_transformer":      None, "low_value": None, "high_value": None},                                   
  #"MAIZE":                           {"default_transformer":      None, "low_value": None, "high_value": None},                                   
  
  ## QSAR/QSPR model-related components
  "AutoQSAR":                         {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
  "DeepQSAR":                         {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
  "pADME": {
          "pADME1":                   {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
          "pADME2":                   {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
          "pADME3":                   {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
          "pADME4":                   {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
          "pADME5":                   {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
          "pADME5":                   {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
          "pADME6":                   {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
          "pADME7":                   {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
          "pADME8":                   {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
          "pADME9":                   {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
          "pADME10":                  {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
  }, 
  #"ChemProp":                        {"default_transformer": None, "low_value": None, "high_value": None},                                   
  #"Qptuna":                          {"default_transformer": None, "low_value": None, "high_value": None},                                   
  
  ## Scoring components about drug-likeness, synthesizability & reactions
  "QED":                              {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
  "SAScore":                          {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
  "ReactionFilter":                   {"default_transformer":      None, "low_value": None, "high_value": None},                                   
  
  ## Generic scoring components
  #"ExternalProcess":                 {"default_transformer": None, "low_value": None, "high_value": None},                                   
  #"REST":                            {"default_transformer": None, "low_value": None, "high_value": None},                                   
  
  ## LinkInvent linker-specific physchem properties
  "FragmentMolecularWeight":          {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
  "FragmentGraphLength":              {"default_transformer": "Sigmoid", "low_value": 50, "high_value": 100},   
  "FragmentHBondAcceptors":           {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "FragmentHBondDonors":              {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "FragmentNumRotBond":               {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "Fragmentnumsp":                    {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "Fragmentnumsp2":                   {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "Fragmentnumsp3":                   {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "FragmentNumRings":                 {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "FragmentNumAromaticRings":         {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  "FragmentNumAliphaticRings":        {"default_transformer": "Step", "low_value": 0,  "high_value": 5},     
  #"FragmentEffectiveLength":         {"default_transformer": None, "low_value": None, "high_value": None},                                   
  #"FragmentLengthRatio":             {"default_transformer": None, "low_value": None, "high_value": None},                                   
}


### Scoring Components with their description
scoring_component = {
            ## Basic Molecular Physical Properties
            "Basic Molecular Physical Properties":
                {
                 'SlogP': 'Crippen SLogP (RDKit)', 'MolecularWeight': 'Molecular weight (RDKit)', 'TPSA': 'Topological polar surface area (RDKit)', 'GraphLength': 'Topological distance matrix (RDKit)', 
                 'NumAtomStereoCenters': 'Number of stereo centers (RDKit)', 'HBondAcceptors': 'Number of hydrogen bond acceptors (RDKit)', 'HBondDonors': 'Number of hydrogen bond donors (RDKit)', 
                 'NumRotBond': 'Number of rotatable bonds (RDKit)', 'Csp3': 'Fraction of sp3 carbons (RDKit)', 'numsp': 'Number of sp hybridized atoms (RDKit)', 'numsp2': 'Number of sp2 hybridized atoms (RDKit)', 
                 'numsp3': 'Number of sp3 hybridized atoms (RDKit)', 'NumHeavyAtoms': 'Number of heavy atoms (RDKit)', 'NumHeteroAtoms': 'Number of hetero atoms (RDKit)', 'NumRings': 'Number of total rings (RDKit)', 
                 'NumAromaticRings': 'Number of aromatic rings (RDKit)', 'NumAliphaticRings': 'Number of aliphatic rings (RDKit)', 'PMI': 'Principal moment of inertia to assess dimensionality (RDKit)', 
                 'MolVolume': 'Molecular volume (RDKIT)'
                 },
                            
            ## Similiarity and Cheminformatics Components
            "Similarity and Cheminformatics Components":
                {
                 'CustomAlerts': 'Penalizes the SMARTS provided by the user (RDKit)', # list of undesired SMARTS patterns
                 'GroupCount': 'Counts how many times the SMARTS pattern is found and used to encourage or discourage groups based on the score transform (RDKit)',
                 'MatchingSubstructure': 'Rewards a molecule for containing a substructure (RDKit)', # 'preserve the final score when the SMARTS pattern is found, otherwise penalize it (multiply by 0.5)'
                 'TanimotoSimilarity': 'Tanimoto similarity using the Morgan fingerprint (RDKit)',
                 'MMP': 'Based on the mmpdb database, identify matched molecular pairs (MMPs) and use them to predict property changes and generate new molecular structures.',
                 'ROCSSimilarity': 'ROCS (OpenEye)'
                 },

            ## Physics/Structure/Ligand based Components
            "Physics/Structure/Ligand based Components":
                {
                 'DockStream': "Generic docking interface with access to Glide SP", # AutoDock Vina, rDock, OpenEye's Hybrid, Schrodinger's Glide and CCDC's GOLD
                 #'Icolos': 'generic interface to Icolos',
                 #'MAIZE': 'generic interface to MAIZE '
                },

            ## QSAR/QSPR Model-related Components
            "QSAR/QSPR Model-related Components":
                {
                 "AutoQSAR": "QSAR models built with AutoQSAR (Schrödinger) that need to be provided by the user",
                 "DeepQSAR": "QSAR models built with DeepQSAR (Schrödinger) that need to be provided by the user",
                 "pADME": "ADME endpoints predicted using the in-house global model pADMEu. For more info, go to 'go/properties'"
                 #'ChemProp': 'ChemProp D-MPNN models',
                 #'Qptuna': 'QSAR models with Qptuna'
                 },

            ## Scoring Components about Drug-Likeness, Synthesizability & Reactions
            "Scoring Components about Drug-Likeness, Synthesizability & Reactions":
                {
                 'QED': 'Drug-likeness estimation (RDKit)',
                 'SAScore': "Score that estimates ease of synthesis (synthetic accessibility) of molecules. The higher it is, the more difficult is to synthetize", 
                 'ReactionFilter': 'Reaction filter for Libinvent, applied to total score'
                 },

            ## Generic scoring components
            "Generic Scoring Components":
                {
                 'ExternalProcess': 'Generic component to run an external process for scoring',
                 'REST': 'Generic REST interface (contributed by Syngenta)'
                 },
            
            ## LinkInvent Linker-specific Physchem Properties
            "LinkInvent Linker-specific Physchem Properties":
                {
                 'FragmentMolecularWeight': 'Fragment Molecular weight (RDKit)', 'FragmentGraphLength': 'Fragment topological distance matrix (RDKit)', 
                 'FragmentHBondAcceptors': 'Fragment number of hydrogen bond acceptors (RDKit)', 'FragmentHBondDonors': 'Fragment number of hydrogen bond donors (RDKit)', 
                 'FragmentNumRotBond': 'Fragment number of rotatable bonds (RDKit)', 'Fragmentnumsp': 'Fragment number of sp hybridized atoms (RDKit)', 'Fragmentnumsp2': 'Fragment number of sp2 hybridized atoms (RDKit)', 
                 'Fragmentnumsp3': 'Fragment number of sp3 hybridized atoms (RDKit)', 'FragmentNumRings': 'Fragment number of total rings (RDKit)', 
                 'FragmentNumAromaticRings': 'Fragment number of aromatic rings (RDKit)', 'FragmentNumAliphaticRings': 'Fragment number of aliphatic rings (RDKit)'
                 },  
        }


### Combine all scoring componenets of the different kinds in the "scoring_component" dict into one dictionary. 
scoring_component_entries = {}
for d in [scoring_component[key] for key in scoring_component.keys()]:
  scoring_component_entries.update(d)


### Run Modes Parameters
run_modes_parameters = {
            ## Run mode: Reinforcement/Staged Learning (RL/SL)
            "Reinforcement/Staged Learning (RL/SL)": 
                {'run_type': 'set to "staged_learning"', 'device': 'set the torch device e.g "cuda:0" or "cpu"', 'use_cuda': '(deprecated) "true" to use GPU, "false" to use CPU',
                 'json_out_config': 'filename of the TOML file in JSON format', 'tb_logdir': 'if not empty string name of the TensorBoard logging directory',
                 '[parameters]': 'starts the parameter section', 'summary_csv_prefix': 'prefix for output CSV filename', 'use_checkpoint': 'if "true" use diversity filter from agent_file if present',
                 'purge_memories': 'if "true" purge all diversity filter memories (scaffold, SMILES) after each stage', 'prior_file': 'filename of the prior model file, serves as reference',
                 'agent_file': 'filename of the agent model file, used for training, replace with checkpoint file from previous stage when needed', 
                 'batch_size': 'batch size, note: affects SGD', 'unique_sequences': 'if "true" only return unique raw sequence (sampling)', 
                 'randomize_smiles': 'if "true" shuffle atoms in input SMILES randomly (sampling)', '[learning_strategy]': 'start section for RL learning strategy',
                 'type': 'use "dap"', 'sigma': 'sigma in the reward function', 'rate': 'learning rate for the torch optimizer', 
                 '[diversity_filter]': 'starts the section for the diversity filter, overwrites all stage DFs', 
                 'type (filter)': 'name of the filter type: "IdenticalMurckoScaffold", "IdenticalTopologicalScaffold", "ScaffoldSimilarity", "PenalizeSameSmiles"', 
                 'bucket_size': 'number of scaffolds to store before molecule is scored zero', 'minscore': 'minimum score', 
                 'minsimilarity': 'minimum similarity in "ScaffoldSimilarity"', 'penalty_multiplier': 'penalty penalty for each molecule in "PenalizeSameSmiles"', 
                 '[inception]': 'starts the inception section', 'smiles_file': 'filename for the "good" SMILES', 'memory_size': 'number of SMILES to hold in inception memory',
                 'sample_size': 'number of SMILES randomly sampled from memory', '[[stage]]': 'starts a stage, note the double brackets',
                 'chkpt_file': 'filename of the checkpoint file, will be written on termination and Ctrl-C', 'termination': 'use "simple", termination criterion',
                 'max_score': 'maximum score when to terminate', 'min_steps': 'minimum number of RL steps to avoid early termination', 
                 'max_steps': 'maximum number of RL steps to run, if maximum is hit all stages will be terminated', 
                 '[diversity_filter]': 'a per stage DF filter can be defined for each stage, global DF will overwrite this'},

            ## Run mode: Transfer Learning (TL)
            "Transfer Learning (TL)": 
                {'run_type': 'set to "transfer_learning"', 'device': 'set the torch device e.g "cuda:0" or "cpu"', 'use_cuda': '(deprecated) "true" to use GPU, "false" to use CPU',
                 'json_out_config': 'filename of the TOML file in JSON format', 'tb_logdir': 'if not empty string name of the TensorBoard logging directory',
                 'number_of_cpus': 'optional parameter to control number of cpus for pair generation. If not provided, only one CPU will be used.',
                 '[parameters]': 'starts the parameter section', 'num_epochs': 'number of epochs to run', 'save_every_n_epochs': 'save checkpoint file every N epochs',
                 'batch_size': 'batch size, note: affects SGD', 'sample_batch_size': 'batch size to calculate the sample loss and other statistics',
                 'num_refs': 'number of references for similarity if > 0, DO NOT use with large dataset (> 200 molecules)', 'input_model_file': 'filename of input prior model',
                 'smiles_file': 'SMILES file for Lib/Linkinvent and Molformer', 'output_model_file': 'filename of the final model',
                 'pairs.upper_threshold': 'Molformer: upper similarity', 'pairs.lower_threshold': 'Molformer: lower similarity', 
                 'pairs.min_cardinality': 'Molformer: min. cardinality', 'pairs.max_cardinality	': 'Molformer: max. cardinality'},

            ## Run mode: Sampling
            "Sampling": 
                {'run_type': 'set to "sampling"', 'device': 'set the torch device e.g "cuda:0" or "cpu"', 'use_cuda': '(deprecated) "true" to use GPU, "false" to use CPU',
                 'json_out_config': 'filename of the TOML file in JSON format', '[parameters]': 'starts the parameter section',
                 'model_file': 'filename to model file from which to sample', 'smiles_file': 'filename for inpurt SMILES for Lib/LinkInvent and Mol2Mol',
                 'sample_strategy': 'transformer models: "beamsearch" or "multinomial"', 'output_file': 'filename for the CSV file with samples SMILES and NLLs',
                 'num_smiles': 'number of SMILES to sample, note: this is multiplied by the number of input SMILES', 'unique_molecules': 'if "true" only return unique canonicalized SMILES',
                 'randomize_smiles': 'if "true" shuffle atoms in input SMILES randomly', 'tb_logdir': 'if not empty string name of the TensorBoard logging directory',
                 'temperature': 'Mol2Mol only: default 1.0', 'target_smiles_path': 'Mol2Mol only: if not empty, filename to provided SMILES, check NLL of generating the provided SMILES'},

            ## Run mode: Scoring
            "Scoring": 
                {'run_type': 'set to "scoring"', 'device': 'set the torch device e.g "cuda:0" or "cpu"', 'use_cuda': '(deprecated) "true" to use GPU, "false" to use CPU',
                 'json_out_config': 'filename of the TOML file in JSON format', '[parameters]': 'starts the parameter section',
                 'smiles_file': 'SMILES filename, SMILES are expected in the first column', '[scoring_function]': 'starts the section for scoring function setup',
                 '[[components]]': 'start the section for a component within [scoring_function] , note the double brackets to start a list',
                 'type': '"custom_sum" for weighted arithmetic mean or "custom_produc" for weighted geometric mean',
                 'component_type': 'name of the component, FIXME: list all', 'name': 'a user chosen name for ouput in CSV files, etc.',
                 'weight': 'the weight for this component'}
        }


### Available pADME models
PADME_models = ["pADME1", "pADME2", "pADME3", "pADME4", "pADME5", "pADME5", "pADME6", "pADME7", "pADME8", "pADME9", "pADME10"]


### SMARTS patterns (refer to the following website for more details: https://www.daylight.com/dayhtml_tutorials/languages/smarts/smarts_examples.html#C)
smarts_patterns = {
  ## C
  "Alkyl Carbon": "[CX4]", "Allenic Carbon": "[$([CX2](=C)=C)]", "Vinylic Carbon": "[$([CX3]=[CX3])]", "Acetylenic Carbon": "[$([CX2]#C)]", "Arene": "c", 

  ## C & O
  "Carbonyl group (Low specificity)": "[CX3]=[OX1]", "Carbonyl group": "[$([CX3]=[OX1]),$([CX3+]-[OX1-])]", "Carbonyl with Carbon": "[CX3](=[OX1])C", 
  "Carbonyl with Nitrogen": "[OX1]=CN", "Carbonyl with Oxygen": "[CX3](=[OX1])O", "Acyl Halide": "[CX3](=[OX1])[F,Cl,Br,I]", 
  "Aldehyde": "[CX3H1](=O)[#6]", "Anhydride": "[CX3](=[OX1])[OX2][CX3](=[OX1])", "Amide": "[NX3][CX3](=[OX1])[#6]", 
  "Carboxylate Ion": "[CX3](=O)[O-]", "Carbonic Acid": "[CX3](=[OX1])(O)O", "Carboxylic acid": "[CX3](=O)[OX2H1]", 
  "Ester (also hits anhydrides)": "[#6][CX3](=O)[OX2H0][#6]", "Ketone": "[#6][CX3](=O)[#6]", "Ether": "[OD2]([#6])[#6]", 

  ## H
  "Hydrogen Atom": "[H]", "Not a Hydrogen Atom": "[!#1]", "Proton": "[H+]", 

  ## N
  # mine (-amino)
  "Primary or secondary amine": "[NX3;H2,H1;!$(NC=O)]", "Enamine": "[NX3][CX3]=[CX3]", "Primary amine, not amide": "[NX3;H2;!$(NC=[!#6]);!$(NC#[!#6])][#6]",
  "Two primary or secondary amines": "[NX3;H2,H1;!$(NC=O)].[NX3;H2,H1;!$(NC=O)]", "Enamine or Aniline Nitrogen": "[NX3][$(C=C),$(cc)]",
  # amino acids
  "Generic amino acid: low specificity": "[NX3,NX4+][CX4H]([*])[CX3](=[OX1])[O,N]", "Dipeptide group. generic amino acid: low specificity": "[NX3H2,NH3X4+][CX4H]([*])[CX3](=[OX1])[NX3,NX4+][CX4H]([*])[CX3](=[OX1])[OX2H,OX1-]",
  "Amino Acid": "[$([NX3H2,NX4H3+]),$([NX3H](C)(C))][CX4H]([*])[CX3](=[OX1])[OX2H,OX1-,N]",
}


### Session States Keys for the different parameters and options for UI states
state_dict_UI = {
  ## Sidebar General Options
  "sidebar_options": {
    "user_modus":        "modus",
    "run_mode":          "run_mode",
  },

  ## Scoring 
  "Scoring": {
    # General Options 
    "json_name":         "Scoring_json_file",
    "use_cuda":          "Scoring_use_cuda",
    "smi_files":         "Scoring_smiles_file",
    "output_csv":        "Scoring_output_csv",
    
    # # Scoring Components
    # "comps":             "Scoring_scor_components",
    # "weight":            "Scoring_weight",
    # "parallel":          "Scoring_parallel",
    # "scoring_file":      "Scoring_scoring_file",
    # "scoring_filename":  "Scoring_scoring_filename",
    # "scoring_filetype":  "Scoring_scoring_filetype",

    # Bash File Options 
    "bash_script":       "Scoring_bash_script",
    "inputfile_name":    "Scoring_inputfile_name",
    "logfile_name":      "Scoring_logfile_name",
    "conda_env":         "Scoring_conda_env",
    "cluster":           "Scoring_cluster_calc",
    "job_name":          "Scoring_job_name",
    "partition_name":    "Scoring_partition_name",
    "num_nodes":         "Scoring_num_nodes",
    "gpus_per_node":     "Scoring_gpus_per_node",
    "time":              "Scoring_time",
  },

  ## Sampling 
  "Sampling": 
  {
    # General Options 
    "json_name":         "Sampling_json_file",
    "use_cuda":          "Sampling_use_cuda",
    #"tb_logdir":         "Sampling_tb_logs",
    "output_csv":        "Sampling_output_csv", 
    "num_smiles":        "Sampling_num_smiles", 
    "unique_molecules":  "Sampling_unique_molecules", 
    "randomize_smiles":  "Sampling_randomize_smiles",
    
    # Molecule Generators 
    "mol_gen":            "Sampling_mol_gen",
    "Reinvent_ext":       "Sampling_Reinvent_ext_model",
    "LibInvent_ext":      "Sampling_LibInvent_ext_model",
    "LibInvent_smi":      "Sampling_LibInvent_smi_file",
    "LinkInvent_ext":     "Sampling_LinkInvent_ext_model",
    "LinkInvent_smi":     "Sampling_LinkInvent_smi_file",
    "Mol2Mol":            "Sampling_Mol2Mol_model_type",
    "Mol2Mol_ext":        "Sampling_Mol2Mol_ext_model",
    "Mol2Mol_smi":        "Sampling_Mol2Mol_smi_file",
    "Mol2Mol_temp":       "Sampling_Mol2Mol_temperature",
    "Mol2Mol_strategy":   "Sampling_Mol2Mol_sample_strategy",
    "Mol2Mol_distance":   "Sampling_Mol2Mol_distance_threshold",
    # "Mol2Mol_pairs_type": "Sampling_Mol2Mol_pairs_type",
    # "Mol2Mol_pairs_upper":"Sampling_Mol2Mol_pairs_upper",
    # "Mol2Mol_pairs_lower":"Sampling_Mol2Mol_pairs_lower",
    # "Mol2Mol_pairs_min":  "Sampling_Mol2Mol_pairs_min",
    # "Mol2Mol_pairs_max":  "Sampling_Mol2Mol_pairs_max",

    # Bash File Options 
    "bash_script":       "Sampling_bash_script",
    "inputfile_name":    "Sampling_inputfile_name",
    "logfile_name":      "Sampling_logfile_name",
    "conda_env":         "Sampling_conda_env",
    "cluster":           "Sampling_cluster_calc",
    "job_name":          "Sampling_job_name",
    "partition_name":    "Sampling_partition_name",
    "num_nodes":         "Sampling_num_nodes",
    "gpus_per_node":     "Sampling_gpus_per_node",
    "time":              "Sampling_time",
  },

  ## Transfer Learning (TL) 
  "Transfer Learning (TL)": 
  {
    # General Options
    "json_name":         "TL_json_file",
    "use_cuda":          "TL_use_cuda",
    #"num_cpus":          "TL_num_cpus",
    "tb_dir":            "TL_tb_dir",

    # Transfer Learning Parameters
    "num_epochs":        "TL_num_epochs",
    "save_every_n":      "TL_save_epochs",
    "batch_size":        "TL_batch_size",
    "num_refs":          "TL_num_refs",
    "sample_batch_size": "TL_sample_batch_size",

    # Molecule Generators 
    "mol_gen":                    "TL_mol_gen",
    "Reinvent_ext":               "TL_Reinvent_ext_model",
    "Reinvent_smi":               "TL_Reinvent_smi_file",
    "Reinvent_Output_model":      "TL_Reinvent_output_model",
    "Reinvent_validation":        "TL_Reinvent_validation_smiles",
    "LibInvent_ext":              "TL_LibInvent_ext_model",
    "LibInvent_smi":              "TL_LibInvent_smi_file",
    "LibInvent_Output_model":     "TL_LibInvent_output_model",
    "LibInvent_validation":       "TL_LibInvent_validation_smiles",
    "LinkInvent_ext":             "TL_LinkInvent_ext_model",
    "LinkInvent_smi":             "TL_LinkInvent_smi_file",
    "LinkInvent_Output_model":    "TL_LinkInvent_output_model",
    "LinkInvent_validation":      "TL_LinkInvent_validation_smiles",
    "Mol2Mol":                    "TL_Mol2Mol_model_type",
    "Mol2Mol_ext":                "TL_Mol2Mol_ext_model",
    "Mol2Mol_smi":                "TL_Mol2Mol_smi_file",
    "Mol2Mol_Output_model":       "TL_Mol2Mol_output_model",
    "Mol2Mol_validation":         "TL_Mol2Mol_validation_smiles",
    #"Mol2Mol_pairs_type":         "TL_Mol2Mol_pairs_type",
    "Mol2Mol_pairs_upper":        "TL_Mol2Mol_pairs_upper",
    "Mol2Mol_pairs_lower":        "TL_Mol2Mol_pairs_lower",
    "Mol2Mol_pairs_min":          "TL_Mol2Mol_pairs_min",
    "Mol2Mol_pairs_max":          "TL_Mol2Mol_pairs_max",

    # Bash File Options 
    "bash_script":       "TL_bash_script",
    "inputfile_name":    "TL_inputfile_name",
    "logfile_name":      "TL_logfile_name",
    "conda_env":         "TL_conda_env",
    "cluster":           "TL_cluster_calc",
    "job_name":          "TL_job_name",
    "partition_name":    "TL_partition_name",
    "num_nodes":         "TL_num_nodes",
    "gpus_per_node":     "TL_gpus_per_node",
    "time":              "TL_time",
  },

  ## Reinforcement Learning (RL)
  "Reinforcement Learning (RL)": 
  {
    # General Options 
    "json_name":         "RL_json_file",
    "use_cuda":          "RL_use_cuda",
    "tb_dir":            "RL_tb_dir",
    "smi_file_name":     "RL_smiles_file",
    "smi_file":          "RL_smi_file",
    "output_csv":        "RL_output_csv",

    # Reinforcement Learning Parameters
    "summary_csv":      "RL_summary_csv",
    "use_checkpoint":   "RL_use_checkpoint",
    #"purge_memories":   "RL_purge_memories",
    "batch_size":       "RL_batch_size",
    "unique_sequences": "RL_unique_sequences",
    "randomize_smiles": "RL_randomize_smiles",
  
    # Molecule Generators 
    "mol_gen":                    "RL_mol_gen",
    "Reinvent_prior_model":       "RL_Reinvent_prior_model",
    "Reinvent_agent_model":       "RL_Reinvent_agent_model",
    "Reinvent_inception":         "RL_Reinvent_inception",
    "Reinvent_smi":               "RL_Reinvent_smi_file",
    "Reinvent_memory":            "RL_Reinvent_memory_size",
    "Reinvent_sample_size":       "RL_Reinvent_sample_size",
    "LibInvent_prior_model":      "RL_LibInvent_prior_model",
    "LibInvent_agent_model":      "RL_LibInvent_agent_model",
    "LibInvent_smi":              "RL_LibInvent_smi_file",
    "LinkInvent_prior_model":     "RL_LinkInvent_prior_model",
    "LinkInvent_agent_model":     "RL_LinkInvent_agent_model",
    "LinkInvent_smi":             "RL_LinkInvent_smi_file",
    "Mol2Mol":                    "RL_Mol2Mol_model_type",
    "Mol2Mol_prior_model":        "RL_Mol2Mol_prior_model",
    "Mol2Mol_agent_model":        "RL_Mol2Mol_agent_model",
    "Mol2Mol_smi":                "RL_Mol2Mol_smi_file",
    "Mol2Mol_temp":               "RL_Mol2Mol_temperature",
    "Mol2Mol_strategy":           "RL_Mol2Mol_sample_strategy",
    "Mol2Mol_distance":           "RL_Mol2Mol_distance_threshold",
    # "Mol2Mol_pairs_type":         "RL_Mol2Mol_pairs_type",
    # "Mol2Mol_pairs_upper":        "RL_Mol2Mol_pairs_upper",
    # "Mol2Mol_pairs_lower":        "RL_Mol2Mol_pairs_lower",
    # "Mol2Mol_pairs_min":          "RL_Mol2Mol_pairs_min",
    # "Mol2Mol_pairs_max":          "RL_Mol2Mol_pairs_max",

    # Learning Strategy
    #"learning_strategy":          "RL_ls_type", 
    "sigma":                      "RL_sigma", 
    "learning_rate":              "RL_lr",

    # Diversity Filter
    "diversity_filter":           "RL_div_filter",
    "diversity_type":             "RL_div_filter_type",
    "buckets":                    "RL_div_filter_bucket",
    "min_score":                  "RL_div_filter_minscore",
    "minsim":                     "RL_div_filter_minsimilarity",
    "penalty":                    "RL_div_filter_penalty",
  
    # Stage
    "chk_name":                   "RL_chk",
    #"terminate":                  "RL_termination",
    "max_score":                  "RL_max_score",
    "max_steps":                  "RL_max_steps",
    "min_steps":                  "RL_min_steps",
    
    # # Scoring Components
    # "comps":             "RL_scor_components",
    # "weight":            "RL_weight",
    # "parallel":          "RL_parallel",
    # "scoring_file":      "RL_scoring_file",
    # "scoring_filename":  "RL_scoring_filename",
    # "scoring_filetype":  "RL_scoring_filetype",

    # Bash File Options 
    "bash_script":       "RL_bash_script",
    "inputfile_name":    "RL_inputfile_name",
    "logfile_name":      "RL_logfile_name",
    "conda_env":         "RL_conda_env",
    "cluster":           "RL_cluster_calc",
    "job_name":          "RL_job_name",
    "partition_name":    "RL_partition_name",
    "num_nodes":         "RL_num_nodes",
    "gpus_per_node":     "RL_gpus_per_node",
    "time":              "RL_time",
  },

  ## Staged Learning (SL)
  "Staged Learning (SL)": 
  {
    # General Options 
    "json_name":         "SL_json_file",
    "use_cuda":          "SL_use_cuda",
    "tb_dir":            "SL_tb_dir",
    "smi_file_name":     "SL_smiles_file",
    "smi_file":          "SL_smi_file",
    "output_csv":        "SL_output_csv",

    # Reinforcement Learning Parameters
    "summary_csv":       "SL_summary_csv",
    "use_checkpoint":    "SL_use_checkpoint",
    #"purge_memories":    "SL_purge_memories",
    "batch_size":        "SL_batch_size",
    "unique_sequences":  "SL_unique_sequences",
    "randomize_smiles":  "SL_randomize_smiles",

    # Molecule Generators 
    "mol_gen":                    "SL_mol_gen",
    "Reinvent_prior_model":       "SL_Reinvent_prior_model",
    "Reinvent_agent_model":       "SL_Reinvent_agent_model",
    "Reinvent_inception":         "SL_Reinvent_inception",
    "Reinvent_smi":               "SL_Reinvent_smi_file",
    "Reinvent_memory":            "SL_Reinvent_memory_size",
    "Reinvent_sample_size":       "SL_Reinvent_sample_size",
    "LibInvent_prior_model":      "SL_LibInvent_prior_model",
    "LibInvent_agent_model":      "SL_LibInvent_agent_model",
    "LibInvent_smi":              "SL_LibInvent_smi_file",
    "LinkInvent_prior_model":     "SL_LinkInvent_prior_model",
    "LinkInvent_agent_model":     "SL_LinkInvent_agent_model",
    "LinkInvent_smi":             "SL_LinkInvent_smi_file",
    "Mol2Mol":                    "SL_Mol2Mol_model_type",
    "Mol2Mol_prior_model":        "SL_Mol2Mol_prior_model",
    "Mol2Mol_agent_model":        "SL_Mol2Mol_agent_model",
    "Mol2Mol_smi":                "SL_Mol2Mol_smi_file",
    "Mol2Mol_temp":               "SL_Mol2Mol_temperature",
    "Mol2Mol_strategy":           "SL_Mol2Mol_sample_strategy",
    "Mol2Mol_distance":           "SL_Mol2Mol_distance_threshold",
    # "Mol2Mol_pairs_type":         "SL_Mol2Mol_pairs_type",
    # "Mol2Mol_pairs_upper":        "SL_Mol2Mol_pairs_upper",
    # "Mol2Mol_pairs_lower":        "SL_Mol2Mol_pairs_lower",
    # "Mol2Mol_pairs_min":          "SL_Mol2Mol_pairs_min",
    # "Mol2Mol_pairs_max":          "SL_Mol2Mol_pairs_max",

    # Learning Strategy
    #"learning_strategy":          "SL_ls_type", 
    "sigma":                      "SL_sigma", 
    "learning_rate":              "SL_lr",

    # Diversity Filter
    "diversity_filter":           "SL_div_filter",
    "diversity_type":             "SL_div_filter_type",
    "buckets":                    "SL_div_filter_bucket",
    "min_score":                  "SL_div_filter_minscore",
    "minsim":                     "SL_div_filter_minsimilarity",
    "penalty":                    "SL_div_filter_penalty",
  
    # Stage
    "num_stages":                 "SL_num_stages",
    # "chk_name":                   "SL_chk",
    # #"terminate":                  "SL_termination",
    # "max_score":                  "SL_max_score",
    # "max_steps":                  "SL_max_steps",
    # "min_steps":                  "SL_min_steps",
    
    # # Scoring Components
    # "comps":             "SL_scor_components",
    # "weight":            "SL_weight",
    # "parallel":          "SL_parallel",
    # "scoring_file":      "SL_scoring_file",
    # "scoring_filename":  "SL_scoring_filename",
    # "scoring_filetype":  "SL_scoring_filetype",

    # Bash File Options 
    "bash_script":       "SL_bash_script",
    "inputfile_name":    "SL_inputfile_name",
    "logfile_name":      "SL_logfile_name",
    "conda_env":         "SL_conda_env",
    "cluster":           "SL_cluster_calc",
    "job_name":          "SL_job_name",
    "partition_name":    "SL_partition_name",
    "num_nodes":         "SL_num_nodes",
    "gpus_per_node":     "SL_gpus_per_node",
    "time":              "SL_time",
  }
}


### Session State Keys for the different parameters and their default values
state_dict_reset = {
  ## Scoring 
  "Scoring": 
  {
    # General Options 
    "json_name":           {"key": "Scoring_json_file", "value": "Scoring_input"},
    "use_cuda":            {"key": "Scoring_use_cuda", "value": "true"},
    "smi_file_name":       {"key": "Scoring_smiles_file", "value": "to_score"},
    "smi_file":            {"key": "Scoring_smi_file", "value": None},
    "output_csv":          {"key": "Scoring_output_csv", "value": "scored"},
    
    # Scoring Components
    # #"comps":               {"key": "Scoring_scor_components", "value": []},
    # "weight":              {"key": "Scoring_weight", "value": "geometric"},
    # "parallel":            {"key": "Scoring_parallel", "value": "true"},
    # #"scoring_file":        {"key": "Scoring_scoring_file", "value": False},
    # "scoring_filename":    {"key": "Scoring_filename", "value": "scoring_file"},
    # "scoring_filetype":    {"key": "Scoring_filetype", "value": "json"},

    # Bash File Options 
    #"bash_script":         {"key": "Scoring_bash_script", "value": False},
    "inputfile_name":      {"key": "Scoring_inputfile_name", "value": "Scoring_input"},
    "logfile_name":        {"key": "Scoring_logfile_name", "value": "logfile"},
    "conda_env":           {"key": "Scoring_conda_env", "value": "reinvent4"},
    "job_name":            {"key": "Scoring_job_name", "value": "reinvent"},
    "partition_name":      {"key": "Scoring_partition_name", "value": "cdd_gpuq"},
    "num_nodes":           {"key": "Scoring_num_nodes", "value": 1},
    "gpus_per_node":       {"key": "Scoring_gpus_per_node", "value": 1},
    "time":                {"key": "Scoring_time", "value": "00-12:00:00"},
  },

  ## Sampling 
  "Sampling": 
  {
    # General Options 
    "json_name":           {"key": "Sampling_json_file", "value": "Sampling_input"},
    "use_cuda":            {"key": "Sampling_use_cuda", "value": "true"},
    #"tb_logdir":           {"key": "Sampling_tb_logs", "value": "TensorBoard_Sampling"},
    "output_csv":          {"key": "Sampling_output_csv", "value": "sampling"}, 
    "num_smiles":          {"key": "Sampling_num_smiles", "value": 100}, 
    "unique_molecules":    {"key": "Sampling_unique_molecules", "value": "true"}, 
    "randomize_smiles":    {"key": "Sampling_randomize_smiles", "value": "true"},
    
    # Molecule Generators 
    #"mol_gen":             {"key": "Sampling_mol_gen", "value": "Reinvent"},
    "Reinvent_ext":        {"key": "Sampling_Reinvent_ext_model", "value": False},  
    "LibInvent_ext":       {"key": "Sampling_LibInvent_ext_model", "value": False},  
    "LibInvent_smi":       {"key": "Sampling_LibInvent_smi_file", "value": "scaffolds"},
    "LinkInvent_ext":      {"key": "Sampling_LinkInvent_ext_model", "value": False},  
    "LinkInvent_smi":      {"key": "Sampling_LinkInvent_smi_file", "value": "warheads"},
    "Mol2Mol":             {"key": "Sampling_Mol2Mol_model_type", "value": "mol2mol_similarity"},
    "Mol2Mol_ext":         {"key": "Sampling_Mol2Mol_ext_model", "value": False},  
    "Mol2Mol_smi":         {"key": "Sampling_Mol2Mol_smi_file", "value": "mol2mol"},
    "Mol2Mol_temp":        {"key": "Sampling_Mol2Mol_temperature", "value": 1.0},
    "Mol2Mol_strategy":    {"key": "Sampling_Mol2Mol_sample_strategy", "value": "multinomial"},
    "Mol2Mol_distance":    {"key": "Sampling_Mol2Mol_distance_threshold", "value": 100},
    # "Mol2Mol_pairs_type":  {"key": "Sampling_Mol2Mol_pairs_type", "value": "Tanimoto"},
    # "Mol2Mol_pairs_upper": {"key": "Sampling_Mol2Mol_pairs_upper", "value": 1.0},
    # "Mol2Mol_pairs_lower": {"key": "Sampling_Mol2Mol_pairs_lower", "value": 0.7},
    # "Mol2Mol_pairs_min":   {"key": "Sampling_Mol2Mol_pairs_min", "value": 1.0},
    # "Mol2Mol_pairs_max":   {"key": "Sampling_Mol2Mol_pairs_max", "value": 199.0},

    # Bash File Options 
    #"bash_script":       {"key": "Sampling_bash_script", "value": False},
    "inputfile_name":    {"key": "Sampling_inputfile_name", "value": "Sampling_input"},
    "logfile_name":      {"key": "Sampling_logfile_name", "value": "logfile"},
    "conda_env":         {"key": "Sampling_conda_env", "value": "reinvent4"},
    "job_name":          {"key": "Sampling_job_name", "value": "reinvent"},
    "partition_name":    {"key": "Sampling_partition_name", "value": "cdd_gpuq"},
    "num_nodes":         {"key": "Sampling_num_nodes", "value": 1},
    "gpus_per_node":     {"key": "Sampling_gpus_per_node", "value": 1},
    "time":              {"key": "Sampling_time", "value": "00-12:00:00"},
  },

  ## Transfer Learning (TL) 
  "Transfer Learning (TL)": 
  {
    # General Options
    "json_name":         {"key": "TL_json_file", "value": "TL_input"},
    "use_cuda":          {"key": "TL_use_cuda", "value": "true"},
    #"num_cpus":          {"key": "TL_num_cpus", "value": 1},
    "tb_dir":            {"key": "TL_tb_dir", "value": "TensoBoard_TL"},

    # Transfer Learning Parameters
    "num_epochs":        {"key": "TL_num_epochs", "value": 10},
    "save_every_n":      {"key": "TL_save_epochs", "value": 5},
    "batch_size":        {"key": "TL_batch_size", "value": 128},
    "num_refs":          {"key": "TL_num_refs", "value": 50},
    "sample_batch_size": {"key": "TL_sample_batch_size", "value": 100},

    # Molecule Generators 
    #"mol_gen":                    {"key": "TL_mol_gen", "value": "Reinvent"},
    "Reinvent_ext":               {"key": "TL_Reinvent_ext_model", "value": False},
    "Reinvent_smi":               {"key": "TL_Reinvent_smi_file", "value": "input_molecules"},
    "Reinvent_Output_model":      {"key": "TL_Reinvent_output_model", "value": "TL_Reinvent"},
    "Reinvent_validation":        {"key": "TL_Reinvent_validation_smiles", "value": "validation_molecules"},
    "LibInvent_ext":              {"key": "TL_LibInvent_ext_model", "value": False},
    "LibInvent_smi":              {"key": "TL_LibInvent_smi_file", "value": "input_molecules"},
    "LibInvent_Output_model":     {"key": "TL_LibInvent_output_model", "value": "TL_LibInvent"},
    "LibInvent_validation":       {"key": "TL_LibInvent_validation_smiles", "value": "validation_molecules"},
    "LinkInvent_ext":             {"key": "TL_LinkInvent_ext_model", "value": False},
    "LinkInvent_smi":             {"key": "TL_LinkInvent_smi_file", "value": "input_molecules"},
    "LinkInvent_Output_model":    {"key": "TL_LinkInvent_output_model", "value": "TL_LinkInvent"},
    "LinkInvent_validation":      {"key": "TL_LinkInvent_validation_smiles", "value": "validation_molecules"},
    "Mol2Mol":                    {"key": "TL_Mol2Mol_model_type", "value": "mol2mol_similarity"},
    "Mol2Mol_ext":                {"key": "TL_Mol2Mol_ext_model", "value": False},
    "Mol2Mol_smi":                {"key": "TL_Mol2Mol_smi_file", "value": "input_molecules"},
    "Mol2Mol_Output_model":       {"key": "TL_Mol2Mol_output_model", "value": "TL_Mol2Mol"},
    "Mol2Mol_validation":         {"key": "TL_Mol2Mol_validation_smiles", "value": "validation_molecules"},
    #"Mol2Mol_pairs_type":         {"key": "TL_Mol2Mol_pairs_type", "value": "Tanimoto"},
    "Mol2Mol_pairs_upper":        {"key": "TL_Mol2Mol_pairs_upper", "value": 1.0},
    "Mol2Mol_pairs_lower":        {"key": "TL_Mol2Mol_pairs_lower", "value": 0.7},
    "Mol2Mol_pairs_min":          {"key": "TL_Mol2Mol_pairs_min", "value": 1.0},
    "Mol2Mol_pairs_max":          {"key": "TL_Mol2Mol_pairs_max", "value": 199.0},

    # Bash File Options 
    #"bash_script":       {"key": "Sampling_bash_script", "value": False},
    "inputfile_name":    {"key": "TL_inputfile_name", "value": "TL_input"},
    "logfile_name":      {"key": "TL_logfile_name", "value": "logfile"},
    "conda_env":         {"key": "TL_conda_env", "value": "reinvent4"},
    "job_name":          {"key": "TL_job_name", "value": "reinvent"},
    "partition_name":    {"key": "TL_partition_name", "value": "cdd_gpuq"},
    "num_nodes":         {"key": "TL_num_nodes", "value": 1},
    "gpus_per_node":     {"key": "TL_gpus_per_node", "value": 1},
    "time":              {"key": "TL_time", "value": "00-12:00:00"},
  },

  ## Reinforcement Learning (RL)
  "Reinforcement Learning (RL)": 
  {
    # General Options 
    "json_name":           {"key": "RL_json_file", "value": "RL_input"},
    "use_cuda":            {"key": "RL_use_cuda", "value": "true"},
    "tb_dir":              {"key": "RL_tb_dir", "value": "TensorBoard_RL"},

    # Reinforcement Learning Parameters
    "summary_csv":         {"key": "RL_summary_csv", "value": "summary_RL"},
    "use_checkpoint":      {"key": "RL_use_checkpoint", "value": "false"},
    #"purge_memories":      {"key": "RL_purge_memories", "value": "true"},
    "batch_size":          {"key": "RL_batch_size", "value": 128},
    "unique_sequences":    {"key": "RL_unique_sequences", "value": "true"},
    "randomize_smiles":    {"key": "RL_randomize_smiles", "value": "true"},
  
    # Molecule Generators 
    #"mol_gen":                    {"key": "RL_mol_gen", "value": "Reinvent"},
    "Reinvent_prior_model":       {"key": "RL_Reinvent_prior_model", "value": False},
    "Reinvent_agent_model":       {"key": "RL_Reinvent_agent_model", "value": False},
    #"Reinvent_inception":         {"key": "RL_Reinvent_inception", "value": False},
    "Reinvent_smi":               {"key": "RL_Reinvent_smi_file", "value": "input_molecules"},
    "Reinvent_memory":            {"key": "RL_Reinvent_memory_size", "value": 100},
    "Reinvent_sample_size":       {"key": "RL_Reinvent_sample_size", "value": 10},
    "LibInvent_prior_model":      {"key": "RL_LibInvent_prior_model", "value": False},
    "LibInvent_agent_model":      {"key": "RL_LibInvent_agent_model", "value": False},
    "LibInvent_smi":              {"key": "RL_LibInvent_smi_file", "value": "input_molecules"},
    "LinkInvent_prior_model":     {"key": "RL_LinkInvent_prior_model", "value": False},
    "LinkInvent_agent_model":     {"key": "RL_LinkInvent_agent_model", "value": False},
    "LinkInvent_smi":             {"key": "RL_LinkInvent_smi_file", "value": "input_molecules"},
    "Mol2Mol":                    {"key": "RL_Mol2Mol_model_type", "value": "mol2mol_similarity"},
    "Mol2Mol_prior_model":        {"key": "RL_Mol2Mol_prior_model", "value": False},
    "Mol2Mol_agent_model":        {"key": "RL_Mol2Mol_agent_model", "value": False},
    "Mol2Mol_smi":                {"key": "RL_Mol2Mol_smi_file", "value": "input_molecules"},
    "Mol2Mol_temp":               {"key": "RL_Mol2Mol_temperature", "value": 1.0},
    "Mol2Mol_strategy":           {"key": "RL_Mol2Mol_sample_strategy", "value": "multinomial"},
    "Mol2Mol_distance":           {"key": "RL_Mol2Mol_distance_threshold", "value": 100},
    # "Mol2Mol_pairs_type":         {"key": "RL_Mol2Mol_pairs_type", "value": "Tanimoto"},
    # "Mol2Mol_pairs_upper":        {"key": "RL_Mol2Mol_pairs_upper", "value": 1.0},
    # "Mol2Mol_pairs_lower":        {"key": "RL_Mol2Mol_pairs_lower", "value": 0.7},
    # "Mol2Mol_pairs_min":          {"key": "RL_Mol2Mol_pairs_min", "value": 1.0},
    # "Mol2Mol_pairs_max":          {"key": "RL_Mol2Mol_pairs_max", "value": 199.0},

    # Learning Strategy
    #"learning_strategy":          {"key": "RL_ls_type", "value": "dap"},
    "sigma":                      {"key": "RL_sigma", "value": 128},
    "learning_strategy":          {"key": "RL_lr", "value": 0.0001},

    # Diversity Filter
    #"diversity_filter":           {"key": "RL_div_filter", "value": False},
    "diversity_type":             {"key": "RL_div_filter_type", "value": "IdenticalMurckoScaffold"},
    "buckets":                    {"key": "RL_div_filter_bucket", "value": 25},
    "min_score":                  {"key": "RL_div_filter_minscore", "value": 0.4},
    "minsim":                     {"key": "RL_div_filter_minsimilarity", "value": 0.4},
    "penalty":                    {"key": "RL_div_filter_penalty", "value": 0.5},

    # Stage
    "chk_name":                   {"key": "RL_chk", "value": "rl_calc"},
    #"terminate":                  {"key": "RL_termination", "value": "simple"},
    "max_score":                  {"key": "RL_max_score", "value": 0.6},
    "max_steps":                  {"key": "RL_max_steps", "value": 10},
    "min_steps":                  {"key": "RL_min_steps", "value": 100},

    # Scoring Components
    # #"comps":               {"key": "RL_scor_components", "value": []},
    # "weight":              {"key": "RL_weight", "value": "geometric"},
    # "parallel":            {"key": "RL_parallel", "value": "true"},
    # #"scoring_file":        {"key": "RL_scoring_file", "value": False},
    # "scoring_filename":    {"key": "RL_scoring_filename", "value": "scoring_file"},
    # "scoring_filetype":    {"key": "RL_scoring_filetype", "value": "json"},

    # Bash File Options 
    #"bash_script":         {"key": "RL_bash_script", "value": False},
    "inputfile_name":      {"key": "RL_inputfile_name", "value": "RL_input"},
    "logfile_name":        {"key": "RL_logfile_name", "value": "logfile"},
    "conda_env":           {"key": "RL_conda_env", "value": "reinvent4"},
    "job_name":            {"key": "RL_job_name", "value": "reinvent"},
    "partition_name":      {"key": "RL_partition_name", "value": "cdd_gpuq"},
    "num_nodes":           {"key": "RL_num_nodes", "value": 1},
    "gpus_per_node":       {"key": "RL_gpus_per_node", "value": 1},
    "time":                {"key": "RL_time", "value": "00-12:00:00"},
  },

  ## Staged Learning (SL)
  "Staged Learning (SL)": 
  {
    # General Options 
    "json_name":           {"key": "SL_json_file", "value": "SL_input"},
    "use_cuda":            {"key": "SL_use_cuda", "value": "true"},
    "tb_dir":              {"key": "SL_tb_dir", "value": "TensorBoard_SL"},

    # Reinforcement Learning Parameters
    "summary_csv":         {"key": "SL_summary_csv", "value": "summary_SL"},
    "use_checkpoint":      {"key": "SL_use_checkpoint", "value": "false"},
    #"purge_memories":      {"key": "SL_purge_memories", "value": "true"},
    "batch_size":          {"key": "SL_batch_size", "value": 128},
    "unique_sequences":    {"key": "SL_unique_sequences", "value": "true"},
    "randomize_smiles":    {"key": "SL_randomize_smiles", "value": "true"},

    # Molecule Generators 
    #"mol_gen":                    {"key": "SL_mol_gen", "value": "Reinvent"},
    "Reinvent_prior_model":       {"key": "SL_Reinvent_prior_model", "value": False},
    "Reinvent_agent_model":       {"key": "SL_Reinvent_agent_model", "value": False},
    #"Reinvent_inception":         {"key": "SL_Reinvent_inception", "value": False},
    "Reinvent_smi":               {"key": "SL_Reinvent_smi_file", "value": "input_molecules"},
    "Reinvent_memory":            {"key": "SL_Reinvent_memory_size", "value": 100},
    "Reinvent_sample_size":       {"key": "SL_Reinvent_sample_size", "value": 10},
    "LibInvent_prior_model":      {"key": "SL_LibInvent_prior_model", "value": False},
    "LibInvent_agent_model":      {"key": "SL_LibInvent_agent_model", "value": False},
    "LibInvent_smi":              {"key": "SL_LibInvent_smi_file", "value": "input_molecules"},
    "LinkInvent_prior_model":     {"key": "SL_LinkInvent_prior_model", "value": False},
    "LinkInvent_agent_model":     {"key": "SL_LinkInvent_agent_model", "value": False},
    "LinkInvent_smi":             {"key": "SL_LinkInvent_smi_file", "value": "input_molecules"},
    "Mol2Mol":                    {"key": "SL_Mol2Mol_model_type", "value": "mol2mol_similarity"},
    "Mol2Mol_prior_model":        {"key": "SL_Mol2Mol_prior_model", "value": False},
    "Mol2Mol_agent_model":        {"key": "SL_Mol2Mol_agent_model", "value": False},
    "Mol2Mol_smi":                {"key": "SL_Mol2Mol_smi_file", "value": "input_molecules"},
    "Mol2Mol_temp":               {"key": "SL_Mol2Mol_temperature", "value": 1.0},
    "Mol2Mol_strategy":           {"key": "SL_Mol2Mol_sample_strategy", "value": "multinomial"},
    "Mol2Mol_distance":           {"key": "SL_Mol2Mol_distance_threshold", "value": 100},
    # "Mol2Mol_pairs_type":         {"key": "SL_Mol2Mol_pairs_type", "value": "Tanimoto"},
    # "Mol2Mol_pairs_upper":        {"key": "SL_Mol2Mol_pairs_upper", "value": 1.0},
    # "Mol2Mol_pairs_lower":        {"key": "SL_Mol2Mol_pairs_lower", "value": 0.7},
    # "Mol2Mol_pairs_min":          {"key": "SL_Mol2Mol_pairs_min", "value": 1.0},
    # "Mol2Mol_pairs_max":          {"key": "SL_Mol2Mol_pairs_max", "value": 199.0},

    # Learning Strategy
    #"learning_strategy":          {"key": "SL_ls_type", "value": "dap"},
    "sigma":                      {"key": "SL_sigma", "value": 128},
    "learning_strategy":          {"key": "SL_lr", "value": 0.0001},

    # Diversity Filter
    #"diversity_filter":           {"key": "SL_div_filter", "value": False},
    "diversity_type":             {"key": "SL_div_filter_type", "value": "IdenticalMurckoScaffold"},
    "buckets":                    {"key": "SL_div_filter_bucket", "value": 25},
    "min_score":                  {"key": "SL_div_filter_minscore", "value": 0.4},
    "minsim":                     {"key": "SL_div_filter_minsimilarity", "value": 0.4},
    "penalty":                    {"key": "SL_div_filter_penalty", "value": 0.4},

    # Stage
    # "num_stages":                 {"key": "SL_num_stages", "value": 2},
    # "chk_name":                   {"key": "SL_chk", "value": "sl_calc"},
    # #"terminate":                  {"key": "SL_termination", "value": "simple"},
    # "max_score":                  {"key": "SL_max_score", "value": 0.6},
    # "max_steps":                  {"key": "SL_max_steps", "value": 10},
    # "min_steps":                  {"key": "SL_min_steps", "value": 100},

    # Scoring Components
    # #"comps":               {"key": "SL_scor_components", "value": []},
    # "weight":              {"key": "SL_weight", "value": "geometric"},
    # "parallel":            {"key": "SL_parallel", "value": "true"},
    # #"scoring_file":        {"key": "SL_scoring_file", "value": False},
    # "scoring_filename":    {"key": "SL_scoring_filename", "value": "scoring_file"},
    # "scoring_filetype":    {"key": "SL_scoring_filetype", "value": "json"},

    # Bash File Options 
    #"bash_script":         {"key": "SL_bash_script", "value": False},
    "inputfile_name":      {"key": "SL_inputfile_name", "value": "SL_input"},
    "logfile_name":        {"key": "SL_logfile_name", "value": "logfile"},
    "conda_env":           {"key": "SL_conda_env", "value": "reinvent4"},
    "job_name":            {"key": "SL_job_name", "value": "reinvent"},
    "partition_name":      {"key": "SL_partition_name", "value": "cdd_gpuq"},
    "num_nodes":           {"key": "SL_num_nodes", "value": 1},
    "gpus_per_node":       {"key": "SL_gpus_per_node", "value": 1},
    "time":                {"key": "SL_time", "value": "00-12:00:00"},
  }
}


### Chemistry tokens Supported by the different molecule generators 
chem_tokens = {
  ## Reinvent Generator
  "Reinvent": '#, =, -, (, ), [, ], 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, Br, C, Cl, F, N, O, S, [N+], [N-], [O-], [S+], [n+], [nH], c, n, o, s', 
  
  ## LibInvent Generator 
  "LibInvent": {
    # Decorator
    "Decorator": '#, =, -, (, ), [, ], 1, 2, 3, 4, 5, 6, Br, C, Cl, F, N, O, S, [N+], [N-], [N], [O-], [O], [S+], [n+], [nH], [s+], c, n, o, s, *, |',
    # Scaffold
    "Scaffold": '#, =, -, (, ), [, ], 1, 2, 3, 4, 5, 6, 7, 8, 9, Br, C, Cl, F, N, O, S, [*], [N+], [N-], [N], [O-], [O], [S+], [n+], [nH], [s+], c, n, o, s'
  },

  ## Linkinvent Generator
  "LinkInvent": {
    # Warheads
    "Warheads": '#, =, -, (, ), [, ], 1, 2, 3, 4, 5, 6, Br, C, Cl, F, N, O, S, [N+], [O-], [O], [S+], [n+], [nH], [s+], c, n, o, s, *, |',
    # Linker
    "Linker": '#, =, -, (, ), [, ], 1, 2, 3, 4, 5, 6, 7, Br, C, Cl, F, N, O, S, [*], [N+], [N-], [O-], [S+], [n+], [nH], [s+], c, n, o, s'
  },

  ## Mol2Mol Generator
  "Mol2Mol": {
    # Mol2mol (high, medium, low similarities)
    "Mol2mol (high, medium, low similarities)": '#, =, -, /, \, (, ), [, ], 1, 2, 3, 4, 5, 6, 7, 8, Br, C, Cl, F, I, N, O, S, [C@@H], [C@@], [C@H], [C@], [N+], [N@+], [N@@+], [N@], [O-], [O], [S@@], [S@], [n+], [nH], c, n, o, s',
    # Mol2mol (mmp)
    "Mol2mol (mmp)": '#, =, -, /, \, (, ), [, ], 1, 2, 3, 4, 5, 6, 7, 8, Br, C, Cl, F, I, N, O, S, [C@@H], [C@@], [C@H], [C@], [N+], [N@+], [N@@+], [O-], [O], [S@@], [S@], [n+], [nH], c, n, o, s',
    # Mol2mol (scaffold)
    "Mol2mol (scaffold)": '#, =, -, /, \, (, ), [, ], 1, 2, 3, 4, 5, 6, 7, 8, Br, C, Cl, F, I, N, O, S, [C@@H], [C@@], [C@H], [C@], [N+], [N@+], [N@@+], [O-], [O], [S@@], [S@], [n+], [nH], c, n, o, s',
    # Mol2mol (scaffold-generic)
    "Mol2mol (scaffold-generic)": '#, =, -, /, \, (, ), [, ], 1, 2, 3, 4, 5, 6, 7, 8, Br, C, Cl, F, I, N, O, S, [C@@H], [C@@], [C@H], [C@], [N+], [N@+], [N@@+], [O-], [O], [S@@], [S@], [n+], [n-], [nH], c, n, o, s'
  }
}