"""
Intergalactic Hitchhiker's Guide Utility

A Python utility that calculates fuel costs in Galactic Credits 
and provides random travel advice for intergalactic travelers.
"""

import logging
import os
import random
from typing import Optional, Tuple


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Custom exception for configuration-related errors."""
    pass


class FuelCostCalculator:
    """Calculate fuel costs for intergalactic travel in Galactic Credits."""

    def __init__(self, base_rate: float = 1.5):
        """
        Initialize the calculator with a base rate per light-year.

        Args:
            base_rate: Base cost in Galactic Credits per light-year (default: 1.5)
        
        Raises:
            ConfigurationError: If base_rate is negative
        """
        if base_rate < 0:
            raise ConfigurationError("Base rate must be non-negative")
        self.base_rate = base_rate

    def calculate_cost(
        self, 
        distance_ly: float, 
        fuel_efficiency: float = 1.0,
        tax_rate: float = 0.1
    ) -> Tuple[float, dict]:
        """
        Calculate the total fuel cost for a journey.

        Args:
            distance_ly: Distance in light-years (must be positive)
            fuel_efficiency: Efficiency multiplier (default: 1.0)
            tax_rate: Galactic tax rate as decimal (default: 0.1 = 10%)

        Returns:
            Tuple of (total_cost, breakdown_dict)

        Raises:
            ConfigurationError: If distance is negative or efficiency <= 0
        """
        if distance_ly < 0:
            raise ConfigurationError("Distance must be non-negative")
        if fuel_efficiency <= 0:
            raise ConfigurationError("Fuel efficiency must be positive")
        
        base_cost = distance_ly * self.base_rate / fuel_efficiency
        tax_amount = base_cost * tax_rate
        total_cost = base_cost + tax_amount

        breakdown = {
            "distance_ly": distance_ly,
            "base_cost": round(base_cost, 2),
            "tax_amount": round(tax_amount, 2),
            "total_cost": round(total_cost, 2),
            "currency": "Galactic Credits"
        }

        logger.info(f"Calculated fuel cost: {breakdown['total_cost']} Galactic Credits")
        
        return total_cost, breakdown


class TravelAdviceGenerator:
    """Generate random travel advice for hitchhikers."""

    def __init__(self):
        self.advice_templates = [
            "Always carry a towel. It's the most important item in the galaxy.",
            "Don't panic! This is just another Tuesday in the cosmos.",
            "If you're lost, try asking a Vogon for directions (but don't expect poetry).",
            "Remember: The universe is bigger than you think.",
            "When traveling through hyperspace, never eat the space food.",
            "A hitchhiker's best friend is a working teleporter.",
            "Check your ship's manual before entering a black hole.",
            "The answer to everything might be 42, but always verify.",
            "Don't trust a planet with more than three moons.",
            "Always tip the space station attendants in Galactic Credits."
        ]

    def get_advice(self) -> str:
        """Return a random piece of travel advice."""
        return random.choice(self.advice_templates)

    def get_multiple_advices(self, count: int = 3) -> list[str]:
        """
        Return multiple pieces of travel advice.

        Args:
            count: Number of advice items to generate (default: 3)

        Returns:
            List of unique advice strings
        
        Raises:
            ConfigurationError: If count is not positive
        """
        if count <= 0:
            raise ConfigurationError("Count must be positive")
        
        return random.sample(self.advice_templates, min(count, len(self.advice_templates)))


def main() -> None:
    """Main function demonstrating the utility."""
    logger.info("Starting Intergalactic Hitchhiker's Guide Utility")

    # Initialize calculator and generator
    calculator = FuelCostCalculator(base_rate=1.5)
    advice_generator = TravelAdviceGenerator()

    print("\n=== INTERGALACTIC HITCHHIKER'S GUIDE UTILITY ===\n")

    # Calculate fuel cost for a journey
    try:
        total_cost, breakdown = calculator.calculate_cost(
            distance_ly=10.5,
            fuel_efficiency=0.8,
            tax_rate=0.15
        )
        
        print("Fuel Cost Calculation:")
        print(f"  Distance: {breakdown['distance_ly']} light-years")
        print(f"  Base Cost: {breakdown['base_cost']} Galactic Credits")
        print(f"  Tax (15%): {breakdown['tax_amount']} Galactic Credits")
        print(f"  Total Cost: {breakdown['total_cost']} Galactic Credits\n")

    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        return

    # Generate travel advice
    print("Travel Advice:")
    for i, advice in enumerate(advice_generator.get_multiple_advices(3), 1):
        print(f"  {i}. {advice}")

    print("\n=== End of Report ===")


if __name__ == "__main__":
    main()