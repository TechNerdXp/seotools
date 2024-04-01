

# SEO Tools 🔍🛠️

Initially being developed for splitting keywords into specs using OpenAI API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Pls make sure Pyton and Node js are installed on your machine.

### Installation

Clone the project and cd into the project dir and run these commands.
`cd client`
`npm install`
`npm run build`
`cd ../  # Go back to the main directory`
`pip install -r requirements.txt`

Create an Open AI API key and an Assistant ID for the prompt pls check prompt section or create your own.
Rename the `.example_env` file to `.env`
Update your OpenAI API key and Assistant ID

Run `py setup.py`

### Running the app

Run `py app.py` It'll run on port 5000 by default

### Setting Up Your Keywords CSV File:

Create a CSV file named keywords.csv and ensure that the first column contains all the keywords you wish to process.

### Uploading Your File:

Navigate to the local interface at http://127.0.0.1:5000.
Go to the ‘Files’ section.
Select and upload your keywords.csv file.

### Processing Your Keywords:

Once uploaded, initiate the processing procedure.
The system will analyze each keyword and segregate them into specific attributes. These attributes will be outputted in a new CSV file named specs.csv, which you can find linked in the ‘Uploaded Files’ table.

### Additionally Compressing Your Specifications:

To condense the specs.csv file into a more compact format, establish a mapping for each specification and its corresponding column in the compressed CSV.
Execute the compression operation. This will generate a compressed.csv file that consolidates all specifications according to the established mapping.

### Accessing Mappings:

Initially, we need to access the mapping for an individual file record from files table.
For a comprehensive view of mappings across all files, simply visit the mapping path without specifying a particular file context.

Using the interface go to 

### Some Helpfull Commands
`ngrok http --domain=proud-moral-seal.ngrok-free.app 5000 --host-header="localhost:5000"`
`pip install -r requirements.txt`
`pip freeze > requirements.txt`

### Prompt 

Input: You are provided with a keyword  (product title)
Task: Split the title into the following components:
- Name: The name of the product.
- Category: The category or type of the product.
- Specs: A dictionary containing relevant specifications or features of the product.
Output: Return a JSON response with the extracted information, consistently using the same names for categories and specs across all responses.

Pls try to process all the keywords their might be some out of shape keywords if you really don't know what to do only then refuse to process.

### Author 

https://github.com/technerdxp