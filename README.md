# Butterfly's Garden: A Predictive Pest Outbreak Simulator

## Overview

**Butterfly's Garden** is a strategic simulation framework designed to model, predict, and visualize the cascading effects of climatic events on agricultural pest outbreaks. This project leverages a `Pygame` front-end to serve as an interactive interface for a sophisticated back-end model grounded in complex systems theory and machine learning. The primary objective is to shift pest management from a reactive to a proactive paradigm by allowing users to explore the consequences of their decisions against a data-driven, probabilistic forecast of pest incidence.

The project's name is inspired by the "butterfly effect," where minor, localized perturbations in initial conditions can result in large-scale, non-linear consequences, a principle that lies at the core of our simulation engine.

## Core Scientific & Technical Concepts

The simulation engine is architected upon established scientific and computational principles to ensure a robust and realistic model:

* **Cellular Automata:** The geographical area is modeled as a grid of discrete cells (a cellular automaton). Each cell's state is a high-dimensional vector of environmental variables. The state of each cell `C` at time `t+1` is a function of its own state and the states of its neighboring cells at time `t`, governed by a learned transition function `f`: `C(t+1) = f(C(t), N(C,t))`, where `N` represents the neighborhood.

* **Complex Systems & Emergent Behavior:** Pest outbreaks are not treated as isolated incidents but as emergent properties of a complex adaptive system. The model simulates how simple, local interactions between environmental variables (e.g., soil moisture, heat accumulation) can aggregate and propagate, leading to the non-linear emergence of a large-scale infestation event.

* **Spatiotemporal Predictive Modeling:** The transition rules `f` of the cellular automaton are not manually defined but are learned from historical data using deep learning. The proposed architecture is a **Convolutional LSTM (ConvLSTM)** network. This architecture is uniquely suited for this problem as it combines the feature extraction capabilities of Convolutional Neural Networks (CNNs) for spatial data with the sequence-handling capabilities of Long Short-Term Memory (LSTM) networks for temporal data. It effectively processes the input as "video frames" of geospatial data to predict future frames.

## Data Sources and Technical Methodology

The predictive power of Butterfly's Garden is derived from the integration and analysis of publicly available satellite data, primarily from NASA's Earth Observing System Data and Information System (EOSDIS).

### Key Data Inputs (Features)

Our model's feature set is composed of multiple layers of geospatial time-series data, which together provide a comprehensive view of the agricultural environment's state:

1.  **Soil Moisture & Surface Temperature:** Crucial indicators for plant health and the proliferation rates of specific pests and fungi. Acquired via platforms like **NASA Giovanni**, which provides access to datasets like the Global Land Data Assimilation System (GLDAS).
2.  **Precipitation:** Directly influences humidity, soil moisture, and leaf wetness, all critical factors for fungal pathogens. Also available through **NASA Giovanni**.
3.  **Evapotranspiration (ET):** A key metric for diagnosing water stress in crops. Stressed plants often exhibit lower resistance to pests. The methodology for deriving and applying ET data follows training provided by **NASA's ARSET program**.
4.  **Crop Classification & Canopy Structure:** Using **Synthetic Aperture Radar (SAR)** data (e.g., from Sentinel-1), we can classify crop types and monitor canopy density and biomass. SAR's ability to penetrate clouds makes it a highly reliable data source for continuous monitoring, a technique also detailed in **ARSET training materials**.
5.  **Vegetation Indices (NDVI, EVI):** Standard indices derived from multispectral imagery (e.g., MODIS, Landsat) to monitor plant vigor and photosynthetic activity.

### Methodological Pipeline

1.  **Data Acquisition & Preprocessing:** Time-series data for the above variables are acquired for a specific Area of Interest (AOI) using portals like **NASA Earthdata Search** and the **Giovanni** interface. Data is co-registered, resampled to a common spatial grid, and stacked into data cubes.
2.  **Exploratory Data Analysis (EDA):** **NASA Worldview** is used for visual inspection of spatiotemporal patterns in the raw data, helping to identify anomalies, correlations, and historical outbreak events.
3.  **Model Training:** The ConvLSTM network is trained on the historical data cubes. The model learns to predict the probability of a significant change in the state of a cell (i.e., an outbreak) based on the sequence of preceding multidimensional frames.
4.  **Simulation & Visualization:** The trained model is integrated into the `Pygame` engine. When a user introduces a new climatic event, this event perturbs the initial state of the simulation, and the model forecasts the cascading effects over subsequent time steps.

## Project Structure
```

butterflys-garden/
├── src/
│   ├── main.py        \# Main entry point for the application.
│   ├── game.py        \# Core game loop, state management, and event handling.
│   └── settings.py    \# Centralized module for constants and configuration.
├── requirements.txt   \# Project dependencies.
└── README.md          \# Project documentation.

````

## Foundational Sources

The methodology and data sources for this project are based on tools and knowledge provided by NASA's Applied Sciences and Earthdata programs.

* **NASA ARSET - Agricultural Crop Classification with Synthetic Aperture Radar:** [Link](https://appliedsciences.nasa.gov/get-involved/training/spanish/arset-clasificacion-de-cultivos-agricolas-con-radar-de-apertura)
* **NASA ARSET - Applications of Remote Sensing-Based Evapotranspiration Data:** [Link](https://appliedsciences.nasa.gov/get-involved/training/english/arset-applications-remote-sensing-based-evapotranspiration-data)
* **NASA Giovanni Data Portal:** [Link](https://giovanni.gsfc.nasa.gov/giovanni/)
* **NASA Earthdata - Agriculture and Water Management:** [Link](https://www.earthdata.nasa.gov/topics/human-dimensions/agriculture-production)
* **NASA Worldview Visualization Interface:** [Link](https://worldview.earthdata.nasa.gov)

### Target Variable Data (Pest Incidence)

To train the predictive model in a supervised learning context, the input features (environmental data) must be correlated with a ground truth target variable: historical pest incidence. For the initial prototype focused on Brazil, a single, centralized real-time database for all pest occurrences is not publicly available. Therefore, the project will employ a composite data acquisition strategy, leveraging information from various official and research-based sources to build a historical dataset.

The primary sources for this data include:

* **National-Level Sources:**
    * **Embrapa (Brazilian Agricultural Research Corporation):** Technical publications, scientific articles, and communications are accessed via the Embrapa Information Agency and its Infoteca-e repository to gather research-backed occurrence data.
    * **MAPA (Ministry of Agriculture and Livestock):** Official phytosanitary alerts and technical notes provide information on the national sanitary situation for plants.
    * **Conab (National Supply Company):** Agricultural monitoring bulletins offer insights into regional trends and concerns regarding pest pressure on crops, although the data is not always quantitative.

* **State-Level Sources:**
    * State agricultural defense agencies are often the best sources for more dynamic and localized information. This includes entities such as the Coordenadoria de Defesa Agropecuária (CDA) in São Paulo, the Agência de Defesa Agropecuária do Paraná (Adapar), the Instituto de Desenvolvimento Rural do Paraná (IDR-Paraná), and the Instituto de Defesa Agropecuária do Estado de Mato Grosso (Indea-MT).

> **Note on Geographic Scalability:**
>
> The data collection methodology for pest incidence is initially focused on Brazilian sources. However, the model is designed for global applicability. By integrating with analogous data sources from other countries and regions (such as the USDA in the United States, the EFSA in Europe, or other national plant protection organizations), the **Butterfly's Garden** simulation engine can be readily adapted to provide forecasts for diverse agricultural landscapes worldwide.

## Installation and Usage

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd butterflys-garden
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # .\venv\Scripts\activate  # On Windows
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the application:
    ```bash
    python src/main.py
    ```

## Contributing

Contributions are welcome. Please submit issues for bug reports and feature requests or open pull requests to propose changes.

## License

This project is licensed under the MIT License.
````