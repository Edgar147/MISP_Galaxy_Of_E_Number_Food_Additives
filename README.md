# MISP Galaxy Of E Number Food Additives

## Context


This project includes scripts and JSON structures to represent E number food additives within MISP galaxies and clusters, developed within the context of an academic MISP project.
The project contributes to the ongoing research and understanding of food safety, particularly regarding the regulation and use of E number food additives.
## Overview

The goal of this project is to scrape food additive data from various sources and to transform this data into MISP galaxy and cluster formats. This allows for better representation and sharing of information regarding food additives that are either approved or banned within the European Union.

Initially, our focus was on identifying and understanding the threats posed by carcinogenic products in our daily lives. We conducted an analysis based on the list of carcinogenic elements provided by the World Health Organization (WHO). This list covered not only elements related to food but also those associated with various activities such as cleaning and work. However, after thorough analysis, we decided to shift our focus from carcinogens to elements commonly used in our daily routines that may pose health risks—specifically, food additives.

In the European Union, food additives are identified by a code starting with the letter 'E,' indicating that they have been evaluated, followed by a number. Over the years, certain E number additives have been banned,but  even though other approved e additives are authorized for use in production, they can still pose health risks. 
So we collected data about all these E additives in this project.

At first, we decided to create 2 galaxies and 2 clusters, the first for approved additives, and the other for banned additives. However, after analyzing the context further, we decided to consolidate our approach and have only one galaxy and one cluster. This decision was made because it provided a more streamlined and cohesive representation of the data, facilitating easier analysis and interpretation.

In the clusters, detailed information is available, including potential dangers, uses, products where they are employed, and whether they can be used in organic products.

For banned additives, most of the information is unavailable because they are no longer used (no products, no need to mention the danger, no need to mention if they are used in organic products).

## Methodology
- Scrape additive names, descriptions, and use cases from sources such as dermnetnz.org and Wikipedia
- Gather additional information about scraped additives from platforms like OpenFoodFacts.org and proe.info
- Generate JSON galaxy and cluster structures adhering to the MISP format.



## Structure

The repository is structured as follows:

- `clusters`: Contains the JSON file representing  cluster of  E food additives.
- `galaxies`: Contains the JSON files representing the galaxy of E food additives.
- `scripts`: Contains Python scripts used to scrape E food additive data and generate the MISP structures.

## Getting Started

To use the scripts provided in this repository, you need to have Python3, BeautifulSoup and Requests installed on your system.

### Clone the repository
```bash
git clone https://github.com/Edgar147/MISP_Galaxy_Of_E_Number_Food_Additives.git
```

### Navigate to the project's script directory
```bash
cd MISP_Galaxy_Of_E_Number_Food_Additives.git/scripts
```

### Install the beautifulSoup
```bash
pip3 install beautifulsoup4
```

### Install the requests
```bash
pip3 install requests
```

### Run the script
```bash
python3 scrap_e_additives.py
```
