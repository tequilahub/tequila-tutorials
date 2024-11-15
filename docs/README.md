Here is a quick instruction on how to document a new package on the site, just like the packages under 
`docs/source` as `.rst` files


## Folder Structure of the Docs 

Firstly you have to gernerally understand the folder structure of the docs using `sphinx`. 

1. Since the project has already been initialised, the packages displayed on the site are under `docs/source` as `.rst` files. 

2. The actual code is in `tequila_code` and it's getting rendered to `.rst` files in `docs/source`

3. `make html` renders the contents of the `source` directory (.rst files and index.rst) and saves them into the `build` directory, whose html content is getting copied to the folder `_site/cods/sphinx` in order to display it on the main tutorials website using `quarto`

4. The individual modules are listed in `modules.rst`, which has to be included in `index.rst` in order for it to be visible on the main page of the docs site

## Documenting 

in order to document a new package follow these steps:

1. place your new package as a folder in `tequila_code`. Along the `.py` files your package must contain an 
`__init__.py` file for it to be rendered correctly by sphinx 

2. run the command `sphinx-apidoc -o docs/source tequila_code` –– this will create out of all the packages in `tequila_code` corresponding `.rst` files and place them in `docs/source`

3. the new generated `.rst` files within `source/docs` contain automatically generated names. Rename these submodules and, at the top of this script, the package as you wish them to appear on the docs site

4. add after each `.. automodule::` for each generated package name the prefix `tequila_code.` as for example in `tequila_code.optimizers.optimizer_base`.
Otherwise sphinx might not recognize where your files are.

5. Note that `sphinx` is not using markdown, but the `reStructured` syntax, in case you want to style a page or add elements like titles and links 