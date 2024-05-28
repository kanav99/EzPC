import os

mute = False

benchmarks = [
    'bert-tiny',
    # 'bert-base',
    # 'bert-large',
    # 'gpt2',
    # 'gptneo'
]

for b in benchmarks:
    print("[+] benchmarking " + b)
    print("[+] compiling...")
    os.system('make benchmark-' + b)
    print("[+] running dealer...")
    os.system(f'./benchmark-{b} 1 &> /dev/null')

