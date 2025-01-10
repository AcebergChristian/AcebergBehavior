import dash
from dash import html, dcc, Input, Output, callback
import feffery_antd_components as fac
from static.routes import routes
from api.eventManage import event_query, columns_query



eventCategoryoptions = [
    {'label': '全埋点', 'value': '全埋点(qmd)'},
    {'label': '行为', 'value': '行为(xw)'},
    {'label': '业务', 'value': '业务(yw)'},
    {'label': '小程序', 'value': '小程序(xchx)'},
    {'label': '直播', 'value': '直播(zhb)'},
    {'label': '拼团', 'value': '拼团(pt)'},
    {'label': '自定义', 'value': '自定义(custom)'},
]


eventManage_layout = html.Div(
[
    # eventManage 全局的message
    html.Div(id='eventManage-message'),
    
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
                                                                    id='eventManage-search-eventName',
                                                                    placeholder='请输入事件名称',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 240
                                                                    },
                                                                ),
                                                                label='事件名称',
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
                                                                    id='eventManage-search-createtime',
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
                                                                    id='eventManage-search',
                                                                    type='primary',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-search'
                                                                    ),
                                                                )
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '重置',
                                                                    id='eventManage-reset',
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
                                                id='eventManage-search-form',
                                            )
                                        ],
                                        id='event-search-form-container',
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
                                                id='eventManage-addevent_btn',
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
                                            id='eventManage-event_table',
                                            # data=events_query(),
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
                                            id='eventManage-addform-eventKey',
                                            name='eventKey',
                                            placeholder='请输入事件Key',
                                            allowClear=True,
                                            style={'width': '100%'},
                                            autoComplete='off',
                                        ),
                                        label='事件Key',
                                        required=True,
                                        id="eventKey"
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                                id='eventManage-addform-eventName',
                                                name='eventName',
                                                placeholder='请输入事件名称',
                                                style={'width': '100%'},
                                                autoComplete='off',
                                            ),
                                            label='事件名称',
                                            required=True,
                                            id='eventName'
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
                                            id='eventManage-addform-eventDesc',
                                            name='eventDesc',
                                            placeholder='请输入事件描述',
                                            allowClear=True,
                                            style={'width': '100%'},
                                            autoSize=True,
                                            autoComplete='off',
                                        ),
                                        label='事件描述',
                                        id='eventDesc',
                                        
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdSelect(
                                            id='eventManage-addform-eventCategory',
                                            name='eventCategory',
                                            options=eventCategoryoptions,
                                            allowClear=True,
                                            style={'width': '100%'},
                                        ),
                                        label='事件分类',
                                        id='eventCategory'
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=10,
                        ),
                    ],
                    id='eventManage-addevent_form',
                    enableBatchControl=True,
                    labelCol={'span': 8},
                    wrapperCol={'span': 16},
                    style={'marginRight': '15px'},
                )
            ],
            id='eventManage-addevent_modal',
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
                                            id='eventManage-updateform-eventKey',
                                            name='eventKey',
                                            placeholder='请输入事件Key',
                                            allowClear=True,
                                            style={'width': '100%'},
                                            autoComplete='off',
                                        ),
                                        label='事件Key',
                                        required=True,
                                        id="eventKey"
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                                id='eventManage-updateform-eventName',
                                                name='eventName',
                                                placeholder='请输入事件名称',
                                                style={'width': '100%'},
                                                autoComplete='off',
                                            ),
                                            label='事件名称',
                                            required=True,
                                            id='eventName'
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
                                            id='eventManage-updateform-eventDesc',
                                            name='eventDesc',
                                            placeholder='请输入事件描述',
                                            allowClear=True,
                                            style={'width': '100%'},
                                            autoComplete='off',
                                        ),
                                        label='事件描述',
                                        id='eventDesc'
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdSelect(
                                            id='eventManage-updateform-eventCategory',
                                            name='eventCategory',
                                            options=eventCategoryoptions,
                                            allowClear=True,
                                            style={'width': '100%'},
                                        ),
                                        label='事件分类',
                                        id='eventCategory'
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=10,
                        ),
                    ],
                    id='eventManage-updateevent_form',
                    enableBatchControl=True,
                    labelCol={'span': 8},
                    wrapperCol={'span': 16},
                    style={'marginRight': '15px'},
                )
            ],
            id='eventManage-updateevent_modal',
            mask=False,
            width=650,
            renderFooter=True,
            okClickClose=True,
        ),
        # 删除用户二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='event-delete-text'),
            id='eventManage-del_modal',
            # visible=False,
            title='提示',
            mask=True,
            renderFooter=True,
            okClickClose=True,
        )
    ]



)

