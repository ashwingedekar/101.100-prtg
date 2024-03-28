# Import pandas package 
import pandas as pd 

# Lists of top 5 batsmen for each format 
test_batsmen = ['Virat Kohli', 'Steve Smith', 'Kane Williamson', 
									'Joe Root', 'David Warner'] 
odi_batsmen = ['Virat Kohli', 'Rohit Sharma', 'Joe Root', 
							'David Warner', 'Babar Azam'] 
t20_batsmen = ['Babar Azam', 'Aaron Finch', 'Colin Munro', 
						'Lokesh Rahul', 'Fakhar Zaman'] 

# Define a dictionary containing ICC rankings for batsmen 
rankings_batsmen = {'test': test_batsmen, 
					'odi': odi_batsmen, 
					't20': t20_batsmen} 

# Convert the dictionary into DataFrame 
rankings_batsmen_pd = pd.DataFrame(rankings_batsmen) 

# Increment the index so that index 
# starts at 1 (starts at 0 by default) 
rankings_batsmen_pd.index += 1

print(rankings_batsmen_pd) 
