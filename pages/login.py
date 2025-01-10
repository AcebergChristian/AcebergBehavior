import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac


login_layout = html.Div(
    [ 
        html.Div(id='login-message'),
        fac.AntdSpace(
            [
                fac.AntdImage(
                    src="../assets/images/logo.png",
                    style={"width": 140, "marginTop": 32, "borderRadius": 8},
                    preview=False,
                ),
                html.Div(
                    [
                        fac.AntdSpace(
                                    [
                                        html.H3("Aceberg用户行为分析",style={"color":"#333333","margin":0}),
                                        html.H4("Design by Aceberg",style={"color":"#333333","margin":0}),
                                    ],
                                    direction="vertical",
                                    style={"margin": '30px 0 0 20px'},
                        ),
                        
                        fac.AntdCenter(
                            [
                                fac.AntdSpace(
                                    [
                                        html.H5("username",
                                                style={"color":"#333333"}),
                                        fac.AntdInput(
                                            id="username",
                                            placeholder="用户名",
                                            style={"width": 240},
                                            autoComplete='off',
                                        ),
                                    ],
                                    style={"marginTop":16},
                                )
                            ],
                            style={"backgroundColor": "null"},
                        ),
                        fac.AntdCenter(
                            [
                                fac.AntdSpace(
                                    [
                                        html.H5("password",
                                                style={"color":"#333333"}),
                                        fac.AntdInput(
                                            id="password",
                                            placeholder="密码",
                                            style={"width": 240},
                                            mode="password",
                                            autoComplete='off',
                                        ),
                                    ]
                                )
                            ],
                            style={"backgroundColor": "null"},
                        ),
                        fac.AntdCenter(
                            [
                                fac.AntdButton(
                                    "登陆",
                                    id="login-btn_login",
                                    style={"width": "80%", "marginTop": 32},
                                    type='primary'
                                )
                            ],
                            style={"backgroundColor": "null"},
                        ),
                    ],
                    style={
                        "width": 360,
                        "height": 420,
                        "backgroundColor": "rgba(255,255,255,0.86)",
                        "borderRadius": 6,
                    },
                ),
            ],
            align="center",
            direction="vertical",
            style={"width": "100%", "height": "100%", "overflowY": "scroll"},
        ),
    ],
    style={
        "width": "100%",
        "height": "100vh",
        "backgroundSize": "cover",
        # "overflowY": "hidden",
        "backgroundImage": "url('../assets/images/bg.jpeg')",
    },
)

