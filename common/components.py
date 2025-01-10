import feffery_antd_components as fac
from dash import callback, Input, Output


# message 组件
def cp_message(app, content="消息内容", type='info'):
    @callback(
        Output('message-basic-demo', 'children'),
        Input('login-btn_login', 'nClicks'),
        prevent_initial_call=True,
    )
    def cp_message_show(nClicks):
        return fac.AntdMessage(content= content, type=type)
    
