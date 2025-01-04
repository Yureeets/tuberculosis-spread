import random

import mesa
import numpy as np
from mesa.space import ContinuousSpace
from settings import config
from agent import Person
from settings import config_colors
from loadgraph import cities_data
import math


class VirusModel(mesa.Model):
    def __init__(self, current_city, nodes):
        super().__init__()
        self.current_city = current_city
        self.nodes = nodes
        self.space = ContinuousSpace(config['width'], config['height'], torus=False)
        self.schedule = mesa.time.RandomActivation(self)

        print(current_city)
        if 'Ukraine' in current_city:
            self.latent = True
        else:
            self.latent = False
            self._infect_agents()
        self._initialize_agents(latent=self.latent)


    def _initialize_agents(self, latent=False):
        """Initialize agents in continuous space based on node positions."""
        for _, node_data in self.nodes.iterrows():
            lat, lon = node_data['x'], node_data['y']
            if latent and random.random() < 0.9:
                person = Person(self.next_id(), self, lat, lon,status=Person.LATENT)
            else:
                person = Person(self.next_id(), self, lat, lon)
            self.space.place_agent(person, (lat, lon))  # Using (lat, lon) directly
            self.schedule.add(person)

    def _infect_agents(self):
        """Infect a random agent at the start of the simulation."""
        if self.schedule.agents:
            agent_to_infect = self.random.choice(self.schedule.agents)
            agent_to_infect.status = Person.INFECTED

    def count_state(self, state):
        return int(
            sum(1 for agent in self.schedule.agents if agent.status == state) * cities_data[self.current_city][
                'population'] / len(self.schedule.agents))

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()

    def get_agent_data(self):
        """Get agent positions and statuses for plotting."""
        num_agents = len(self.schedule.agents)
        x_data = np.zeros(num_agents)
        y_data = np.zeros(num_agents)
        colors = np.zeros(num_agents, dtype=object)
        sizes = np.zeros(num_agents)
        opacity = np.zeros(num_agents)
        for i, agent in enumerate(self.schedule.agents):
            x, y = agent.pos
            x_data[i] = x
            y_data[i] = y

            color = config_colors.get(agent.status, 'gray')
            colors[i] = color

            if agent.status == Person.INFECTED:
                sizes[i] = 15
                opacity[i] = 1
            elif agent.status == Person.LATENT:
                sizes[i] = 10
                opacity[i] = 0.4
            else:
                sizes[i] = 8
                opacity[i] = 0.2

        return x_data, y_data, colors, sizes, opacity
