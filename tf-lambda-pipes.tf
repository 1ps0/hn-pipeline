
provider "aws" {
    access_key = "AKIAIUCFSOUD6IAJZKMQ"
    secret_key = "/wCX5KPA8xz8JBMDiViTis2TcRJ2IsE2LdbYP2en"
    region     = "us-east-1"
}

resource "aws_sqs_hn_scraper" "?" {
    instance = "${aws_instance.example.id}"
}

resource "aws_s3_bucket" "example" {
    bucket = "article-cache"
    acl    = "private"
}

resource "aws_lambda_story_inlet" "example" {
    function_name = "ScraperHNStoryInlet"
}

resource "aws_lambda_story_etl" "example" {
    function_name = "ScraperHNStoryETL"
    handler       = "scraper-hn-inlet.run"
}


# todo make sqs for stories
# todo lambda for pushing to sqs
# todo lambda for consuming from sqs
# todo cloudwatch cron
# todo cloudwatch log pipe for lambdas and sqs
# todo xray?