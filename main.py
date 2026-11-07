"""Main entry point for "If I Am Not Embarrassed, Others Will"."""

from src import World


def main():
    print("=" * 60)
    print("If I Am Not Embarrassed, Others Will")
    print("GitHub Game Off 2026 - Theme: SHIFT")
    print("Two Worlds. One Kingdom. Five Heroes. One Battle for Power.")
    print("=" * 60)
    print()

    # Initialize the game world
    world = World()
    print(world)
    print()

    # Demonstrate the SHIFT mechanic
    print("--- SHIFT DEMONSTRATION ---")
    print(f"Starting in: {world.current_kingdom}")
    print()

    # Shift to Shadow Kingdom
    shadow_kingdom = world.switch_kingdom()
    print(f"Shifted to: {shadow_kingdom}")
    print()

    # Shift back to Living Kingdom
    living_kingdom = world.switch_kingdom()
    print(f"Shifted back to: {living_kingdom}")
    print()

    # Show territory details from current kingdom
    print("--- CURRENT KINGDOM TERRITORIES ---")
    for terr_id, territory in world.current_kingdom.territories.items():
        yield_amount = territory.resource_yield()
        print(f"  {territory.id}: {territory.name} - Yield: {yield_amount}")

    print()
    print("--- RESOURCE YIELD ---")
    total_yield = world.current_kingdom.total_resource_yield()
    print(f"Total resource yield from all territories: {total_yield}")

    print()
    print("=" * 60)
    print("World initialization complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()