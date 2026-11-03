import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


def bar_chart(data, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=data.index.astype(str), y=data.values, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def pie_chart(data, title):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(data.values, labels=data.index.astype(str), autopct="%1.1f%%", startangle=140)
    ax.set_title(title)
    ax.axis("equal")
    fig.tight_layout()
    return fig


def line_chart(data, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data.index.astype(str), data.values, marker="o")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig

