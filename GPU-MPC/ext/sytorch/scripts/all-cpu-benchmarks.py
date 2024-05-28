import subprocess

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

