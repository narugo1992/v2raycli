# v2raycli

[![PyPI](https://img.shields.io/pypi/v/v2raycli)](https://pypi.org/project/v2raycli/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/v2raycli)

[![Docs Deploy](https://github.com/narugo1992/v2raycli/workflows/Docs%20Deploy/badge.svg)](https://github.com/narugo1992/v2raycli/actions?query=workflow%3A%22Docs+Deploy%22)
[![Code Test](https://github.com/narugo1992/v2raycli/workflows/Code%20Test/badge.svg)](https://github.com/narugo1992/v2raycli/actions?query=workflow%3A%22Code+Test%22)
[![Package Release](https://github.com/narugo1992/v2raycli/workflows/Package%20Release/badge.svg)](https://github.com/narugo1992/v2raycli/actions?query=workflow%3A%22Package+Release%22)
[![codecov](https://codecov.io/gh/narugo1992/v2raycli/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/narugo1992/v2raycli)

![GitHub Org's stars](https://img.shields.io/github/stars/narugo1992)
[![GitHub stars](https://img.shields.io/github/stars/narugo1992/v2raycli)](https://github.com/narugo1992/v2raycli/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/narugo1992/v2raycli)](https://github.com/narugo1992/v2raycli/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/narugo1992/v2raycli)
[![GitHub issues](https://img.shields.io/github/issues/narugo1992/v2raycli)](https://github.com/narugo1992/v2raycli/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/narugo1992/v2raycli)](https://github.com/narugo1992/v2raycli/pulls)
[![Contributors](https://img.shields.io/github/contributors/narugo1992/v2raycli)](https://github.com/narugo1992/v2raycli/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/narugo1992/v2raycli)](https://github.com/narugo1992/v2raycli/blob/master/LICENSE)

Python CLI for v2ray.

## Quick Start

You can install `v2raycli` with PyPI

```shell
pip install v2raycli
```

or with source code

```shell
git clone https://github.com/narugo1992/v2raycli.git
cd v2raycli
pip install .
```

Then you need to download v2ray CLI from [here](https://github.com/v2ray/dist/)

After that, we can start your local proxy service

```shell
# Use your own subscription url
export V2RAY_SUBSCRIPTION='https://jmssub.net/members/getsub.php?service=777777&id=4c646243-6c01-42f4-a4f1-eef212b2e659'
# Use your own v2ray binary executable
export V2RAY_BIN=./bin/v2ray

v2raycli list                  # List the sites in subscription
v2raycli run                   # Start the proxy (socks5 protocol, port 17777)
v2raycli run -P http -p 16384  # Start at port 16384 with http protocol
v2raycli run -R                # DO NOT ASK ME! Just randomly use one site
```
