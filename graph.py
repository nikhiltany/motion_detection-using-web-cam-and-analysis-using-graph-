from motion_detector import df
from bokeh.plotting import figure,show,output_file
import bokeh.layouts
from bokeh.models import HoverTool, ColumnDataSource,FixedTicker

df["Starting_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["Ending_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds=ColumnDataSource(df)

plot=figure(x_axis_type='datetime',height=100,width=500,title="Motion Graph")

plot.sizing_mode="scale_width"

plot.yaxis.minor_tick_line_color=None


hover=HoverTool(tooltips=[("Start: ","@Starting_string"),("End: ","@Ending_string")])
plot.add_tools(hover)


q=plot.quad(left="Start",right="End",bottom=0,top=1,color="skyblue",source=cds)

output_file("Time_Graph.html")

show(plot)
