directories, files = glob_wildcards("data/{dir}/{file}.csv")
# directories, files = glob_wildcards("data/leaf_n10_experiment1/{dir}/{file}.csv")
# directories, files = glob_wildcards("data/leaf_n10_experiment1/leaf_n10_reticulation_r2/{dir}/{file}.csv")
paths = [d+"/"+f for d,f in zip(directories, files)]


rule aggregate:
    resources:
        runtime_min=60,
        mem_mb=1000
    threads:
        1
    input:
        expand("results_raw/{path}_{algo}",
               path=paths, algo=["H", "NFPT", "HSP", "HFPT", "N"]) # no HS because it is somehow very slow...
    output:
        "aggregated.txt"
    shell:
        "cat {input} >> results_raw/aggregated.csv"

rule experiment:
    resources:
        runtime_min=600,
        mem_mb=2000
    threads:
        1
    input:
        "data/{path}.csv"
    output:
        "results_raw/{path}_{algo}"
    shell:
        "python code/experiment.py -f {input} -o {output} -a {wildcards.algo}"