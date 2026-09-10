from invoke import task


@task
def format(ctx, targets="src tests"):
    print(f"Linting {targets}...")
    try:
        ctx.run(f"ruff check --fix --quiet {targets}")
    except Exception:
        print("Linting failed! Fix reported issues.")
        raise
    print("Done!")
    print(f"Formatting {targets}...")
    ctx.run(f"black --quiet {targets}")
    ctx.run(f"isort --quiet {targets}")
    print("Done!")


@task()
def lint(ctx, targets="src tests"):
    print(f"Checking {targets} with ruff...")
    ctx.run(f"ruff check {targets}")


@task()
def typecheck(ctx, targets="src tests"):
    print(f"Type checking {targets} with mypy...")
    ctx.run(f"mypy {targets}")


@task
def test(ctx, suite=""):
    """Run the test suite. Pass suite=unit or suite=integration to filter."""
    if suite:
        ctx.run(f"pytest -v tests/{suite}")
    else:
        ctx.run("pytest -v tests/")


@task
def clean(ctx):
    print("Cleaning...")
    ctx.run("rm -rf dist/ build/ .pytest_cache .ruff_cache .mypy_cache")
    ctx.run('find . -name "*.egg-info" -type d -exec rm -r {} +')
    ctx.run('find . -name "__pycache__" -type d -exec rm -r {} +')
    print("Done!")


@task(pre=[clean])
def build(ctx):
    ctx.run("python -m build")


@task(pre=[build])
def publish(ctx):
    ctx.run("twine upload dist/*")
