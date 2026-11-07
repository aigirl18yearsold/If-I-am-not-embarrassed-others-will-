"""
World module for "If I Am Not Embarrassed, Others Will".

Defines the two dimensions (Living Kingdom and Shadow Kingdom),
their territories, resources, and the SHIFT mechanic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple


class KingdomType(Enum):
    """The two dimensions that exist side by side."""
    LIVING = "living"  # The Living Kingdom: build, expand, develop settlements
    SHADOW = "shadow"  # The Shadow Kingdom: explore, discover, alternate routes


class TerrainType(Enum):
    """Types of terrain that can exist in territories."""
    GRASS = "grass"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    LAKE = "lake"
    SHRINES = "shrines"
    SHADOW_RUINS = "shadow_ruins"


@dataclass
class Resource:
    """A resource type with a name and description."""
    name: str
    base_value: int = 1  # Base yield per turn
    description: str = ""

    def __str__(self) -> str:
        return self.name


@dataclass
class Territory:
    """A territory within a kingdom, defined by its terrain and resources."""
    id: str
    name: str
    kingdom: KingdomType
    terrain: TerrainType
    resources: List[Resource] = field(default_factory=list)
    level: int = 1  # Territory development level
    population: int = 0  # Population working the land
    controlled_by: Optional[str] = None  # Player ID or "neutral"

    def resource_yield(self) -> int:
        """Calculate total resource yield from this territory."""
        total = sum(r.base_value for r in self.resources)
        # Higher level territories produce more
        total *= self.level
        return max(1, total)

    def __str__(self) -> str:
        return f"{self.name} ({self.terrain.value})"


@dataclass
class Kingdom:
    """Represents one of the two dimensions a player can rule."""
    id: str
    name: str
    kingdom_type: KingdomType
    territories: Dict[str, Territory] = field(default_factory=dict)
    capital: Optional[Territory] = None
    resources: Dict[Resource, int] = field(default_factory=dict)  # resource -> amount
    turn_count: int = 0

    def add_territory(self, territory: Territory) -> None:
        """Add a territory to this kingdom."""
        self.territories[territory.id] = territory
        if self.capital is None:
            self.capital = territory

    def get_territory(self, territory_id: str) -> Optional[Territory]:
        """Get a territory by ID."""
        return self.territories.get(territory_id)

    def total_resource_yield(self) -> int:
        """Get total resource yield from all territories."""
        total = 0
        for territory in self.territories.values():
            total += territory.resource_yield()
        return total

    def shift_dimension(self) -> Kingdom:
        """Shift to the opposite dimension.

        In the SHIFT mechanic, moving between dimensions reveals
        different opportunities and threats.
        """
        if self.kingdom_type == KingdomType.LIVING:
            from . import world as w
            return w.Kingdom(
                id=f"{self.id}-shadow",
                name=f"{self.name} (Shadow)",
                kingdom_type=KingdomType.SHADOW,
            )
        return self

    def __str__(self) -> str:
        return f"{self.name} ({self.kingdom_type.value})"


# Pre-defined territories for initial game setup
def create_living_kingdom() -> Kingdom:
    """Create the Living Kingdom with initial territories."""
    kingdom = Kingdom(id="living-1", name="Living Kingdom", kingdom_type=KingdomType.LIVING)

    # Starting territories
    starting_territories = [
        Territory(
            id="living-01",
            name="Springfield Plains",
            kingdom=KingdomType.LIVING,
            terrain=TerrainType.GRASS,
            resources=[Resource(name="food", base_value=2)],
        ),
        Territory(
            id="living-02",
            name="Oakhaven Forest",
            kingdom=KingdomType.LIVING,
            terrain=TerrainType.FOREST,
            resources=[Resource(name="wood", base_value=2)],
        ),
        Territory(
            id="living-03",
            name="Silverleaf Meadows",
            kingdom=KingdomType.LIVING,
            terrain=TerrainType.GRASS,
            resources=[Resource(name="food", base_value=1)],
        ),
        Territory(
            id="living-04",
            name="Stoneheart Mountains",
            kingdom=KingdomType.LIVING,
            terrain=TerrainType.MOUNTAIN,
            resources=[Resource(name="stone", base_value=2)],
        ),
        Territory(
            id="living-05",
            name="Crystal Lake",
            kingdom=KingdomType.LIVING,
            terrain=TerrainType.LAKE,
            resources=[Resource(name="water", base_value=1)],
        ),
    ]

    for territory in starting_territories:
        kingdom.add_territory(territory)

    return kingdom


def create_shadow_kingdom() -> Kingdom:
    """Create the Shadow Kingdom with initial territories."""
    kingdom = Kingdom(id="shadow-1", name="Shadow Kingdom", kingdom_type=KingdomType.SHADOW)

    # Starting territories
    starting_territories = [
        Territory(
            id="shadow-01",
            name="Whispering Mist",
            kingdom=KingdomType.SHADOW,
            terrain=TerrainType.FOREST,
            resources=[Resource(name="essence", base_value=2)],
        ),
        Territory(
            id="shadow-02",
            name="Ebonvale Ruins",
            kingdom=KingdomType.SHADOW,
            terrain=TerrainType.SHRINES,
            resources=[Resource(name="dark_essence", base_value=3)],
        ),
        Territory(
            id="shadow-03",
            name="Moonlit Caves",
            kingdom=KingdomType.SHADOW,
            terrain=TerrainType.LAKE,
            resources=[Resource(name="moonstone", base_value=2)],
        ),
        Territory(
            id="shadow-04",
            name="Voidwald",
            kingdom=KingdomType.SHADOW,
            terrain=TerrainType.FOREST,
            resources=[Resource(name="shadowstuff", base_value=1)],
        ),
        Territory(
            id="shadow-05",
            name="Starlight Peaks",
            kingdom=KingdomType.SHADOW,
            terrain=TerrainType.MOUNTAIN,
            resources=[Resource(name="starlight_shards", base_value=3)],
        ),
    ]

    for territory in starting_territories:
        kingdom.add_territory(territory)

    return kingdom


# World state management
class World:
    """Manages the overall game world state, including both kingdoms."""

    def __init__(self) -> None:
        self.living_kingdom = create_living_kingdom()
        self.shadow_kingdom = create_shadow_kingdom()
        self.current_kingdom: Kingdom = self.living_kingdom
        self.turn: int = 0

    def switch_kingdom(self) -> Kingdom:
        """Switch between Living and Shadow Kingdom (SHIFT mechanic)."""
        if self.current_kingdom.kingdom_type == KingdomType.LIVING:
            self.current_kingdom = self.shadow_kingdom
        else:
            self.current_kingdom = self.living_kingdom
        self.turn += 1
        return self.current_kingdom

    def get_current_territory(self, territory_id: str) -> Optional[Territory]:
        """Get a territory from the current kingdom."""
        return self.current_kingdom.get_territory(territory_id)

    def add_territory_to_current(self, territory: Territory) -> None:
        """Add a territory to the current kingdom."""
        self.current_kingdom.add_territory(territory)

    def current_resources(self) -> Dict:
        """Get resources from the current kingdom."""
        return dict(self.current_kingdom.resources)

    def __str__(self) -> str:
        return (
            f"World State:\n"
            f"  Turn: {self.turn}\n"
            f"  Current Dimension: {self.current_kingdom}\n"
            f"  Living Kingdom: {self.living_kingdom.name} ({len(self.living_kingdom.territories)} territories)\n"
            f"  Shadow Kingdom: {self.shadow_kingdom.name} ({len(self.shadow_kingdom.territories)} territories)"
        )