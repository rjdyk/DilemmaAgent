# DilemmaAgent

DilemmaAgent is a minimal viable platform for running game theory experiments with iterated prisoner's dilemma games. This was originally designed as part of my capstone project for BlueDot's AI Safety Fundamentals Course.

## Overview
Users can pit any two strategies against each other, including classical game theory strategies and an AI agent (Claude Haiku).

## Architecture Overview
DilemmaAgent is structured around a modular architecture that allows for easy integration of new strategies and game types. The core components include:
- **Strategies**: Implementations of various game strategies, including classical and AI-based strategies.
- **Game Engine**: Manages the game flow, including rounds, scoring, and strategy interactions.
- **Experiment Runner**: Facilitates running multiple experiments and collecting results for analysis.
- **Storage**: Handles saving and retrieving experiment results, both in a database and as CSV files.

## Repro Instructions
To reproduce the experiments conducted in this project, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/DilemmaAgent.git
   cd DilemmaAgent
   ```

2. **Set Up the Environment**:
   Create a virtual environment and install the required dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Run Experiments**:
   You can run the experiments using the provided script:
   ```bash
   python backend/test_run.py
   ```

## API Integration
DilemmaAgent can be integrated with various AI models for strategy implementation. Currently, it supports integration with Claude Haiku, an AI agent designed for strategic reasoning in the context of the prisoner's dilemma.

To integrate a new strategy, implement the `BaseStrategy` interface and define the required methods for move selection and reasoning.

## Contribution Guidelines
Contributions are welcome! If you would like to contribute to DilemmaAgent, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear messages.
4. Push your branch and create a pull request.

Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## Future Work
For the scope of the AI Safety Fundamentals course, this repo represents a simple MVP but it has the potential to extend to further experimentation. Several promising avenues for future research emerge from this work:
- **Expanding the experiment to include direct communication between AI agents**: Investigate how strategies evolve when agents can communicate their intentions.
- **Testing with larger, more capable models**: Explore the impact of using more advanced AI models on strategy performance.
- **Implementing tournament-style play to better understand strategy evolution**: Create a framework for running tournaments between multiple strategies to analyze their performance over time.
- **Exploring different prompt engineering approaches to encourage more optimal play**: Experiment with various prompts to see how they influence AI decision-making.
- **Investigating the impact of different alignment techniques on strategic behavior**: Study how different alignment methods affect the behavior of AI agents in the game.

### Special Thanks
The [BlueDot Team](https://aisafetyfundamentals.com/) for their support and all my cohort mates for the encouragement.  
Nicky Case's [Evolution of Trust](https://ncase.me/trust/) for being an inspiration for this whole project.