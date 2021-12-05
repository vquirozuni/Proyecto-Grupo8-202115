from datetime import datetime
import settings
import boto3
from botocore.exceptions import ClientError

sqs = boto3.resource('sqs',
                     region_name='us-east-1',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    aws_session_token=settings.AWS_SESSION_TOKEN)


def build_pack(path, file_name, old_format, id):
    return {
        "id": {'StringValue': str(id), 'DataType': 'String'},
        "file_name": {'StringValue': file_name, 'DataType': 'String'},
        "old_format": {'StringValue': old_format, 'DataType': 'String'},
        "path": {'StringValue': path, 'DataType': 'String'},
    }


def send_message(queue, message_body, message_attributes):
    """
    Send a message to an Amazon SQS queue.
    :param queue: The queue that receives the message.
    :param message_body: The body text of the message.
    :param message_attributes: Custom attributes of the message. These are key-value
                               pairs that can be whatever you want.
    :return: The response from SQS that contains the assigned message ID.
    """

    try:
        response = queue.send_message(
            MessageBody=message_body,
            MessageAttributes=message_attributes
        )
        print(f"[{datetime.now()}] message Send: {message_body}")
        return response
    except ClientError as error:
        print(f"[{datetime.now()}] Send message failed: {message_body}")


def delete_messages(queue, messages):
    """
    Delete a batch of messages from a queue in a single request.
    :param queue: The queue from which to delete the messages.
    :param messages: The list of messages to delete.
    :return: The response from SQS that contains the list of successful and failed
             message deletions.
    """
    try:
        entries = [{
            'Id': str(ind),
            'ReceiptHandle': msg.receipt_handle
        } for ind, msg in enumerate(messages)]
        response = queue.delete_messages(Entries=entries)
        if 'Successful' in response:
            for msg_meta in response['Successful']:
                print(
                    f"[{datetime.now()}] Deleted {messages[int(msg_meta['Id'])].body}")
        if 'Failed' in response:
            for msg_meta in response['Failed']:
                print(
                    "Could not delete %s",
                    messages[int(msg_meta['Id'])].body
                )
    except ClientError:
        print("Couldn't delete messages from queue %s", queue)
    else:
        return response


def receive_messages(queue, max_number, wait_time):
    """
    Receive a batch of messages in a single request from an SQS queue.
    :param queue: The queue from which to receive messages.
    :param max_number: The maximum number of messages to receive. The actual number
                       of messages received might be less.
    :param wait_time: The maximum time to wait (in seconds) before returning. When
                      this number is greater than zero, long polling is used. This
                      can result in reduced costs and fewer false empty responses.
    :return: The list of Message objects received. These each contain the body
             of the message and metadata and custom attributes.
    """
    try:
        messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=max_number,
            WaitTimeSeconds=wait_time
        )
        for msg in messages:
            print(
                f"[{datetime.now()}] Received message {msg.message_id}, {msg.body}")
        return messages
    except ClientError as error:
        print(f"[{datetime.now()}] could not receive messages{error}")
