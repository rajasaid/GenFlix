# This is GraphGenerator.py Python file
import matplotlib.pyplot as plt
import seaborn as sns
from User import User
import pandas as pd
from GraphGenerator import GraphGenerator

class UserGraphGenerator(GraphGenerator):
    def __init__(self, data_frame: pd.DataFrame, user: User) -> None:
        super().__init__(data_frame)
        self.user = user

    def plot_user_graph(self, user_id: int, graph_type: str) -> None:
        
        if not (user_id == self.user.user_id):
            raise ValueError("❌ user ID Invalid.")  

        match graph_type:
            case "ratings_over_time":
                df = self.data_frame
                user_ratings = df[df["user_id"] == user_id]
                user_ratings = user_ratings.sort_values("date")
                plt.figure(figsize=(12, 6))
                plt.plot(user_ratings["date"], user_ratings["user_rating"], marker='o')
                plt.title(f"Ratings Over Time for {self.user.name}")
                plt.xlabel("Date")
                plt.xticks(rotation=45)
                plt.ylabel("Rating")
                plt.ylim(0, 6)
                plt.grid()
                plt.show()
                plt.pause(1)
                plt.close()
            case "genres_over_time":
                df = self.data_frame
                # choose rows for the user only
                df_user = df[df["user_id"] == user_id].copy()
                # sum = how many movies of each genre watched on that date
                genre_cols = [column for column in df_user.columns if column.startswith("IS_")]
                # --- GROUP BY Year ---
                df_user_year = (
                    df_user
                    .groupby(pd.Grouper(key="date", freq="YE"))[genre_cols]
                    .sum()        # sum = how many movies of each genre watched that year
                )
                # convert to long format for easier plotting
                df_long = df_user_year.reset_index().melt(
                    id_vars="date",
                    value_vars=genre_cols,
                    var_name="genre",
                    value_name="count"
                )

                # drop zeros (days where genre not watched)
                df_long = df_long[df_long["count"] > 0]

                # nicer labels
                df_long["genre"] = df_long["genre"].str.replace("IS_", "")
                plt.figure(figsize=(12, 6))

                sns.scatterplot(
                    data=df_long,
                    x="date",
                    y="genre",
                    hue="count",
                    size="count",
                    palette="viridis",
                    sizes=(20, 200)
                )

                plt.title(f"Genres watched over time Grouped by Year for User {user_id}")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
                plt.pause(1)
                plt.close()
            case _:
                print("❌ Invalid graph type.")
