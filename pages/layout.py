import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac
from static.routes import routes


layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        # 左侧菜单栏
        html.Div(
            [
                fac.AntdCenter(
                    [
                        fac.AntdImage(
                            src="../assets/images/logo.png",
                            style={
                                "width": 140,
                                "margin": "12px 0",
                                "borderRadius": 8,
                            },
                            preview=False,
                        ),
                    ],
                    style={"backgroundColor": "null"},
                ),
                fac.AntdMenu(
                    id="layout-menu",
                    menuItems=routes,
                    mode="inline",
                    theme="dark",
                    style={"width": 240},
                ),
            ],
            style={
                "backgroundColor": "#011528",
                "height": "100vh",
                "width": "240px",
                "overflowY": "auto",
                "overflowX": "hidden",
                # 隐藏滚动条
                "scrollbarWidth": "none",
            },
        ),
        # 右侧内容
        html.Div(
            [
                # nav
                html.Div(
                    [
                        html.Span(
                            [],
                            id="layout-rightContent-nav-path",
                            style={
                                "marginLeft": 20,
                                "fontSize": 14,
                                "color": "#6c6c6c",
                            },
                        ),
                        html.Div(
                        [
                            fac.AntdButton(
                                icon=fac.AntdIcon(icon='antd-download'),
                                id="layout-rightContent-nav-download",
                            ),
                            fac.AntdButton(
                                icon=fac.AntdIcon(icon='antd-full-screen'),
                                id="layout-rightContent-nav-fullScreen",
                            ),
                            fac.AntdDropdown(
                                fac.AntdAvatar(
                                    icon="antd-user",
                                    size="large",
                                    style={
                                        "marginRight": 50,
                                        "width": 32,
                                        "height": 32,
                                        "background": "#1f63fb", 
                                        "cursor": "pointer"
                                    },
                                ),
                                menuItems=[
                                    {
                                        "title": fac.AntdSpace(
                                            [
                                                fac.AntdAvatar(
                                                    icon="antd-user",
                                                    style={
                                                        "background": "#f7f8f9",
                                                        "color": "#9ea5b5",
                                                        "width": 20,
                                                        "height": 20,
                                                    },
                                                ),
                                                fac.AntdText(
                                                    [],
                                                    id="layout-rightContent-nav-dropdown-accountrole"
                                                ),
                                            ]
                                        ),
                                        "key": "user"
                                    },
                                    {
                                        "title": fac.AntdSpace(
                                            [
                                                fac.AntdAvatar(
                                                    icon="antd-power-off",
                                                    style={
                                                        "background": "#f7f8f9",
                                                        "color": "#9ea5b5",
                                                        "width": 24,
                                                        "height": 24,
                                                    },
                                                ),
                                                "logout",
                                            ]
                                        ),
                                        "key": "logout"
                                    }
                                ],
                                trigger="hover",
                                placement="bottomRight",
                                id='layout-rightContent-nav-dropdown',
                            ),
                        ],
                        id="layout-rightContent-nav-div",
                        style={
                            "display": "flex",
                            "alignItems": "center",
                            "gap": 20,
                        }
                        ),
                        
                    ],
                    id="layout-rightContent-nav",
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                        "alignItems": "center",
                        "justifyContent": "space-between",
                        "width": "100%",
                        "height": "50px",
                        "backgroundColor": "#ffffff",
                        "lineHeight": "50px",
                    },
                ),
                html.Div(
                    [],
                    id="layout-rightContent-content",
                    style={
                        "margin": "10px 10px",
                        "height": "calc(100% - 70px)",
                        "overflowY": "auto",
                        "overflowX": "hidden",
                        "backgroundColor": "#f7f9fa",
                    },
                ),
            ],
            id="layout-rightContent",
            style={
                "width": "calc(100vw - 240px)",
                "height": "100%",
                # "backgroundColor": "#1f63fb",
            },
        ),
    ],
    style={
        "display": "flex",
        "flexDirection": "row",
        "flexWrap": "nowrap",
        "width": "100vw",
        "height": "100vh",
        "backgroundColor": "#f7f9fa",
        # "backgroundImage": "url("https://dss3.bdstatic.com/iPoZeXSm1A5BphGlnYG/skin/54.jpg")",
        "overflowY": "hidden",
        "margin": 0,
        "padding": 0,
    },
)
