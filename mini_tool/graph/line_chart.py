from mini_tool.graph.base_chart import ChartFrame, Line, opts
from mini_tool.common import random_name


class LineChart(ChartFrame):

    def __init__(self, parent, x=None, y=None, title="折线图示例", html_path=None):
        filename = random_name()
        self.html_name = filename
        self.html_path = html_path
        self.x = x
        self.y = y
        self.title = title
        ChartFrame.__init__(self, parent, title, filename)

    def read_html(self):
        html_path = self.html_path or self.build_html()
        return html_path

    def build_html(self):
        line = Line(init_opts=opts.InitOpts(width="500px", height="300px"))
        line.add_xaxis(self.x.to_list())
        self.add_yaxis(line)
        line.set_global_opts(
            title_opts=opts.TitleOpts(title=self.title),
            toolbox_opts=opts.ToolboxOpts(
                is_show=True,  # 是否显示该工具
                orient="vertical",  # 工具栏 icon 的布局朝向
                pos_left="right"  # 工具栏组件离容器左侧的距离
            ),
            # 区域缩放
            datazoom_opts=opts.DataZoomOpts(
                is_show=True,  # 是否显示 组件。如果设置为 false，不会显示，但是数据过滤的功能还存在
                type_="slider",  # 组件类型，可选 "slider", "inside"
                orient="horizontal"  # 可选值为：'horizontal', 'vertical'
            ),
            # 提示
            tooltip_opts=opts.TooltipOpts(
                is_show=True,  # 是否显示提示框组件，包括提示框浮层和 axisPointer。
                # 触发类型。可选：
                # 'item': 数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用。
                # 'axis': 坐标轴触发，主要在柱状图，折线图等会使用类目轴的图表中使用。
                # 'none': 什么都不触发
                trigger="item",
            )
        )

        html_path = line.render(self.html_name)
        return html_path

    def add_yaxis(self, line):
        for column_name in self.y.columns:
            line.add_yaxis(column_name, self.y[column_name].to_list())
