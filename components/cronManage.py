import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac
from static.routes import routes
from api.cronManage import cron_query, columns_query



cronManage_layout = html.Div(
[
    # cronManage 全局的messages
    html.Div(id='cronManage-message'),
    
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
                                                                    id='cronManage-search-cronName',
                                                                    placeholder='请输入任务名称',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 240
                                                                    },
                                                                ),
                                                                label='任务名称',
                                                            )
                                                        ],
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                    fac.AntdSpace(
                                                        [
                                                            fac.AntdFormItem(
                                                                fac.AntdDateRangePicker(
                                                                    id='cronManage-search-createtime',
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
                                                                    id='cronManage-search',
                                                                    type='primary',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-search'
                                                                    ),
                                                                )
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '重置',
                                                                    id='cronManage-reset',
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
                                                id='cronManage-search-form',
                                            )
                                        ],
                                        id='cron-search-form-container',
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
                                                id='cronManage-addcron_btn',
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
                                            id='cronManage-cron_table',
                                            # data=crons_query(),
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
                                            id='cronManage-addform-cronName',
                                            name='cronKey',
                                            placeholder='请输入任务名称',
                                            allowClear=True,
                                            style={'width': '100%'},
                                            autoComplete='off',
                                        ),
                                        label='任务名称',
                                        required=True,
                                        id="cronName"
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                                id='cronManage-addform-cronContent',
                                                name='cronContent',
                                                placeholder='请输入任务内容',
                                                style={'width': '100%'},
                                                autoComplete='off',
                                            ),
                                            label='任务内容',
                                            required=True,
                                            id='cronContent'
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
                                            id='cronManage-addform-cronDesc',
                                            name='cronDesc',
                                            placeholder='请输入任务描述',
                                            allowClear=True,
                                            style={'width': '100%'},
                                            autoSize=True,
                                            autoComplete='off',
                                        ),
                                        label='任务描述',
                                        id='cronDesc',
                                        
                                    ),
                                    span=12,
                                )
                            ],
                            gutter=10,
                        ),
                    ],
                    id='cronManage-addcron_form',
                    enableBatchControl=True,
                    labelCol={'span': 8},
                    wrapperCol={'span': 16},
                    style={'marginRight': '15px'},
                )
            ],
            id='cronManage-addcron_modal',
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
                                            id='cronManage-updateform-cronName',
                                            name='cronName',
                                            placeholder='请输入任务名称',
                                            allowClear=True,
                                            style={'width': '100%'},
                                            autoComplete='off',
                                        ),
                                        label='任务名称',
                                        required=True,
                                        id="cronName"
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                                id='cronManage-updateform-cronContent',
                                                name='cronContent',
                                                placeholder='请输入任务内容',
                                                style={'width': '100%'},
                                                autoComplete='off',
                                            ),
                                            label='任务内容',
                                            required=True,
                                            id='cronContent'
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
                                            id='cronManage-updateform-cronDesc',
                                            name='cronDesc',
                                            placeholder='请输入任务描述',
                                            allowClear=True,
                                            style={'width': '100%'},
                                            autoComplete='off',
                                        ),
                                        label='任务描述',
                                        id='cronDesc'
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=10,
                        ),
                    ],
                    id='cronManage-updatecron_form',
                    enableBatchControl=True,
                    labelCol={'span': 8},
                    wrapperCol={'span': 16},
                    style={'marginRight': '15px'},
                )
            ],
            id='cronManage-updatecron_modal',
            mask=False,
            width=650,
            renderFooter=True,
            okClickClose=True,
        ),
        # 删除用户二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='cron-delete-text'),
            id='cronManage-del_modal',
            # visible=False,
            title='提示',
            mask=True,
            renderFooter=True,
            okClickClose=True,
        )
    ]



)

