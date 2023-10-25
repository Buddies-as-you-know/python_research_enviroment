# とりあえずすぐ始める方法
git clone して
```
rm -rf .git (gitを削除して新たにgitを作成)
poetry shell (仮想環境に入る)
```
# 手を動かしたい場合
## 1.pythonのインストール
ここではpyenvを使用して指定のバージョンのpythonを入れる方法を紹介します。
```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
# pyenvでインストールできるpythonバージョンを更新するために必要
git clone https://github.com/pyenv/pyenv-update.git $(pyenv root)/plugins/pyenv-update
pyenv update
# pyenv-updateを入れなくても、以下のコマンドでできます。
cd ~/.pyenv && git fetch && git pull
pyenv local <python-version>
pyenv global <python-version>
```
これでpythonの指定のバージョンを入れることができます。
## 2.poetryのインストール
```bash
#公式のインストーラーを使用してインストール
curl -sSL https://install.python-poetry.org | python3 -  
#pathを設定。$HOMEのところをは適宜書き換える。上記インストールのときの出力に実行コマンドが書かれている。例：Add `export PATH="/home/username/.local/bin:$PATH"` to your shell configuration file.
echo PATH="$HOME/.local/bin:$PATH" >> ~/.bashrc 
#poetryで作る仮想環境をプロジェクト直下に生成するようにする。その他の設定はpoetry config --listで見れる
poetry config virtualenvs.in-project true 
```
# ディレクトリの作成、python環境の構築
```bash
# ディレクトリ作成
mkdir python-demo
cd python-demo
# pythonバージョンのインストールとそのディレクトリで使用するpythonバージョンの指定
pyenv install 3.11.0
pyenv local 3.11.0
# 仮想環境の構築
python -m venv .venv
# poetryの初期設定
poetry init
# ライブラリの追加
poetry add <package> # プログラムの動作に必要なパッケージの追加
# poetry addで対応できないパッケージはpyproject.tomlに記述して以下のコマンドを打つ
poetry update
# sample.pyというプログラムを書いたら、以下のコマンドで実行
poetry run python sample.py
```
これでpythonの環境構築ができました。
## 静的解析、自動整形ツールのインストール
```bash
poetry add --group dev flake8 pyproject-flake8==6.0.4 flake8-isort flake8-bugbear flake8-builtins flake8-eradicate flake8-unused-arguments flake8-pytest-style pep8-naming mypy black isort ruff
```
pyproject.tomlの中に下記を追加
```pyproject.toml

[tool.ruff]
target-version = "py38"
line-length = 100
select = [
  "E", # pycodestyle errors
  "W", # pycodestyle warnings
  "F", # pyflakes
  "B", # flake8-bugbear
  "I", # isort
]

ignore = [
  "E501", # line too long, handled by black
  "B008", # do not perform function calls in argument defaults
]

unfixable = [
  "F401", # module imported but unused
  "F841", # local variable is assigned to but never used
]
[tool.mypy]
# エラー時のメッセージを詳細表示
show_error_context = true
# エラー発生箇所の行数/列数を表示
show_column_numbers = true
# import 先のチェックを行わない (デフォルトだとサードパーティーライブラリまでチェックする)
ignore_missing_imports = true
# 関数定義の引数/戻り値に型アノテーション必須
disallow_untyped_defs = true
# デフォルト引数に None を取る場合型アノテーションに Optional 必須
no_implicit_optional = true
# 戻り値が Any 型ではない関数の戻り値の型アノテーションが Any のとき警告
warn_return_any = true
# mypy エラーに該当しない箇所に `# type: ignore` コメントが付与されていたら警告
# ※ `# type: ignore` が付与されている箇所は mypy のエラーを無視出来る
warn_unused_ignores = true
# 冗長なキャストに警告
warn_redundant_casts = true

[tool.black]
line-length = 79

[tool.isort]
profile = "black"
line_length = 79
# 各ライブラリ群の説明を追記する
import_heading_stdlib      = "Standard Library"
import_heading_thirdparty  = "Third Party Library"
import_heading_firstparty  = "First Party Library"
import_heading_localfolder = "Local Library"
# from third_party import lib1, lib2...のような記述時の改行方法の設定(https://pycqa.github.io/isort/docs/configuration/multi_line_output_modes.html)
multi_line_output = 3
# 最後の要素の末尾に","を付けるようにする設定
include_trailing_comma = true

[tool.flake8]
max-line-length = 79
# E203: ":"の前の空白を入れないルール
# W503: 演算子の前に改行しないようにするルール
extend-ignore = ["E203", "W503"]
exclude = [".venv", ".git", "__pycache__",]
max-complexity = 10
```
vscodeでCtrl+,を開きsetting.jsonから
```setting.json
    "[python]": {
        // タブサイズは 4
        "editor.tabSize": 4,
        // ファイル保存時にフォーマット
        "editor.formatOnSave": true
    },
    // tests ディレクトリから src ディレクトリのモジュールをインポートするときの vscode 上でモジュールが見つからないエラー防止
    "python.analysis.extraPaths": [
        "./src"
    ],
    // .venv 内の python を使用
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    // フォーマッターは black を使用
    "python.formatting.provider": "black",
    "python.formatting.blackPath": "${workspaceFolder}/.venv/bin/black",
    "python.sortImports.path": "${workspaceFolder}/.venv/bin/isort",
    // リンターに flake8 と mypy を使用
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--ignore=E203, W503",
	// E203: ":"の前の空白を入れないルール
	// W503: 演算子の前に改行しないようにするルール
	"--max-complexity=10",
    ],
    "python.linting.flake8Path": "${workspaceFolder}/.venv/bin/flake8",
    "python.linting.mypyEnabled": true,
    "python.linting.mypyPath": "${workspaceFolder}/.venv/bin/mypy",
    // docstring は nympy スタイル (ここは完全好みです)
    "autoDocstring.docstringFormat": "numpy",
```
## dockerfileとdocker-compose
これらはこちらのgithubからコピペ推奨
## ディレクトリの構成
こちらも自由ですが書きを参照してください。

## ハードコーディングをさせるために
config.pyのdataclassをしようしてましょう。





# 改善
もっと上手い人がいた場合、改善をお願いします。
## pullrequestの出し方
https://qiita.com/takamii228/items/80c0996a0b5fa39337bd
# 開発環境
計算機(実際にプログラムを動かすマシン)のOS：Ubuntu

コードエディタ：VS Code
# ssh接続
## github
https://qiita.com/shizuma/items/2b2f873a0034839e47ce
# python環境構築
## 採用技術
### Pyenv
pythonのマイナーバージョンのインストール及びプロジェクトごとに使用するpythonの切り替えを行います。
### venv
pythonの仮想環境の構築を行います。
### Poetry
使用する外部ライブラリの依存関係の管理を行います。
## インストール
### Pyenv

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
# pyenvでインストールできるpythonバージョンを更新するために必要
git clone https://github.com/pyenv/pyenv-update.git $(pyenv root)/plugins/pyenv-update
pyenv update
# pyenv-updateを入れなくても、以下のコマンドでできます。
cd ~/.pyenv && git fetch && git pull
```

### Poetry

```bash
#可能な限り最新のstableのpythonバージョンを指定(poetryの最新バージョンが入らないので3.6とかは使わない)
pyenv local <python-version>
#公式のインストーラーを使用してインストール
curl -sSL https://install.python-poetry.org | python3 -  
#pathを設定。$HOMEのところをは適宜書き換える。上記インストールのときの出力に実行コマンドが書かれている。例：Add `export PATH="/home/username/.local/bin:$PATH"` to your shell configuration file.
echo PATH="$HOME/.local/bin:$PATH" >> ~/.bashrc 
#poetryで作る仮想環境をプロジェクト直下に生成するようにする。その他の設定はpoetry config --listで見れる
poetry config virtualenvs.in-project true 
```
## それで結局どういう流れで使うんですか
例えば、最新版のpython3.11.0を使ったpython-demoというプロジェクトを作る場合は、以下のような操作をすることになります。
```bash
# ディレクトリ作成
mkdir python-demo
cd python-demo
# pythonバージョンのインストールとそのディレクトリで使用するpythonバージョンの指定
pyenv install 3.11.0
pyenv local 3.11.0
# 仮想環境の構築
python -m venv .venv
# poetryの初期設定
poetry init
# ライブラリの追加
poetry add <package> # プログラムの動作に必要なパッケージの追加
# poetry addで対応できないパッケージはpyproject.tomlに記述して以下のコマンドを打つ
poetry update
# sample.pyというプログラムを書いたら、以下のコマンドで実行
poetry run python sample.py
```

# 静的解析＆自動整形
読みにくいコードを避けるのとコードの書き方を統一する。
今後、コードを共有する機会が来たときに読みにくいものをなくすため
https://zenn.dev/zenizeni/books/a64578f98450c2/viewer/ac820f

上記のサイトの真似をする。
コードの書き方を出来る限り統一する。
型もできる限り書く（サボらない）

https://flake8.pycqa.org/en/latest/
https://mypy-lang.org/

# Makefile
コマンドひとつで自動化できるのがめちゃくちゃ便利。

```bash
make lint
```
規約に即しているかの確認

```bash
make format
```
コードの自動整形




# docker
dockerは再現性を保つために使用する。
環境に依存しなくなるためdockerがあれば再現可能になる。
しかし、起動が遅い。
open3dを動かすためにimageはubunutを使用

```Dockerfile
# This could also be another Ubuntu or Debian based distribution
# This could also be another Ubuntu or Debian based distribution
FROM ubuntu:22.04
# Install Open3D system dependencies 
ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    gcc \
    libegl1 \
    libgl1 \
    libgomp1 \
    wget \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Size reduction by removing unnecessary things
RUN apt-get autoremove -y
# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
# Set the path for Poetry
ENV PATH /root/.local/bin:$PATH

# Prevent Poetry from creating a virtual environment
RUN poetry config virtualenvs.create false

# Create project directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

# Copy code for experimentation
COPY . .

```
## 実行時
src配下のmain.pyが実行されるようになっている。
```bash
make build
```

## open3d用
http://www.open3d.org/docs/release/docker.html

## GPGエラーを起こした場合
https://qiita.com/nissei777/items/9758b8f5140f2b8957a4
```
docker pull ubuntu
```
### 容量がいっぱいな場合
https://qiita.com/zembutsu/items/f577ea8dad6dc64d70b6
```bash
make delete
```

#　ディレクトリ構成
https://github.com/drivendata/cookiecutter-data-science

上記を参照して少し改造中、現状まだ足りてません。

```
.
├── Dockerfile
├── Makefile
├── README.md
├── Reports   論文を書くのに必要な図などを入れる。
│   └── Figuare
├── data　　　
│   ├── result
│   └── row
├── docker-compose.yml
├── docs　　　ここに生成されパラメータのoutputを入れる。
├── poetry.lock
├── pyproject.toml
└── src
    ├── __init__.py
    ├── config
    ├── features
    ├── main.py
    └── models

```
https://zenn.dev/hpp/articles/6307447e5a037d
階層をsrcより上に入れる場合は上記のサイト参照

# 実験設定の管理


# 参考文献

https://zenn.dev/zenizeni/books/a64578f98450c2/viewer/e5747f

https://speakerdeck.com/hpprc/zi-yuan-tositejian-rushi-yan-puroguramu

https://www.slideshare.net/cvpaperchallenge/tips-ver2-250474910

https://tech-blog.abeja.asia/entry/container-enironment-202310


# やること
- [x] SSH接続
- [x] Python環境構築[Pyenv+Poetry]
- [x] 静的解析＆自動整形[flake8+black+isort+mypy]
- [x] Makefileの作成
- [x] dockerの構成
- [x] ディレクトリ構成
- [ ] Pythonデバッグ
- [x] 実験設定の管理[ハードコーディングを避ける]
- [ ] [WIP]適切なログの出力 ~printからの脱却~
