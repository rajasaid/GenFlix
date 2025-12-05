from GenFlix import GenFlix

MIN_MOVIES = 100
MAX_MOVIES = 200
MIN_USERS = 100
MAX_USERS = 200
RATINGS_PER_USER = 5
MAX_RECOMMENDATIONS = 10

def initiate_genflix():
    print('''*** Hi! Welcome to GenFlex! *** 
    
Here you can generate your own video platform and get an understanding of movie recommendation and statistics!

Let's get started!''')

    while True:
        try:
            users_amount = int(input(f'Choose the amount of users on the platform (between {MIN_USERS} and {MAX_USERS}): '))
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
            genflix.Start_Genflix()
            main_menu(genflix)
            break
        break


def main_menu(genflix):
    print("*** Now when it is on set, let’s dive into the data! ***")
    while True:
        print("""
    What do you want to do:
      Get user info            (u)
      Get movie info           (m)
      Look at graphs           (g)
      Regenerate sample        (r)
      Exit                     (x)
    """)

        user_choice = input("Choose an option: ").strip().lower()

        match user_choice:
            case "u":
                genflix.find_user_data()
            case "m":
                genflix.find_movie_data()
            case "g":
                try:
                    genflix.plot_distribution_graphs()
                except Exception as e:
                    print("❌ Error while plotting graph:", repr(e))
            case "r":
                genflix.Start_Genflix()
            case "x":
                print("Goodbye!")
                break
            case _:
                print("❌ Invalid option. Please try again.")

def user_menu(genflix, user_id):
    recommendations_amount = 0
    while True:
        print("""
    What do you want to do:
      Get user recommendations (r)
      Show Trend of ratings    (t)
      Show Trend of Genres     (g)           
      Exit                     (x)
    """)
        user_choice = input("Choose an option: ").strip().lower()
        match user_choice:
            case "r":
                recommendations_amount = get_rec_amount()
                recommendation_list = genflix.recommend_movies_to_user(user_id, recommendations_amount)
                print(f"Here are {recommendations_amount} top movies for {genflix.users[user_id-1].name}")
                for i in range(len(recommendation_list)):
                    print(f"{i+1}. {recommendation_list[i]}")
            case "t":
                try:
                    genflix.plot_user_graphs(user_id, "ratings_over_time")        
                except Exception as e:
                    print("❌ Error while plotting graph:", repr(e))
            case "g":
                try:
                    genflix.plot_user_graphs(user_id, "genres_over_time")
                except Exception as e:
                    print("❌ Error while plotting graph:", repr(e))
            case "x":
                print("Goodbye!")
                break
            case _:
                print("❌ Invali d option. Please try again.")

def movie_menu(genflix, movie_title):
    while True:
        print("""
    What do you want to do:
      Get similar movies       (r)
      Exit                     (x)
    """)
        user_choice = input("Choose an option: ").strip().lower()
        match user_choice:
            case "r":
                recommendations_amount = get_rec_amount()
                recommendation_list = genflix.recommend_similar_movies(movie_title, recommendations_amount)
                print(f"Here are {recommendations_amount} similar movies for '{movie_title}'")
                for i in range(len(recommendation_list)):
                    print(f"{i + 1}. {recommendation_list[i]}")

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