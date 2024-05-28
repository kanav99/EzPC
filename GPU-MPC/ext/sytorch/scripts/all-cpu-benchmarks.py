import subprocess
import csv

mute = False

benchmarks = [
    'bert-tiny',
    # 'bert-base',
    # 'bert-large',
    # 'gpt2',
    # 'gptneo'
]

def run_seq(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p.wait()


def run_par(cmd1, cmd2):
    p1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p1.wait()
    p2.wait()

for b in benchmarks:
    print("[+] benchmarking " + b)
    print("[+] --- compiling...")
    run_seq('make benchmark-' + b)
    print("[+] --- running dealer...")
    run_seq(f'./benchmark-{b} 1')
    print("[+] --- running online phase...")
    run_par(f'OMP_NUM_THREADS=4 ./benchmark-{b} 2', f'OMP_NUM_THREADS=4 ./benchmark-{b} 3')

    total_time = 0.0
    total_comm = 0.0
    act_time = 0.0
    act_comm = 0.0
    softmax_time = 0.0
    softmax_comm = 0.0
    norm_time = 0.0
    norm_comm = 0.0
    with open('llama3.csv') as f:
        csvFile = csv.reader(f)
        for lines in csvFile:
            if rows[0].startswith('GeLU::'):
                act_time += float(rows[1])
                act_comm += float(rows[2])
            elif rows[0].startswith('LayerNorm::'):
                norm_time += float(rows[1])
                norm_comm += float(rows[2])
            elif rows[0].startswith('nExp::'):
                softmax_time += float(rows[1])
                softmax_comm += float(rows[2])
            elif rows[0].startswith('Softmax::'):
                softmax_time += float(rows[1])
                softmax_comm += float(rows[2])
            total_time += float(rows[1])
            total_comm += float(rows[2])
    print("[+] --- online time = " + str(total_time/1000.0) + " s")
    print("[+] --- online comm = " + str(total_comm/1024.0) + " GB")

