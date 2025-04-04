from gns3fy import Gns3Connector

BASE_IP = "http://10.48.229."
GNS3_USER = "gns3"
GNS3_PW = "gns3"

#list of specific projects to delete
PROJECTS_TO_DELETE = ["test1"]
# Read last octets from datastore
try:
    with open("last_octet", "r") as f:
        content = f.read().strip()
        SERVER_LAST_OCTETS = [int(o.strip()) for o in content.split(",") if o.strip().isdigit()]
except Exception as e:
    print("Error reading last_octet file:", e)
    SERVER_LAST_OCTETS = []

if not SERVER_LAST_OCTETS:
    raise ValueError("No valid server last octets found in 'datastore'.")

SERVER_URLS = [f"{BASE_IP}{octet}:80" for octet in SERVER_LAST_OCTETS]

# Connect and delete all projects from each server
for SERVER_URL in SERVER_URLS:
    try:
        server = Gns3Connector(url=SERVER_URL, user=GNS3_USER, cred=GNS3_PW)
        version = server.get_version()
        print(f"\nConnected to GNS3 server {SERVER_URL} (version: {version})")

        projects = server.get_projects() #print out all projects existing in the machine
        if not projects:
            print("  No projects to delete.")
        else:
            for project in projects:
                if project["name"] in PROJECTS_TO_DELETE:
                    print(f" Deleting project '{project['name']} '...")
                    server.delete_project(project_id=project["project_id"])
                    print("Specific projects have been deleted!")
                #print(f"  Deleting project '{project['name']}'...")
                # server.delete_project(project_id=project["project_id"])
           # print("  All projects deleted.")

    except Exception as e:
        print(f"Failed to process {SERVER_URL}: {e}")
