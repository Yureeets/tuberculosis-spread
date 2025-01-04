# Tuberculosis Spread Simulation

This project is a simulation of the spread of tuberculosis using agent-based modeling, built
with [MESA](https://mesa.readthedocs.io/en/stable/) and [Dash](https://dash.plotly.com/). It provides an interactive
dashboard to visualize the movement and infection dynamics of agents over time across different cities.

## Features

- **Agent-Based Modeling:** Simulates individual agents with different states: susceptible, latent, infected, and
  deceased.
- **City-Specific Simulation:** Allows users to simulate tuberculosis spread in various cities.
- **Dynamic Visualization:** Visualize agent movement on a map and track infection trends over time with interactive
  graphs.
- **Restart & Pause Simulation:** Control the simulation's progress with buttons to pause, restart, or toggle between
  cities.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd tuberculosis-simulation
2. Install dependencies (you should use python=3.11):
    ```bash
    pip install -r requirements.txt
3. Download or ensure access to city graph data using **loadgraph.py**

## Usage

1. Run the application:
    ```bash
    python app.py
2. Open your browser and navigate to http://127.0.0.1:8050/.
3. Use the dropdown to select a city and click the "Start Simulation" button to begin

## Simulation Dashboard

The dashboard consists of the following components:

1. **City Selection**
   A dropdown menu to select a city for the simulation.
2. **Agent Map**
   A map-based visualization of agents, color-coded by their current health status:
   Susceptible: Default state of agents.
   Latent: Carriers of tuberculosis but not infectious.
   Infected: Actively infectious agents.
   Deceased: Agents who have succumbed to the disease.
3. **Graphs**
   Infected Count Plot: Tracks the number of infected agents over time.
   Latent Count Plot: Tracks the number of latent agents over time.
   Susceptible Count Plot: Tracks the number of susceptible agents over time.
4. **Simulation Controls**
   Start/Pause Simulation: Toggles the simulation on or off.
   Restart Simulation: Resets the simulation for the selected city.
   Configuration
   The simulation can be customized by editing the following files:

## File Structure

   ```bash
   tuberculosis-simulation/
   ├── app.py # Main application file for the Dash dashboard
   ├── model.py # VirusModel class implementing the simulation
   ├── agent.py # Definition of the Person agent
   ├── settings.py # Configuration settings for the simulation
   ├── loadgraph.py # Data loader for city-specific graph data
   ├── requirements.txt # Python dependencies
   └── README.md # Project documentation
   ```

## How It Works
1. Initialization:
The VirusModel is initialized with agents placed at positions based on city graph data.
2. Agent States:
Agents can transition between the states Susceptible, Latent, Infected, and Deceased based on predefined probabilities.
3. Simulation Steps:
The simulation progresses in daily steps, updating agent states and positions.
4. Visualization:
Agent data is visualized on a map and tracked in time-series graphs.
5. Dependencies
MESA for agent-based modeling.
Dash for interactive visualizations.
Plotly for creating dynamic plots.
Other Python libraries such as pandas, numpy, and random.
6. Customization

## You can customize the simulation by:

1. Adding cities: Extend all_nodes and cities_data with new cities.
2. Changing infection dynamics: Modify the _infect_agents and _initialize_agents methods in model.py.
3. Updating visuals: Adjust marker sizes, colors, or opacity in the get_agent_data method.

## Contact

For any inquiries, feedback, or suggestions, feel free to reach out:

- **LinkedIn:** [Yurii Polulikh](https://www.linkedin.com/in/yurii-polulikh/)

I’m happy to help or collaborate on related projects!