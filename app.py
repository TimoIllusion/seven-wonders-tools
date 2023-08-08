from itertools import product

import numpy as np

import streamlit as st

SYMBOL_IDS = [0, 1, 2] # triangles stones wheels

def permutation_to_card_numbers(permutation: list):
    triangles, stones, wheels = 0, 0, 0

    for symbol_id in permutation:

        if symbol_id == 0:
            triangles += 1
        elif symbol_id == 1:
            stones += 1
        elif symbol_id == 2:
            wheels += 1
        else:
            raise ValueError(f"Wrong symbol_id in permutation! - > {symbol_id}")

    return triangles, stones, wheels

def calculate_research_win_points(num_cards_symbol_a: int, num_cards_symbol_b: int, num_cards_symbol_c: int, has_leader: bool) -> int:

    if has_leader:
        points_per_set = 10
    else:
        points_per_set = 7

    set_points = min((num_cards_symbol_a, num_cards_symbol_b, num_cards_symbol_c)) * points_per_set

    single_card_points = num_cards_symbol_a ** 2 + num_cards_symbol_b ** 2 + num_cards_symbol_c ** 2

    total_points = set_points + single_card_points

    print("Cards of type A:", num_cards_symbol_a)
    print("Cards of type B:", num_cards_symbol_b)
    print("Cards of type C:", num_cards_symbol_c)

    print("Resulting win points:", total_points)
    return total_points


def main():
    st.title("Research points calculator")
    
    # Input fields for three numbers
    num_fixed_triangles = st.number_input("Enter amount of cards with triangles:", value=0)
    num_fixed_stones = st.number_input("Enter amount of cards with stones:", value=0)
    num_fixed_wheels = st.number_input("Enter amount of cards with wheels:", value=0)
    num_flex_cards = st.number_input("Enter amount of cards with flexible symbols:", value=0)
    has_leader = st.checkbox("Have you played the leader \"ARISTOTELES\"?", value=False)
    
    # Calculate the sum
    if num_flex_cards == 0:
        
        total_win_points = calculate_research_win_points(num_fixed_triangles, num_fixed_stones, num_fixed_wheels, has_leader)

    elif num_flex_cards >= 1:

        permutations = list(product(SYMBOL_IDS, repeat=num_flex_cards))

        total_win_points_for_each_permutation = []

        for permutation in permutations:
            triangles, stones, wheels = permutation_to_card_numbers(permutation)

            triangles += num_fixed_triangles
            stones += num_fixed_stones
            wheels += num_fixed_wheels

            total_win_points = calculate_research_win_points(triangles, stones, wheels, has_leader)
            total_win_points_for_each_permutation.append(total_win_points)

        max_permutation_ids = np.argmax(total_win_points_for_each_permutation)
        print(max_permutation_ids)

        best_permutation = permutations[max_permutation_ids]

        triangles, stones, wheels = permutation_to_card_numbers(best_permutation)

        total_win_points = calculate_research_win_points(
            triangles + num_fixed_triangles, 
            stones + num_fixed_stones, 
            wheels + num_fixed_wheels,
            has_leader
            )
        
        st.write("Optimal flex card triangles / stones / wheels:", triangles, stones, wheels)

    
    # Display the sum
    st.write("Total resulting win points:", total_win_points)

if __name__ == "__main__":
    main()
