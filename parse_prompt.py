import re
import pandas as pd

text = """
Sure, I'll provide prompts for each part of your game plan.

Game Objective:
"Create an image depicting the lovable character Pigsy from the Chinese mythological tale 'Journey to the West', on a quest to find his love, Chang'e, in the Moon Palace. Pigsy is eager to invite Chang'e for a dinner. The image should convey his determination and romantic intention."

Game Background:
"Visualize a hypothetical episode from the ancient Chinese mythology 'Journey to the West'. Pigsy has accidentally found himself in the Moon Palace. He is charmed by Chang'e, the moon goddess, and wants to invite her for dinner. However, Chang'e is somewhere in the labyrinth of the Moon Palace. The image should show Pigsy in the labyrinth of the Moon Palace, with a sense of anticipation and excitement."

Player Items:
1. "Design an image of a 'Gourmet Map', a unique item that will guide Pigsy to the entrance of the Moon Palace.
 It should look ancient and mystical, filled with symbols and signs of various delicacies."
2. "Illustrate a 'Magical Pig Snout', a humorous item that can sniff out delicious food. The snout should be exaggerated and comically depicted, emphasizing its magical abilities."
3. "Generate an image of a 'Pack of Spicy Strips', a popular snack. The pack should be colorful and appetizing,
 indicating its irresistible appeal."
4. "Create an image of a 'Magical Fan', a mythical item in 'Journey to the West'. The fan should look magical and powerful, with intricate designs and symbols."

Game Procedures:
1. "Create a scene where the 'Gourmet Map' is leading Pigsy to the entrance of the Moon Palace. The entrance should be grand and mystical, with the moon shining brightly above it."
2. "Illustrate a scene inside the labyrinth of the Moon Palace, where the 'Magical Pig Snout' is sniffing out the direction towards Chang'e. The labyrinth should look vast and complex, with Pigsy appearing both determined and hopeful."

Humorous & Absurd Elements Explanation:
1. "The 'Magical Pig Snout': This item is full of absurdity and humor. Typically, a pig's snout represents gluttony. The image should capture this humor by showing the snout in action, sniffing out food in the most unexpected places."
"""

prompts = re.findall(r'"([^"]*)"', text)
print(prompts)
