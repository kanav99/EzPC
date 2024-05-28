import os

benchmarks = [
    'bert-tiny',
    'bert-base',
    'bert-large',
    'gpt2',
    'gptneo'
]

os.system('make ' + ' '.join(benchmarks))
