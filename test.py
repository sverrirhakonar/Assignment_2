# In test_loader.py
from PriceLoader import PriceLoader # Assuming your class is in PriceLoader.py
import time

if __name__ == "__main__":
    print("Initializing PriceLoader...")
    loader = PriceLoader()

    print("Calling get_prices()...")
    start_time = time.time()
    
    # This is the main call to your class method
    price_data = loader.get_prices()
    
    end_time = time.time()
    print(f"Data loading took {end_time - start_time:.2f} seconds.")

    # Verification steps
    if not price_data.empty:
        print("\nSuccessfully loaded data!")
        print("DataFrame shape:", price_data.shape)
        print("\nFirst 5 rows of data:")
        print(price_data.head())
        print("\nLast 5 rows of data:")
        print(price_data.tail())
    else:
        print("\nError: Data loading failed, returned an empty DataFrame.")