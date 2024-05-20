# TDDD96-PUM15


#### Project Overview


This project implements a sound source localization system using various techniques to determine the position of a sound source based on the signals received at multiple microphones. It supports trilateration based on time differences of arrival (TDOA) and amplitude differences (AD), accommodating different environments and accuracy requirements.

## Structure

The project is structured into several directories, each with a specific purpose:

- `cli/`: Contains the main command-line interface for the project.
- `coordinate_conversion/`: Contains scripts for converting coordinates.
- `data-collection/`: Contains scripts for collecting data.
- `positioning/`: Contains scripts and modules related to positioning.
- `realtime-trilateration/`: Contains scripts for real-time trilateration.
- `system_tests/`: Contains system tests for the project.

#### Features
- **Multiple Localization Algorithms:** Supports grid-based, gradient-based, and amplitude difference algorithms to cater to various precision and performance needs.
- **Dynamic Microphone Configuration:** Allows configuration with variable numbers of microphones in different dimensional spaces (2D and 3D).
- **CLI Support:** Features a command-line interface for easy interaction with the system, enabling users to add microphones and sound files dynamically.
- **Performance Optimized:** Includes settings for adjusting the granularity of the search grid and the expansion strategy for robust localization.
- **Extensive Testing Framework:** Utilizes pytest for comprehensive testing across multiple scenarios to ensure reliability and accuracy.


#### Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/chrnas/tddd96-pum15
   cd tddd96-pum15
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

#### Usage
To use the sound source localization system, you need to configure the microphone settings and specify the algorithm to use. Here’s a basic example:

```python
from TDOAMethod import TDOAMethod
from receiver import Receiver

# Setup Microphone Data
mic_data = {
    Receiver([0, 0]): "path_to_file1.wav",
    Receiver([10, 0]): "path_to_file2.wav",
    Receiver([5, 5]): "path_to_file3.wav"
}

# Initialize TDOA Method
tdoa_method = TDOAMethod()

# Configure settings if necessary
tdoa_method.set_setting("algorithm", "grid")

# Find the source
estimated_position = tdoa_method.find_source(mic_data)
print(f"Estimated Source Position: {estimated_position}")
```

#### Testing
This project uses `pytest` for running unit tests. To execute the tests, navigate to the project directory and run:

```bash
pytest
```

#### Contributing
Contributions to this project are welcome! Please fork the repository, make your changes, and submit a pull request. 

#### License
MIT License 
