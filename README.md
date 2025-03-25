### Dummy Network Security Phishing Data Model.

#### Requirements
- The -e . In the requirements file is intended to be used by pip instead of pip install -r requirements. This will allow anyone who sets up your project to install all the packages and requirements
- Also, It will make your code modular without relative imports hedache! You can import anything anywhere and it will work.

#### Logging
- We created a custom logger function that will create a timestamped .log file that tracks each run errors or successful runs or whatever information needs to be logged.

#### Exception Handling
- We created a custom exception handler for the entire project that accepts a custom message and returns where exactly the error happened and when and why.

#### MongoDB Atlas
- We'll create a cluster on mongo atlas, this will allow us to store data and actually create the pipeline.
- We created the pipeline using the `push_data.py` file, you can see the collections in the cluster0 in the atlas: [here](https://cloud.mongodb.com/v2#/org/67e2d4523c165050c1738d80/projects)
