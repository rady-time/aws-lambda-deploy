import json
import logging
import os
import traceback
from datetime import datetime, timedelta, timezone
from typing import Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

JST = timezone(timedelta(hours=+9), 'JST')

def lambda_handler(event: dict, context: Any) -> int:
    """
    テスト

    Args:
        - event:   EventBridgeから定期実行したときのイベント情報
        - context: Lambda実行のコンテキスト
    Return:
        - result:  0（正常終了）／-1（異常終了）
    """

    # コネクション作成
    try:
        # 現在時間取得
        now = datetime.now(JST)
        logger.info(f'実行日時： {now}')

    except Exception:
        logger.exception('処理中にエラーが発生しました。')
        raise

