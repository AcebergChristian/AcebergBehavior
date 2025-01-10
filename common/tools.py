import hashlib

# SHA-256 哈希函数
def sha256_encrypt(password):
    # 创建 SHA-256 哈希对象
    sha256_hash = hashlib.sha256()
    # 更新哈希对象
    sha256_hash.update(password.encode())
    # 返回十六进制表示的哈希值
    return sha256_hash.hexdigest()


# eventAnalysis 事件查询逻辑
def eventAnalysis_whererule(event_where):
    '''
        res = [
                {"label": "总次数", "value": "total_num"},
                {"label": "人均次数", "value": "ave_num"},
                {"label": "用户数", "value": "user_num"},
                {"label": "过去7天总次数", "value": "total_num_last7"},
                {"label": "过去7天用户数", "value": "user_num_last7"},
                {"label": "过去30天总次数", "value": "total_num_last30"},
                {"label": "过去30天用户数", "value": "user_num_last30"},
                {"label": "当月总次数", "value": "total_num_currentmonth"},
                {"label": "当月用户数", "value": "user_num_currentmonth"},
            ]
    '''
    if event_where == "total_num":
        return "count(*)"
    elif event_where == "ave_num":
        return "count(*)/count(distinct user_id)"
    elif event_where == "user_num":
        return "count(distinct user_id)"
    elif event_where == "total_num_last7":
        return "count(*)"
    elif event_where == "user_num_last7":
        return "count(distinct user_id)"
    elif event_where == "total_num_last30":
        return "count(*)"
    elif event_where == "user_num_last30":
        return "count(distinct user_id)"
    elif event_where == "total_num_currentmonth":
        return "count(*)"
    elif event_where == "user_num_currentmonth":
        return "count(distinct user_id)"
    
    
def eventAnalysis_summarymethodrule(event_summarymethod):
    '''
        res = [
                            {"label": "总和", "value": "sum"},
                            {"label": "均值", "value": "ave"},
                            {"label": "最大值", "value": "max"},
                            {"label": "最小值", "value": "min"},
                            {"label": "人均值", "value": "aveperuser"},
                            {"label": "去重数", "value": "distinct"},
                            {"label": "下四分位数", "value": "q1"},
                            {"label": "中位数", "value": "median"},
                            {"label": "上四分位数", "value": "q3"},
                            {"label": "P90", "value": "p90"},
                            {"label": "P95", "value": "p95"},
                            {"label": "P99", "value": "p99"},
            ]
    '''