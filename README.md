[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![HitCount](http://hits.dwyl.io/cnaimo/ExaFLOP.svg)](http://hits.dwyl.io/cnaimo/ExaFLOP) [![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![GitHub pull-requests](https://img.shields.io/github/issues-pr/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/pull/) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)  

# ExaFLOP
A cluster computing library for Python3 and Linux

# Contact
Questions? Feel free to reach out via my LinkedIn on my profile page. I'm also seeking employment in data science/finance!

# About
ExaFLOP is intended to be a tractable cluster computing solution for Python. Communication between the client and compute nodes is accomplished using a Flask-based API. The client is able to scan the existing LAN for compute nodes with the assistance of the [neighborhood layer 2 network discovery tool](https://github.com/bwaldvogel/neighbourhood). Once the client has gathered all available compute nodes, it can send copies of a project to each node which will run predetermined parts in a Python virtual environment. Each node will report back any output files to the client. This project is still in developement but all contributions are welcome!
