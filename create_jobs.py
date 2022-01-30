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
#MSUB -l pmem={int(memory/1000)}gb
#MSUB -N {job_name}
# Now call the program which does the work depending on the job id
source ~/anaconda3/bin/activate reg_cocktails-env
JOBID={job_id}
    """

    return header, ""


def generate_job_file(cluster, experiment_details, file_to_run, save_folder, task_id=1, partition='bosch_cpu-cascadelake',
                      time_limit=(3, 00, 00), memory=6000):
    job_name = f"{task_id}_{experiment_details['seed']}_ensemble_learning"

    python_call = f"python {file_to_run} --task_id {task_id} --wall_time {experiment_details['wall_time']} --epochs {experiment_details['epochs']} --seed {experiment_details['seed']} --nr_workers {experiment_details['nr_workers']}"
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
args = parser.parse_args()
options = vars(args)
print(options)


if __name__ == '__main__':
    task_ids = get_task_ids()
    task_times = get_task_times()
    file_to_run = args.file_name
    save_folder = f'{args.cluster}_search'
    os.makedirs(save_folder, exist_ok=True)
    for (task_id, task_time) in zip(task_ids, task_times):
        experiment_details = dict()
        experiment_details['epochs'] = args.epochs
        experiment_details['nr_workers'] = args.nr_workers
        experiment_details['seed'] = args.seed
        experiment_details['exp_dir'] = args.exp_dir
        experiment_details['wall_time'] = args.wall_time
        experiment_details['func_eval_time'] = task_time
        experiment_details['experiment_name'] = args.experiment_name

        generate_job_file(
            task_id=int(task_id),
            experiment_details=experiment_details,
            memory=args.mem_limit,
            file_to_run=file_to_run,
            save_folder=save_folder,
            time_limit=(1, 5, 0),
            cluster=args.cluster)
