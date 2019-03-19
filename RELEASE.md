- To release a new version of jupyter_innotater on PyPI:

Update __meta__.py (set release version, remove 'dev')
Also change version number in package.json
git add the __meta__.py file and git commit
`python setup.py sdist upload`
`python setup.py bdist_wheel upload`
`git tag -a X.X.X -m 'comment'`
Update _version.py (add 'dev' and increment minor)
git add and git commit
git push
git push --tags


- To release a new version of jupyter-innotater on NPM:

```
# clean out the `dist` and `node_modules` directories
git clean -fdx
npm install
npm publish
```