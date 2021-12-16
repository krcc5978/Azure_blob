import shutil
import cv2
import os


# コンテナ作成
def create_container(blob_service_client, container_name):
    blob_service_client.create_container(container_name)  # 引数：（作成したいコンテナ名）


# BLOB作成（データのアップロード）
def upload_blob(blob_service_client, container_name, blob_name, input_path):
    # Azure Storageの指定コンテナに接続するブロブのクライアントインスタンスを生成する
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Azure Storageへアップロード
    with open(input_path, "rb") as data:
        blob_client.upload_blob(data)


# BLOB作成（画像データのアップロード）
def image_upload(blob_service_client, container_name, input_path):
    tree_list = input_path.split("/")
    file_name = tree_list.pop(len(tree_list) - 1)
    # Azure Storageの指定コンテナに接続するブロブのクライアントインスタンスを生成する
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    # Azure Storageへアップロード
    with open(input_path, "rb") as data:
        blob_client.upload_blob(data)


# BLOB作成（動画分割～データのアップロード）
def frame_upload(blob_service_client, container_name, input_path):
    # tmpディレクトリ作成
    tmp_dir = "./tmp"
    os.makedirs(tmp_dir, exist_ok=True)
    # 動画読み込み
    cap = cv2.VideoCapture(input_path)
    # フレーム数所得
    number = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    # ファイルが開くかを確認
    if not cap.isOpened():
        return
    n = 0  # 連番カウント変数
    # フレーム保存～blobアップロード
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        filename = f"frame_{str(n).zfill(number)}.jpg"
        cv2.imwrite(tmp_dir + "/" + filename, frame)
        # blobアップロード
        image_upload(blob_service_client, container_name, tmp_dir + "/" + filename)
        n += 1
    # フレーム削除
    shutil.rmtree(tmp_dir)

    print("アップロードが完了しました。")


# BLOB作成（ディレクトリのアップロード（jpg, png））
def dir_upload(blob_service_client, container_name, input_path):
    for filename in os.listdir(input_path):
        if ".jpg" in filename or ".png" in filename:  # 入力データ：画像
            image_upload(blob_service_client, container_name, input_path + "/" + filename)


# BLOB取得（データのダウンロード）
def download_blob(blob_service_client, container_name, blob_name, filepath):
    # Azure Storageの指定コンテナに接続するブロブのクライアントインスタンスを生成する
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # BLOBのダウンロード
    with open(filepath, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())


# BLOB取得（階層ありデータのダウンロード）
def download_tree_blob(blob_service_client, container_name, src_dir_path, output_obj):
    # 接続するコンテナのクライアントインスタンスを生成する
    container_client = blob_service_client.get_container_client(container_name)
    # BLOB一覧取得
    blob_list = container_client.list_blobs()
    count = 0  # カウント用
    for obj in output_obj:
        # ディレクトリ作成しダウンロードを行う。
        for blob in blob_list:
            if obj + "-PascalVOC-export" in blob.name:
                tree_list = blob.name.split("/")
                file_name = tree_list.pop(len(tree_list) - 1)  # ファイル名取得
                dir_path = src_dir_path + "/".join(tree_list) + "/"
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                # ファイル存在確認
                if os.path.exists(dir_path+file_name):
                    continue
                # blobダウンロード
                download_blob(blob_service_client, container_name, blob.name, dir_path+file_name)
                count += 1

                # 進捗状況
                if count != 0 and count % 50 == 0:
                    print(f"{count}項目のダウンロードが完了しました。\n")
    print("全てのダウンロードが完了しました。")


# ブロブ削除
def delete_blob(blob_service_client, container_name, blob_name):
    # Azure Storageの指定コンテナに接続するブロブのクライアントインスタンスを生成する
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.delete_blob()
