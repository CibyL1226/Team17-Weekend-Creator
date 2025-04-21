import api_request as ar
import time  # To respect API rate limits
import json
import boto3
import datetime
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function that fetches event data from the Ticketmaster API page by page,
    processes it, and stores each page's processed data into an S3 bucket as separate JSON files.
    """
    s3 = boto3.client('s3')
    bucket_name = "ticketmasterdata-tae-v1"  # Your S3 bucket name

    # Check if the bucket exists; if not, create it.
    try:
        s3.head_bucket(Bucket=bucket_name)
        logger.info(f"Bucket {bucket_name} exists.")
    except s3.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        # Bucket not found
        if error_code == '404':
            logger.info(f"Bucket {bucket_name} does not exist. Creating bucket.")
            current_region = boto3.session.Session().region_name
            if current_region == 'us-east-1':
                s3.create_bucket(Bucket=bucket_name)
            else:
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': current_region}
                )
        else:
            logger.error(f"Error checking bucket: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error checking bucket: {e}')
            }

    # Process pages from 1 to 100
    for page in range(1, 101):
        print('page :', page)
        page_events = []  # List to store events for the current page
        
        # Fetch API data for the current page
        data = ar.api_request(page)
        if data and '_embedded' in data:
            list_of_events = data['_embedded']['events']
            for e in list_of_events:
                event_info = {}  # Create a new dictionary for each event
                # Process each key-value pair in the event data
                for key, value in e.items():
                    if key in ['_links', 'pleaseNote', 'info', 'boxOfficeInfo', 'images','seatmap']:
                        continue        
                    elif key == '_embedded':
                        venue_data = e['_embedded']['venues']
                        event_info['venues'] = venue_data
                        continue
                    event_info[key] = value
                page_events.append(event_info)
        else:
            print('no data')

        # Respect API rate limit (max 5 requests per second)
        time.sleep(0.2)

        # Generate a unique filename for this page
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"ticketmasterdata-tae-v1/data/ticketmasterdata_{timestamp}_page-{page}.json"


        # Upload this page's data to S3
        try:
            s3.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=json.dumps(page_events),
                ContentType="application/json"
            )
            logger.info(f"Page {page} data successfully saved to S3 as {file_name}")
        except Exception as e:
            logger.error(f"Error saving page {page} data to S3: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error saving page {page} data to S3: {e}')
            }

    return {
        'statusCode': 200,
        'body': json.dumps('Data saved to S3 successfully for all pages!')
    }
