import random

from mini_tool.graph.base_chart import ChartFrame, Bar3D, opts
from mini_tool.common import random_name


class D3Chart(ChartFrame):

    def __init__(self, parent, x=None, y=None, title="折线图示例"):
        filename = random_name()
        self.html_name = filename
        self.x = x
        self.y = y
        self.title = title
        ChartFrame.__init__(self, parent, title, filename)

    def read_html(self):
        html_path = self.build_html()
        return html_path

    def build_html(self):
        x_data = y_data = list(range(10))

        def generate_data():
            data = []
            for j in range(10):
                for k in range(10):
                    value = random.randint(0, 9)
                    data.append([j, k, value * 2 + 4])
            return data

        bar3d = Bar3D()
        for _ in range(10):
            bar3d.add(
                "",
                generate_data(),
                shading="lambert",
                xaxis3d_opts=opts.Axis3DOpts(data=x_data, type_="value"),
                yaxis3d_opts=opts.Axis3DOpts(data=y_data, type_="value"),
                zaxis3d_opts=opts.Axis3DOpts(type_="value"),
            )
        bar3d.set_global_opts(title_opts=opts.TitleOpts("Bar3D-堆叠柱状图示例"))
        bar3d.set_series_opts(**{"stack": "stack"})
        bar3d.render("bar3d_stack.html")

        html_path = bar3d.render("bar3d_stack.html")
        return html_path

    def add_yaxis(self, line):
        for column_name in self.y.columns:
            line.add_yaxis(column_name, self.y[column_name].to_list())
