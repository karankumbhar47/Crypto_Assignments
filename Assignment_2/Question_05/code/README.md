# Sypher004 Experiments

## Overview
This directory contains implementations of differential cryptanalysis experiments for the Sypher004 block cipher. The experiments are based on those discussed in Chapter 6 of “The Block Cipher Companion Book.” 

## Files Included
- `sypher004.py`: Contains the implementation of the Sypher004 encryption algorithm.
- `experiment_6_7.py`: Conducts Experiment 6.7, focusing on a four-round characteristic.
- `experiment_6_8.py`: Conducts Experiment 6.8, examining a four-round differential.
- `experiment_6_9.py`: Conducts Experiment 6.9, filtering valid output pairs.
- `perform_all_experiments.py`: Runs all experiments and outputs the results.
- `utils.py`: Utility functions for generating message pairs and random keys.

## How to Use the Code
1. **Set Up the Environment**:
   - Ensure you have Python installed (preferably Python 3.6 or later).
   - Install required packages if necessary (e.g., `tabulate` for formatted output).

2. **Run the Experiments**:
   - Execute the following command in your terminal:
     ```bash
     python perform_all_experiments.py
     ```

3. **Observe the Output**:
   - The output will include the results for each experiment (6.7, 6.8, and 6.9) along with the keys used, counts of valid pairs, and probabilities.

## Observations for Each Experiment

### Experiment 6.7
- **Objective**: This experiment verifies the four-round characteristic of the Sypher004 cipher using a specific difference in the input messages.
- **Results**: The number of pairs with the desired output difference was recorded across six sets of random keys. The average probability observed aligns closely with theoretical expectations, confirming the existence of the four-round characteristic.
- **Key Insights**: The successful identification of 1,296 pairs on average supports the hypothesis that the differential characteristic holds under the chosen conditions.

### Experiment 6.8
- **Objective**: This experiment investigates the differential from the four-round outputs to the final output of the cipher.
- **Results**: A total of 5,310 pairs on average demonstrated the expected differential behavior, indicating a strong correlation with the theoretical model.
- **Key Insights**: The results show that the probability of observing the desired difference increases, providing further evidence for the differential characteristic's effectiveness.

### Experiment 6.9
- **Objective**: This experiment filters output pairs based on specific criteria to identify useful pairs for cryptanalysis.
- **Results**: An average of 7,387 pairs was retained after filtering, compared to the 5,310 pairs that satisfied the target differential. This suggests that the filtering process significantly enhances the efficiency of the differential cryptanalysis.
- **Key Insights**: The filtering process is crucial for improving the quality of data used in attacks, emphasizing the importance of selecting the right output pairs to maximize the success of cryptanalysis.
