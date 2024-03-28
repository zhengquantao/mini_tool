from mini_tool.graph.base_chart import ChartFrame, Scatter, opts
from mini_tool.common import random_name


class ScatterChart(ChartFrame):

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
        data = [
            [10.0, 8.04],
            [8.0, 6.95],
            [13.0, 7.58],
            [9.0, 8.81],
            [11.0, 8.33],
            [14.0, 9.96],
            [6.0, 7.24],
            [4.0, 4.26],
            [12.0, 10.84],
            [7.0, 4.82],
            [5.0, 5.68],
        ]
        data.sort(key=lambda x: x[0])
        x_data = [d[0] for d in data]
        y_data = [d[1] for d in data]

        html_path = (
            Scatter()
                .add_xaxis(xaxis_data=x_data)
                .add_yaxis(
                series_name="",
                y_axis=y_data,
                symbol_size=20,
                label_opts=opts.LabelOpts(is_show=False),
            )
                .set_series_opts()
                .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
                ),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
                tooltip_opts=opts.TooltipOpts(is_show=False),
            )
                .render("basic_scatter_chart.html")
        )

        return html_path

    def add_yaxis(self, line):
        for column_name in self.y.columns:
            line.add_yaxis(column_name, self.y[column_name].to_list())
