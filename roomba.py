import requests,urllib.parse,getpass,logging,argparse
from AwsRequest import AwsRequest

class IrobotAuthorization:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        response = requests.get("https://disc-prod.iot.irobotapi.com/v1/discover/endpoints?country_code=US")
        res_json = response.json()

        deployment = res_json['deployments'][next(iter(res_json['deployments']))]
        self.httpBase = deployment['httpBase']
        iotBase = deployment['httpBaseAuth']
        iotUrl = urllib.parse.urlparse(iotBase)
        self.iotHost = iotUrl.netloc
        region = deployment['awsRegion']

        self.apikey = res_json['gigya']['api_key']
        self.gigyaBase = res_json['gigya']['datacenter_domain']

        data = {"apiKey": self.apikey,
                "targetenv": "mobile",
                "loginID": self.username,
                "password": self.password,
                "format": "json",
                "targetEnv": "mobile",
                }

        response = requests.post(
            "https://accounts.%s/accounts.login" % self.gigyaBase, data=data)
        res_json = response.json()

        uid = res_json['UID']
        uidSig = res_json['UIDSignature']
        sigTime = res_json['signatureTimestamp']

        data = {
            "app_id": "ANDROID-C7FB240E-DF34-42D7-AE4E-A8C17079A294",
            "assume_robot_ownership": "0",
            "gigya": {
                "signature": uidSig,
                "timestamp": sigTime,
                "uid": uid,
            }
        }

        response = requests.post("%s/v2/login" % self.httpBase, json=data)
        res_json = response.json()
        access_key = res_json['credentials']['AccessKeyId']
        secret_key = res_json['credentials']['SecretKey']
        session_token = res_json['credentials']['SessionToken']
        self.data = res_json

        self.amz = AwsRequest(region, access_key, secret_key,
                              session_token, "execute-api")
        
        
    def get_details(self):
        return self.data['robots']
    
    def get_credentials(self):
        robot_keys = self.data['robots'].keys()
        device_id = next(iter(robot_keys))

       # password = self.data['robots']['password']
        return device_id


    def get_maps(self, robot):

        r = (self.amz.get(self.iotHost, '/v1/%s/pmaps' % robot, query="activeDetails=2")).json()
        pmaps = []
        for map_dict in r:
            pmap_id = map_dict['pmap_id']
            pmapv_id = map_dict['active_pmapv_details']['active_pmapv']['pmapv_id']
            pmaps.append([pmap_id, pmapv_id])

        return pmaps

    def view_maps(self,robot,pmap,pmapv):
        r = (self.amz.get(self.iotHost, '/v1/%s/pmaps/%s/versions/%s/umf' % (robot,pmap,pmapv), query="activeDetails=2")).json()
        return r
def main():
    loglevel = logging.DEBUG
    LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level=loglevel)
    '''
    irobot = IrobotAuthorization("sJuwnA28H27nnA82@gmail.com","P2p$912#")
    irobot.login()
    maps = (irobot.get_maps("340EE4928078487E853BF9F3180A3898"))
    robotID = irobot.get_credentials()
    pmaps = irobot.get_maps(robotID)
    print(pmaps)
    print(irobot.view_maps(robotID,pmaps[0][0],pmaps[0][1]))
    '''
     
    parser = argparse.ArgumentParser(description="Roomba tool command line interface.")
    
    #parser.add_argument("command", choices=[
    #                    "get_robots"], help="the command to run")
      
    args = parser.parse_args()
    print(f"Please enter your iRobot API credentials to continue:\n")

    username = input("Username: ")
    password = getpass.getpass(prompt="Password: ")
    '''
    '''
    irobot_auth = IrobotAuthorization(username,password)
    irobot_auth.login()
    while True:

        print("Available commands:\n")
        print("1. Get robot details")
        print("2. Roomba map details")
        print("3. Quit\n")

        command = input("Enter command number: \n")

        if command == "1":
            robot = irobot_auth.get_details()
            print(robot)

        elif command == "2":
            robotID = irobot_auth.get_credentials()
            robot = irobot_auth.get_maps(robotID)
            if len(robot) == 1:
                print(robot[0])
            else:
                while True:
                    print("Available maps:\n")
                    for i, map in enumerate(robot):
                        print(f"{i+1}. {map}")
                    print(f"{len(robot)+1}. Go back")
                    subcommand = input("Enter map number: ")
                    if subcommand.isdigit() and int(subcommand) in range(1, len(robot)+2):
                        subcommand = int(subcommand)
                        if subcommand == len(robot)+1:
                            break
                        else:
                            pmap_id, pmapv_id = robot[subcommand-1]
                            print(pmap_id, pmapv_id)
                            view_map = input("Do you want to view the map? (y/n)\n")
                            if view_map == "y":
                                print(irobot_auth.view_maps(robotID, pmap_id, pmapv_id))
                            break
                    else:
                        print("Invalid command. Please enter a valid command number.\n")
        elif command == "3":
            
            print("You have successfully logged out.")
            break
        else:
            print("Invalid choice. Please enter a valid choice.")
    
if __name__ == '__main__':

    main()
