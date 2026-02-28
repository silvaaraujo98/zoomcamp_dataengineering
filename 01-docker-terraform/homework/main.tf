provider "google" {
  project = "armas-388817"
  region  = "us-central1"
  zone    = "us-central1-c"
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = "test"
  friendly_name               = "test"
  description                 = "This is a test description"
  location                    = "EU"
  default_table_expiration_ms = 3600000

  labels = {
    env = "default"
  }
  }