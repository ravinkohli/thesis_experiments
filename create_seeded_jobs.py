import pandas as pd
import argparse

import os


def get_slurm_jobfile_template(job_name, env_name, partition='bosch_cpu-cascadelake',
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


def get_nemo_jobfile_template(job_name, env_name, partition='bosch_cpu-cascadelake',
                               time_limit=(3, 00, 00), log_dir='./log', memory=6000, n_cores=10):
    hours = time_limit[0] * 24 + time_limit[1]
    hours = '{:0>2d}'.format(hours)
    minutes = '{:0>2d}'.format(time_limit[2])
    job_id = "(${MOAB_JOBID //[/})"
    header = f"""#!/bin/bash
#MSUB -l walltime={hours}:{minutes}:00
#MSUB -l nodes=1:ppn={n_cores}
#MSUB -l pmem={int(memory/10000)}gb
#MSUB -N {job_name}

# Now call the program which does the work depending on the job id
source ~/anaconda3/bin/activate {env_name}
JOBID={job_id}
    """

    return header, ""


def generate_job_file(experiment_details, file_to_run, save_folder, env_name, task_id=1, partition='bosch_cpu-cascadelake',
                      time_limit=(3, 00, 00), memory=6000, cluster='slurm'):
    job_name = f"{task_id}_{experiment_details['argument']}_{experiment_details['seed']}_autoPyTorch_cocktails"

    python_call = f"python {file_to_run} --task_id {task_id} --wall_time {experiment_details['wall_time']} --epochs {experiment_details['epochs']} --seed {experiment_details['seed']} --updates_reg_cocktails_paper {experiment_details['updates_reg_cocktails_paper']} --nr_workers {experiment_details['nr_workers']}"
    if not experiment_details['is_flag']:
        job_name = f"{job_name}_{experiment_details['arg_value']}"
        python_call = f"{python_call} --{experiment_details['argument']} {experiment_details['arg_value']}"
    else:
        python_call = f"{python_call} --{experiment_details['argument']}"
        if 'command' in experiment_details:
            job_name = f"{job_name}_{experiment_details['arg_value']}"
            python_call = f"{python_call} --{experiment_details['command']} {experiment_details['arg_value']}"
    # func_eval_time = get_increased_task_time(job_name, experiment_details['func_eval_time'])
    exp_dir = os.path.join(experiment_details['exp_dir'], f'{job_name}')
    python_call = f"{python_call} --tmp_dir {exp_dir} --output_dir {exp_dir} --func_eval_time {experiment_details['func_eval_time']} --dataset_compression {experiment_details['dataset_compression']}"
    template_func = get_slurm_jobfile_template if cluster.lower() == 'slurm' else get_nemo_jobfile_template
    header, footer = template_func(job_name=job_name, partition=partition,
                                   time_limit=time_limit, log_dir='./logs',
                                   memory=memory, n_cores=experiment_details['nr_workers'],
                                   env_name=env_name)
    file_ext = 'sh' if cluster.lower() == 'slurm' else 'moab'
    with open(f'./{save_folder}/{job_name}.{file_ext}', 'w') as f:
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
    '--file_to_run',
    type=str,
    default='./cocktails/icml_space_experiment.py',
)
parser.add_argument(
    '--nr_workers',
    type=int,
    default=1,
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
    '--cluster',
    type=str,
    default='nemo',
)
parser.add_argument(
    '--env_name',
    type=str,
    default='reg_cocktails-env',
)
parser.add_argument(
    '--dataset_compression',
    help='whether to use search space updates from the reg cocktails paper',
    default=False,
)
parser.add_argument(
    '--task_ids_file',
    help='which tasks',
    type=str,
    choices=['4days_task_ids', '2days_task_ids', 'task_ids_s_218'],
    default='task_ids_s_218',
)
parser.add_argument(
    '--use_ensemble_opt_loss',
    type=bool,
    default=False
)
parser.add_argument(
    '--num_stacking_layers',
    type=int,
    default=1
)
parser.add_argument(
    '--ensemble_size',
    type=int,
    default=7
)
parser.add_argument(
    '--posthoc_ensemble_fit_stacking_ensemble_optimization',
    type=bool,
    default=False
)
parser.add_argument(
    '--enable_traditional_pipeline',
    type=bool,
    default=False
)
parser.add_argument(
    '--splits',
    type=int,
    default=5,
)
parser.add_argument(
    '--repeats',
    type=int,
    default=2,
)
parser.add_argument(
    '--experiment_name',
    type=str,
    default='stacked_ensemble'
)
args = parser.parse_args()
options = vars(args)
print(options)


if __name__ == '__main__':
    dataset_info = pd.read_csv(f'./{args.task_ids_file}.csv')
    save_folder = 'NEMO_reg_cocktails_paper_reproduce_pytorch_embedding_multiseeded_4days'
    seeds = [364, 438, 444, 875]  # random.sample(range(1000), 4)
    for seed in seeds:
        seed_save_folder = os.path.join(save_folder, f'{seed}')
        os.makedirs(seed_save_folder, exist_ok=True)
        for task_id in dataset_info['Task_id']:
            experiment_details = dict()
            experiment_details['epochs'] = args.epochs
            experiment_details['nr_workers'] = args.nr_workers
            experiment_details['seed'] = seed
            experiment_details['exp_dir'] = args.exp_dir
            experiment_details['wall_time'] = args.wall_time
            experiment_details['func_eval_time'] = args.func_eval_time
            experiment_details['dataset_compression'] = args.dataset_compression

            seconds_in_day = 60 * 60 * 24
            seconds_in_hour = 60 * 60
            seconds_in_minute = 60
            seconds = min(args.wall_time + 12 * seconds_in_hour, 345600)
            days = seconds // seconds_in_day
            hours = (seconds - (days * seconds_in_day)) // seconds_in_hour
            minutes = (seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute

            generate_job_file(task_id=int(task_id),
                                experiment_details=experiment_details,
                                memory=120000,
                                file_to_run=args.file_to_run,
                                save_folder=seed_save_folder,
                                time_limit=(days, hours, minutes),
                                cluster=args.cluster,
                                env_name=args.env_name)
