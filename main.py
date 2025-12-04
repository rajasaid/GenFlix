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

if __name__ == "__main__":
    main()