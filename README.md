# 研究用puyhon環境

## とりあえずすぐ始める方法

1.リポジトリをクローンします：

```bash
git clone <repository_url>
```

2.以下のコマンドを実行して、既存のgitを削除し、新しいgitを作成します：

```bash
rm -rf .git
```

3.仮想環境を作成します。：

```bash
poetry install
```

## 手を動かしたい場合

### 1. Pythonのインストール

Pyenvを使用して指定のバージョンのPythonをインストールします：

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
git clone https://github.com/pyenv/pyenv-update.git $(pyenv root)/plugins/pyenv-update
pyenv update
cd ~/.pyenv && git fetch && git pull
pyenv local <python-version>
pyenv global <python-version>

```

### 2. Poetryのインストール

```bash
curl -sSL https://install.python-poetry.org | python3 -
echo PATH="$HOME/.local/bin:$PATH" >> ~/.bashrc 
poetry config virtualenvs.in-project true 

```

### 3. ディレクトリの作成、Python環境の構築

```bash
mkdir python-demo
cd python-demo
pyenv install 3.11.0
pyenv local 3.11.0
python -m venv .venv
poetry init
poetry add <package>
poetry update
poetry run python sample.py

```

### 4. 静的解析、自動整形ツールのインストール

```bash
poetry add --group dev flake8 pyproject-flake8==6.0.4 flake8-isort flake8-bugbear flake8-builtins flake8-eradicate flake8-unused-arguments flake8-pytest-style pep8-naming mypy black isort ruff

```

pyproject.tomlに下記を追加します：

```toml

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

VS Codeのsettings.jsonに以下を追加します：

```json
{
    "[python]": {
        "editor.tabSize": 4,
        "editor.formatOnSave": true
    },
    "python.analysis.extraPaths": ["./src"],
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.formatting.provider": "black",
    "python.formatting.blackPath": "${workspaceFolder}/.venv/bin/black",
    "python.sortImports.path": "${workspaceFolder}/.venv/bin/isort",
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--ignore=E203, W503",
        "--max-complexity=10"
    ],
    "python.linting.flake8Path": "${workspaceFolder}/.venv/bin/flake8",
    "python.linting.mypyEnabled": true,
    "python.linting.mypyPath": "${workspaceFolder}/.venv/bin/mypy",
    "autoDocstring.docstringFormat": "numpy"
}

```

### 5. Dockerfileとdocker-compose

これらは[こちらのgithub](https://github.com/Buddies-as-you-know/python_research_enviroment)からコピペ推奨です。

pytorchを使用する場合,[こちらのサイト](https://qiita.com/nyakiri_0726/items/a33f404b5e1be9352b85)参考にしてください。

### 6. ディレクトリの構成

ディレクトリ構成は自由ですが、[こちら](https://github.com/drivendata/cookiecutter-data-science)を参照してください。

### 7. ハードコーディングをさせるために

config.pyのdataclassを使用してください。

dataclassの[参考資料](https://docs.python.org/ja/3.11/library/dataclasses.html)

## 改善

もっと上手い人がいた場合、改善をお願いします。

### Pull requestの出し方

[こちら](https://qiita.com/takamii228/items/80c0996a0b5fa39337bd)を参照してください。

## 開発環境

- 計算機(実際にプログラムを動かすマシン)のOS：Ubuntu
- コードエディタ：VS Code

### SSH接続

[Github SSH接続](https://qiita.com/shizuma/items/2b2f873a0034839e47ce)

## 参考文献

- [資源として見る実験プログラム](https://speakerdeck.com/hpprc/zi-yuan-tositejian-rushi-yan-puroguramu)
- [研究のためのPython開発環境](https://zenn.dev/zenizeni/books/a64578f98450c2)
- [研究効率化Tips Ver.2
](https://www.slideshare.net/cvpaperchallenge/tips-ver2-250474910)
- [開発品質とDeveloper eXperienceを高めるコンテナ開発環境のご紹介 (Python)](https://tech-blog.abeja.asia/entry/container-enironment-202310)

## やること

- [x] SSH接続
- [x] Python環境構築[Pyenv+Poetry]
- [x] 静的解析＆自動整形[flake8+black+isort+mypy]
- [x] Makefileの作成
- [x] dockerの構成
- [x] ディレクトリ構成
- [ ] Pythonデバッグ ([参考](https://buildersbox.corp-sansan.com/entry/2023/10/25/110000))
- [x] 実験設定の管理[ハードコーディングを避ける]
- [ ] [WIP]適切なログの出力 ~printからの脱却~
