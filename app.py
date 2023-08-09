from dataclasses import dataclass
from itertools import product
from copy import deepcopy
from typing import List

import numpy as np

import streamlit as st


@dataclass
class ActiveLeaders:
    aristoteles: bool =  False
    enheduanna: bool = False
    aganike: bool = False

@dataclass
class Permutation:
    triangle_cards: int
    stone_cards: int
    wheel_cards: int
    fixed_triangle_cards: int
    fixed_stone_cards: int
    fixed_wheel_cards: int

    def increase_highest_card_by_one_if_fixed_card_exist(self):
        
        if self.fixed_stone_cards +  self.fixed_triangle_cards + self.fixed_wheel_cards > 0:
                
            cards = [self.fixed_stone_cards, self.fixed_triangle_cards, self.fixed_wheel_cards]
            highest_id = np.argmax(cards)
            if highest_id == 0:
                self.fixed_stone_cards += 1
            elif highest_id == 1:
                self.fixed_triangle_cards += 1
            else:
                self.fixed_wheel_cards += 1

            print(f"Increased highest id {highest_id} to {self}")

        else:

            print("No fixed cards.")

    def offset_fixed_cards_by_id(self, id: int, offset: int):
        if id == 0:
            self.fixed_triangle_cards += offset
        elif id == 1:
            self.fixed_stone_cards += offset
        elif id == 2:
            self.fixed_wheel_cards += offset
        else:
            raise ValueError("Wrong id.")
        
    def any_card_is_below_zero(self):
        return self.fixed_triangle_cards < 0 or self.fixed_stone_cards < 0 or self.fixed_wheel_cards < 0
    
    def get_total_cards(self):
        return self.triangle_cards + self.fixed_triangle_cards, self.stone_cards + self.fixed_stone_cards, self.wheel_cards + self.fixed_wheel_cards


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

class App:
    active_leaders: ActiveLeaders
    SYMBOL_IDS = [0, 1, 2] # triangles stones wheels

    

    def run(self):

        st.title("Research points calculator")
    
        # Input fields for three numbers
        self.num_fixed_triangles = st.number_input("Enter amount of cards with triangles:", value=0)
        self.num_fixed_stones = st.number_input("Enter amount of cards with stones:", value=0)
        self.num_fixed_wheels = st.number_input("Enter amount of cards with wheels:", value=0)
        self.num_flex_cards = st.number_input("Enter amount of cards with flexible symbols:", value=0)

        has_aristoteles = st.checkbox("Have you played the leader \"ARISTOTELES\"?", value=False)
        has_eheduanna = st.checkbox("Have you played the special leader \"EHEDUANNA\"?", value=False)
        has_aganike = st.checkbox("Have you played the special leader \"AGANIKE\"?", value=False)

        self.active_leaders = ActiveLeaders(has_aristoteles, has_eheduanna, has_aganike)

        total_win_points = self._determine_optimal_symbols()
        
        # Display the sum
        st.write("Total resulting win points:", total_win_points)

    def _determine_optimal_symbols(self):

        permutations = list(product(self.SYMBOL_IDS, repeat=self.num_flex_cards))
        combined_permutations: List[Permutation] = []
        for permutation in permutations:
            triangles, stones, wheels = permutation_to_card_numbers(permutation)
            p = Permutation(triangles, stones, wheels, self.num_fixed_triangles, self.num_fixed_stones, self.num_fixed_wheels)

            if self.active_leaders.enheduanna:
                p.increase_highest_card_by_one_if_fixed_card_exist()
            
            p_default = deepcopy(p)

            combined_permutations.append(p_default)

            if self.active_leaders.aganike:

                transfer_permutations = list(product([0, 1, 2], repeat=2))

                for t_permutation in transfer_permutations:

                    p_temp = deepcopy(p)

                    source_id = t_permutation[0]
                    target_id = t_permutation[1]

                    # transfer cards
                    p_temp.offset_fixed_cards_by_id(source_id, -1)
                    p_temp.offset_fixed_cards_by_id(target_id, +1)

                    if p_temp.any_card_is_below_zero():
                        pass
                    else:
                        combined_permutations.append(p_temp)


            


        total_win_points_for_each_permutation = []

        for permutation in combined_permutations:

            triangles, stones, wheels = permutation.get_total_cards()
            total_win_points = self._calculate_research_win_points(triangles, stones, wheels)
            total_win_points_for_each_permutation.append(total_win_points)

        max_permutation_ids = np.argmax(total_win_points_for_each_permutation)
        print(max_permutation_ids)

        best_permutation: Permutation = combined_permutations[max_permutation_ids]
        print(best_permutation)

        triangles, stones, wheels = best_permutation.get_total_cards()

        total_win_points = self._calculate_research_win_points(
            triangles, 
            stones, 
            wheels,
            )
        
        st.write("Flex cards for triangles / stones / wheels:", best_permutation.triangle_cards, best_permutation.stone_cards, best_permutation.wheel_cards)
        st.write("Total cards for triangles / stones / wheels:", triangles, stones, wheels)

        
        return total_win_points
    
    def _calculate_research_win_points(self, num_cards_symbol_a: int, num_cards_symbol_b: int, num_cards_symbol_c: int) -> int:

        if self.active_leaders.aristoteles:
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
        

if __name__ == "__main__":
    app = App()
    app.run()
