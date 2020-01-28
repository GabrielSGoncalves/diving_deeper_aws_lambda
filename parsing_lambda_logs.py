import boto3

def parsing_lambda_logs(RequestId, GroupName , StreamName):
    """
    Function that parses Lambda Logs on CloudWatch using boto3
    
    Parameters:
    ===========
    RequestId (str): Unique identifier for each AWS Lambda call
    GroupName (str): Name of the Lambda Function group on CloudWatch
    StreamName (str): Name of the log stream for the Function container
    Return:
    =======
    log_function_msgs (list): List of lines for the RequestID log
    lambda_status (boolean): False if ERROR line is found on the execution
    """

    logging_end = False
    while logging_end ==  False:

         # Parse information from Cloudwatch
        client_logs = boto3.client('logs')
        response_logs = client_logs.get_log_events(
                logGroupName=GroupName,
                logStreamName=StreamName)

        log_events = response_logs.get('events')

        # Parse the Cloudwatch log stream
        log_function_msgs = []
        log_stream = False
        for e in log_events:
            # Check for first line of log for RequestId
            if RequestId in e.get('message') or log_stream == True:
                log_function_msgs.append(e.get('message'))
                log_stream = True
            # Break loop when reaches REPORT line
            if log_stream == True and 'REPORT' in e.get('message'):
                break
        
        # Check if there is an error on function log
        lambda_status = True
        log_error_list = [True if '[ERROR]' in e \
                      else False for e in log_function_msgs ]
        if True in set(log_error_list):
            lambda_status=False

        # Check for the END of execution
        check_report = [True if 'END' in e and RequestId in e\
                      else False for e in log_function_msgs ]
        if True in set(check_report):
            logging_end = True

    return (log_function_msgs, lambda_status)