routes = [
    {
        "component": "SubMenu",
        "props": {"key": "home", "title": "首页"},
    },
    {
        "component": "SubMenu",
        "props": {"key": "actionAnalysis", "title": "行为分析"},
        "children": [
            {
                "component": "ItemGroup",
                "props": {"key": "userData", "title": "用户数据"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "tagAnalysis", "title": "标签分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "eventAnalysis", "title": "事件分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "funnelAnalysis", "title": "漏斗分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "retentionAnalysis", "title": "留存分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "distributionAnalysis", "title": "分布分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "LTVAnalysis", "title": "LTV分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "sessionAnalysis", "title": "session分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "userpathAnalysis", "title": "用户路径分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "customAnalysis", "title": "自定义查询"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "intervalAnalysis", "title": "间隔分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "attributionAnalysis", "title": "归因分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "heatAnalysis", "title": "热力分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "clickAnalysis", "title": "点击分析"},
            }
        ],
    },
    {
        "component": "SubMenu",
        "props": {"key": "userAnalysis", "title": "用户分析"},
        "children": [
            {
                "component": "ItemGroup",
                "props": {"key": "userPortraitAnalysis", "title": "用户画像分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "userPortraitReport", "title": "用户画像报告"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "attributeAnalysis", "title": "属性分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "userScan", "title": "用户细查"},
            },
        ],
    },
    {
        "component": "SubMenu",
        "props": {"key": "operationsAnalysis", "title": "运营分析"},
        "children": [
            {
                "component": "ItemGroup",
                "props": {"key": "dynamicsalesAnalysis", "title": "动销分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "searchAnalysis", "title": "搜索分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "functionAnalysis", "title": "功能分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "vipAnalysis", "title": "会员分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "categoryAnalysis", "title": "品类分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "groupbuyAnalysis", "title": "拼团分析"},
            },
        ],
    },
    {
        "component": "SubMenu",
        "props": {"key": "adsAnalysis", "title": "广告分析"},
        "children": [
            {
                "component": "ItemGroup",
                "props": {"key": "adsOverview", "title": "广告概览"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "launchAnalysis", "title": "投放分析"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "promotionAnalysis", "title": "推广分析"},
            }
        ],
    },
    {
        "component": "SubMenu",
        "props": {"key": "sysManage", "title": "系统管理"},
        "children": [
            {
                "component": "ItemGroup",
                "props": {"key": "userManage", "title": "用户管理"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "tagManage", "title": "标签管理"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "eventManage", "title": "事件管理"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "cronManage", "title": "定时任务"},
            },
            {
                "component": "ItemGroup",
                "props": {"key": "simulateAction", "title": "模拟行为"},
            },
        ],
    },
]





"""
-   首页【关键指标】
-   行为分析
        用户数据
        标签分析
        事件分析
        漏斗分析
        留存分析
        分布分析
        LTV分析
        Session分析
        用户路径分析
        间隔分析
        归因分析
        网页热力分析
        点击分析


-   用户分析
        用户群画像分析
        用户群画像报告
        属性分析
        用户细查


-   智能分析
        动销分析
        搜索分析
        功能分析
        会员分析
        品类分析
        拼团分析
 

-   广告分析
        广告概览
        投放分析
        推广分析
"""