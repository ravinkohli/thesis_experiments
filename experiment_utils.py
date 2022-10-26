# EBO+RBS
# EBO+RBM
# EBO
# iEBO
# iEBO+RBS
# iEBO+RBM
# HPO+GES
# HPO+GES+RBS
# HPO+GES+RBM
# FiSEBO
# AutoGluon

from re import A


# Y_MAP = [0, 0.25, 0.5, 0.75, 1]
X_MAP = {
    14965: [1e3,3e5],
    146195: [1e3, 3e5],
    10101: [8e2, 5e4],
    3: [1e2, 3e5],
    31: [1e3, 8e4],
    7592: [1e3, 3e5],
    9981: [1e3, 3e5],
    168335: [2e4, 3e5]
}

SETS = {
    'size_5': {
  
        'all':{
             "strategies": [
                "ebo_pef_T_etp_F_ueol_F_w_F_nsl_1",
                "ebo_pef_T_etp_T_ueol_F_w_F_nsl_1",
                "ebo_pef_F_etp_F_ueol_F_w_F_nsl_1",
                "ebor_pef_T_etp_T_ueol_F_w_F_nsl_2",
                "ebos_pef_T_etp_T_ueol_F_w_F_nsl_2",
                "es_pef_F_etp_F_ueol_F_w_F_nsl_1",
                "es_pef_F_etp_T_ueol_F_w_F_nsl_1",
                "eih_pef_T_etp_F_ueol_F_w_F_nsl_1",
                "eih_pef_T_etp_T_ueol_F_w_F_nsl_1",
                "eih_pef_T_etp_F_ueol_F_w_T_nsl_1",
                "eih_pef_T_etp_T_ueol_F_w_T_nsl_1",
                "eih_pef_F_etp_F_ueol_F_w_T_nsl_1",
                "eih_pef_F_etp_T_ueol_F_w_T_nsl_1",
                "eih_pef_F_etp_F_ueol_F_w_F_nsl_1",
                "ebo_pef_F_etp_F_ueol_T_w_F_nsl_1",
                "ebo_pef_T_etp_F_ueol_T_w_F_nsl_1",
                "ebo_pef_T_etp_T_ueol_T_w_F_nsl_1",
                "ebor_pef_T_etp_F_ueol_T_w_F_nsl_2",
                "ebos_pef_T_etp_F_ueol_T_w_F_nsl_2",
                "ebor_pef_T_etp_T_ueol_T_w_F_nsl_2",
                "ebos_pef_T_etp_T_ueol_T_w_F_nsl_2",
                "sespl_pef_F_etp_F_ueol_F_w_F_nsl_2",
                "esr_pef_F_etp_F_ueol_F_w_F_nsl_2",
                "sespl_pef_F_etp_T_ueol_F_w_F_nsl_2",
                "esr_pef_F_etp_T_ueol_F_w_F_nsl_2",
                "eihr_pef_T_etp_F_ueol_F_w_T_nsl_2",
                "eihs_pef_T_etp_F_ueol_F_w_T_nsl_2",
                "eihs_pef_T_etp_T_ueol_F_w_T_nsl_2",
                "eihr_pef_T_etp_T_ueol_F_w_T_nsl_2",
                "eihr_pef_T_etp_F_ueol_F_w_F_nsl_2",
                "eihs_pef_T_etp_F_ueol_F_w_F_nsl_2",
                "sft_pef_T_etp_F_ueol_F_w_F_nsl_2",
                "eihr_pef_T_etp_T_ueol_F_w_F_nsl_2",
                "sft_pef_T_etp_T_ueol_F_w_F_nsl_2",
                "eihs_pef_T_etp_T_ueol_F_w_F_nsl_2",
                "sft_pef_F_etp_F_ueol_F_w_F_nsl_2",
                "eihr_pef_F_etp_F_ueol_F_w_T_nsl_2",
                "eihs_pef_F_etp_F_ueol_F_w_T_nsl_2",
                "sa_pef_F_etp_F_ueol_F_w_F_nsl_2",
            ],
            "NAME_TO_LABEL": {
                "ebo_pef_T_etp_F_ueol_F_w_F_nsl_1": 'EBO (Post)',
                "ebo_pef_T_etp_T_ueol_F_w_F_nsl_1": 'EBO (Post)',
                "ebo_pef_F_etp_F_ueol_F_w_F_nsl_1": 'EBO (Post)',
                "ebor_pef_T_etp_T_ueol_F_w_F_nsl_2": 'EBO (Post)',
                "ebos_pef_T_etp_T_ueol_F_w_F_nsl_2": 'EBO (Post)',
                "es_pef_F_etp_F_ueol_F_w_F_nsl_1": 'EBO (Post)',
                "es_pef_F_etp_T_ueol_F_w_F_nsl_1": 'EBO (Post)',
                "eih_pef_T_etp_F_ueol_F_w_F_nsl_1": 'EBO (Post)',
                "eih_pef_T_etp_T_ueol_F_w_F_nsl_1": 'EBO (Post)',
                "eih_pef_T_etp_F_ueol_F_w_T_nsl_1": 'EBO (Post)',
                "eih_pef_T_etp_T_ueol_F_w_T_nsl_1": 'EBO (Post)',
                "eih_pef_F_etp_F_ueol_F_w_T_nsl_1": 'EBO (Post)',
                "eih_pef_F_etp_T_ueol_F_w_T_nsl_1": 'EBO (Post)',
                "eih_pef_F_etp_F_ueol_F_w_F_nsl_1": 'EBO (Post)',
                "ebo_pef_F_etp_F_ueol_T_w_F_nsl_1": 'EBO (Post)',
                "ebo_pef_T_etp_F_ueol_T_w_F_nsl_1": 'EBO (Post)',
                "ebo_pef_T_etp_T_ueol_T_w_F_nsl_1": 'EBO (Post)',
                "ebor_pef_T_etp_F_ueol_T_w_F_nsl_2": 'EBO (Post)',
                "ebos_pef_T_etp_F_ueol_T_w_F_nsl_2": 'EBO (Post)',
                "ebor_pef_T_etp_T_ueol_T_w_F_nsl_2": 'EBO (Post)',
                "ebos_pef_T_etp_T_ueol_T_w_F_nsl_2": 'EBO (Post)',
                "sespl_pef_F_etp_F_ueol_F_w_F_nsl_2": 'EBO (Post)',
                "esr_pef_F_etp_F_ueol_F_w_F_nsl_2": 'EBO (Post)',
                "sespl_pef_F_etp_T_ueol_F_w_F_nsl_2": 'EBO (Post)',
                "esr_pef_F_etp_T_ueol_F_w_F_nsl_2": 'EBO (Post)',
                "eihr_pef_T_etp_F_ueol_F_w_T_nsl_2": 'EBO (Post)',
                "eihs_pef_T_etp_F_ueol_F_w_T_nsl_2": 'EBO (Post)',
                "eihs_pef_T_etp_T_ueol_F_w_T_nsl_2": 'EBO (Post)',
                "eihr_pef_T_etp_T_ueol_F_w_T_nsl_2": 'EBO (Post)',
                "eihr_pef_T_etp_F_ueol_F_w_F_nsl_2": 'EBO (Post)',
                "eihs_pef_T_etp_F_ueol_F_w_F_nsl_2": 'EBO (Post)',
                "sft_pef_T_etp_F_ueol_F_w_F_nsl_2": 'EBO (Post)',
                "eihr_pef_T_etp_T_ueol_F_w_F_nsl_2": 'EBO (Post)',
                "sft_pef_T_etp_T_ueol_F_w_F_nsl_2": 'EBO (Post)',
                "eihs_pef_T_etp_T_ueol_F_w_F_nsl_2": 'EBO (Post)',
                "sft_pef_F_etp_F_ueol_F_w_F_nsl_2": 'EBO (Post)',
                "eihr_pef_F_etp_F_ueol_F_w_T_nsl_2": 'EBO (Post)',
                "eihs_pef_F_etp_F_ueol_F_w_T_nsl_2": 'EBO (Post)',
                "sa_pef_F_etp_F_ueol_F_w_F_nsl_2": 'EBO (Post)',
                
                'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'EBO (Post)',
                'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post+Trad)',
                'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'EBO',
                'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+Trad+RBM)',
                'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+Trad+RBM)',
                'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'BO (Post)',
                'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'BO (Post+Trad)',
                # 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1': 'iEBO (Post)',
                # 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1': 'iEBO (Post+Trad)',
                'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'iEBO (Post)',
                'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'iEBO (Post+Trad)',
                'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'iEBO',
                # 'eih_pef_F_etp_T_ueol_F_w_T_nsl_1': 'EBO (Post)',
                # 'eih_pef_F_etp_F_ueol_F_w_F_nsl_1': 'EBO (Post)',
                # 'ebo_pef_F_etp_F_ueol_T_w_F_nsl_1': 'EBO (Post)',
                # 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1': 'EBO (Post)',
                # 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1': 'EBO (Post)',
                # 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2': 'EBO (Post)',
                # 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2': 'EBO (Post)',
                # 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2': 'EBO (Post)',
                # 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2': 'EBO (Post)',
                'sespl_pef_F_etp_F_ueol_F_w_F_nsl_2': 'BO (Post+RBS)',
                'esr_pef_F_etp_F_ueol_F_w_F_nsl_2': 'BO (Post+RBM)',
                'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+Trad+RBS)',
                'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+Trad+RBM)',
                'eihr_pef_T_etp_F_ueol_F_w_T_nsl_2': 'iEBO (Post+RBM)',
                'eihs_pef_T_etp_F_ueol_F_w_T_nsl_2': 'iEBO (Post+RBS)',
                'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'EBO (Post+Trad+RBS)',
                # 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2': 'EBO (Post)',
                # 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2': 'EBO (Post)',
                'sft_pef_T_etp_F_ueol_F_w_F_nsl_2': 'FiSEBO (Post)',
                # 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post)',
                'sft_pef_T_etp_T_ueol_F_w_F_nsl_2': 'FiSEBO (Post+Trad)',
                # 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post)',
                'sft_pef_F_etp_F_ueol_F_w_F_nsl_2': 'FiSEBO',
                'eihr_pef_F_etp_F_ueol_F_w_T_nsl_2': 'iEBO (RBM)',
                'eihs_pef_F_etp_F_ueol_F_w_T_nsl_2': 'iEBO (RBS)',
                'sa_pef_F_etp_F_ueol_F_w_F_nsl_2': 'Autogluon (fixed-defaults)',
                # 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'EBO (Post)',
                # 'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'EBO',
                # 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post+Trad)', 
            },
            "color_marker": {
                'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'red',
                'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'green',
                'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'blue'
            }
        },
        # 'ebo_uoel':{
        # "strategies": [
        #     'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1', 
        #     'ebo_pef_F_etp_F_ueol_T_w_F_nsl_1',
        #     # 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1',
        # ],
        # "NAME_TO_LABEL": {
        #     'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'EBO ',
        #     'ebo_pef_F_etp_F_ueol_T_w_F_nsl_1': 'EBO (Normalized Margin Loss)',
        #     # 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1': 'EBO (Post+Trad)', 
        # },
        # "color_marker": {
        #     'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'green',
        #     'ebo_pef_F_etp_F_ueol_T_w_F_nsl_1': 'red',
        #     # 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1': 'blue'
        # }
        # },
        # 'ebo_uoel_pef':{
        #     "strategies": [
        #         'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 
        #         'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1',
        #         # 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1',
        #     ],
        #     "NAME_TO_LABEL": {
        #         'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'EBO (Post)',
        #         'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1': 'EBO (Post + Normalized Margin Loss)',
        #         # 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1': 'EBO (Post+Trad)', 
        #     },
        #     "color_marker": {
        #         'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'green',
        #         'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1': 'red',
        #         # 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1': 'blue'
        #     }
        # },
    'ebo_1_all': {
        "strategies": [
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
        ],
        "NAME_TO_LABEL": {
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'EBO (Post)',
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'EBO',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post+Trad)', 
        },
        "color_marker": {
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'red',
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'green',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'blue'
        }
    },
    
    # 'ebo_all_stack': {
    #     "strategies": [
    #         'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1',
    #         'ebor_pef_F_etp_F_ueol_F_w_F_nsl_2', 
    #         'ebos_pef_F_etp_F_ueol_F_w_F_nsl_2',
    #     ],
    #     "NAME_TO_LABEL": {
    #         'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'EBO',
    #         'ebor_pef_F_etp_F_ueol_F_w_F_nsl_2': 'EBO (RBM)',
    #         'ebos_pef_F_etp_F_ueol_F_w_F_nsl_2': 'EBO (RBS)', 
    #     },
    #     "color_marker": {
    #         'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'red',
    #         'ebor_pef_F_etp_F_ueol_F_w_F_nsl_2': 'green',
    #         'ebos_pef_F_etp_F_ueol_F_w_F_nsl_2': 'blue'
    #     }
    # },
    'ebo_all_stack_pef': {
        "strategies": [
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
            'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2', 
            'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2',
        ],
        "NAME_TO_LABEL": {
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post)',
            'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+RBM)',
            'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+RBS)', 
        },
        "color_marker": {
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'red',
            'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'green',
            'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2': 'blue'
        }
    },
    # 'iebo_all_stack': {
    #     "strategies": [
    #         'eih_pef_F_etp_F_ueol_F_w_T_nsl_1',
    #         'eihr_pef_F_etp_F_ueol_F_w_T_nsl_2', 
    #         'eihs_pef_F_etp_F_ueol_F_w_T_nsl_2',
    #     ],
    #     "NAME_TO_LABEL": {
    #         'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'iEBO',
    #         'eihr_pef_F_etp_F_ueol_F_w_T_nsl_2': 'iEBO (RBM)',
    #         'eihs_pef_F_etp_F_ueol_F_w_T_nsl_2': 'iEBO (RBS)', 
    #     },
    #     "color_marker": {
    #         'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'red',
    #         'eihr_pef_F_etp_F_ueol_F_w_T_nsl_2': 'green',
    #         'eihs_pef_F_etp_F_ueol_F_w_T_nsl_2': 'blue'
    #     }
    # },
    'iebo_all_stack_etp': {
        "strategies": [
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2', 
            'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
        ],
        "NAME_TO_LABEL": {
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'iEBO (Post)',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post+RBM)',
            'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post+RBS)', 
        },
        "color_marker": {
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'red',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'green',
            'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'blue'
        }
    },
    'es_all_stack_etp': {
        "strategies": [
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
            'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
        ],
        "NAME_TO_LABEL": {
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'BO (Post)',
            'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+RBM)',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+RBS)', 
        },
        "color_marker": {
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'red',
            'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'green',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'blue'
        }
    },
    # 'es_all_stack': {
    #     "strategies": [
    #         'es_pef_F_etp_F_ueol_F_w_F_nsl_1',
    #         'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 
    #         'sespl_pef_F_etp_F_ueol_F_w_F_nsl_2',
    #     ],
    #     "NAME_TO_LABEL": {
    #         'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'BO (Post)',
    #         'esr_pef_F_etp_F_ueol_F_w_F_nsl_2': 'BO (Post+RBM)',
    #         'sespl_pef_F_etp_F_ueol_F_w_F_nsl_2': 'BO (Post+RBS)', 
    #     },
    #     "color_marker": {
    #         'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'red',
    #         'esr_pef_F_etp_F_ueol_F_w_F_nsl_2': 'green',
    #         'sespl_pef_F_etp_F_ueol_F_w_F_nsl_2': 'blue'
    #     }
    # },
    
    # 'eih_1_pef': {
    #     "strategies": [
    #         'eih_pef_F_etp_F_ueol_F_w_T_nsl_1',
    #         'eih_pef_T_etp_F_ueol_F_w_T_nsl_1', 
    #         # 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1',
    #     ],
    #     "NAME_TO_LABEL": {
    #         'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'iEBO',
    #         'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': "iEBO (Post)", 
    #         # 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1': 'iEBO (Post)', 
    #     },
    #     "color_marker": {
    #         'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'red',
    #         'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'green',
    #         # 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1': 'blue'
    #     }
    # },
    'eih_1_etp': {
        "strategies": [
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1', 
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1',
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1',
        ],
        "NAME_TO_LABEL": {
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'iEBO (Post)',
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'iEBO',
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'iEBO (Post+Trad)', 
        },
        "color_marker": {
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'red',
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'green',
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'blue'
        }
    },
    'es_1_etp': {
        "strategies": [
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
            # 'eih_pef_T_etp_F_ueol_F_w_T_nsl_1',
        ],
        "NAME_TO_LABEL": {
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'BO (Post)',
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'BO (Post+Trad)',
            # 'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'iEBO (post-hoc ensemble)', 
        },
        "color_marker": {
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'red',
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'green',
        }
    },
    'nsl_1': {
        "strategies": [
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1', 
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1'
        ],
        "NAME_TO_LABEL": {
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'iEBO (Post+Trad)',
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'BO (Post+Trad)',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post+Trad)'
        },
        "color_marker": {
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'red',
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'green',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'blue'
        }
    },
    'nsl_1_post': {
        "strategies": [
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1', 
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1',
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1', 
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1',
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1'
        ],
        "NAME_TO_LABEL": {
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': "iEBO", 
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': "EBO",
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'iEBO (Post)',
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'BO (Post)',
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'EBO (Post)'
        },
        "color_marker": {
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': "brown",
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': "black",
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'red',
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'green',
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'blue'
        }
    },
    'nsl_1_post+trad': {
        "strategies": [
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1', 
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1',
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1',
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1', 
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1'
        ],
        "NAME_TO_LABEL": {
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': "iEBO (Post)", 
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1': "BO (Post)",
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': "EBO (Post)",
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'iEBO (Post+Trad)',
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'BO (Post+Trad)',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post+Trad)'
        },
        "color_marker": {
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': "brown",
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1': "violet",
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': "black",
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'red',
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'green',
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'blue'
        }
    },
    'ebo_all': {
        "strategies": [
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
            'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2',
            'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post)',
        'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+RBM)',
        'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+RBS)' ,
    },
    "color_marker": {
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'red',
            'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'green',
            'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2': 'blue'
    }
},
# 'ebo_all': {
#         "strategies": [
#             'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
#             'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2',
#             'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2',
#         ],
#     "NAME_TO_LABEL": {
#         'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post+Trad)',
#         'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+Trad+RBM)',
#         'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+Trad+RBS)' ,
#     },
#     "color_marker": {
#             'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'red',
#             'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'green',
#             'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2': 'blue'
#     }
# },
# 'ebo_all': {
#         "strategies": [
#             'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
#             'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2',
#             'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2',
#         ],
#     "NAME_TO_LABEL": {
#         'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post)',
#         'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+RBM)',
#         'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+RBS)' ,
#     },
#     "color_marker": {
#             'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'red',
#             'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'green',
#             'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2': 'blue'
#     }
# },
    'eih_all':{
        "strategies": [
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'iEBO (Post)',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post+RBM)',
        'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post+RBS)' ,
    },
    "color_marker": {
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'red',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'green',
            'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'blue'
    }
    },

    'es_all':{
        "strategies": [
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
            'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'BO (Post)',
        'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+RBM)',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+RBS)' ,
    },
    "color_marker": {
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'red',
            'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'green',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'blue'
    }
    },
    'all_best': {
        "strategies":[
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post)',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post+RBM)',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+RBS)' ,
    },
    "color_marker": {
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'red',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'green',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'blue'
    }
    },
    'all_best_nsl_2': {
        "strategies":[
            'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+RBM)',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post+RBM)',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+RBS)' ,
    },
    "color_marker": {
            'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'red',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'green',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'blue'
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
        'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'BO (Post)' ,
    },
    "color_marker": {
            'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'green',
            'eih_pef_F_etp_F_ueol_F_w_T_nsl_1': 'red',
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'blue'
    }
    },
    'all_base_pef': {
        "strategies":[
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1',
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1',
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1',
        ],
    "NAME_TO_LABEL": {
        'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'EBO (Post)',
        'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'iEBO (Post)',
        'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'BO (Post)' ,
    },
    "color_marker": {
            'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'red',
            'eih_pef_T_etp_F_ueol_F_w_T_nsl_1': 'green',
            'es_pef_F_etp_F_ueol_F_w_F_nsl_1': 'blue'
    }
    },
    'all_base_etp': {
        "strategies":[
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1',
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
        ],
    "NAME_TO_LABEL": {
        'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post+Trad)',
        'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'iEBO (Post+Trad)',
        'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'BO (Post+Trad)',
    },
    "color_marker": {
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'green',
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1': 'blue',
            'es_pef_F_etp_T_ueol_F_w_F_nsl_1': 'red'
    }
    },
    'sft': {
        "strategies":[
            'sft_pef_T_etp_F_ueol_F_w_F_nsl_2',
            'sft_pef_T_etp_T_ueol_F_w_F_nsl_2',
            'sft_pef_F_etp_F_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'sft_pef_T_etp_F_ueol_F_w_F_nsl_2': 'FiSEBO (Post)',
        'sft_pef_T_etp_T_ueol_F_w_F_nsl_2': 'FiSEBO (Post+Trad)',
        'sft_pef_F_etp_F_ueol_F_w_F_nsl_2': 'FiSEBO' ,
    },
    "color_marker": {
            'sft_pef_T_etp_F_ueol_F_w_F_nsl_2': 'red',
            'sft_pef_T_etp_T_ueol_F_w_F_nsl_2': 'green',
            'sft_pef_F_etp_F_ueol_F_w_F_nsl_2': 'blue'
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
        'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post)',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post+RBM)',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+RBS)' ,
        'sft_pef_T_etp_T_ueol_F_w_F_nsl_2': 'FiSEBO (Post+Trad)',
    },
    "color_marker": {
            'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'green',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'blue',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'purple',
            'sft_pef_T_etp_T_ueol_F_w_F_nsl_2': 'red',
    }
    },
    'all_best_repeat_stack': {
        "strategies":[
            'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2',
            'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
            # 'sft_pef_T_etp_T_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+RBS)',
        'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post+RBS)',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+RBS)' ,
        'sft_pef_T_etp_T_ueol_F_w_F_nsl_2': 'FiSEBO (Post+Trad)',
    },
    "color_marker": {
            'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2': 'green',
            'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'blue',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'purple',
            'sft_pef_T_etp_T_ueol_F_w_F_nsl_2': 'red',
    }
    },
    },
    'size_11': {
    'all_best_size_11': {
        "strategies":[
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+Trad+RBM)',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post+Trad+RBM)',
        'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2':  'iEBO (Post+Trad+RBS)',
        'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+Trad+RBM)',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+Trad+RBS)',
    },
    "color_marker": {
        'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'red',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'green',
        'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'blue',
        'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'red',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2':'blue',
    }
},
'all_best_size_11_overfit': {
        "strategies":[
            'sa_pef_F_etp_F_ueol_F_w_F_nsl_2',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
        ],
    "NAME_TO_LABEL": {
        'sa_pef_F_etp_F_ueol_F_w_F_nsl_2': 'Fixed Defaults (AutoGluon)',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post+RBM)',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+RBS)',
    },
    "color_marker": {
        'sa_pef_F_etp_F_ueol_F_w_F_nsl_2': 'green',
        'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'blue',
        'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2':'red',
    }
},
#     'iebo_vs_es_size_11': {
#         "strategies":[
#             'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
#             'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
#             'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
#             'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
#         ],
#     "NAME_TO_LABEL": {
#         'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+Trad+RBM)',
#         'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post+Trad+RBM)',
#         'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2':  'iEBO (Post+Trad+RBS)',
#         'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+Trad+RBM)',
#         'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+Trad+RBS)',
#     },
#     "color_marker": {
#         'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'red',
#         'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'green',
#         'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'blue',
#         'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'red',
#         'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2':'blue',
#     }
# },
#     'all_best_size_11+sa': {
#         "strategies":[
#             'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2',
#             'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
#             'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
#             'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
#             'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
#             'sa_pef_F_etp_F_ueol_F_w_F_nsl_2'
#         ],
#     "NAME_TO_LABEL": {
#         'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+Trad+RBM)',
#         'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post+Trad+RBM)',
#         'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2':  'iEBO (Post+Trad+RBS)',
#         'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+Trad+RBM)',
#         'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+Trad+RBS)',
#         'sa_pef_F_etp_F_ueol_F_w_F_nsl_2': 'Fixed Defaults (AutoGluon)'
#     },
#     "color_marker": {

#         'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'red',
#         'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'green',
#         'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'blue',
#         'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'red',
#         'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2':'blue',
#         'sa_pef_F_etp_F_ueol_F_w_F_nsl_2': 'yellow'
#     }
# },
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
#         'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post+Trad+RBM)',
#         'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'iEBO (Post+Trad+RBM)',
#         'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2':  'iEBO (Post+Trad+RBS)',
#         'esr_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+Trad+RBM)',
#         'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2': 'BO (Post+Trad+RBS)',
#     },
#     "color_marker": {

#         'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'red',
#         'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2': 'green',
#         'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2': 'blue',
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
    'ebo_etp_F_w_F_pef_T_ueol_F': 'red',
    'ebo_etp_T_w_F_pef_T_ueol_F': 'green',
    # 'EBO': {'color': 'violet', 'marker': 'o'},
    # 'iEBO': {'color': 'green', 'marker': 'o'},
    # 'iEBO+RBS': {'color': 'deeppink', 'marker': 'o'},
    # 'iEBO+RBM': {'color': 'grey', 'marker': 'o'},
    # 'HPO+GES': {'color': 'yellow', 'marker': 'o'},
    # 'HPO+GES+RBS': {'color': 'darkmagenta', 'marker': 'o'},
    # 'HPO+GES+RBM': {'color': 'darkblue', 'marker': 'o'},
    # 'FiSEBO': {'color': 'red', 'marker': 'o'},
    # 'AutoGluon': {'color': 'darkred', 'marker': 'o'},
    # '': {'color': 'darkkhaki', 'marker': 'o'},
    # ': {'color': 'darkgreen', 'marker': 'o'},
    # ': {'color': 'gold', 'marker': 'o'},
    # 'reg_cocktails_reproduce_multi-seeded_small': {'color': 'blue', 'marker': 'o'},
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