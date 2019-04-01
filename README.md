# DynamicUIRestAPI  
## Forecast Weather  
This application provides the Dynamic UI for the weather forecast application.  
Rest Webservices already developed are used from RestWSAndSwagger2 [https://github.uc.edu/koppuka/RestWSAndSwagger2]. Check this git repository's README.md for any further reference.

### Setup application in EC2 AWS 

* Create a folder at your convenient location and clone the repository.  
* Sign in to your AWS Account.  
* Follow the User guide documentation to launch Amazon EC2 Linux Instance.  
  [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#ec2-launch-instance]  
* Once your instance is in running state, check if the status checks are passed. Then, connect to your instance using putty.  
[https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html]  
* Set up WinSCP to transfer files to your Linux instance. Steps are provided in the above link.  
* Once connected to WinSCP, transfer the project folder DynamicUIRestAPI to /home/ec2-user/  

### Run your Application in Cloud
Now, set the current directory to /home/ec2-user/DynamicUIRestAPI/ in EC2 Console opened via putty.  
`cd /home/ec2-user/DynamicUIRestAPI/`  

Run `sudo python app.py`  
Now, Flask starts serving your app at port 80 by default.  
`app.run(host="0.0.0.0", port = 80)`  

### Access HomePage
Once your web server is up and running, use your public ip to access the homepage.  
This can be fetched from Description tab of Instances screen in EC2 console.

### Available Options for User:
1. Get All Dates of Weather Information Available  
2. Get Weather of a Particular Day  
3. Add/Update Weather Information for a Day  
4. Delete Existing Weather Information for a Day  
5. Forecast Weather  
Select the the operation to be done and give the inputs if necessary then hit submit to get the corresponding output.  
