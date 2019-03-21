- To release a new version of jupyter_innotater on PyPI:

Update __meta__.py (set release version, remove 'dev')
Also change version number in package.json
git add the __meta__.py file and git commit
delete dist folder

`python setup.py sdist`

`twine upload dist/*`

git add and git commit

`git tag -a X.X.X -m 'comment'`

`git push`

`git push --tags`


- To release a new version of jupyter-innotater on NPM:

```
# clean out the `dist` and `node_modules` directories
git clean -fdx
npm install
npm publish
```