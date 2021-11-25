# Contributing qulacs-visualizer

## Start coding

プロジェクトをセットアップします．

1. リポジトリをクローンします．

```bash
git clone git@github.com:Qulacs-Osaka/qulacs-visualizer.git
cd qulacs-visualizer
```

2. 依存ライブラリや開発用ツールをインストールします．  
qulacs-visualizer では開発環境の管理に [poetry](https://github.com/python-poetry/poetry) を利用しています．

```bash
poetry install
```

次は毎回のコードの編集からマージまでの流れについてです．  

3. `main` と同期します(初回は不要)

```bash
git switch main
git pull # Shorthand for `git pull origin main`
```

4. ブランチを切ります．  

対応する Issue の番号と開発する内容を組み合わせたブランチ名にします．

```bash
git switch -c 99-wonderful-model
```

5. コミットの前にフォーマットとリント，テストを実行します．

```bash
make check
make test
```

Git で追跡されているファイルにのみフォーマットが適用されます．新しくファイルを作成した場合は `git add` してください．
リントエラーはエラーメッセージに沿って手で直す必要があります．やむを得ない場合、特定の行に対して無効化することが出来ます．詳しくは各ドキュメントを参照してください．

- [black #code-style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#code-style)
- [isort #skip-processing-of-imports-outside-of-configuration](https://github.com/PyCQA/isort#skip-processing-of-imports-outside-of-configuration)
- [flake8 #in-line-ignoring-errors](https://flake8.pycqa.org/en/latest/user/violations.html#in-line-ignoring-errors)
- [mypy #spurious-errors-and-locally-silencing-the-checker](https://mypy.readthedocs.io/en/stable/common_issues.html#spurious-errors-and-locally-silencing-the-checker)

コードフォーマットやリントは `make format` ， `make lint` で実行することも出来ます．  

6. 編集したファイルをコミットしてプッシュします．

```bash
git add MODIFIED_FILE
git commit
# For the first push in the branch
git push -u origin 99-wonderful-model
# After first push
git push
```

7. そのブランチで開発すべき機能ができたらプルリクエスト(PR)を出します． 基本的に他の人にレビューを受けるようにします． ただし軽微な変更の場合はレビューをスキップしても問題ない場合もあります．

## Testing

新しい機能を開発したときにはテストを書くようにします． このテストは基本的に自動で実行されるものです．

1. `tests` ディレクトリに `test_*.py` というファイルを作ります． テストの内容を大まかに表すファイル名をつけます．
2. そのファイルの中に `test_` で始まる関数を作ります． 
3. テストを実行します．

```bash
make test
```

アサーションに失敗すると赤色で内容が表示されます． それが表示されなければ全てのテストに通っています．

テストには `pytest` を使用しています． 詳しい使い方は[ドキュメント](https://docs.pytest.org/en/6.2.x/)を参照してください．
また、matplotlibで生成した画像をテストするために、[pytest-mpl](https://github.com/matplotlib/pytest-mpl)を利用しています。

テスト用の画像データはGit LFSを用いて管理されています。詳しくは、ドキュメントを参照してください。
Git LFSをインストールした後、以下のコマンドで画像ファイルを取得することが出来ます。

```bash
git lfs pull
```

## CI

GitHub Actions で CI を実行します． 基本的に CI に通らないとマージできません．
CI ではテストとコードフォーマット，リンタのエラーがないことの確認をします．
CI の目的には次のようなものがあります．

- コードが正常に確認していることを全体で共有する
- 手元では気づかなかったエラーを発見する
- コードがフォーマットされておりリンタのエラーがないことを強制することで，余計な diff が生まれないようにする

## Build

ビルドすることで、成果物として `dist` フォルダに `*.whl` と`*.tar.gz` が生成されます。

```bash
poetry build
```

## Installation

GitHub リポジトリからインストールすることが出来ます。

```bash
pip install git+https://github.com/Qulacs-Osaka/qulacs-visualizer
```

## Documentation

このライブラリの API ドキュメントはここから参照できます: https://qulacs-osaka.github.io/qulacs-visualizer

このドキュメントは `main` ブランチにプッシュ(PR からのマージ)したときにビルドされ，デプロイされます．

### Build document

`docs` フォルダに移動し、コマンドを実行することで、ドキュメントを生成することが出来ます。

```bash
cd docs
make html
```

`docs/build/html` に HTML ファイルなどのビルド成果物が入っています．
