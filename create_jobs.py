import argparse
import os
from dataset_collection import get_task_ids, get_task_times

def get_slurm_jobfile_template(job_name, partition='bosch_cpu-cascadelake',
                               time_limit=(3, 00, 00), log_dir='./log', memory=6000, n_cores=10):
    hours = '{:0>2d}'.format(time_limit[1])
    minutes = '{:0>2d}'.format(time_limit[2])
    header = f"""#!/bin/bash
#SBATCH -p {partition} # partition (queue)
#SBATCH --mem {memory} # memory pool for all cores (4GB)
#SBATCH -t {time_limit[0]}-{hours}:{minutes} # time (D-HH:MM)
#SBATCH -c {n_cores} # number of cores
#SBATCH -o {log_dir}/%x.%N.%j.out # STDOUT  (the folder log has to be created prior to running or this won't work)
#SBATCH -e {log_dir}/%x.%N.%j.err # STDERR  (the folder log has to be created prior to running or this won't work)
#SBATCH -J {job_name} # sets the job name. If not specified, the file name will be used as job name
#SBATCH --mail-type=END,FAIL # (recive mails about end and timeouts/crashes of your job)
# Print some information about the job to STDOUT
echo \"Workingdir: $PWD\";
echo \"Started at $(date)\";
echo \"Running job $SLURM_JOB_NAME using $SLURM_JOB_CPUS_PER_NODE cpus per node with given JID $SLURM_JOB_ID on queue $SLURM_JOB_PARTITION\";
            """
    footer = """exit $?
# Print some Information about the end-time to STDOUT
echo "DONE";
echo "Finished at $(date)";
"""
    return header, footer


def get_nemo_jobfile_template(job_name, partition='bosch_cpu-cascadelake',
                               time_limit=(3, 00, 00), log_dir='./log', memory=6000, n_cores=10):
    hours = time_limit[0] * 24 + time_limit[1]
    hours = '{:0>2d}'.format(hours)
    minutes = '{:0>2d}'.format(time_limit[2])
    job_id = "(${MOAB_JOBID //[/})"
    header = f"""#!/bin/bash
#MSUB -l walltime={hours}:{minutes}:00
#MSUB -l nodes={n_cores}:ppn=1
#MSUB -l pmem={int((memory/1000)*1.25)}gb
#MSUB -N {job_name}
# Now call the program which does the work depending on the job id
source ~/anaconda3/bin/activate thesis_exp-env
JOBID={job_id}
    """

    return header, ""


def generate_job_file(cluster, experiment_details, file_to_run, save_folder, task_id=1, partition='bosch_cpu-cascadelake',
                      time_limit=(3, 00, 00), memory=6000):
    job_name = f"{task_id}_{experiment_details['seed']}_{experiment_details['experiment_name']}"

    python_call = f"python {file_to_run} --task_id {task_id} --wall_time {experiment_details['wall_time']} --min_budget {experiment_details['min_budget']} --max_budget {experiment_details['max_budget']} --seed {experiment_details['seed']} --nr_workers {experiment_details['nr_workers']}"
    exp_dir = os.path.join(experiment_details['exp_dir'], f'{job_name}')
    python_call = f"{python_call} --tmp_dir {exp_dir} --output_dir {exp_dir} --func_eval_time {experiment_details['func_eval_time']} --experiment_name {experiment_details['experiment_name']}"
    template_func = get_slurm_jobfile_template if cluster.lower() == 'slurm' else get_nemo_jobfile_template
    header, footer = template_func(job_name=job_name, partition=partition,
                                   time_limit=time_limit, log_dir='./logs',
                                   memory=memory, n_cores=experiment_details['nr_workers'])
    with open(f'./{save_folder}/{job_name}.moab', 'w') as f:
        f.write(header)
        f.write(f"""
{python_call}\n\n""")
        f.write(footer)


parser = argparse.ArgumentParser(
    description='Run autoPyTorch on a benchmark'
)
parser.add_argument(
    '--epochs',
    type=int,
    default=105,
)
parser.add_argument(
    '--seed',
    type=int,
    default=11,
)
parser.add_argument(
    '--exp_dir',
    type=str,
    default='./runs/autoPyTorch_cocktails',
)
parser.add_argument(
    '--nr_workers',
    type=int,
    default=10,
)
parser.add_argument(
    '--wall_time',
    type=int,
    default=600,
)
parser.add_argument(
    '--func_eval_time',
    type=int,
    default=100800,
)
parser.add_argument(
    '--mem_limit',
    type=int,
    default=4000,
)
parser.add_argument(
    '--cluster',
    type=str,
    default='NEMO',
)
parser.add_argument(
    '--experiment_name',
    type=str,
    default='stacked_ensemble'
)
parser.add_argument(
    '--file_name',
    type=str,
    default='run_dataset.py'
)
parser.add_argument(
    '--min_budget',
    type=float,
    default=12.5,
)
parser.add_argument(
    '--max_budget',
    type=float,
    default=50,
)
args = parser.parse_args()
options = vars(args)
print(options)


if __name__ == '__main__':
    task_ids = get_task_ids()
    # task_times = get_task_times()
    file_to_run = args.file_name
    save_folder = f'{args.cluster}_search_{args.experiment_name}'
    os.makedirs(save_folder, exist_ok=True)
    for task_id in task_ids: # for (task_id, task_time) in zip(task_ids, task_times):
        experiment_details = dict()
        experiment_details['min_budget'] = args.min_budget
        experiment_details['max_budget'] = args.max_budget
        experiment_details['nr_workers'] = args.nr_workers
        experiment_details['seed'] = args.seed
        experiment_details['exp_dir'] = os.path.join(args.exp_dir, args.experiment_name)
        experiment_details['wall_time'] = args.wall_time
        experiment_details['func_eval_time'] = 126000
        experiment_details['experiment_name'] = args.experiment_name

        generate_job_file(
            task_id=int(task_id),
            experiment_details=experiment_details,
            memory=args.mem_limit,
            file_to_run=file_to_run,
            save_folder=save_folder,
            time_limit=(4, 0, 0),
            cluster=args.cluster)

14888060,14888139,14888140,14888141,14888142,14888143,14888144,14888145,14888146,14888147,14888148,14888149,14888150,14888151,14888152,14888153,14888154,14888155,14888156,14888158,14888159,14888160,14888161,14888162,14888163,14888164,14888165,14888166,14888167,14888168,14888169,14888170,14888171,14888172,14888173,14888174,14888175,14888177,14888178,14888179,14888180,14888181,14888182,14888183,14888184,14888185,14888186,14888187,14888188,14888189,14888190,14888191,14888192,14888193,14888194,14888195,14888197,14888198,14888199,14888200,14888201,14888202,14888203,14888204,14888205,14888206,14888207,14888208,14888209,14888210,14888138,14888211,14888216,14888217,14888218,14888219,14888220,14888221,14888222,14888223,14888224,14888225,14888226,14888227,14888228,14888229,14888230,14888231,14888232,14888233,14888235,14888236,14888237,14888238,14888239,14888240,14888241,14888242,14888243,14888244,14888245,14888246,14888247,14888248,14888249,14888250,14888251,14888252,14888254,14888255,14888256,14888257,14888258,14888259,14888260,14888261,14888262,14888263,14888264,14888265,14888266,14888267,14888268,14888269,14888270,14888271,14888272,14888274,14888275,14888276,14888277,14888278,14888279,14888280,14888281,14888282,14888283,14888284,14888285,14888286,14888287,14888289,14888290,14888291,14888292,14888293,14888294,14888295,14888296,14888297,14888298,14888299,14888300,14888301,14888302,14888303,14888304,14888305,14888306,14888307,14888309,14888310,14888311,14888312,14888313,14888314,14888315,14888316,14888317,14888318,14888319,14888320,14888321,14888322,14888323,14888324,14888325,14888326,14888328,14888329,14888330,14888331,14888332,14888333,14888334,14888335,14888336,14888337,14888338,14888339,14888340,14888341,14888342,14888343,14888344,14888345,14888346,14888348,14888349,14888350,14888351,14888352,14888353,14888354,14888355,14888356,14888357,14888358,14888359,14888360,14888361,14888363,14888364,14888365,14888366,14888367,14888368,14888369,14888370,14888371,14888372,14888373,14888374,14888375,14888376,14888377,14888378,14888379,14888380,14888382,14888383,14888384,14888385,14888386,14888387,14888388,14888389,14888390,14888391,14888392,14888393,14888394,14888395,14888396,14888397,14888398,14888399,14888400,14888402,14888403,14888404,14888405,14888406,14888407,14888408,14888409,14888410,14888411,14888412,14888413,14888414,14888415,14888416,14888417,14888418,14888419,14888421,14888422,14888423,14888424,14888425,14888426,14888427,14888428,14888429,14888430,14888431,14888432,14888433,14888434,14888436,14888437,14888438,14888439,14888440,14888441,14888442,14888443,14888444,14888445,14888446,14888447,14888448,14888449,14888450,14888451,14888452,14888453,14888455,14888456,14888457,14888458,14888459,14888460,14888461,14888462,14888463,14888464,14888465,14888466,14888467,14888468,14888469,14888470,14888471,14888472,14888473,14888475,14888476,14888477,14888478,14888479,14888480,14888481,14888482,14888483,14888484,14888485,14888486,14888487,14888488,14888489,14888490,14888491,14888492,14888494,14888495,14888496,14888497,14888498,14888499,14888500,14888501,14888502,14888503,14888504,14888505,14888506,14888510,14888511,14888512,14888513,14888514,14888515,14888516,14888517,14888518,14888519,14888520,14888521,14888522,14888523,14888524,14888525,14888526,14888527,14888529,14888530,14888531,14888532,14888533,14888534,14888535,14888536,14888537,14888538,14888539,14888540,14888541,14888542,14888543,14888544,14888545,14888546,14888547,14888548,14888550,14888551,14888552,14888553,14888554,14888555,14888556,14888557,14888558,14888559,14888560,14888561,14888562,14888563,14888564,14888565,14888566,14888567,14888568,14888569,14888570,14888572,14888573,14888574,14888575,14888576,14888577,14888578,14888579,14888580,14888581,14888582,14888583,14888584,14888507,14888585,14888642,14888643,14888645,14888646,14888647,14888648,14888587,14888588,14888589,14888590,14888591,14888592,14888593,14888594,14888595,14888596,14888597,14888598,14888599,14888600,14888601,14888602,14888603,14888604,14888606,14888607,14888608,14888609,14888610,14888611,14888612,14888613,14888614,14888615,14888616,14888617,14888618,14888619,14888620,14888621,14888622,14888623,14888624,14888626,14888627,14888628,14888629,14888630,14888631,14888632,14888633,14888634,14888635,14888636,14888637,14888638,14888639,14888640,14888641,