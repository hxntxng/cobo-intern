# Install on Mac m1 chip

```
python -m venv argusfarming
source ./argusfarming/bin/activate
pip install wheel -v
pip install "cython<3.0.0" pyyaml==5.4.1 --no-build-isolation -v
pip install -r ./requirements.txt
brownie networks import ./network-config.yaml True

安装
https://github.com/foundry-rs/foundry

```
