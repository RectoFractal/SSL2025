# Strategy Project

## 📦 Installation

Clone the repository with submodules and install dependencies:

```bash
git clone git@github.com:SPbUnited/strategy.git
cd strategy
make init
```

## ⚙️ Configuration

After the first run of the project, a `.env` file will be generated. This file contains all the main configuration parameters of the program, each of which is described in detail. You can modify the values in `.env` to adjust the behavior of the project without changing the code directly.

## ▶️ Running the Project

```bash
make run
```
or 
```bash
python3 main.py
```

## 🔍 Static Analysis

Check the entire project:

```bash
make syntax
```

Check all Python files in the `bridge/strategy/` directory:

```bash
make syntax_strategy
```


## 🛠️ Auto Formatting

Install [pre-commit](https://pre-commit.com/) and run auto-formatting:

```bash
make auto_format
```

Pre-commit hooks will automatically:

* Remove unused imports and variables with `autoflake`
* Sort imports according to `isort`
* Format code with `black`
* Check code style with `flake8`
* Perform static type checking with `mypy`


## 🤖 Recommended Program: PAcmaCS

For full control of the robots, data visualization, and telemetry topics, it is recommended to use [PAcmaCS](https://github.com/SPbUnited/PAcmaCS). This framework is designed for developing strategies in RoboCup SSL.

PAcmaCS uses ZeroMQ for inter-module communication, automates dependency installation, builds, and runs the services. With Serviz, you can visualize the game field with objects, control robots via keyboard, and configure display layers.

Follow the [PAcmaCS README](https://github.com/SPbUnited/PAcmaCS) for installation and setup. Once running, you can access the interface at [http://localhost:8000](http://localhost:8000).
