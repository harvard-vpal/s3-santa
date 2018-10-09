import random
import math

adjs = [
    "autumn", "hidden", "misty", "silent", "empty", "dry", "dark",
    "summer", "icy", "quiet", "white", "cool", "spring", "winter",
    "patient", "twilight", "crimson", "wispy", "weathered", "blue",
    "billowing", "broken", "cold", "damp", "falling", "frosty", "green",
    "long", "bold", "morning", "crimson","rainbow",
    "red", "rough", "still", "small", "sparkling", "shy",
    "wandering", "withered", "wild", "black", "solitary",
    "fragrant", "aged", "snowy", "proud", "floral", "restless",
    "polished", "ancient", "purple", "lively", "nameless"
 ]
nouns = [
    "waterfall", "river", "breeze", "moon", "rain", "wind", "sea", "morning",
    "snow", "lake", "sunset", "pine", "shadow", "leaf", "dawn", "glitter",
    "forest", "hill", "cloud", "meadow", "sun", "glade", "bird", "brook",
    "butterfly", "bush", "dew", "dust", "field", "fire", "flower", "firefly",
    "feather", "grass", "haze", "mountain", "night", "pond", "darkness",
    "snowflake", "silence", "sound", "sky", "shape", "surf", "thunder",
    "violet", "water", "wildflower", "wave", "water", "resonance", "sun",
    "wood", "cherry", "tree", "fog", "frost", "paper",
    "frog", "star"
]

def generate_name(adjs=adjs, nouns=nouns, separator='-'):
    num = int(math.floor(random.random() * math.pow(2,12)))
    adj = random.choice(adjs)
    noun = random.choice(nouns)
    return '{adj}{separator}{noun}{separator}{num}'.format(
         adj=adj,
         noun=noun,
         num=num,
         separator=separator
     )

if __name__ == "__main__":
    print(generate_name())
