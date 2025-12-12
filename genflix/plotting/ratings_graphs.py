# This is GraphGenerator.py Python file
import matplotlib.pyplot as plt
import pandas as pd

class GraphGenerator:
    def __init__(self, data_frame: pd.DataFrame) -> None:
        self.data_frame = data_frame

    def plot_main_graph(self):
        df = self.data_frame

        genre_cols = [column for column in df.columns if column.startswith("IS_")]
        genre_counts = df[genre_cols].sum()
        genre_avg_rating = { column: df.loc[df[column] == 1, "user_rating"].mean() for column in genre_cols}

        genres = [column.replace("IS_", "") for column in genre_cols]
        counts = [genre_counts[column] for column in genre_cols]
        avg_ratings = [genre_avg_rating[column] for column in genre_cols]

        fig, ax1 = plt.subplots(figsize=(10, 6))
        # bars - movies count grouped by genre
        ax1.bar(genres, counts)
        ax1.set_xlabel("Genre")
        ax1.set_ylabel("Number of ratings (count)", color="black")
        ax1.tick_params(axis="y", labelcolor="black")
        ax1.set_xticks(range(len(genres)))
        ax1.set_xticklabels(genres, rotation=45, ha="right")

        # plot - genre average rating
        ax2 = ax1.twinx()
        ax2.plot(genres, avg_ratings, marker="o", color="red")
        ax2.set_ylabel("Average rating", color="black")
        ax2.tick_params(axis="y", labelcolor="black")
        ax2.set_ylim(0, 5)  # если рейтинг 1–5

        plt.title("Platform-wide genre distribution & average rating by genre")
        plt.tight_layout()
        plt.show()
        plt.pause(1)
        plt.close(fig)

        return