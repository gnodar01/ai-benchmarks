import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium", layout_file="layouts/explore.grid.json")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell
def _():
    import marimo as mo
    from datasets import load_dataset
    import json
    from pathlib import Path
    import os
    import tomlkit
    from tomlkit import toml_file

    return Path, json, load_dataset, mo, os, toml_file


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Agent Benchmarks

    Most interested in
    * Terminal-Bench (agentic terminal coding)
      - 2.0
    * SWE-Bench (agentic coding)
      - Pro
      - Verified

    Other important-seeming ones
    * Humanity's last exam (Multidisciplinary reasoning)
    * OSWorld-Verified (agentic computer use)
    * ARC-AGI (AGI; Francois Chollet)
    * CyberGym (cybersecurity vulnerability reproduction)
    * GPQA Diamond (graduate-level reasoning)
    * CharXiv Reasoning (visual reasoning)
    * [GDPval](https://arxiv.org/abs/2510.04374) (economically viable tasks)

    Ones I don't think I've heard about
    * [LiveBench](https://livebench.ai/)

    Categories
    * Agent
    * SWE
    * Memory
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## SWE-Bench

    ### Paper highlights

    [SWE-bench: can language models resolve real-world GitHub Issues](https://openreview.net/pdf?id=VTF8yNQM66) (Jimenez, et. al.; ICLR; 2024)

    The [original SWE-bench](https://www.swebench.com/original.html), released in late 2023, tests AI systems' ability to solve GitHub Issues. It is a collection of 2,294 task instances collected by crawling PRs and Issues from 12 popular Python repositories (filtered down from 90,000 by excluding PRs not associated with issues, not associated with a fail-to-pass test outcome before and after the PR is applied, or having a runtime/installation error). A criteria used is that each PR is associated with an issue and modified >= 1 testing-related file. Each instance is put into a Docker image with the commit associated with the PR. Pre-PR, there are failing tests, and post-PR all tests pass.

    > In the real world... Fixing a bug might involve navigating a large repository, understanding the interplay between functions in different files, or spotting a small error in convoluted code. Inspired by this, we introduce SWE-bench, a benchmark that evaluates LMs in a realistic software engineering setting.
    """)
    return


@app.cell
def _(mo):
    mo.image('public/swe-bench_overview.png')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The AI system is given the issue text (both bug reports and feature requests), and must modify the codebase in order to resolve the described issues. The fail-to-pass tests are used to evaluate the modifications and are not given as input. An extension also uses pass-to-pass tests.

    Resolving issues in SWE-bench frequently requires understanding and coordinating changes across multiple functions, classes, and even files simultaneously, calling for models to interact with execution environments, process extremely long contexts and perform complex reasoning that goes far beyond traditional code generation tasks.

    At the time of publishing, the best model on this benchmark was Claude 2, which could solve 1.96% of issues.

    Compared to other benchmarks (esp. at the time):
    * real-world SWE tasks
    * easily extensible corpus of tasks
    * diverse long inputs - issues are typically long and detailed
    * robust evaluation - at least one fail-to-pass test, with 40% having two or more
    * wide scope for possible solutions
    """)
    return


@app.cell
def _(mo):
    mo.image('public/swe-bench_repo-dist.png')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Retrieval-based approach

    SWE-bench instances provide an issue description and a codebase as input to the model. While issue descriptions are usually short, codebases consist of many more tokens (438K lines on average) than can typically be fit into an LMs context window. To rank and select appropriate files to insert into the context, a retrieval system was used with two context settings:
    1) Sparse retrieval. BM25 (Robertson et L., 2009) retrieval: a ranking function used in search systems.
    2) "Oracle retrieval". Files edited by the reference patch are retrieved. Less realistic since an engineer wouldn't have this information given to them, and limiting since there are other untouched files that are still relevant to understanding the full context of the issue.

    In 40% of instances, BM25 retrieves a superset of the oracle files. In almost half of instances, it retrieves none of the oracle files.

    ### SWE-Bench Variants

    #### SWE-bench Lite

    [SWE-bench lite](https://www.swebench.com/lite.html) is a smaller, carefully selected subset of 300 tasks from the full benchmark. Selected to preserve the distribution and difficulty spectrum of the original benchmark while focusing on more self-contained, functional bug fixes.

    Removed instances:
    * with images, external hyperlinks, references to specific commit SHAs, PRs or issues
    * with fewer than 40 words in problem statement
    * that edited more than 1 file
    * where the gold patch has more than 3 edit hunks
    * that create or remove files
    * that contain tests with error message checks

    Claude-2 resolves a little over 3% of issues.

    #### SWE-bench Verified

    [SWE-bench verified](https://www.swebench.com/verified.html) is a human-filtered subset of 500 instances from SWE-bench in [collab with OpenAI](https://openai.com/index/introducing-swe-bench-verified/). Human annotators reviewed each instance to ensure the problem descriptions are clear, the test patches correct, and the tasks are solvable given the available information.

    The instances are also categorized into difficulty categories from 'easy' (196 <15-minute fix tasks) to 'hard' (45 >1-hour tasks).

    The verified leaderboard features results from a wide variety of AI coding systems, from simple LM agent loops to RAG systems to multi-rollout and review type systems.

    For apples-to-apples comparison of LMs, all LMs use [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) in a minimal BASH environment. No tools, no special scaffold structure. Only a simple [ReAct](https://arxiv.org/abs/2210.03629) agent loop.

    #### SWE-bench Multimodal

    [SWE-bench multimodal](https://www.swebench.com/multimodal.html) is an extension to the original benchmark with 517 issues containing visual elements such as:
    * Screenshots of bugs or interface issues
    * Design mockups or wireframes
    * Diagrams explaining desired functionality
    * Error messages with visual context

    Introduced in [SWE-bench Multimodal: Do AI systems generalize to visual software domains](https://arxiv.org/pdf/2410.03859) (Yang et al., 2024), it adds popular user-facing JavaScript repos and issues that contain a visual aspect such as mapping, plotting, or syntax highlighting.

    #### SWE-bench Multilingual

    [SWE-bench multilingual](https://www.swebench.com/multilingual.html) extends SWE-bench to evaluate LMs across 9 programming languages: C (30), C++ (12), Go (42), Java (43), JS/TS (43), PHP (43), Ruby (44), Rust (43). It consists of 300 curated tasks across 42 repos.

    #### Konwinski Prize

    The [Konwinski Prize](https://www.kaggle.com/competitions/konwinski-prize) offered $1 million for the first team that developed an agent that will solves 90% of issues in an independently developed SWE-bench dataset collected after freezing submissions. It is a contamination-free leaderboard where models (likely) could not have been trained on the issues collected. The submission window as Dec 11, 2024 - Mar 12, 2025. The competition ended on July 9, 2025. The [top team](https://www.kaggle.com/competitions/konwinski-prize/writeups/eduardo-rocha-de-andrade-1st-place-solution-write-) trained a model which resolved [8%](https://www.kaggle.com/competitions/konwinski-prize/discussion/609204) of tasks.
    """)
    return


@app.cell
def _(load_dataset):
    sbv = load_dataset('SWE-bench/SWE-bench_Verified', split='test')
    return (sbv,)


@app.cell
def _(sbv):
    sbv.num_rows
    return


@app.cell
def _(sbv):
    sbv.features
    return


@app.cell
def _(sbv):
    sb_by_difficulty = dict()

    for i in range(len(sbv)):
        cat = sbv[i]['difficulty']
        if cat in sb_by_difficulty:
            sb_by_difficulty[cat].append(sbv[i])
        else:
            print(f"adding diff level: {cat}")
            sb_by_difficulty[cat] = [sbv[i]]

    SB_MED_EASY, SB_MED_HARD, SB_EASY, SB_HARD = tuple(sb_by_difficulty.keys())
    return SB_EASY, SB_HARD, SB_MED_EASY, SB_MED_HARD, sb_by_difficulty


@app.cell
def _(SB_EASY, SB_HARD, SB_MED_EASY, SB_MED_HARD, sb_by_difficulty):
    len(sb_by_difficulty[SB_EASY]), len(sb_by_difficulty[SB_MED_EASY]), len(sb_by_difficulty[SB_MED_HARD]), len(sb_by_difficulty[SB_HARD])
    return


@app.cell
def _(sbv):
    repos = set([sbv[i]['repo'] for i in range(len(sbv))])
    print('\n'.join(repos))
    return


@app.cell
def _(json, mo):
    def esc(s, noop=False):
        if noop:
            return s
        else:
            return s.replace('"', "'")

    def sb_md(instance):
        if instance is None:
            return ""
        return mo.md(
            f"""
    # Meta

    Repo: [{instance['repo']}](https://github.com/{instance['repo']})

    Instance Id: {instance['instance_id']}

    Created at: {instance['created_at']}

    Version: {instance['version']}

    Difficulty: {instance['difficulty']}

    # Tests

    Fail-to-Pass Tests:

    * {'\n* '.join(json.loads(instance['FAIL_TO_PASS']))}

    Num Pass-to-Pass: {len(json.loads(instance['PASS_TO_PASS']))}

    # GH Links

    * [base commit - {instance['base_commit']}](https://github.com/{instance['repo']}/commit/{instance['base_commit']})
    * [env setup commit - {instance['environment_setup_commit']}](https://github.com/{instance['repo']}/commit/{instance['environment_setup_commit']})

    # Problem Statement

    {instance['problem_statement']}

    # Hints Text

    {instance['hints_text']}

    # Patch

    ```python
    {'\n'.join(esc(instance['patch']).split('\n')[0:])}
    ```

    # Test Patch

    ```python
    {'\n'.join(esc(instance['test_patch']).split('\n')[0:])}
    ```
            """
        )

    return (sb_md,)


@app.cell
def _():
    # sb_md(sb_by_difficulty[SB_EASY][0])
    return


@app.cell
def _():
    # sb_md(sb_by_difficulty[SB_MED_EASY][0])
    return


@app.cell
def _():
    # sb_md(sb_by_difficulty[SB_MED_HARD][0])
    return


@app.cell
def _():
    # sb_md(sb_by_difficulty[SB_HARD][0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Terminal-bench

    ### Paper highlights

    Formerly called cli-bench, with [initial commit](https://github.com/harbor-framework/terminal-bench/commits/main/?after=1a6ffa9674b571da0ed040c470cb40c4d85f9b9b+890) on Jan 17, 2025, then T-bench, [then](https://github.com/harbor-framework/terminal-bench/commit/88387bef42a3f56b7241fdd30ba3b56daf2f8c87) terminus, then [a day later](https://github.com/harbor-framework/terminal-bench/commit/b099cd498965b729bb0e4a24673919c7057182c0) on May 19, 2025 to Terminal-bench.

    [Terminal-bench: benchmarking agents on hard, realistic tasks in command line interfaces](https://arxiv.org/pdf/2601.11868) (Merrill et al., 2026; arXiv)

    > Current benchmarks either do not measure real-world tasks, or are not sufficiently difficult to meaningfully measure frontier models. To this end, we present Terminal-Bench 2.0: a carefully curated hard benchmark composed of 89 tasks in computer terminal environments inspired by problems from real workflows. Each task features a unique environment, human written solution, and comprehensive tests for verification.

    A Terminal-Bench task consists of an instruction, a Docker image, a set of tests, an example solution, and a time limit. The tests do not test the agent’s commands or console output, as Terminal-bench is an *outcome-driven* framework where agents are free to accomplish the task using a variety of approaches.
    """)
    return


@app.cell
def _(mo):
    mo.image('public/terminal-bench_overview.png')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Tasks

    Tasks are interactive. Within the bounds of the Docker environment the agent must explore and manipulate the environment by calling tools.

    Terminal-bench 2.0 contains a diverse range of tasks which are crowd-sourced through open-source contributions. 93 contributors created 229 tasks, of which 89 were selected for inclusion based on the difficulty and quality assessments made by three experienced human reviewers.

    Each task has an oracle solution. Task authors proved a guess on how long they think a junior SWE with little familiarity with the topic would take to complete the task, called the "junior time estimate", and how long a domain expert would require, called the "expert time estimate". Authors also reported a high-level category for each task (SWE, Sys Admin, Data Science, Security, Scientific Computing, File Operations, Debugging, Data Processing, Model Training, Mathematics, Machine Learning, Games, Video Processing, Data Querying, Optimization, Personal Assistant).

    #### Terminus 2

    Because Terminal-Bench is an interactive framework, agent and model performance are hard to decouple. Many agent scaffolds have been engineered to accommodate the tendencies of certain models, especially when the model and agent are developed by the same organization. Additionally, despite the name, agents are not explicitly required to use a terminal as their sole tool. Instead, they are free to manipulate the container however they please.

    Many agents are installed directly into the container by a package manager and wield tools that are actually executable programs, far more complex than a typical Bash command. To account for the constraints and biases of most agents, and to remain true to the benchmark’s premise, a simple scaffold, Terminus 2, was created to serve as a neutral testbed for comparing model performance. Terminus 2 has a single tool, a headless terminal, and completes tasks using only Bash commands.

    #### Harbor

    Tasks are specified in the [Harbor task format](https://www.harborframework.com/docs/tasks) and are run in the [Harbor harness](https://www.harborframework.com/docs), which supports multiple popular agents like Claude Code, Codex CLI, Mine-SWE-Agent (SWE-bench's agent) and Terminus 2 (Terminal-bench's agent). Terminal-bench is distributed via the [Harbor registry](https://hub.harborframework.com/).

    ```
    | instruction.md
    | task.toml
    | environment
    |     Dockerfile
    |     ...
    | solution
    |     solve.sh
    |     ...
    | tests
    |     test.sh
    |     ...
    ```

    #### Resuls

    At time of publishing, Codex CLI paired with GPT-5.2 achieves the highest average resolution rate of 63%, followed by Terminus 2 with Claude Opus 4.5 and Terminus 2 with Gemini 3 Pro at 58% and 57%, respectively. Proprietary models paired with various agents occupy the top 13 positions in the rankings, with Terminus 2 and Kimi K2 Thinking performing best among the open-weight models, resolving 36% of tasks on average.

    Running Terminal-Bench 2.0 costs anywhere from one to a hundred dollars, depending on the model’s price. Tasks usually take less than 20 minutes for most models, though a rare few take up to two hours with hundreds of API calls and almost 100 million tokens.
    """)
    return


@app.cell
def _(mo):
    mo.image('public/terminal-bench_difficulty.png')
    return


@app.cell
def _(Path, os, toml_file):
    tb_path = Path('terminal-bench-2')
    task_paths = [Path(tb_path / d) for d in os.listdir(tb_path) if os.path.isdir(tb_path / d)]
    task_defs = {pth: toml_file.TOMLFile(pth / 'task.toml').read() for pth in task_paths}
    return (task_defs,)


@app.cell
def _(task_defs):
    tb_by_difficulty = dict()

    for k,v in task_defs.items():
        tb_diff = v['metadata']['difficulty']
        if tb_diff in tb_by_difficulty:
            tb_by_difficulty[tb_diff].append({'path': k, 'def': v})
        else:
            tb_by_difficulty[tb_diff] = [{'path': k, 'def': v}]
    return (tb_by_difficulty,)


@app.cell
def _(tb_by_difficulty):
    TB_HARD, TB_MED, TB_EASY = tuple(tb_by_difficulty.keys())
    return TB_EASY, TB_HARD, TB_MED


@app.cell
def _(TB_EASY, TB_HARD, TB_MED, tb_by_difficulty):
    len(tb_by_difficulty[TB_HARD]), len(tb_by_difficulty[TB_MED]), len(tb_by_difficulty[TB_EASY])
    return


@app.cell
def _(mo, os):
    def all_files_md(pth, first):
        res = ""
        first_contents = (pth / first).read_text()
        res += f"## {str(first)}\n\n"
        res += f"```\n{first_contents}\n```\n"
        rest = [x for x in os.listdir(pth) if x != first and os.path.isfile(x)]
        for file in rest:
            file_contents = (pth / file).read_text()
            res += f"## {str(file)}\n\n"
            res += f"\n```\n{file_contents}\n```\n"
        return res
    

    def tb_md(instance):
        if instance is None:
            return ""
        task_pth = instance['path']
        task_def = instance['def']
        task_instructions = (task_pth / 'instruction.md').read_text()
        env_pth = task_pth / 'environment'
        readme = (task_pth / 'README.md').read_text()
        sol_pth = task_pth / 'solution'
        tst_pth = task_pth / 'tests'
    
        return mo.md(f"""
    # Meta

    Task Name: {task_def['task']['name']}

    Task Description: {task_def['task']['description']}

    Task Keywords:
    * {'\n* '.join(task_def['task']['keywords'])}

    Category: Difficulty: {task_def['metadata']['category']}

    Difficulty: {task_def['metadata']['difficulty']}

    Expert Time Min Estimate: {task_def['metadata']['expert_time_estimate_min']}

    Junior Time Min Estimate: {task_def['metadata']['junior_time_estimate_min']}

    ---

    # README

    {readme}

    ---

    # Environment

    Files:

    * {'\n* '.join(os.listdir(env_pth))}

    {all_files_md(env_pth, 'Dockerfile')}

    # Instructions

    {task_instructions}

    # Solution

    Files:

    * {'\n* '.join(os.listdir(sol_pth))}

    {all_files_md(sol_pth, 'solve.sh')}

    # Tests

    Files:

    * {'\n* '.join(os.listdir(tst_pth))}

    {all_files_md(tst_pth, 'test.sh')}
        """)

    return (tb_md,)


@app.cell
def _():
    # tb_md(tb_by_difficulty[TB_EASY][0])
    return


@app.cell
def _():
    # tb_md(tb_by_difficulty[TB_MED][0])
    return


@app.cell
def _():
    # tb_md(tb_by_difficulty[TB_HARD][0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Upcoming

    #### Terminal-bench 3.0

    There is an open call for contributions for [terminal-bench 3.0](https://www.tbench.ai/news/tb3-contribution-call). The goal is to have 100 diverse tasks targeting at most 30% solve rate from the best models at time of release. Broadly they desire tasks that are longer-horizon, need richer environments, and require specialized expertise.

    While terminal-bench 2.0 covers SWE, sys-admin, security, and scientific computing; terminal-bench 3.0 is expanding to a wider variety of domains, so long as they are realistic and accomplished via CLI.

    ### Terminal-bench-science

    The goal of [terminal-bench-science](https://www.tbench.ai/news/tb-science-announcement) (TB-science) is to extend into complex real-world computational workflows that natural scientists run in their research labs.

    The claim is that current "AI for science" benchmarks test textbook knowledge or abstrac capabilities like hypothesis generation, rather than measuring whether an AI system can execute the end-to-end computational workflows that drive modern research. TB-science plans to port real workflows from leading research labs into executable benchmark tasks, evaluated in containerized environments with determenistic, programmatic verification.

    There will be an open contribution call in Q2 2026.
    """)
    return


@app.cell
def _(mo):
    SB_SELECT = 'SWE-BENCH'
    TB_SELECT = 'TERMINAL-BENCH'

    benchmark_select = mo.ui.dropdown([SB_SELECT, TB_SELECT])
    return SB_SELECT, TB_SELECT, benchmark_select


@app.cell
def _(
    SB_SELECT,
    TB_SELECT,
    benchmark_select,
    mo,
    sb_by_difficulty,
    tb_by_difficulty,
):
    cats = {
        SB_SELECT: list(map(str, sb_by_difficulty.keys())),
        TB_SELECT: list(map(str, tb_by_difficulty.keys())),
        None: []
    }[benchmark_select.value]

    diff_cat_select = mo.ui.dropdown(cats)
    return (diff_cat_select,)


@app.cell
def _(
    SB_SELECT,
    TB_SELECT,
    benchmark_select,
    sb_by_difficulty,
    tb_by_difficulty,
):
    by_difficulty = {
        SB_SELECT: dict({None: [None]}, **sb_by_difficulty),
        TB_SELECT: dict({None: [None]}, **tb_by_difficulty),
        None: {None: [None]}
    }[benchmark_select.value]
    return (by_difficulty,)


@app.cell
def _(by_difficulty, diff_cat_select, mo):
    instance_idx_select = mo.ui.slider(start=0, stop=len(by_difficulty[diff_cat_select.value]), step=1, debounce=True, show_value=True)
    return (instance_idx_select,)


@app.cell
def _(SB_SELECT, TB_SELECT, benchmark_select, sb_md, tb_md):
    md_gen_fn = {
        SB_SELECT: sb_md,
        TB_SELECT: tb_md,
        None: (lambda x: None)
    }[benchmark_select.value]
    return (md_gen_fn,)


@app.cell
def _(benchmark_select, diff_cat_select, instance_idx_select, mo):
    mo.md(f"""
    Select a Benchmark: {benchmark_select}

    Select a difficulty category: {diff_cat_select}

    Select a task id: {instance_idx_select}
    """)
    return


@app.cell
def _(by_difficulty, diff_cat_select, instance_idx_select, md_gen_fn):
    md_gen_fn(by_difficulty[diff_cat_select.value][instance_idx_select.value])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
