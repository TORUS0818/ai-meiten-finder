"""
ログ設定を一元管理するモジュール
"""

import logging
import structlog
from pathlib import Path


def setup_logging(
    log_file: str = "log/app.log",
    log_level: int = logging.INFO,
) -> None:
    """
    アプリケーション全体のログ設定を行う

    Args:
        log_file: ログファイル名
        log_level: ログレベル
    """
    # ログディレクトリの作成
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # 標準loggingの設定
    logging.basicConfig(
        filename=log_file,
        level=log_level,
        format="%(message)s",
        force=True,  # 既存の設定を上書き
    )

    # structlogの設定
    structlog.configure(
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = None):
    """
    構造化ログのロガーを取得する

    Args:
        name: ロガー名（通常は__name__を使用）

    Returns:
        構造化ログのロガー
    """
    return structlog.get_logger(name)
