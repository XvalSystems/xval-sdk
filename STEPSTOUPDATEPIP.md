1. Increment version in `pyproject.toml`
2. `py -m build`
3. `py -m twine check dist/*`
4. `py -m twine upload dist/*`