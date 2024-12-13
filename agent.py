import mesa
import random


class Person(mesa.Agent):
    """Agent representing a person in the TB simulation with geographic attributes."""

    SUSCEPTIBLE = "SUSCEPTIBLE"
    LATENT = "LATENT"
    INFECTED = "INFECTED"
    RECOVERED = "RECOVERED"
    DECEASED = "DECEASED"

    def __init__(self, unique_id, model, lat, lon):
        super().__init__(unique_id, model)
        self.status = self.SUSCEPTIBLE
        self.days_infected = 0
        self.lat = lat
        self.lon = lon
        self.contagiousness = 0.0
        self.bacterium_loss_days = None
        self.progression_days = None
        self.infection_rate = 0.4
        self.latent_to_infected_probability = 0.015
        self.mortality_rate = 0.0024
        self.recovery_threshold = 25

    def step(self):
        # Each step is now 10 days.
        if self.status == self.INFECTED:
            self.days_infected += 10
            self.spread_infection()
            self.check_recovery_or_death()
        elif self.status == self.LATENT:
            self.days_infected += 10
            self.check_progression_to_infected()
            self.check_bacterium_loss()

    def spread_infection(self):
        """Spread infection to nearby susceptible agents."""
        neighbors = self.model.space.get_neighbors(self.pos, radius=0.003)

        for neighbor in neighbors:
            if neighbor.status == self.SUSCEPTIBLE:
                if random.random() < self.infection_rate:
                    if random.random() < 0.88:
                        # Transition to LATENT state
                        neighbor.status = self.LATENT
                        neighbor.bacterium_loss_days = random.randint(70, 90)
                    else:
                        # Transition to INFECTED state
                        neighbor.status = self.INFECTED

    def check_progression_to_infected(self):
        """Progress from latent to infected status."""
        if self.progression_days is None:
            self.progression_days = random.randint(30, 50)  # latent period
        if self.days_infected >= self.progression_days:
            if random.random() < self.latent_to_infected_probability:
                self.status = self.INFECTED
                self.days_infected = 0

    def check_bacterium_loss(self):
        """Check for bacterium loss and possible return to susceptible state."""
        if self.bacterium_loss_days is None:
            self.bacterium_loss_days = random.randint(70, 90)
        elif self.days_infected >= self.bacterium_loss_days and random.random() < 0.5:
            self.status = self.SUSCEPTIBLE
            self.days_infected = 0

    def check_recovery_or_death(self):
        """Check for recovery or death from infection."""
        if self.days_infected >= self.recovery_threshold:
            if random.random() < self.mortality_rate:
                self.status = self.DECEASED
            else:
                self.status = self.RECOVERED
            # Reset after recovery or death
            if self.status == self.RECOVERED:
                self.status = self.LATENT
                self.bacterium_loss_days = random.randint(70, 90)
            self.days_infected = 0
