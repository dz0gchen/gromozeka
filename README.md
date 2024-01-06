![My animated logo](gromozeka.png)

## Description

gromozeka is a simple command line utility launched by the python interpreter for testing the load on the web server

## Getting Started

### Dependencies

os gnu/linux and interpreter python >= 3.7

### Installing

```
git clone https://github.com/dz0gchen/gromozeka.git
cd gromozeka
python3.7 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Executing program

```
python gromozeka.py --rps=5 --users=10 --url=http://127.0.0.1:8080 --duration=5
```

### Help

```
python gromozeka.py -h, --help
```


## Version History

* 0.1
    * initial release

## License

This project is licensed under the Unlicense