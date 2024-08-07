import gzip
import logging
import logging.config
import os
import shutil
from logging.handlers import TimedRotatingFileHandler

import toml
from dotenv import load_dotenv


class CompressedTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    Custom handler to compress old log files
    and move them to a specified directory
    after log file rotation
    """

    def doRollover(self):
        # 通常のログローテーションの実行
        super().doRollover()

        # ログディレクトリの取得
        log_dir = os.path.dirname(self.baseFilename)
        old_log_dir = os.path.join(log_dir, "old")

        # logディレクトリ配下にoldディレクトリがない場合作成する
        if not os.path.exists(old_log_dir):
            os.makedirs(old_log_dir)

        for filename in os.listdir(log_dir):
            # ローテーションされたログファイルのみ対象とし
            # 圧縮済みのファイルについては対象外とする
            if filename.startswith(
                os.path.basename(self.baseFilename)
            ) and not filename.endswith(".gz"):
                file_path = os.path.join(log_dir, filename)
                # ファイル名が現在のログファイルではない場合圧縮する
                if file_path != self.baseFilename:
                    # ファイル圧縮処理
                    with open(file_path, "rb") as f_in:
                        with gzip.open(file_path + ".gz", "wb") as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    # 圧縮元ファイルの削除
                    os.remove(file_path)
                    # 圧縮ファイルをoldディレクトリに移動する
                    shutil.move(
                        file_path + ".gz", os.path.join(old_log_dir, filename + ".gz")
                    )


class LOG:
    def __init__(self):
        # envファイルの読み込み
        load_dotenv("../.env/.env")

        config_dir_path = os.getenv("LOG_CONFIG_DIR_PATH")
        config_file_name = os.getenv("LOG_CONFIG_FILE_NAME")
        config_file_path = os.path.join(config_dir_path, config_file_name)

        with open(config_file_path, "r") as f:
            config = toml.load(f)

        logging.config.dictConfig(config)

    @staticmethod
    def get_logger(name: str):
        return logging.getLogger(name)
