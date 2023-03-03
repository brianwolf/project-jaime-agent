from dataclasses import dataclass

@dataclass
class TestClusterResult():
    success: bool
    text: str

    