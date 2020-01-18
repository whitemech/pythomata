## Release summary

Version number: [e.g. 1.0.1]

## Release details

Describe in short the main changes with the new release.

## Checklist

_Put an `x` in the boxes that apply._

https://github.com/whitemech/pythomata/blob/master/CONTRIBUTING.md
- [ ] I have read the `CONTRIBUTING.md` file
- [ ] I am making a pull request against the `master` branch (left side), from `release-<version-number>`
- [ ] I've updated the dependencies versions in `Pipfile` to the latest, wherever is possible.
- [ ] Lint and unit tests pass locally
- [ ] I built the documentation and updated it with the latest changes
- [ ] I've added an item in `HISTORY.md` for this release
- [ ] I bumped the version number in the `__version__.py` file.
- [ ] I published the latest version on TestPyPI and checked that the following command work:
       ```pip install pythomata==<version-number> --index-url https://test.pypi.org/simple --force --no-cache-dir --no-deps```
- [ ] After merging the PR, I'll publish the build also on PyPI. Then, I'll make sure the following
      command will work:
      ```pip install pythomata==<version_number> --force --no-cache-dir --no-deps```
- [ ] I tagged the merge commit with `v<version-number>`
- [ ] I published the docs: `mkdocs gh-deploy`

## Further comments

Write here any other comment about the release, if any.
