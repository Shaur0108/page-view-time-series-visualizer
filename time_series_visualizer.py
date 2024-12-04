import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col="date", parse_dates=True)

# Clean data
percentile_2_5 = df['value'].quantile(0.025)
percentile_97_5 = df['value'].quantile(0.975)
df = df[(df['value'] >= percentile_2_5) & (df['value'] <= percentile_97_5)]

# Draw Line Plot
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='blue', linewidth=1)

    # Set the title and labels
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig
    fig.savefig('line_plot.png')
    return fig

# Draw Bar Plot
# Draw Bar Plot
def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Reorder the months to ensure they are plotted in chronological order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)

    # Calculate the average page views per month per year
    df_bar_avg = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Draw the bar plot
    fig, ax = plt.subplots(figsize=(12, 6))
    df_bar_avg.plot(kind='bar', ax=ax)

    # Set the labels and legend
    ax.set_title('Average Daily Page Views by Month')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')

    # Save image and return fig
    fig.savefig('bar_plot.png')
    return fig


# Draw Box Plot
def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box['date']]
    df_box['month'] = [d.strftime('%b') for d in df_box['date']]

    # Draw the box plots using Seaborn
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

    # Year-wise Box Plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # Month-wise Box Plot (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2, order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Save image and return fig
    fig.savefig('box_plot.png')
    return fig

# Main execution
if __name__ == "__main__":
    draw_line_plot()
    draw_bar_plot()
    draw_box_plot()
