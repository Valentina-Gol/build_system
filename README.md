# build_system
Build system for resource management.

## Install

1. Clone this repository.
2. Move in root of cloned repository.
3. *Create and activate virtual env.
4. Install dependencies.

```
git clone git@github.com:Valentina-Gol/build_system.git
cd build_system
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

## Usage
## Resources list
View uploaded task names:
```
python3 build_system.py --list tasks
```
View uploaded build names:
```
python3 build_system.py --list builds
```
## Resources info
View information about a task:
```
python3 build_system.py --get task <task_name>
```
View information about a build:
```
python3 build_system.py --get build <build_name>
```
## Run tests
```
python3 -m unittest tests/test_build_system.py 
```