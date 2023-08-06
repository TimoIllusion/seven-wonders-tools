
import streamlit as st


def calculate_research_win_points(num_cards_symbol_a: int, num_cards_symbol_b: int, num_cards_symbol_c: int) -> int:

    set_points = min((num_cards_symbol_a, num_cards_symbol_b, num_cards_symbol_c)) * 7

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
    num1 = st.number_input("Enter amount of cards with triangles:", value=0)
    num2 = st.number_input("Enter amount of cards with stones:", value=0)
    num3 = st.number_input("Enter amount of cards with wheels:", value=0)
    
    # Calculate the sum
    total_win_points = calculate_research_win_points(num1, num2, num3)
    
    # Display the sum
    st.write("Total win points:", total_win_points)

if __name__ == "__main__":
    main()
