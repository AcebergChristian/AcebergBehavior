import dash
from dash import html
import feffery_antd_components as fac



tagManage_columns = [
    {'dataIndex': 'key', 'title': 'key', 'renderOptions': {'renderType': 'ellipsis'}},
    {'dataIndex': 'tag_key', 'title': 'tag_key', 'renderOptions': {'renderType': 'ellipsis'}},
    {'dataIndex': 'tag_name', 'title': 'tag_name', 'renderOptions': {'renderType': 'ellipsis'}},
    {'dataIndex': 'value', 'title': 'value', 'renderOptions': {'renderType': 'ellipsis'}},
    {'dataIndex': 'togroup', 'title': 'togroup', 'renderOptions': {'renderType': 'ellipsis'}},
    {'dataIndex': 'datatype', 'title': 'datatype', 'renderOptions': {'renderType': 'ellipsis'}},
    {'dataIndex': 'coverusercount', 'title': 'coverusercount', 'renderOptions': {'renderType': 'ellipsis'}},
    {'dataIndex': 'status', 'title': 'status', 'renderOptions': {'renderType': 'ellipsis'}},
    {'dataIndex': 'createmethod', 'title': 'createmethod', 'renderOptions': {'renderType': 'ellipsis'}},
    {'dataIndex': 'creator', 'title': 'creator', 'renderOptions': {'renderType': 'ellipsis'}},
    {'dataIndex': 'createtime', 'title': 'createtime', 'renderOptions': {'renderType': 'ellipsis'}},
    {'title': '操作', 'dataIndex': 'operation', 'width': 120, 'renderOptions': {'renderType': 'dropdown',
                                                                              'dropdownProps': {'title': '更多'}}}]


tagManage_layout = html.Div(
[
    # tagManage 全局的message
    html.Div(id='tagManage-message'),
    
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
                                                                    id='tagManage-search-tagName',
                                                                    placeholder='请输入标签名称',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 240
                                                                    },
                                                                ),
                                                                label='标签名称',
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
                                                                    id='tagManage-search-createtime',
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
                                                                    id='tagManage-search',
                                                                    type='primary',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-search'
                                                                    ),
                                                                )
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '重置',
                                                                    id='tagManage-reset',
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
                                                id='tagManage-search-form',
                                            )
                                        ],
                                        id='tag-search-form-container',
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
                                                id='tagManage-addtag_btn',
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
                                            id='tagManage-tag_table',
                                            rowSelectionType='checkbox',
                                            rowSelectionWidth=50,
                                            columns=tagManage_columns,
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
                                            id='tagManage-addform-tag_key',
                                            name='tag_key',
                                            placeholder='请输入标签Key',
                                            allowClear=True,
                                            style={'width': '100%'},
                                            autoComplete='off',
                                        ),
                                        label='标签Key',
                                        required=True,
                                        id="tag_key"
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                                id='tagManage-addform-tag_name',
                                                name='tag_name',
                                                placeholder='请输入标签名称',
                                                style={'width': '100%'},
                                                autoComplete='off',
                                            ),
                                            label='标签名称',
                                            required=True,
                                            id='tag_name'
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
                                        fac.AntdSelect(
                                            id='tagManage-addform-togroup',
                                            name='togroup',
                                            options=['活跃度', '用户行为']
                                        ),
                                        label='所属群组',
                                        id='togroup',
                                        
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdSelect(
                                            id='tagManage-addform-datatype',
                                            name='datatype',
                                            options=["string", "number", "boolean"],
                                            allowClear=True,
                                            style={'width': '100%'},
                                        ),
                                        label='数据类型',
                                        id='datatype'
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
                                        fac.AntdSelect(
                                            id='tagManage-addform-createmethod',
                                            name='createmethod',
                                            options=["手动创建","custom"]
                                        ),
                                        label='创建方式',
                                        id='createmethod',
                                        
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdSelect(
                                            id='tagManage-addform-status',
                                            name='status',
                                            options=[{"label": "激活", "value": "active"}, {"label": "未激活", "value": "inactive"}]
                                        ),
                                        label='状态',
                                        id='status',
                                        
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=10,
                        ),
                    ],
                    id='tagManage-addtag_form',
                    enableBatchControl=True,
                    labelCol={'span': 8},
                    wrapperCol={'span': 16},
                    style={'marginRight': '15px'},
                )
            ],
            id='tagManage-addtag_modal',
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
                                            id='tagManage-addform-tag_key',
                                            name='tag_key',
                                            placeholder='请输入标签Key',
                                            allowClear=True,
                                            style={'width': '100%'},
                                            autoComplete='off',
                                        ),
                                        label='标签Key',
                                        required=True,
                                        id="tag_key"
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                                id='tagManage-addform-tag_name',
                                                name='tag_name',
                                                placeholder='请输入标签名称',
                                                style={'width': '100%'},
                                                autoComplete='off',
                                            ),
                                            label='标签名称',
                                            required=True,
                                            id='tag_name'
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
                                        fac.AntdSelect(
                                            id='tagManage-addform-togroup',
                                            name='togroup',
                                            options=['活跃度', '用户行为']
                                        ),
                                        label='所属群组',
                                        id='togroup',
                                        
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdSelect(
                                            id='tagManage-addform-datatype',
                                            name='datatype',
                                            options=["string", "number", "boolean"],
                                            allowClear=True,
                                            style={'width': '100%'},
                                        ),
                                        label='数据类型',
                                        id='datatype'
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
                                        fac.AntdSelect(
                                            id='tagManage-addform-createmethod',
                                            name='createmethod',
                                            options=["手动创建","custom"]
                                        ),
                                        label='创建方式',
                                        id='createmethod',
                                        
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdSelect(
                                            id='tagManage-addform-status',
                                            name='status',
                                            options=[{"label": "激活", "value": "active"}, {"label": "未激活", "value": "inactive"}]
                                        ),
                                        label='状态',
                                        id='status',
                                        
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=10,
                        ),
                    ],
                    id='tagManage-updatetag_form',
                    enableBatchControl=True,
                    labelCol={'span': 8},
                    wrapperCol={'span': 16},
                    style={'marginRight': '15px'},
                )
            ],
            id='tagManage-updatetag_modal',
            mask=False,
            width=650,
            renderFooter=True,
            okClickClose=True,
        ),
        # 删除用户二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='tag-delete-text'),
            id='tagManage-del_modal',
            # visible=False,
            title='提示',
            mask=True,
            renderFooter=True,
            okClickClose=True,
        ),
        
        # 详情modal
        fac.AntdModal(
            # [
            #     html.Div(
            #         id='tagManage-info_chart',
            #         style={'width': '100%', 'height': '100%'}
            #     )
            # ],
            id='tagManage-info_modal',
            mask=True,
            renderFooter=True,
            okClickClose=True,
        )
    ]



)

