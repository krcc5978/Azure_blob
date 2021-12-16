from azure.storage.blob import BlobServiceClient
import configparser
from processing import frame_upload, image_upload, dir_upload, download_tree_blob
import sys
import os

if __name__ == '__main__':
    # configparserの宣言
    config_ini = configparser.ConfigParser()
    config_ini.read("config.ini", encoding="utf-8")

    # 設定ファイル(config.ini)の読み込み
    src_dir_path = config_ini["PATH"]["src_dir_path"]
    input_path = config_ini["PATH"]["input_path"]
    output_obj = eval(config_ini["PATH"]["output_obj"])
    account_name = config_ini["CONTAINER01"]["account_name"]
    connect_str = config_ini["CONTAINER01"]["connect_str"]
    container_name = config_ini["CONTAINER01"]["container_name"]

    # Azure Storageに接続するためのインスタンスを作成する
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    if len(sys.argv) == 1:
        print("upload? or download?")
    # ------入力：upload　→　blobをアップロード------
    elif sys.argv[1] == "upload":
        # 入力データ：ディレクトリ
        if os.path.isdir(input_path):
            dir_upload(blob_service_client, container_name, input_path)
        # 入力データ：動画
        elif ".avi" in input_path or ".mp4" in input_path:
            frame_upload(blob_service_client, container_name, input_path)
        # 入力データ：画像
        elif ".jpg" in input_path or ".png" in input_path:
            image_upload(blob_service_client, container_name, input_path)
    # ------入力：download　→　blobダウンロード（階層あり）------
    elif sys.argv[1] == "download":
        download_tree_blob(blob_service_client, container_name, src_dir_path, output_obj)