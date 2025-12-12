from ..core.service import GenFlix
from ..core.service import GenFlixService
from ..models.user import User
from ..models.movie import Movie
from ..plotting.ratings_graphs import GraphGenerator
from ..plotting.user_graphs import UserGraphGenerator


MIN_MOVIES = 100
MAX_MOVIES = 200
MIN_USERS = 100
MAX_USERS = 200
RATINGS_PER_USER = 25
MAX_RECOMMENDATIONS = 10

def initiate_genflix():
    print("""
    ============================================================
                         *** WELCOME TO GENFLIX ***
    ============================================================

    Here you can generate your own video platform and explore
    how movie recommendations and analytics are built.

    Let's get started.


    ------------------------------------------------------------
    """)

    while True:
        try:
            users_amount = int(input(
                f"Choose the amount of users on the platform "
                f"(between {MIN_USERS} and {MAX_USERS}): "
            ))
            if not (MIN_USERS <= users_amount <= MAX_USERS):
                raise ValueError("Number out of range")

        except ValueError:
            print("❌ Invalid input. Please enter an integer within the correct range.")
            continue

        while True:
            try:
                movies_amount = int(input(f'Choose the amount of movies on the platform (between {MIN_MOVIES} and {MAX_MOVIES}): '))
                if not (MIN_MOVIES <= movies_amount <= MAX_MOVIES):
                    raise ValueError("Number out of range")

            except ValueError:
                print("❌ Invalid input. Please enter an integer within the correct range.")
                continue

            ratings_amount = users_amount * RATINGS_PER_USER
            genflix = GenFlix(users_amount, movies_amount, ratings_amount)
            genflix_service = GenFlixService(genflix)
            input("\nPress ENTER to continue...")
            main_menu(genflix_service)
            break
        break


def main_menu(genflix_service: GenFlixService)  -> None:
    print("*** Now when it is on set, let’s dive into the data! ***")
    while True:
        print("""
        ============================================================
                                  MAIN MENU
        ============================================================

        What do you want to do:

            [U]  GET USER INFO
            [M]  GET MOVIE INFO
            [G]  VIEW GRAPHS
            [R]  REGENERATE SAMPLE
            [X]  EXIT

        ------------------------------------------------------------
        """)

        user_choice = input("Choose an option: ").strip().lower()

        match user_choice:
            case "u":
                user_id = genflix_service.find_user_data()  # we will make this return the ID
                if user_id:
                    input("\nPress ENTER to continue...")
                    user_menu(genflix_service, user_id)
            case "m":
                movie_title = genflix_service.find_movie_data()  # returns a title
                if movie_title:
                    input("\nPress ENTER to continue...")
                    movie_menu(genflix_service, movie_title)
            case "g":
                try:
                    df = genflix_service.get_ratings_dataframe()
                    graph_gen = GraphGenerator(df)
                    graph_gen.plot_main_graph()
                except Exception as e:
                    print("❌ Error while plotting graph:", repr(e))
            case "r":
                genflix_service.restart()
                input("\nPress ENTER to continue...")
            case "x":
                print("Goodbye!")
                break
            case _:
                print("❌ Invalid option. Please try again.")

def user_menu(genflix_service:GenFlixService, user_id: int)  -> None:
    while True:
        print("""
        ============================================================
                                  USER MENU
        ============================================================

        What do you want to do:

            [R]  USER RECOMMENDATIONS
            [T]  TREND OF RATINGS
            [G]  TREND OF GENRES
            [X]  EXIT

        ------------------------------------------------------------
        """)
        user_choice = input("Choose an option: ").strip().lower()
        match user_choice:
            case "r":
                try:
                    recommendations_amount = get_rec_amount()
                    recommendation_list = genflix_service.recommend_movies_to_user(user_id, recommendations_amount)

                    title = f"Top {recommendations_amount} Movies for {genflix_service.get_user_name(user_id)}"
                    print_recommendations(title, recommendation_list)

                    input("\nPress ENTER to continue...")
                    for i in range(len(recommendation_list)):
                        print(f"{i+1}. {recommendation_list[i]}")
                except Exception as e:
                    print("❌ Error while getting recommendations:", repr(e))        
            case "t":
                try:
                    user_graph_service = UserGraphGenerator(
                        genflix_service.get_ratings_dataframe(),
                        genflix_service.genflix.users[user_id - 1]
                    )
                    user_graph_service.plot_user_graph(user_id, "ratings_over_time")      
                except Exception as e:
                    print("❌ Error while plotting graph:", repr(e))
            case "g":
                try:
                    user_graph_service = UserGraphGenerator(
                        genflix_service.get_ratings_dataframe(),
                        genflix_service.genflix.users[user_id - 1]
                    )
                    user_graph_service.plot_user_graph(user_id, "genres_over_time")
                except Exception as e:
                    print("❌ Error while plotting graph:", repr(e))
            case "x":
                print("Goodbye!")
                break
            case _:
                print("❌ Invali d option. Please try again.")

def movie_menu(genflix_service:GenFlixService, movie_title: str)  -> None:
    while True:
        print("""
        ============================================================
                                  MOVIE MENU
        ============================================================

        What do you want to do:

            [R]  SIMILAR MOVIES
            [X]  EXIT

        ------------------------------------------------------------
        """)
        user_choice = input("Choose an option: ").strip().lower()
        match user_choice:
            case "r":
                try:
                    recommendations_amount = get_rec_amount()
                    recommendation_list = genflix_service.recommend_similar_movies(movie_title, recommendations_amount)

                    title = f"{recommendations_amount} Similar Movies for '{movie_title}'"
                    print_recommendations(title, recommendation_list)

                    input("\nPress ENTER to continue...")
                    for i in range(len(recommendation_list)):
                        print(f"{i + 1}. {recommendation_list[i]}")
                except Exception as e:
                    print("❌ Error while getting recommendations:", repr(e))
            case "x":
                print("Goodbye!")
                break
            case _:
                print("❌ Invali d option. Please try again.")

def get_rec_amount():
    while True:
        try:
            recommendations = int(
                input(f'Choose the number of recommendations you want to get (between 1 and {MAX_RECOMMENDATIONS}): ')
            )
            if not (1 <= recommendations <= MAX_RECOMMENDATIONS):
                raise ValueError("Number out of range")
            return recommendations
        except ValueError:
            print("❌ Invalid input. Please enter an integer within the correct range.")



def print_recommendations(title:str, rec_list: list[str])  -> None:

    # Determine final box width for PyCharm (looks best around 90)
    BOX_WIDTH = 90

    # Build top box line
    print("\n" + "┌" + "─" * BOX_WIDTH + "┐")
    print("│" + f"{title.upper():^{BOX_WIDTH}}" + "│")
    print("└" + "─" * BOX_WIDTH + "┘\n")

    # Print recommendation list
    if not rec_list:
        print("  No recommendations found.\n")
        return

    for i, movie in enumerate(rec_list, start=1):
        print(f"   {i:>2}. {movie}")

    print("\n" + "─" * (BOX_WIDTH + 2) + "\n")