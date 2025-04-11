1. Increment version in `pyproject.toml`
2. `py -m build`
3. `py -m twine check dist/*`
4. `py -m twine upload dist/*`
5. `git add .`
6. `git commit -m "vX.Y.Z"`
7. `git push`