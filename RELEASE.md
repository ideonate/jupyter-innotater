NEED TO RELEASE ON NPM AND PYPI

- To release a new version of jupyter_innotater on PyPI:

Change version number in package.json
And in .binder/requirements.txt
git add the __meta__.py file and git commit
delete dist folder

`python setup.py sdist bdist_wheel`

`twine upload dist/*`

git add and git commit

`git tag -a X.X.X -m 'comment'`

`git push`

`git push --tags`


- To release a new version of jupyter-innotater on NPM:

```
yarn publish --new-version
```



