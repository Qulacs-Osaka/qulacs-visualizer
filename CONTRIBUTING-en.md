# Contributing scikit-qulacs

## Start coding

Set up the project.

1. First, clone this repository.

```bash
git clone git@github.com:Qulacs-Osaka/qulacs-visualizer.git
cd qulacs-visualizer
```

2. Install dependencies and development tools.  
The qulacs-visualizer uses [poetry](https://github.com/python-poetry/poetry) to manage the development environment.

```bash
poetry install
```

Next, workflow through modification to merge.  

3. Synchronize with `main`(not necessary for the first time).

```bash
git switch main
git pull # Shorthand for `git pull origin main`
```

4. Create branch.

The branch name should be a combination of the issue number and the content to be developed.

```bash
git switch -c 99-wonderful-model
```

5. Format, lint and test code before commit.

```bash
make check
make test
```

The formatting is only applied to files that are tracked by Git. If you have created a new file, run `git add`.
Lint errors should be fixed by hand along error messages.  
If this is unavoidable, it is possible to disable it for a specific line. See the documentation for details.

- [black #code-style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#code-style)
- [isort #skip-processing-of-imports-outside-of-configuration](https://github.com/PyCQA/isort#skip-processing-of-imports-outside-of-configuration)
- [flake8 #in-line-ignoring-errors](https://flake8.pycqa.org/en/latest/user/violations.html#in-line-ignoring-errors)
- [mypy #spurious-errors-and-locally-silencing-the-checker](https://mypy.readthedocs.io/en/stable/common_issues.html#spurious-errors-and-locally-silencing-the-checker)

Code formatting and linting can also be run with `make format` and `make lint`.  

6. Commit and push modified files.

```bash
git add MODIFIED_FILE
git commit
# For the first push in the branch
git push -u origin 99-wonderful-model
# After first push
git push
```

7. Create a pull request(PR) after you finish the development at the branch. Basically you need someone to review your code. If modification is subtle, you might not need a review.

## Testing

Write tests when you develop a new feature. Tests are executed automatically.

1. Create `test_*.py` in `tests` directory. Describe what to test in the file name.
2. Create a function whose name starts with `test_`. 
3. Then run tests.

```bash
make test
```

If assertion fail, error contents are displayed with red. If you do not see that, all test are successful.

We use `pytest` for testing. Detailed instructions are available in the [pytest document](https://docs.pytest.org/en/6.2.x/).

## CI
Run CI at GitHub Actions. You cannot merge a branch unless CI passes.
In CI, we run tests and check code format and linter error.
The purpose of CI is
* Share our code works properly in the team.
* Find error you cannot notice at your local machine.
* Avoid unnecessary diff by forcing code format and linter error.

## Build

The build will generate `*.whl` and `*.tar.gz` in the `dist` folder as artifacts.

```bash
poetry build
```

## Installation

You can install qulacs-visualizer from the GitHub repository.

```bash
pip install git+https://github.com/Qulacs-Osaka/qulacs-visualizer
```

## Documentation

API document of this library is available here: https://qulacs-osaka.github.io/qulacs-visualizer

The documentation is built and deployed on pushing(merged from PR) to `main` branch.

### Build document

Move to the `docs` folder and run the command to generate the documentation.

```bash
cd docs
make html
```

In `doc/build/html`, you can find build artifacts including HTML files.