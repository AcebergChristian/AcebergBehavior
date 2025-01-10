# layouts.py
from dash import html
import feffery_antd_components as fac

# 定义新闻页面的布局
news_layout = html.Div([
    html.H1("新闻页面"),
    html.Div("新闻内容"),
    fac.AntdInput(placeholder='mode="default"（默认）'),
])

