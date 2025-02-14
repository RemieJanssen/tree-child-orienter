directories, files = glob_wildcards("data/{dir}/{file}.csv")
# directories, files = glob_wildcards("data/leaf_n10_experiment1/{dir}/{file}.csv")
# directories, files = glob_wildcards("data/leaf_n10_experiment1/leaf_n10_reticulation_r2/{dir}/{file}.csv")
paths = [d+"/"+f for d,f in zip(directories, files)]


rule all:
    input:
        ["results/aggregated.csv", "results/aggregated_properties.csv"]

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
        "results/aggregated.csv"
    shell:
        "cat {input} >> results/aggregated.csv"

rule experiment:
    resources:
        runtime_min=3000,
        mem_mb=16000
    threads:
        1
    input:
        "data/{path}.csv"
    output:
        "results_raw/{path}_{algo}"
    shell:
        "python code/experiment.py -f {input} -o {output} -a {wildcards.algo}"

rule aggregate_properties:
    resources:
        runtime_min=10,
        mem_mb=1000
    threads:
        1
    input:
        expand("results_properties/{path}", path=paths)
    output:
        "results/aggregated_properties.csv"
    shell:
        "cat {input} >> results/aggregated_properties.csv"

rule properties:
    resources:
        runtime_min=5,
        mem_mb=2000
    threads:
        1
    input:
        "data/{path}.csv"
    output:
        "results_properties/{path}"
    shell:
        "python code/properties.py -f {input} -o {output}"