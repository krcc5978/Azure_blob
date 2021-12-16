@echo off
rem
rem blobをダウンロードするプログラム
rem

rem 仮想環境の有効化
call C:\Users\y-matsushita\python\virtual_environment\Azure_ver12\Scripts\activate

rem pyファイル実行
python main.py download

rem 仮想環境の無効化
call C:\Users\y-matsushita\python\virtual_environment\Azure_ver12\Scripts\deactivate.bat


exit