import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from math import ceil


class Visualiser:
    def __init__(self, dataframe, products, volume_data):
        self.df = dataframe
        self.products = products
        self.volume_data = volume_data
        new_cols = [col + "_pos" for col in self.volume_data.columns]
        self.volume_data.columns = new_cols

    def __create_graphs(self):
        subplot_titles = ("Pnl", "Positions", *self.products)
        fig = make_subplots(ceil(len(self.products) / 2) + 1, 2, subplot_titles=subplot_titles)

        # PnL plot
        pnl_plot = px.line(self.df, x=self.df.index, y="pnl")
        for trace in pnl_plot.data:
            trace.name = "PnL"
            trace.showlegend = True
            fig.add_trace(trace, col=1, row=1)

        # Positions plot
        labels = [product +"_pos" for product in self.products]
        pos_plot = px.line(self.volume_data, x=self.volume_data.index, y=labels)
        for trace in pos_plot.data:
            fig.add_trace(trace, row=1, col=2)

        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=2)

        # Product price plots
        prod_idx = 0
        for i in range(ceil(len(self.products) / 2)):
            for j in range(2):
                if prod_idx >= len(self.products):
                    break
                graph_labels = [self.products[prod_idx], self.products[prod_idx] + "_bid",
                                self.products[prod_idx] + "_offer"]
                prod_plot = px.line(self.df, x=self.df.index, y=graph_labels)
                for trace_idx, trace in enumerate(prod_plot.data):
                    if trace_idx == 0:
                        trace.name = f"{self.products[prod_idx]} Mid"
                    elif trace_idx == 1:
                        trace.name = f"{self.products[prod_idx]} Bid"
                    else:
                        trace.name = f"{self.products[prod_idx]} Offer"
                    fig.add_trace(trace, row=i + 2, col=j + 1)
                prod_idx += 1

        fig.update_layout(height=300 * (ceil(len(self.products) / 2) + 1))

        return fig

    def display_visualisation(self):
        fig = self.__create_graphs()
        fig.show()
