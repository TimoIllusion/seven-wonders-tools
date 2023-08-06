import streamlit as st


def calculate_research_win_points(research_card_distribution: list) -> int:

    assert len(research_card_distribution) == 3, "Needs 3 ints"

    ELEMENT_A = int(research_card_distribution[0])
    ELEMENT_B = int(research_card_distribution[1])
    ELEMENT_C = int(research_card_distribution[2])

    set_points = min((ELEMENT_A, ELEMENT_B, ELEMENT_C)) * 7

    single_card_points = ELEMENT_A ** 2 + ELEMENT_B ** 2 + ELEMENT_C ** 2

    total_points = set_points + single_card_points

    print("Cards of type A:", ELEMENT_A)
    print("Cards of type B:", ELEMENT_B)
    print("Cards of type C:", ELEMENT_C)

    print("Resulting win points:", total_points)
    return total_points


def main():
    st.title("Research points calculator")
    
    # Input fields for three numbers
    num1 = st.number_input("Enter amount of cards with triangles:", value=0)
    num2 = st.number_input("Enter amount of cards with stones:", value=0)
    num3 = st.number_input("Enter amount of cards with wheels:", value=0)
    
    # Calculate the sum
    total_win_points = calculate_research_win_points([num1, num2, num3])
    
    # Display the sum
    st.write("Total win points:", total_win_points)

if __name__ == "__main__":
    main()
