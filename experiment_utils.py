# EBO + RBS
# EBO + RBM
# EBO
# iEBO
# iEBO + RBS
# iEBO + RBM
# HPO + GES
# HPO + GES + RBS
# HPO + GES + RBM
# FiSEBO
# AutoGluon

from re import A


X_MAP = [0, 25, 50, 75, 100]

# Y_MAP = {
#     10101: {"ebo": [0, 20], "RQ_1b": [7, 20], "RQ_2": [9, 11], "RQ_2a": [8, 11], "RQ_2b": [8, 11]},
#     "colorectal_histology": {"RQ_1a": [4, 10], "RQ_1b": [4, 10], "RQ_2": [4, 10], "RQ_2a": [4, 8], "RQ_2b": [4, 8]},
#     "fashion_mnist": {"RQ_1a": [4.5, 8], "RQ_1b": [4.5, 8], "RQ_2": [4.75, 6], "RQ_2a": [4.5, 6], "RQ_2b": [4.5, 6]},
# }
SETS = {
    'size_5': {
  
    'ebo_1_all': {
        "strategies": [
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
        ],
        "NAME_TO_LABEL": {
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'EBO (Post-hoc)',
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'EBO',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post-hoc + Trad.)', 
        },
        "color_marker": {
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'black',
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'purple',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'brown'
        }
    },
    'ebo_all_stack': {
        "strategies": [
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1',
            'ebor_pef_F_etp_F_ueol_F_w_F_nsl_2', 
            'ebos_pef_F_etp_F_ueol_F_w_F_nsl_2',
        ],
        "NAME_TO_LABEL": {
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'EBO',
            'ebor_pef_F_etp_F_ueol_F_w_F_nsl_2': 'EBO (RBM)',
            'ebos_pef_F_etp_F_ueol_F_w_F_nsl_2': 'EBO (RBS)', 
        },
        "color_marker": {
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'black',
            'ebor_pef_F_etp_F_ueol_F_w_F_nsl_2': 'purple',
            'ebos_pef_F_etp_F_ueol_F_w_F_nsl_2': 'brown'
        }
    },
    'ebo_all_stack_pef': {
        "strategies": [
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1',
            'ebor_pef_T_etp_F_ueol_F_w_F_nsl_2', 
            'ebos_pef_T_etp_F_ueol_F_w_F_nsl_2',
        ],
        "NAME_TO_LABEL": {
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'EBO',
            'ebor_pef_T_etp_F_ueol_F_w_F_nsl_2': 'EBO (RBM)',
            'ebos_pef_T_etp_F_ueol_F_w_F_nsl_2': 'EBO (RBS)', 
        },
        "color_marker": {
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'black',
            'ebor_pef_T_etp_F_ueol_F_w_F_nsl_2': 'purple',
            'ebos_pef_T_etp_F_ueol_F_w_F_nsl_2': 'brown'
        }
    },
    'iebo_all_stack': {
        "strategies": [
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1',
            'eihr_pef_F_etp_F_ueol_F_w_T_nsl_2', 
            'eihs_pef_F_etp_F_ueol_F_w_T_nsl_2',
        ],
        "NAME_TO_LABEL": {
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'iEBO',
            'eihr_pef_F_etp_F_ueol_F_w_T_nsl_2': 'iEBO (RBM)',
            'eihs_pef_F_etp_F_ueol_F_w_T_nsl_2': 'iEBO (RBS)', 
        },
        "color_marker": {
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'black',
            'eihr_pef_F_etp_F_ueol_F_w_T_nsl_2': 'purple',
            'eihs_pef_F_etp_F_ueol_F_w_T_nsl_2': 'brown'
        }
    },
    'iebo_all_stack_pef': {
        "strategies": [
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1',
            'eihr_pef_T_etp_F_ueol_F_w_T_nsl_2', 
            'eihs_pef_T_etp_F_ueol_F_w_T_nsl_2',
        ],
        "NAME_TO_LABEL": {
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'iEBO',
            'eihr_pef_T_etp_F_ueol_F_w_T_nsl_2': 'iEBO (RBM)',
            'eihs_pef_T_etp_F_ueol_F_w_T_nsl_2': 'iEBO (RBS)', 
        },
        "color_marker": {
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'black',
            'eihr_pef_T_etp_F_ueol_F_w_T_nsl_2': 'purple',
            'eihs_pef_T_etp_F_ueol_F_w_T_nsl_2': 'brown'
        }
    },
    'es_all_stack_etp': {
        "strategies": [
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
            'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
        ],
        "NAME_TO_LABEL": {
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'HPO + GES',
            'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'HPO + GES (RBM)',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'HPO + GES (RBS)', 
        },
        "color_marker": {
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'black',
            'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'purple',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'brown'
        }
    },
    'es_all_stack': {
        "strategies": [
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1',
            'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 
            'sespl_pef_F_etp_F_ueol_F_w_F_nsl_2',
        ],
        "NAME_TO_LABEL": {
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'HPO + GES',
            'esr_pef_F_etp_F_ueol_F_w_F_nsl_2': 'HPO + GES (RBM)',
            'sespl_pef_F_etp_F_ueol_F_w_F_nsl_2': 'HPO + GES (RBS)', 
        },
        "color_marker": {
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'black',
            'esr_pef_F_etp_F_ueol_F_w_F_nsl_2': 'purple',
            'sespl_pef_F_etp_F_ueol_F_w_F_nsl_2': 'brown'
        }
    },
    
    # 'eih_1_pef': {
    #     "strategies": [
    #         'eih_pef_F_etp_F_ueol_F_w_T_nsl_1',
    #         'eih_pef_T_etp_F_ueol_F_w_T_nsl_1', 
    #         # 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1',
    #     ],
    #     "NAME_TO_LABEL": {
    #         'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'iEBO',
    #         'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': "iEBO (Post-hoc)", 
    #         # 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1': 'iEBO (Post-hoc)', 
    #     },
    #     "color_marker": {
    #         'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'black',
    #         'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'purple',
    #         # 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1': 'brown'
    #     }
    # },
    'eih_1_etp': {
        "strategies": [
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1', 
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1',
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1',
        ],
        "NAME_TO_LABEL": {
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'iEBO (Post-hoc)',
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'iEBO',
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'iEBO (Post-hoc + Trad.)', 
        },
        "color_marker": {
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'black',
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'purple',
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'brown'
        }
    },
    'es_1_etp': {
        "strategies": [
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
            # 'eih_pef_T_etp_F_ueol_F_w_T_nsl_1',
        ],
        "NAME_TO_LABEL": {
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'ES',
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'ES (Trad.)',
            # 'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'iEBO (post-hoc ensemble)', 
        },
        "color_marker": {
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'black',
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'purple',
        }
    },
    'nsl_1': {
        "strategies": [
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1', 
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1'
        ],
        "NAME_TO_LABEL": {
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'iEBO (Post-hoc + Trad.)',
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'ES (Trad.)',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post-hoc + Trad.)'
        },
        "color_marker": {
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'black',
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'purple',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'brown'
        }
    },
    'ebo_all': {
        "strategies": [
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
            'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2',
            'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post-hoc + Trad.)',
        'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post-hoc + Trad. + RBM)',
        'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post-hoc + Trad. + RBS)' ,
    },
    "color_marker": {
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'black',
            'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'purple',
            'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2': 'brown'
    }
},
    'eih_all':{
        "strategies": [
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'iEBO (Post-hoc + Trad.)',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post-hoc + Trad. + RBM)',
        'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post-hoc + Trad. + RBS)' ,
    },
    "color_marker": {
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'black',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'purple',
            'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'brown'
    }
    },

    'es_all':{
        "strategies": [
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
            'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'HPO + GES (Trad.)',
        'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'HPO + GES (Trad. + RBM)',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'HPO + GES (Trad. + RBS)' ,
    },
    "color_marker": {
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'black',
            'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'purple',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'brown'
    }
    },
    'all_best': {
        "strategies":[
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post-hoc + Trad.)',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post-hoc + Trad. + RBM)',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'HPO + GES (Trad. + RBS)' ,
    },
    "color_marker": {
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'black',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'purple',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'brown'
    }
    },
    'all_base': {
        "strategies":[
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1',
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1',
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1',
        ],
    "NAME_TO_LABEL": {
        'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'EBO',
        'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'iEBO',
        'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'HPO + GES' ,
    },
    "color_marker": {
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'black',
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'purple',
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'brown'
    }
    },
    'all_base_pef': {
        "strategies":[
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1',
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1',
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1',
        ],
    "NAME_TO_LABEL": {
        'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'EBO (Post-hoc)',
        'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'iEBO (Post-hoc)',
        'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'HPO + GES' ,
    },
    "color_marker": {
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'black',
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'purple',
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'brown'
    }
    },
    'all_base_etp': {
        "strategies":[
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1',
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
        ],
    "NAME_TO_LABEL": {
        'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post-hoc + Trad.)',
        'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'iEBO (Post-hoc +Trad.)',
        'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'HPO + GES (Trad.)',
    },
    "color_marker": {
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'black',
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'purple',
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'brown'
    }
    },
    'sft': {
        "strategies":[
            'sft_pef_T_etp_F_ueol_F_w_F_nsl_2',
            'sft_pef_T_etp_T_ueol_F_w_F_nsl_2',
            'sft_pef_F_etp_F_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'sft_pef_T_etp_F_ueol_F_w_F_nsl_2': 'FiSEBO (Post-hoc)',
        'sft_pef_T_etp_T_ueol_F_w_F_nsl_2': 'FiSEBO (Post-hoc + Trad.)',
        'sft_pef_F_etp_F_ueol_F_w_F_nsl_2': 'FiSEBO' ,
    },
    "color_marker": {
            'sft_pef_T_etp_F_ueol_F_w_F_nsl_2': 'black',
            'sft_pef_T_etp_T_ueol_F_w_F_nsl_2': 'purple',
            'sft_pef_F_etp_F_ueol_F_w_F_nsl_2': 'brown'
    }
    },
    'all_best+sft': {
        "strategies":[
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
            'sft_pef_T_etp_T_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post-hoc + Trad.)',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post-hoc + Trad. + RBM)',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'HPO + GES (Trad. + RBS)' ,
        'sft_pef_T_etp_T_ueol_F_w_F_nsl_2': 'FiSEBO (Post-hoc + Trad.)',
    },
    "color_marker": {
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'black',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'purple',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'brown',
            'sft_pef_T_etp_T_ueol_F_w_F_nsl_2': 'red',
    }
    },
    },
    'size_11': {
    'all_best_size_11': {
        "strategies":[
            'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post-hoc + Trad. + RBM)',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post-hoc + Trad. + RBM)',
        'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2':  'iEBO (Post-hoc + Trad. + RBS)',
        'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'HPO + GES (Trad. + RBM)',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'HPO + GES (Trad. + RBS)',
    },
    "color_marker": {
        'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'black',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'purple',
        'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'brown',
        'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'red',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2':'blue',
    }
},
    'iebo_vs_es_size_11': {
        "strategies":[
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post-hoc + Trad. + RBM)',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post-hoc + Trad. + RBM)',
        'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2':  'iEBO (Post-hoc + Trad. + RBS)',
        'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'HPO + GES (Trad. + RBM)',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'HPO + GES (Trad. + RBS)',
    },
    "color_marker": {
        'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'black',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'purple',
        'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'brown',
        'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'red',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2':'blue',
    }
},
    'all_best_size_11+sa': {
        "strategies":[
            'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
            'sa_pef_F_etp_F_ueol_F_w_F_nsl_2'
        ],
    "NAME_TO_LABEL": {
        'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post-hoc + Trad. + RBM)',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post-hoc + Trad. + RBM)',
        'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2':  'iEBO (Post-hoc + Trad. + RBS)',
        'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'HPO + GES (Trad. + RBM)',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'HPO + GES (Trad. + RBS)',
        'sa_pef_F_etp_F_ueol_F_w_F_nsl_2': 'Fixed Defaults (AutoGluon)'
    },
    "color_marker": {

        'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'black',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'purple',
        'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'brown',
        'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'red',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2':'blue',
        'sa_pef_F_etp_F_ueol_F_w_F_nsl_2': 'yellow'
    }
},
}
#     'all_best_size_11': {
#         "strategies":[
#             'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2',
#             'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
#             'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
#             'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
#             'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
#         ],
#     "NAME_TO_LABEL": {
#         'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post-hoc + Trad. + RBM)',
#         'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post-hoc + Trad. + RBM)',
#         'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2':  'iEBO (Post-hoc + Trad. + RBS)',
#         'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'HPO + GES (Trad. + RBM)',
#         'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'HPO + GES (Trad. + RBS)',
#     },
#     "color_marker": {

#         'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'black',
#         'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'purple',
#         'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'brown',
#         'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'red',
#         'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2':'blue',
#     }
# }
}
DATASET_INFO = "dataset_collection.csv"

TASKS = [10101, 3, 168335, 14965, 146195, 31, 9981, 7592]

SEEDS = [839, 106, 355]

def replace_key(key: str) -> str:
    key = key.split('_')
    params = [key[0]]
    for i in range(1, len(key)):
        if i % 2 !=0:
            params.append(f"{key[i]}_{key[i+1]}")

    final = params[0]
    order = ['pef', 'etp', 'ueol', 'w']
    for o in order:
        param = [i for i in params if o in i][0]
        final = f"{final}_{param}"
    if 'es' in params[0]:
        if 'sespl' in params[0] or 'esr' in params[0]:
            final = f"{final}_nsl_2"
        else:
            final = f"{final}_nsl_1"
    else:
        if 's' in params[0] or 'r' in params[0]:
            final = f"{final}_nsl_2"
        else:
            final = f"{final}_nsl_1"
    return final


COLOR_MARKER_DICT = {
    'ebo_etp_F_w_F_pef_T_ueol_F': 'black',
    'ebo_etp_T_w_F_pef_T_ueol_F': 'purple',
    # 'EBO': {'color': 'violet', 'marker': 'o'},
    # 'iEBO': {'color': 'green', 'marker': 'o'},
    # 'iEBO + RBS': {'color': 'deeppink', 'marker': 'o'},
    # 'iEBO + RBM': {'color': 'grey', 'marker': 'o'},
    # 'HPO + GES': {'color': 'yellow', 'marker': 'o'},
    # 'HPO + GES + RBS': {'color': 'darkmagenta', 'marker': 'o'},
    # 'HPO + GES + RBM': {'color': 'darkblue', 'marker': 'o'},
    # 'FiSEBO': {'color': 'black', 'marker': 'o'},
    # 'AutoGluon': {'color': 'darkred', 'marker': 'o'},
    # '': {'color': 'darkkhaki', 'marker': 'o'},
    # ': {'color': 'darkgreen', 'marker': 'o'},
    # ': {'color': 'gold', 'marker': 'o'},
    # 'reg_cocktails_reproduce_multi-seeded_small': {'color': 'brown', 'marker': 'o'},
    # 'reg_cocktails_reproduce_pytorch_embedding_multi-seeded_multi_fidelity_small': {'color': 'green', 'marker': 'o'},
    # 'reg_cocktails_reproduce_pytorch_embedding_multi-seeded_small': {'color': 'deeppink', 'marker': 'o'},
    # 'reg_cocktails_lucas_paper_multi-seeded_multi_fidelity_small': {'color': 'grey', 'marker': 'o'}
}
X_LABEL = "Total Walltime (s)"
Y_LABEL = "Balanced Accuracy [%]"

MAX_BUDGET = {
    146212: 258314.078,
    12: 220709.001,
    7592: 258214.646,
    146822: 184748.352,
    53: 86717.397,
    9981: 258299.887,
    14965: 258287.794,
    168911: 189259.621,
    3: 112325.322,
    168331: 255289.376,
    146825: 242392.002,
    146818: 49764.143,
    168330: 256309.298,
    146195: 258466.567,
    168335: 250449.875,
    168909: 249914.35,
    168912: 220371.154,
    10101: 49961.487,
    9952: 220437.196,
    167120: 258548.317,
    168910: 255259.578,
    146821: 61796.968,
    3917: 128803.558,
    31: 75587.103,
    168908: 256625.872,
    9977: 253810.082,
    167119: 258931.245,
    168329: 257096.852,
    # 146606: 0,
    # 168868: 0
}