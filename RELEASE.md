NEED TO RELEASE ON NPM AND PYPI

- To release a new version of jupyter-innotater on NPM:

```
# clean out the `dist` and `node_modules` directories
git clean -fdx
npm install
npm run build
npm publish
```


- To release a new version of jupyter_innotater on PyPI:

Update __meta__.py (set release version, remove 'dev')
Also change version number in package.json
And in .binder/requirements.txt
git add the __meta__.py file and git commit
delete dist folder

`python setup.py sdist bdist_wheel`

`twine upload dist/*`

git add and git commit

`git tag -a X.X.X -m 'comment'`

`git push`

`git push --tags`

