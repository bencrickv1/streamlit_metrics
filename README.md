
# Streamlit Demo

This is the front-end / dashboard demo app for the DLUHC National Planning Applications API pilot. In production, this would connect directly to the planning applications database to retrieve and display data. Currently, generated example planning application data is used instead.

## Setup and Deployment

### Connecting to PostgreSQL Database

Database information must be added to .streamlit/secrets.toml: https://docs.streamlit.io/knowledge-base/tutorials/databases/postgresql

### Running the App Locally

The app can be run using the 'streamlit run' command on the entry point file.

`streamlit run Metrics_Overview.py`

Additional options are detailed here: https://docs.streamlit.io/library/advanced-features/configuration

### Deployment to Streamlit

The app can be deployed to Streamlit via GitHub: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app

### Custom Deployment

Other options for deploying Streamlit in other environments are listed here: https://docs.streamlit.io/knowledge-base/tutorials/deploy

For a portable option, Docker deployment is described here: https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker