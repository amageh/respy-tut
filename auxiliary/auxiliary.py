"""This file contains auxiliary function that we use throughout the respy tutorial."""
import matplotlib.pyplot as plt
import pandas as pd


def plot_fishing_grounds(df):
    """Plot choice shares for observables example."""
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    for i, observable in enumerate(["rich", "poor"]):
        df.query("Fishing_Grounds == @observable").groupby(
            "Period"
        ).Choice.value_counts(normalize=True,).unstack().plot.bar(
            width=0.4, stacked=True, rot=0, legend=False, ax=ax[i]
        )
        ax[i].set_title("Fishing grounds: " + observable, pad=10)
        ax[i].xaxis.label.set_visible(False)

    plt.legend(loc="lower center", bbox_to_anchor=(-0.15, -0.3), ncol=2)
    plt.suptitle("Robinson's choices by period", y=1.05)

    plt.show()


def plot_choice_shares(df, friday=False):
    """Plot choice shares."""
    if friday:
        color = ["C0", "C2", "C1"]
        choices = 3
    else:
        color = ["C0", "C1"]
        choices = 2

    fig, ax = plt.subplots()

    df.groupby("Period").Choice.value_counts(normalize=True).unstack().plot.bar(
        stacked=True, ax=ax, color=color
    )

    plt.xticks(rotation="horizontal")

    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.275), ncol=choices)

    plt.show()
    plt.close()


def plot_choice_prob_and_exp_level(df):
    """Plot choices and experience levels."""
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))

    (
        df.groupby("Period")
        .Choice.value_counts(normalize=True)
        .unstack()
        .plot.bar(ax=axs[0], stacked=True, rot=0, title="Choice Probabilities")
    )

    (
        df.groupby("Period")
        .Experience_Fishing.value_counts(normalize=True)
        .unstack()
        .plot.bar(
            ax=axs[1],
            stacked=True,
            rot=0,
            title="Share of Experience Level per Period",
            cmap="Blues",
        )
    )

    axs[0].legend(loc="lower center", bbox_to_anchor=(0.5, -0.4), ncol=2)
    axs[1].legend(loc="right", bbox_to_anchor=(1.3, 0.5), ncol=1, title="Experience")

    plt.show()


def plot_choice_prob(df):
    """Plot choices."""
    fig, ax = plt.subplots()

    df.groupby("Period").Choice.value_counts(normalize=True).unstack().plot.bar(
        stacked=True, ax=ax
    )

    plt.xticks(rotation="horizontal")

    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.275), ncol=2)

    plt.show()
    plt.close()


def plot_choices_kw(example="1994"):
    """Plot models from Keane and Wolpin (1994,1997,2000)."""
    if example == "1994":
        fig, ax = plt.subplots(1, 3, figsize=(15, 5))
        models = ["kw_94_one", "kw_94_two", "kw_94_three"]

    if example == "1997":
        fig, ax = plt.subplots(1, 2, figsize=(15, 5))
        models = ["kw_97_basic", "kw_97_extended"]

    for i, model in enumerate(models):
        df = pd.read_pickle(f"data/choices_{model}.pkl")
        df.plot(
            alpha=0.8,
            stacked=True,
            ax=ax[i],
            legend=False,
            kind="area",
            rot=0,
            title=f"Example model: {model}",
            linewidth=0,
        )
        df.plot(stacked=True, ax=ax[i], legend=False, color="white", linewidth=1, rot=0)
        ax[i].margins(x=0)
        ax[i].spines["right"].set_visible(False)
        ax[i].spines["top"].set_visible(False)

        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        if len(ax) % 2 == 1:
            move_left = -0.7
        else:
            move_left = -0.2
        plt.legend(
            by_label.values(),
            by_label.keys(),
            loc="lower center",
            ncol=len(df.columns),
            bbox_to_anchor=(move_left, -0.25),
            fontsize=12,
        )
    plt.show()


def plot_kw_97_comparison():
    """Plot comparison of KW 97 models and observed data."""
    models = ["kw_97_obs", "kw_97_basic", "kw_97_extended"]
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
    data = {}
    for model in models:
        df = pd.read_pickle(f"data/choices_{model}.pkl")
        data[model] = df
    fig, ax = plt.subplots(2, 3, figsize=(15, 9))
    ax = ax.ravel()
    for i, (choice, color) in enumerate(zip(df.columns, colors)):
        ax[i].plot(
            data["kw_97_obs"][choice], linestyle="dashed", color="k", label="Observed"
        )
        ax[i].plot(
            data["kw_97_basic"][choice],
            linestyle="dotted",
            alpha=0.8,
            color=color,
            label="kw_97_basic",
        )
        ax[i].plot(
            data["kw_97_extended"][choice],
            color=color,
            alpha=0.8,
            label="kw_97_extended",
        )
        ax[i].set_title(choice.capitalize().replace("_", " "))
        ax[i].set_xlabel("Period")
    ax[4].legend(
        loc="lower center", ncol=5, bbox_to_anchor=(-0.3, -0.3), fontsize=12,
    )
    fig.delaxes(ax[5])
    plt.show()
