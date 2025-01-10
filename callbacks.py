import dash
from dash import callback, Input, Output, State, html, clientside_callback
from dash import dcc 
from pages.login import login_layout
from pages.layout import layout
from pages.news import news_layout
from dash.dependencies import ClientsideFunction

from api.login import login, logout


import feffery_antd_components as fac
from common.tools import sha256_encrypt

from components.home import home_layout

# from components.dashBoard import dashBoard_layout
from components.userData import userData_layout
from components.tagAnalysis import tagAnalysis_layout
from components.eventAnalysis import eventAnalysis_layout
from components.funnelAnalysis import funnelAnalysis_layout
from components.retentionAnalysis import retentionAnalysis_layout
from components.distributionAnalysis import distributionAnalysis_layout
from components.LTVAnalysis import LTVAnalysis_layout
from components.sessionAnalysis import sessionAnalysis_layout
from components.userpathAnalysis import userpathAnalysis_layout
from components.customAnalysis import customAnalysis_layout
from components.userPortraitAnalysis import userPortraitAnalysis_layout

from components.dynamicsalesAnalysis import dynamicsalesAnalysis_layout




from components.userManage import userManage_layout
from components.eventManage import eventManage_layout
from components.tagManage import tagManage_layout
from components.cronManage import cronManage_layout
from components.simulateAction import simulateAction_layout

# exception
from components.exception import exception_layout



# 装饰器：检查 localStorage 中的登录状态
def login_required(f):
    def wrapper(*args, **kwargs):
        # 判断localstorage里是否有登陆信息，没有则回到 /login
        pathname, data = args
        if data:
            pass
        else:
            return login_layout, '/login'
        return f(*args, **kwargs)
    return wrapper


def register_callbacks(app):
    
    @callback(
        Output('maincontainer', 'children'),
        Output('mainurl', 'pathname'),
        
        Input('mainurl', 'pathname'),
        State('loginStatus', 'data'),
        prevent_initial_call=True,
    )
    @login_required
    def display_page(pathname, data):
        
        if pathname == '/login':
            if data and data['status'] == 'login':
                return layout, '/home'
            else:
                return login_layout, '/login'
        else:
            if data and data['status'] == 'logout':
                return login_layout, '/login'
            else:
                return layout, pathname
    
    
    # 从路由到menu 
    @callback(
        Output('layout-menu', 'currentKey'),
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def route_to_menu(pathname):
        name = pathname.split('/')[1]
        return name

    ######## login页面 ########
    
    # 登陆到home页面
    @callback(
        Output('mainurl', 'pathname', allow_duplicate=True),
        Output('login-message', 'children'),  # 添加此行以返回消息
        Output('loginStatus', 'data'),
        [Input('login-btn_login', 'nClicks')],
        State('username', 'value'),
        State('password', 'value'),
        prevent_initial_call=True,
    )
    def login_to_home(nClicks, username, password):
        if nClicks is not None and nClicks > 0:
            res = login(username, sha256_encrypt(password))
            if res[0]:
                # 用户数据存到localStorage, key为'loginStatus'
                user_data = {'username': username,'password':sha256_encrypt(password), 'status': 'login'}  
                
                return '/home', dash.no_update, user_data  # 登录成功，返回主页和 cookie 数据
            else:
                return dash.no_update, fac.AntdMessage(content=res[3], type='error'), dash.no_update
            
        return dash.no_update, dash.no_update, dash.no_update
    


    ######## home页面 ########

    # 从home页面退出
    @callback(
        Output('mainurl', 'pathname', allow_duplicate=True),
        Output('loginStatus', 'data', allow_duplicate=True),
        Input('layout-rightContent-nav-dropdown', 'clickedKey'), 
        Input('layout-rightContent-nav-dropdown', 'nClicks'),
        State('loginStatus', 'data'),
        prevent_initial_call=True,
    )
    def home_to_login(clickedKey, nClicks, data):
        if nClicks and nClicks > 0:
            if clickedKey == 'logout':
                res = logout(data['username'], data['password']) # 更新数据库状态
                if res[0]:
                    user_data = {'username': '', 'password': '', 'status': 'logout'}
                    return '/login', user_data
                else:
                    return dash.no_update, dash.no_update
        
        return dash.no_update, dash.no_update
    


    # home页面 点击menu item
    @callback(
        Output('layout-rightContent-nav-path', 'children'),
        Output('layout-rightContent-content', 'children'),  # 更新右侧内容的组件
        Output('url', 'pathname', allow_duplicate=True),
        Input('layout-menu', 'currentItemPath'),
        prevent_initial_call=True,
    )
    def menu_callback( currentItemPath, ):
        if currentItemPath:
            
            # 添加逻辑以确保面包屑展示当前页面标题
            fist =  currentItemPath[0]['props']['title']
            last = currentItemPath[-1]['props']['title']   
            lastkey = currentItemPath[-1]['props']['key']  
            
            try:
                layout_to_render = globals()[f"{lastkey}_layout"]
                return f"{fist} / {last}", layout_to_render, f"/{lastkey}"
            except:
                return f"{fist} / {last}", exception_layout, f"/{lastkey}"
        else:
            return dash.no_update, dash.no_update, dash.no_update
    



    # 右上角的用户头像下拉菜单
    @callback(
        Output('layout-rightContent-nav-dropdown-accountrole', 'children'),
        Input('mainurl', 'pathname'),
        State('loginStatus', 'data'),
        prevent_initial_call=True,
    )
    def nav_dropdown_accountrole(pathname, data):
        name = f"当前用户({data['username']})" if data else "未登录"
        return name
    
    
    # 点击全屏
    # layout-rightContent-nav-fullScreen
    clientside_callback(
            """
                function(nClicks) {
                    if (nClicks > 0) {
                        const ele = document.getElementById("layout-rightContent-content");
                        if (ele && ele.requestFullscreen) {
                            ele.requestFullscreen().catch(err => {
                                console.error("Error attempting to enable full-screen mode:", err);
                            });
                        } else {
                            console.error("Fullscreen API is not supported or element not found");
                        }
                    }
                    return window.dash_clientside.no_update;
                }
            """,
            Output('layout-rightContent-nav-div', 'data', allow_duplicate=True),
            Input('layout-rightContent-nav-fullScreen', 'nClicks'),
            prevent_initial_call=True,
    )
    @callback(
        Output('layout-rightContent-nav', 'data', allow_duplicate=True),
        Input('layout-rightContent-nav-fullScreen', 'nClicks'),
        prevent_initial_call=True,
    )
    def nav_fullScreen(nClicks):
        try:
            if nClicks is not None and nClicks > 0:
                return "dash.no_update"
            else:
                return dash.no_update
        except Exception as e:
            return dash.no_update
        
        
    # 点击下载图片
    # layout-rightContent-nav-download
    app.clientside_callback(
            """
                function(nClicks) {
                    if (nClicks > 0) {
                        const ele = document.getElementById("layout-rightContent-content");
                        console.log(ele)
                        html2canvas(ele, {
                            useCORS: true,  // 允许跨域资源
                            scrollX: 0,
                            scrollY: 0,
                            width: ele.scrollWidth,  // 使用元素的完整宽度
                            height: ele.scrollHeight,  // 使用元素的完整高度
                            windowWidth: document.documentElement.scrollWidth,
                            windowHeight: document.documentElement.scrollHeight,
                            onclone: (documentClone) => {
                                // 确保克隆的文档中样式被正确应用
                                const clonedEle = documentClone.getElementById("layout-rightContent-content");
                                clonedEle.style.display = 'block';
                                clonedEle.style.height = 'auto';  // 确保高度是自动的
                            }
                        }).then(canvas => {
                            canvas.toBlob(blob => {
                                saveAs(blob, "screenshot.png");
                            });
                        });
                    }
                    return window.dash_clientside.no_update;
                }
            """,
            Output('layout-rightContent-nav-div', 'data', allow_duplicate=True),
            Input('layout-rightContent-nav-download', 'nClicks'),
            prevent_initial_call=True,
    )
    def nav_download(nClicks):
        if nClicks is not None and nClicks > 0:
            return dash.no_update
        else:
            return dash.no_update