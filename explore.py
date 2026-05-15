import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium", layout_file="layouts/explore.slides.json")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Agent Benchmarks
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Covered here:
    * Terminal-Bench (agentic terminal coding)
    * SWE-Bench (agentic coding)

    Other important/interesting-seeming ones
    * [Humanity's last exam](https://lastexam.ai/) (AGI; Multidisciplinary reasoning)
    * [OSWorld](https://os-world.github.io/) / [OSWorld-Verified](https://xlang.ai/blog/osworld-verified) (agentic computer use)
    * [ARC-AGI-3](https://arcprize.org/arc-agi/3) (AGI; Francois Chollet)
    * [CyberGym](https://www.cybergym.io/) (cybersecurity)
    * [GPQA](https://github.com/idavidrein/gpqa/) (graduate-level reasoning)
    * [CharXiv Reasoning](https://charxiv.github.io/) (multimodal; visual reasoning)
    * [GDPval](https://openai.com/index/gdpval/) (economically viable tasks)
    * [LiveBench](https://livebench.ai/) (contamination-free)
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


@app.function
def bullets(itr):
    """Util for markdown conversion of iterable to list of bullet points"""
    return f"\n* {'\n* '.join(itr)}"


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## SWE-Bench
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Paper highlights

    [SWE-bench: can language models resolve real-world GitHub Issues](https://openreview.net/pdf?id=VTF8yNQM66) (Jimenez, et. al.; ICLR; 2024)

    > In the real world... Fixing a bug might involve navigating a large repository, understanding the interplay between functions in different files, or spotting a small error in convoluted code. Inspired by this, we introduce SWE-bench, a benchmark that evaluates LMs in a realistic software engineering setting.

    The [original SWE-bench](https://www.swebench.com/original.html), released in late 2023, tests AI systems' ability to solve GitHub Issues.

    * 2,294 task instances
    * scraped PRs and Issues from 12 popular Python repositories
    * filtered down from 90,000
    * PR must have issue
    * must have fail-to-pass test outcome before & after PR applied
    * no runtime/installation error
    """)
    return


@app.cell
def _(mo):
    mo.image('public/swe-bench_repo-dist.png')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    AI system given issue text (both bug reports and feature requests), and must modify the codebase in order to resolve the described issues.
    Fail-to-pass tests are used to evaluate the modifications and are not given as input.
    An extension also uses pass-to-pass tests.

    > Resolving issues in SWE-bench frequently requires understanding and coordinating changes across multiple functions, classes, and even files simultaneously, calling for models to interact with execution environments, process extremely long contexts and perform complex reasoning that goes far beyond traditional code generation tasks.
    """)
    return


@app.cell
def _(mo):
    mo.image('public/swe-bench_overview.png')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    At the time of publishing, the best model on this benchmark was Claude 2, which could solve 1.96% of issues.

    Compared to other benchmarks (esp. at the time):
    * real-world SWE tasks
    * easily extensible corpus of tasks
    * diverse long inputs - issues are typically long and detailed
    * robust evaluation - at least one fail-to-pass test, with 40% having two or more
    * wide scope for possible solutions
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Retrieval-based approach

    SWE-bench instances provided an issue description and codebase as input to the model.

    Codebases consist of many tokens (438K lines on average). More than can fit into an LMs context window.

    To rank & select appropriate files for insertion into context, a retrieval system was used with two context settings:

    1) Sparse retrieval / BM25 (Robertson et L., 2009) retrieval - a ranking function used in search systems.

    In 40% of instances, BM25 retrieves a superset of the oracle files. In almost half of instances, it retrieves none of the oracle files.

    2) "Oracle retrieval" - Files edited by the reference patch are retrieved.

    Oracle Retrieval is less realistic since an engineer wouldn't have this information given to them, and limiting since there are other untouched files that are still relevant to understanding the full context of the issue.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SWE-Bench Variants
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### SWE-bench Verified

    [SWE-bench verified](https://www.swebench.com/verified.html) is a human-filtered subset of 500 instances from SWE-bench in [collab with OpenAI](https://openai.com/index/introducing-swe-bench-verified/).

    * Human annotators reviewed each instance to ensure the problem descriptions are clear, the test patches correct, and the tasks are solvable given the available information.
    * The instances are also categorized into difficulty categories.
    * The verified leaderboard features results from a wide variety of AI coding systems, from simple LM agent loops to RAG systems to multi-rollout and review type systems.

    For apples-to-apples comparison of LMs, all LMs use [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) in a minimal BASH environment. Only a simple [ReAct](https://arxiv.org/abs/2210.03629) agent loop is used. No tools or special scaffold are provided.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### SWE-bench Multimodal

    [SWE-bench multimodal](https://www.swebench.com/multimodal.html) is an extension to the original benchmark with 517 issues containing visual elements such as:
    * Screenshots of bugs or interface issues
    * Design mockups or wireframes
    * Diagrams explaining desired functionality
    * Error messages with visual context

    Introduced in [SWE-bench Multimodal: Do AI systems generalize to visual software domains](https://arxiv.org/pdf/2410.03859) (Yang et al., 2024), it adds popular user-facing JavaScript repos and issues that contain a visual aspect such as mapping, plotting, or syntax highlighting.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### SWE-bench Multilingual

    [SWE-bench multilingual](https://www.swebench.com/multilingual.html) extends SWE-bench to evaluate LMs across 9 programming languages: C (30), C++ (12), Go (42), Java (43), JS/TS (43), PHP (43), Ruby (44), Rust (43). It consists of 300 curated tasks across 42 repos.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Konwinski Prize

    The [Konwinski Prize](https://www.kaggle.com/competitions/konwinski-prize) offered $1 million for the first team that developed an agent that will solves 90% of issues in an independently developed SWE-bench dataset collected after freezing submissions. It is a contamination-free leaderboard where models (likely) could not have been trained on the issues collected. The submission window as Dec 11, 2024 - Mar 12, 2025. The competition ended on July 9, 2025. The [top team](https://www.kaggle.com/competitions/konwinski-prize/writeups/eduardo-rocha-de-andrade-1st-place-solution-write-) trained a model which resolved [8%](https://www.kaggle.com/competitions/konwinski-prize/discussion/609204) of tasks.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SWE-bench Verified Exploration
    """)
    return


@app.cell
def _(load_dataset):
    sbv = load_dataset('SWE-bench/SWE-bench_Verified', split='test')
    return (sbv,)


@app.cell
def _(mo, sbv):
    mo.md(f"""
    There are {sbv.num_rows} task instances
    """)
    return


@app.cell
def _(mo, sbv):
    mo.md(f"""
    Each tasks consists of these features:{bullets(map(lambda f: str(f[0]), sbv.features.items()))}
    """)
    return


@app.cell
def _(mo, sbv):
    sb_by_difficulty = dict()

    for i in range(len(sbv)):
        cat = sbv[i]['difficulty']
        if cat in sb_by_difficulty:
            sb_by_difficulty[cat].append(sbv[i])
        else:
            sb_by_difficulty[cat] = [sbv[i]]

    SB_MED_EASY, SB_MED_HARD, SB_EASY, SB_HARD = tuple(sb_by_difficulty.keys())

    def _():
        num_per_cat = map(
            lambda c: f"{c.replace('>', 'gt ').replace('<', 'lt ')} ({len(sb_by_difficulty[c])})",
            sb_by_difficulty.keys()
        )
        return mo.md(f"Difficulty levels (num instances):{bullets(num_per_cat)}")
    _()
    return (sb_by_difficulty,)


@app.cell
def _(mo, sbv):
    mo.md(f"""
    Repos:{bullets(set([sbv[i]['repo'] for i in range(len(sbv))]))}
    """)
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

    {bullets(json.loads(instance['FAIL_TO_PASS']))}

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

    Formerly called cli-bench, with [initial commit](https://github.com/harbor-framework/terminal-bench/commits/main/?after=1a6ffa9674b571da0ed040c470cb40c4d85f9b9b+890) on Jan 17, 2025, then T-bench, [then](https://github.com/harbor-framework/terminal-bench/commit/88387bef42a3f56b7241fdd30ba3b56daf2f8c87) terminus, then [a day later](https://github.com/harbor-framework/terminal-bench/commit/b099cd498965b729bb0e4a24673919c7057182c0) on May 19, 2025 to Terminal-bench.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Paper highlights

    [Terminal-bench: benchmarking agents on hard, realistic tasks in command line interfaces](https://arxiv.org/pdf/2601.11868) (Merrill et al., 2026; arXiv)

    > Current benchmarks either do not measure real-world tasks, or are not sufficiently difficult to meaningfully measure frontier models. To this end, we present Terminal-Bench 2.0: a carefully curated hard benchmark composed of 89 tasks in computer terminal environments inspired by problems from real workflows. Each task features a unique environment, human written solution, and comprehensive tests for verification.

    A Terminal-Bench task consists of:
    * an instruction
    * a Docker image
    * a set of tests
    * an example solution
    * a time limit.

    The tests do not test the agent’s commands or console output, as Terminal-bench is an *outcome-driven* framework where agents are free to accomplish the task using a variety of approaches.
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

    * interactive - within the bounds of the Docker environment the agent must explore and manipulate the environment by calling tools
    * crowd-sourced through open-source contributions

    93 contributors created 229 tasks, of which 89 were selected for inclusion based on the difficulty and quality assessments made by three experienced human reviewers
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Terminus 2

    Terminus 2 is a simple scaffold created to serve as a neutral testbed for comparing model performance.

    It has a single tool, a headless terminal.

    It completes tasks using only Bash commands.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Selected Results

    At time of publishing, Codex CLI paired with GPT-5.2 achieves the highest average resolution rate of 63%, followed by Terminus 2 with Claude Opus 4.5 and Terminus 2 with Gemini 3 Pro at 58% and 57%, respectively.

    Proprietary models paired with various agents occupy the top 13 positions in the rankings, with Terminus 2 and Kimi K2 Thinking performing best among the open-weight models, resolving 36% of tasks on average.

    Running Terminal-Bench 2.0 costs anywhere from one to a hundred dollars, depending on the model’s price. Tasks usually take less than 20 minutes for most models, though a rare few take up to two hours with hundreds of API calls and almost 100 million tokens.
    """)
    return


@app.cell
def _(mo):
    mo.image('public/terminal-bench_difficulty.png')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Upcoming Variants
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Terminal-bench 3.0

    There is an open call for contributions for [terminal-bench 3.0](https://www.tbench.ai/news/tb3-contribution-call).

    The goal is to have 100 diverse tasks targeting at most 30% solve rate from the best models at time of release.

    Broadly, they desire tasks that are longer-horizon, need richer environments, and require specialized expertise.

    While terminal-bench 2.0 covers SWE, sys-admin, security, and scientific computing; terminal-bench 3.0 is expanding to a wider variety of domains, so long as they are realistic and accomplished via CLI.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Terminal-bench-science

    The goal of [terminal-bench-science](https://www.tbench.ai/news/tb-science-announcement) (TB-science) is to extend into complex real-world computational workflows that natural scientists run in their research labs.

    The claim is that current "AI for science" benchmarks test textbook knowledge or abstrac capabilities like hypothesis generation, rather than measuring whether an AI system can execute the end-to-end computational workflows that drive modern research.

    TB-science plans to port real workflows from leading research labs into executable benchmark tasks, evaluated in containerized environments with determenistic, programmatic verification.

    There will be an open contribution call in Q2 2026.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Terminal-bench 2.0 Exploration
    """)
    return


@app.cell
def _(Path, os, toml_file):
    tb_path = Path('terminal-bench-2')
    task_paths = [Path(tb_path / d) for d in os.listdir(tb_path) if os.path.isdir(tb_path / d)]
    task_defs = {pth: toml_file.TOMLFile(pth / 'task.toml').read() for pth in task_paths}
    return (task_defs,)


@app.cell
def _(mo, task_defs):
    mo.md(f"""
    There are {len(task_defs)} task instances
    """)
    return


@app.cell
def _(mo, task_defs):
    mo.md(f"""
    Unique Tags: {bullets(set([tag for _, v in task_defs.items() for tag in v['metadata']['tags']]))}
    """)
    return


@app.cell
def _(mo, task_defs):
    mo.md(f"""
    Unique Keywords: {bullets(set([kwd for _, v in task_defs.items() for kwd in v['task']['keywords']]))}
    """)
    return


@app.cell
def _(mo, task_defs):
    tb_by_difficulty = dict()

    for k,v in task_defs.items():
        tb_diff = v['metadata']['difficulty']
        if tb_diff in tb_by_difficulty:
            tb_by_difficulty[tb_diff].append({'path': k, 'def': v})
        else:
            tb_by_difficulty[tb_diff] = [{'path': k, 'def': v}]

    TB_HARD, TB_MED, TB_EASY = tuple(tb_by_difficulty.keys())

    def _():
        num_per_cat = map(
            lambda c: f"{c.replace('>', 'gt ').replace('<', 'lt ')} ({len(tb_by_difficulty[c])})",
            tb_by_difficulty.keys()
        )
        return mo.md(f"Difficulty levels (num instances):{bullets(num_per_cat)}")
    _()
    return (tb_by_difficulty,)


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
    {bullets(task_def['task']['keywords'])}

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
    ## Task Explorer
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


if __name__ == "__main__":
    app.run()
