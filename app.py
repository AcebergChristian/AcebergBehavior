from dash import Dash
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash import html, dcc
from callbacks import register_callbacks  # 导入注册回调函数的函数
from pages.layout import layout

# 首页
from api.home import register_callbacks_home

# menu
from api.userData import register_callbacks_userData
from api.tagAnalysis import register_callbacks_tagAnalysis
from api.eventAnalysis import register_callbacks_eventAnalysis
from api.funnelAnalysis import register_callbacks_funnelAnalysis
from api.retentionAnalysis import register_callbacks_retentionAnalysis
from api.distributionAnalysis import register_callbacks_distributionAnalysis
from api.LTVAnalysis import register_callbacks_LTVAnalysis
from api.sessionAnalysis import register_callbacks_sessionAnalysis
from api.userpathAnalysis import register_callbacks_userpathAnalysis
from api.customAnalysis import register_callbacks_customAnalysis
from api.userPortraitAnalysis import register_callbacks_userPortraitAnalysis

from api.dynamicsalesAnalysis import register_callbacks_dynamicsalesAnalysis



# 系统管理
from api.userManage import register_callbacks_userManage
from api.eventManage import register_callbacks_eventManage
from api.tagManage import register_callbacks_tagManage
from api.cronManage import register_callbacks_cronManage
from api.simulateAction import register_callbacks_simulateAction


import random


app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_scripts=[
        'assets/materials/echarts.min.js'   # 'https://cdn.jsdelivr.net/npm/echarts@5.3.0/dist/echarts.min.js',
    ],
    index_string='''
        <!DOCTYPE html>
        <html>
            <head>
                {%metas%}
                <title>{%title%}</title>
                {%favicon%}
                {%css%}
                <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
        '''
    )


app.layout = html.Div([
    # 存储到localstorage
    dcc.Store(id='loginStatus', storage_type='local'),
    
    dcc.Location(id='mainurl', refresh=False),
    html.Div(id='maincontainer'), 
    ]
)

# 注册应用内的回调函数
register_callbacks(app)

# 注册各个menu的回调函数
register_callbacks_home(app)


register_callbacks_userData(app)
register_callbacks_tagAnalysis(app)
register_callbacks_eventAnalysis(app)
register_callbacks_funnelAnalysis(app)
register_callbacks_retentionAnalysis(app)
register_callbacks_distributionAnalysis(app)
register_callbacks_LTVAnalysis(app)
register_callbacks_sessionAnalysis(app)
register_callbacks_userpathAnalysis(app)
register_callbacks_customAnalysis(app)
register_callbacks_userPortraitAnalysis(app)

register_callbacks_dynamicsalesAnalysis(app)


register_callbacks_userManage(app)
register_callbacks_eventManage(app)
register_callbacks_tagManage(app)
register_callbacks_cronManage(app)
register_callbacks_simulateAction(app)



    
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=True, port=8888)