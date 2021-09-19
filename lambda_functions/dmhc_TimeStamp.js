// Handler called by IoT Analytics - pipeline dmhc_host_pipeline
exports.handler = function handler(event, context, callback) {
    
        //Add timestamp to incoming data and name it "server_time"
        event[0].server_time = Date.now();
        
        // Return the data        
        callback(null, event);
};
