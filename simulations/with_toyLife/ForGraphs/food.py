from dataclasses import dataclass
from pathlib import Path

from ForGraphs.data_frames import get_food_df


@dataclass(kw_only=True)
class _FoodData:
    amount_of_food: int
    food_len: int
    number_of_1: int
    mean_of_1: float
    percentage_of_1: float


def write_food_data(folder_path: Path, food_data: _FoodData) -> None:
    """Writes the food data into the Readme.md file.

    Args:
        folder_path (Path): the data folder we are looking at.
        food (int): the food parameter.
    """

    with open(folder_path / "Readme.md", "a") as readme:
        readme.write("---  \n")
        readme.write("## Food Data  \n")
        for key, value in food_data.__dict__.items():
            readme.write(f"{key} = {value}  \n")


def food_statistics(folder_path: Path) -> _FoodData:
    """This function reads the food.csv file and returns the data in a _FoodData object.

    Args:
        dir_path (Path): the path to the data folder.

    Returns:
        _FoodData: a dataclass with the food data.
    """
    df = get_food_df(folder_path)
    food_len = len(df.iloc[0]["Binary"])
    amount_of_food = len(df)

    total_slots = food_len * amount_of_food

    df["1_count"] = df["Binary"].apply(lambda x: x.count("1"))
    df["0_count"] = food_len - df["1_count"]

    number_of_1 = df["1_count"].sum()
    mean_of_1 = df["1_count"].mean()

    percentage_of_1 = number_of_1 / total_slots

    return _FoodData(
        amount_of_food=amount_of_food,
        food_len=food_len,
        number_of_1=number_of_1,
        mean_of_1=mean_of_1,
        percentage_of_1=percentage_of_1,
    )


def main(folder_path: Path) -> None:
    food_object = food_statistics(folder_path)
    write_food_data(folder_path, food_object)
