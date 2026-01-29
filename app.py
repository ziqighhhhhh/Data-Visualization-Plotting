import os
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


CATALOG = [
    {
        "id": "v1",
        "name": "月–季–年三层级柱状对比图",
        "description": "对比月 / 季 / 年结构与趋势",
        "image_url": "https://github.com/user-attachments/assets/98e3a031-2cde-41a4-bdaa-98b0ae217035",
        "script": "月-季-年三层级柱状对比图.py",
    },
    {
        "id": "v2",
        "name": "消费总量环形柱状图",
        "description": "总量 + 结构的同图表达",
        "image_url": "https://github.com/user-attachments/assets/6496ad02-93d3-4445-84c1-72a9ef36559e",
        "script": "消费总量环形柱状图.py",
    },
    {
        "id": "v3",
        "name": "3D 瀑布图",
        "description": "多时间维度销售结构",
        "image_url": "https://github.com/user-attachments/assets/4b909597-cdc0-40f9-ae9e-c714138b7935",
        "script": "3D瀑布图.py",
    },
    {
        "id": "v4",
        "name": "图基悬挂根图",
        "description": "当前分布 vs 历史基准分布",
        "image_url": "https://github.com/user-attachments/assets/da64ceac-0e50-4b9e-8b4a-05fc055fb2d0",
        "script": "图基悬挂根图.py",
    },
    {
        "id": "v5",
        "name": "扇形预测区间图",
        "description": "不确定性随时间扩散",
        "image_url": "https://github.com/user-attachments/assets/b126d0e0-d3d3-4d8a-a093-624ea8fb9740",
        "script": "扇形预测区间图.py",
    },
    {
        "id": "v6",
        "name": "事件时间线图",
        "description": "事件 / 节点 / 里程碑叙事",
        "image_url": "https://github.com/user-attachments/assets/a6a2e399-3bbb-489c-8da8-fb55d0e8596d",
        "script": "事件时间线图.py",
    },
    {
        "id": "v7",
        "name": "复合气泡图与饼图",
        "description": "年份、总量、结构占比、类别分布",
        "image_url": "https://github.com/user-attachments/assets/91ade8cb-6721-4a81-9149-6f803e2acf92",
        "script": "复合气泡图和饼图.py",
    },
    {
        "id": "v8",
        "name": "蝴蝶条形图",
        "description": "左右镜像对比结构",
        "image_url": "https://github.com/user-attachments/assets/1a9a4e32-2a05-4c81-9bf2-4de62522a9dd",
        "script": "蝴蝶条形图.py",
    },
    {
        "id": "v9",
        "name": "旭日图",
        "description": "国家 → 品类层级结构",
        "image_url": "https://github.com/user-attachments/assets/c7e3de87-5881-4055-93cb-baf504e34c8c",
        "script": "旭日图.py",
    },
    {
        "id": "v10",
        "name": "比例面积图",
        "description": "面积对比占比",
        "image_url": "https://github.com/user-attachments/assets/3c6181e2-a3bf-4b83-a4df-69cd5d460717",
        "script": "比例面积图.py",
    },
    {
        "id": "v11",
        "name": "极坐标面积图",
        "description": "12个月分面 + 多品类堆叠",
        "image_url": "https://github.com/user-attachments/assets/4fd9d1a3-4155-483d-9b39-6ce396d9e4ef",
        "script": "极坐标图.py",
    },
    {
        "id": "v12",
        "name": "Marimekko 图",
        "description": "矩形面积代表贡献",
        "image_url": "https://github.com/user-attachments/assets/5bf85fc4-e79a-40c3-88b9-034afabfa474",
        "script": "Marimekko图.py",
    },
    {
        "id": "v13",
        "name": "柱线组合图",
        "description": "规模 + 增速双轴",
        "image_url": "https://github.com/user-attachments/assets/2a9c6741-b2bc-434e-8019-08a0dbcce534",
        "script": "柱线组合图.py",
    },
    {
        "id": "v14",
        "name": "饼中饼",
        "description": "主类占比 + 子类拆解",
        "image_url": "https://github.com/user-attachments/assets/4f1fd7a8-f0c8-42e5-ab8f-b82b799ba9b4",
        "script": "饼中饼.py",
    },
    {
        "id": "v15",
        "name": "表格 + 条形数据条",
        "description": "表格读数 + 视觉排序",
        "image_url": "https://github.com/user-attachments/assets/90069421-4d3a-4b76-a839-3856b186fdb9",
        "script": "表格 + 条形数据条.py",
    },
    {
        "id": "v16",
        "name": "用户转化漏斗图",
        "description": "流量/线索/转化漏斗",
        "image_url": "https://github.com/user-attachments/assets/fa066404-5024-497b-8892-7e18b75f8a34",
        "script": "漏斗图 .py",
    },
    {
        "id": "v17",
        "name": "堆叠进度条形图 + 达成率折线图",
        "description": "结构进度 + 目标达成率",
        "image_url": "https://github.com/user-attachments/assets/bb1d889b-aa13-4956-a561-d483665dbe15",
        "script": "堆叠进度条形图 + 达成率折线图 .py",
    },
    {
        "id": "v18",
        "name": "分组柱状图 + 同比变化",
        "description": "两期对比 + 增长信息",
        "image_url": "https://github.com/user-attachments/assets/7662a446-af4f-4464-8594-9a612991aa32",
        "script": "分组柱状图 + 同比变化 .py",
    },
    {
        "id": "v19",
        "name": "多面板年度对比仪表式柱状图",
        "description": "规模 + 增长 + 结构 + 指标",
        "image_url": "https://github.com/user-attachments/assets/1af10919-43d8-467c-a33c-10fca146ef6d",
        "script": "多面板年度对比仪表式柱状图 .py",
    },
    {
        "id": "v20",
        "name": "渐变山峰面积图",
        "description": "趋势强弱与波动节奏",
        "image_url": "https://github.com/user-attachments/assets/04083b76-f29a-4e6f-8c99-ddb0f2ca39a7",
        "script": "渐变山峰面积图.py",
    },
]


st.set_page_config(page_title="图表方法库", layout="wide")

st.title("图表方法库与在线绘图")
st.markdown(
    "这个页面汇总了仓库中的可视化方法，并提供上传数据快速绘图的入口。"
)

catalog_tab, upload_tab = st.tabs(["方法总览", "上传数据绘图"])

with catalog_tab:
    st.subheader("方法总览")
    st.markdown("点击图片可查看示例，右侧显示对应脚本名称。")
    for chunk_start in range(0, len(CATALOG), 3):
        chunk = CATALOG[chunk_start : chunk_start + 3]
        columns = st.columns(len(chunk))
        for column, item in zip(columns, chunk):
            with column:
                st.markdown(
                    f"""
                    <a href="{item['image_url']}" target="_blank">
                      <img src="{item['image_url']}" style="width: 100%; border-radius: 8px;" />
                    </a>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(f"**{item['name']}**")
                st.caption(item["description"])
                st.code(item["script"], language="text")

with upload_tab:
    st.subheader("上传数据绘图")
    st.markdown(
        "上传 CSV 或 Excel 文件即可快速生成常见图表。复杂图形可以参考对应脚本进行二次定制。"
    )

    uploaded_file = st.file_uploader("上传数据文件", type=["csv", "xlsx", "xls"])
    if uploaded_file:
        file_suffix = os.path.splitext(uploaded_file.name)[1].lower()
        try:
            if file_suffix == ".csv":
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)
        except Exception as exc:  # noqa: BLE001
            st.error(f"读取文件失败: {exc}")
            st.stop()

        if data.empty:
            st.warning("文件为空，无法绘图。")
            st.stop()

        st.markdown("**数据预览**")
        st.dataframe(data.head(20), use_container_width=True)

        numeric_columns: List[str] = data.select_dtypes(include="number").columns.tolist()
        if not numeric_columns:
            st.warning("未检测到数值列，请检查文件内容。")
            st.stop()

        x_column = st.selectbox("X 轴字段", options=data.columns.tolist())
        y_columns = st.multiselect(
            "Y 轴数值字段 (可多选)",
            options=numeric_columns,
            default=numeric_columns[:1],
        )

        chart_type = st.selectbox(
            "图表类型",
            options=["折线图", "柱状图", "面积图", "散点图"],
        )

        if st.button("生成图表"):
            if not y_columns:
                st.warning("请至少选择一个数值字段。")
            else:
                fig, ax = plt.subplots(figsize=(9, 4.8))
                if chart_type == "折线图":
                    data.plot(x=x_column, y=y_columns, ax=ax, marker="o")
                elif chart_type == "柱状图":
                    data.plot(x=x_column, y=y_columns, ax=ax, kind="bar")
                elif chart_type == "面积图":
                    data.plot(x=x_column, y=y_columns, ax=ax, kind="area", alpha=0.7)
                else:
                    y_column = y_columns[0]
                    ax.scatter(data[x_column], data[y_column], alpha=0.8)
                    ax.set_ylabel(y_column)
                    ax.set_xlabel(x_column)

                ax.set_title(f"{chart_type} - {', '.join(y_columns)}")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig, clear_figure=True)
