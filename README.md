## Tree Dump

## Python 3.10.11

### Building

`pyinstaller --onefile tree_dump.py`

### Install to system

Mac OS:

```
cp ./dist/tree_dump /usr/local/bin
```

### Commands

```
tree_dump --dir ./ --mode include --item "app/*" --global-excludes __pycache__ ".*" --output ./output.txt

tree_dump --dir ./ --mode exclude --item "venv" ".*" --global-excludes __pycache__ ".*" --output ./output.txt
```
