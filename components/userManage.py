import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac
from static.routes import routes
from api.userManage import users_query, columns_query


# from dash import dcc, html
# from api.system.user import UserApi
# from callbacks.system_c.user_c import user_c
# from components import ManuallyUpload
# from components.ApiRadioGroup import ApiRadioGroup
# from components.ApiSelect import ApiSelect
# from utils.permission_util import PermissionManager
# from . import allocate_role, profile  # noqa: F401

userManage_layout = html.Div(
[
    # userManage 全局的message
    html.Div(id='userManage-message'),
    
fac.AntdRow(
            [
                fac.AntdCol(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    html.Div(
                                        [
                                            fac.AntdForm(
                                                [
                                                    fac.AntdSpace(
                                                        [
                                                            fac.AntdFormItem(
                                                                fac.AntdInput(
                                                                    id='userManage-search-account',
                                                                    placeholder='请输入用户名称',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 240
                                                                    },
                                                                ),
                                                                label='用户名称',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdInput(
                                                                    id='userManage-search-phone',
                                                                    placeholder='请输入手机号码',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 240
                                                                    },
                                                                ),
                                                                label='手机号码',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdSelect(
                                                                    # dict_type='sys_normal_disable',
                                                                    id='userManage-search-loginstatus',
                                                                    options=["登陆","离线"],
                                                                    placeholder='登陆状态',
                                                                    style={
                                                                        'width': 240
                                                                    },
                                                                ),
                                                                label='登陆状态',
                                                            ),
                                                        ],
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                    fac.AntdSpace(
                                                        [
                                                            fac.AntdFormItem(
                                                                fac.AntdDateRangePicker(
                                                                    id='userManage-search-createtime',
                                                                    style={
                                                                        'width': 240
                                                                    },
                                                                    showTime=True,
                                                                    needConfirm=True,
                                                                ),
                                                                label='创建时间',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '搜索',
                                                                    id='userManage-search',
                                                                    type='primary',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-search'
                                                                    ),
                                                                )
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '重置',
                                                                    id='userManage-reset',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-sync'
                                                                    ),
                                                                )
                                                            ),
                                                        ],
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                ],
                                                layout='inline',
                                                enableBatchControl=True,
                                                id='userManage-search-form',
                                            )
                                        ],
                                        id='user-search-form-container',
                                        hidden=False,
                                    ),
                                ),
                            ]
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdSpace(
                                        [
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-plus'
                                                    ),
                                                    '新增',
                                                ],
                                                id='userManage-adduser_btn',
                                                style={
                                                    'color': '#1890ff',
                                                    'background': '#e8f4ff',
                                                    'border-color': '#a3d3ff',
                                                },
                                            ),
                                        ],
                                        style={'paddingBottom': '10px'},
                                    ),
                                    span=24,
                                ),
                            ],
                            # gutter=5,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdSpin(
                                        fac.AntdTable(
                                            id='userManage-user_table',
                                            # data=users_query(),
                                            columns=columns_query()+
                                            [
                                                {
                                                    'title': '操作',
                                                    'dataIndex': 'operation',
                                                    'width': 120,
                                                    'renderOptions': {
                                                        'renderType': 'dropdown',
                                                        'dropdownProps': {
                                                            'title': '更多',
                                                        },
                                                    },
                                                },
                                            ],
                                            rowSelectionType='checkbox',
                                            rowSelectionWidth=50,
                                            bordered=True,
                                            # pagination=[],
                                            mode='server-side',
                                            style={
                                                'width': '100%',
                                                'paddingRight': '10px',
                                            },
                                        ),
                                        text='数据加载中',
                                    ),
                                )
                            ]
                        ),
                    ],
                    span=24,
                ),
            ],
            gutter=5,
        ),
        # 新增用户表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='userManage-addform-user_account',
                                            name='account',
                                            placeholder='请输入用户昵称',
                                            allowClear=True,
                                            style={'width': '100%'},
                                            autoComplete='off',
                                        ),
                                        label='用户昵称',
                                        required=True,
                                        id="account"
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                                id='userManage-addform-user_password',
                                                name='password',
                                                placeholder='请输入密码',
                                                mode='password',
                                                passwordUseMd5=True,
                                                style={'width': '100%'},
                                                autoComplete='off',
                                            ),
                                            label='用户密码',
                                            required=True,
                                            id='password'
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=10,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='userManage-addform-user_phone',
                                            name='phone',
                                            placeholder='请输入手机号码',
                                            allowClear=True,
                                            style={'width': '100%'},
                                            autoComplete='off',
                                        ),
                                        label='手机号码',
                                        id='phone',
                                        
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdSelect(
                                            id='userManage-addform-user_role',
                                            name='role',
                                            placeholder='请选择角色',
                                            style={'width': '100%'},
                                            options=["subadmin", "user"]
                                        ),
                                        label='角色',
                                        id='role'
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=10,
                        ),
                    ],
                    id='userManage-adduser_form',
                    enableBatchControl=True,
                    labelCol={'span': 8},
                    wrapperCol={'span': 16},
                    style={'marginRight': '15px'},
                )
            ],
            id='userManage-adduser_modal',
            mask=False,
            width=650,
            renderFooter=True,
            okClickClose=True,
        ),
        # 编辑用户表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='userManage-updateform-user_account',
                                            name='account',
                                            placeholder='请输入用户昵称',
                                            allowClear=True,
                                            style={'width': '100%'},
                                            autoComplete='off',
                                        ),
                                        label='用户昵称',
                                        required=True,
                                        id="account"
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                                id='userManage-updateform-user_password',
                                                name='password',
                                                placeholder='请输入密码',
                                                mode='password',
                                                passwordUseMd5=True,
                                                style={'width': '100%'},
                                                autoComplete='off',
                                            ),
                                            label='用户密码',
                                            required=True,
                                            id='password'
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=10,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='userManage-updateform-user_phone',
                                            name='phone',
                                            placeholder='请输入手机号码',
                                            allowClear=True,
                                            style={'width': '100%'},
                                            autoComplete='off',
                                        ),
                                        label='手机号码',
                                        id='phone'
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdSelect(
                                            id='userManage-updateform-user_role',
                                            name='role',
                                            placeholder='请选择角色',
                                            style={'width': '100%'},
                                            options=["subadmin", "user"]
                                        ),
                                        label='角色',
                                        id='role'
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=10,
                        ),
                    ],
                    id='userManage-updateuser_form',
                    enableBatchControl=True,
                    labelCol={'span': 8},
                    wrapperCol={'span': 16},
                    style={'marginRight': '15px'},
                )
            ],
            id='userManage-updateuser_modal',
            mask=False,
            width=650,
            renderFooter=True,
            okClickClose=True,
        ),
        # 删除用户二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='user-delete-text'),
            id='userManage-del_modal',
            # visible=False,
            title='提示',
            mask=True,
            renderFooter=True,
            okClickClose=True,
        )
    ]



)

