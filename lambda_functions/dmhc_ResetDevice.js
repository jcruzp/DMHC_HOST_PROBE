var AWS = require('aws-sdk');

// Define object AWS IoT Core with endpoint
var iotdata = new AWS.IotData({endpoint: 'a2i2bsijbyml6j-ats.iot.us-west-2.amazonaws.com' });
// Define object AWS SNS for SMS and Slack notifications
var sns = new AWS.SNS();

//Call by AWS EventBridge
exports.handler = async(event, context) => {
    //Prepare json data to send notification msg to Slack
    console.log("Send msg to Slack with topic dmhc_sns_topic...");
    var params = {
        Message:  '{ \
                     "version": "0",\
                     "id":"'.concat(context.awsRequestId).concat('",').concat(' \
                     "detail-type":"Is time to check your health! Please go to DMHC Host Probe.", \
                     "source":"aws.events", \
                     "account": "537233203723", \
                     "time":"'.concat(new Date().toISOString()).concat('",').concat(' \
                     "region": "us-west-2" \
                  }')), 
        Subject: "DMHC HOST Probe",
        TopicArn: "arn:aws:sns:us-west-2:537233203723:dmhc_sns_topic"
    };
    // Publish to SNS dmhc_sns_topic
    sns.publish(params, context.done);
    

    // Create publish parameters for SMS Number
    console.log("Send msg to SMS topic...");
    var params = {
      Message: 'Is time to check your health! Please go to DMHC Host Probe.', 
      PhoneNumber: 'YOUR PHONE NUMBER'
    };
    // Publish to SNS SMS number attach
    sns.publish(params, context.done);

    // Publish to IoT Core topic dmhc/reset
    console.log("Publish in topic dmhc/reset...");
    var params = {
        topic: "dmhc/reset", //send any msg to this topic to reset edukit
        payload: JSON.stringify(event),           
        qos: 0
    };

    //Send reset request to DMHC HOST Probe topic dmhc/reset
    const request = iotdata.publish(params);
    request
        .on('success', () => console.log("Success"))
        .on('error', () => console.log("Error"))
    return new Promise(() => request.send());
};
