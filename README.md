# Page View Time Series Visualizer

This project is part of the ***Data Analysis with Python*** certification from freeCodeCamp.

## Project Description

The goal of this project is to analyze and visualize time series data representing daily page views on the freeCodeCamp forum.

The dataset covers the period from **May 2016 to December 2019** and is used to identify trends, seasonality, and growth patterns.

The project focuses on:
- data cleaning
- time series transformation
- data visualization using:
  
  a. **line plot** (to show overall trend and growth when displaying daily page views over time)
  
  b. **bar plot** (to help compare seasonal patterns across years when displaying average monthly page views grouped by year)
  
  c. **box plot** (to show trend over time and seasonality more by statistical measures)

The visualizations help reveal patterns such as yearly growth and monthly fluctuations in page views.

## Technologies Used

* Python
* Pandas
* NumPy
* Seaborn
* Matplotlib

## Dataset

https://raw.githubusercontent.com/freeCodeCamp/boilerplate-page-view-time-series-visualizer/refs/heads/main/fcc-forum-pageviews.csv

It contains daily page views when date supposes to be an index.

## How to Run

1. Clone the repository:
   git clone https://github.com/MarekGabriel/FreeCodeCamp_page-view-time-series-visualizer.git

2. Navigate to the project folder:
   cd FreeCodeCamp_page-view-time-series-visualizer

3. Run the script:
   time_series_visualizer.py

## Example Usage

Input:

no input needed (when running time_series_visualizer.py it imports proper data from .csv)

Output:

To be reached when calling functions implemented:
* `time_series_visualizer.draw_line_plot()`
* `time_series_visualizer.draw_bar_plot()`
* `time_series_visualizer.draw_box_plot()`

<p float="left">
  <img src="/lineplot.png" width="250"/>
  <img src="/barplot.png" width="250"/>
  <img src="/boxplots.png" width="350"/>
</p>

## Project Structure

* time_series_visualizer.py — main functions: `draw_line_plot()`, `draw_bar_plot()` & `draw_box_plot()` implementation
* main.py — An entrypoint file to be used in development. It imports main functions implemented and runs unit tests automatically.
* test_module.py — unit tests provided by freeCodeCamp
