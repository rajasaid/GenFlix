## test and do the application of GenFlix
from GenFlix import GenFlix

def main():
    # Initialize GenFlix with desired numbers
    genflix = GenFlix(number_of_users=10, number_of_movies=20, number_of_ratings=50)
    
    # Generate data
    genflix.Start_Genflix()
    
    # Print generated data for verification
    print("Generated Users:")
    for user in genflix.users:
        user.print_details()
        print("-" * 40)
    
    print("\nGenerated Movies:")
    for movie in genflix.movies:
        print(movie)
    
    print("\nGenerated Ratings:")
    for rating in genflix.ratings:
        print(rating)
    
    movies = genflix.recommend_movies_to_user(1, 5)
    print("\nRecommended Movies for User ID 1:")
    for movie in movies:
        print(movie)
    # get recommendations similar to Firm serve as example
    print(genflix.movies[0])
    movies_similar_to_firm = genflix.recommend_similar_movies(genflix.movies[0].title, 5)
    print("\nMovies similar to 'Firm serve':")
    for movie in movies_similar_to_firm:
        print(movie)
if __name__ == "__main__":
    main()