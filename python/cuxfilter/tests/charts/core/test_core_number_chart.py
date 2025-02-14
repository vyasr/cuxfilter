import pytest
import cuxfilter
from cuxfilter.charts.core.aggregate.core_number_chart import BaseNumberChart
from cuxfilter.layouts import chart_view

from ..utils import initialize_df, df_types

df_args = {"key": [0, 1, 2, 3, 4], "val": [float(i + 10) for i in range(5)]}
dfs = [initialize_df(type, df_args) for type in df_types]
cux_dfs = [cuxfilter.DataFrame.from_dataframe(df) for df in dfs]


class TestBaseNumberChart:
    _datasize_title = "_datasize_indicator_Datapoints Selected"

    def test_variables(self):
        bnc = BaseNumberChart(title="custom_title")

        # BaseChart variables
        assert bnc.x is None
        assert bnc.expression is None
        assert bnc.title == "custom_title"
        assert bnc.aggregate_fn == "count"
        assert bnc.format == "{value}"
        assert bnc.colors == []
        assert bnc.font_size == "18pt"
        assert bnc.chart_type == "number_chart_widget"
        assert bnc.use_data_tiles is True
        assert bnc._library_specific_params == {}
        assert bnc.is_datasize_indicator is True
        assert bnc.name == "_number_chart_widget_custom_title"

    @pytest.mark.parametrize("cux_df", cux_dfs)
    @pytest.mark.parametrize(
        "x, expression, min_, max_",
        [
            (None, None, 0, 5),  # 0, len(df)
            ("key", None, 0, 0),
            (None, "key+val", 0, 0),
        ],
    )
    def test_initiate_chart(self, cux_df, x, expression, min_, max_):
        bnc = BaseNumberChart(x, expression)
        dashboard = cux_df.dashboard(charts=[])
        bnc.initiate_chart(dashboard)

        assert bnc.min_value == min_
        assert bnc.max_value == max_

    @pytest.mark.parametrize("cux_df", cux_dfs)
    @pytest.mark.parametrize("chart, _chart", [(None, None), (1, 1)])
    def test_view(self, cux_df, chart, _chart):
        bnc = BaseNumberChart()
        dashboard = cux_df.dashboard(charts=[])
        bnc.initiate_chart(dashboard)
        bnc.chart = chart
        bnc.title = "title"

        assert str(bnc.view()) == str(chart_view(_chart, title="title"))
